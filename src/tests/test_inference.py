#!/usr/bin/env python3
"""
DeepSeek-OCR Inference Test Script
Tests both offline and online inference modes with proper error handling
"""

import sys
import time
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import json

try:
    from openai import OpenAI
    from PIL import Image
    import requests
except ImportError as e:
    print(f"❌ Missing required packages. Please install: pip install -r requirements.txt")
    print(f"   Error: {e}")
    sys.exit(1)

# Configure logging with emojis
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('deepseek_ocr_test.log')
    ]
)
logger = logging.getLogger(__name__)


class DeepSeekOCRTester:
    """Test DeepSeek-OCR inference via vLLM API"""
    
    def __init__(self, base_url: str = "http://localhost:8000/v1", api_key: str = "EMPTY"):
        """
        Initialize the tester
        
        Args:
            base_url: vLLM API base URL
            api_key: API key (use "EMPTY" for local vLLM)
        """
        self.base_url = base_url
        self.client = OpenAI(api_key=api_key, base_url=base_url, timeout=300)
        self.model_name = "deepseek-ai/DeepSeek-OCR"
        
    def check_server_health(self) -> bool:
        """Check if vLLM server is healthy"""
        try:
            health_url = self.base_url.replace('/v1', '/health')
            logger.info(f"🏥 Checking server health at {health_url}")
            response = requests.get(health_url, timeout=5)
            
            if response.status_code == 200:
                logger.info("✅ Server is healthy!")
                return True
            else:
                logger.warning(f"⚠️  Server returned status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Server health check failed: {e}")
            logger.error(f"   Make sure vLLM server is running at {self.base_url}")
            return False
    
    def test_ocr_with_url(self, image_url: str, prompt: str = "Free OCR.") -> Optional[Dict[str, Any]]:
        """
        Test OCR with an image URL
        
        Args:
            image_url: URL to the image
            prompt: OCR prompt (default: "Free OCR.")
            
        Returns:
            Response dict or None if failed
        """
        try:
            logger.info(f"📸 Testing OCR with image URL: {image_url}")
            logger.info(f"💬 Prompt: {prompt}")
            
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url}
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
            
            start_time = time.time()
            logger.info("⏳ Sending request to vLLM...")
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=2048,
                temperature=0.0,
                extra_body={
                    "skip_special_tokens": False,
                    "vllm_xargs": {
                        "ngram_size": 30,
                        "window_size": 90,
                        "whitelist_token_ids": [128821, 128822],  # <td>, </td>
                    }
                }
            )
            
            elapsed_time = time.time() - start_time
            
            result = {
                "text": response.choices[0].message.content,
                "elapsed_time": elapsed_time,
                "usage": response.usage.model_dump() if response.usage else None
            }
            
            logger.info(f"✅ OCR completed in {elapsed_time:.2f}s")
            logger.info(f"📊 Tokens used: {result['usage']}")
            logger.info(f"📝 Extracted text preview: {result['text'][:200]}...")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ OCR failed: {e}")
            return None
    
    def test_ocr_with_local_file(self, image_path: Path, prompt: str = "Free OCR.") -> Optional[Dict[str, Any]]:
        """
        Test OCR with a local image file
        
        Args:
            image_path: Path to local image file
            prompt: OCR prompt
            
        Returns:
            Response dict or None if failed
        """
        try:
            if not image_path.exists():
                logger.error(f"❌ Image file not found: {image_path}")
                return None
            
            logger.info(f"📁 Testing OCR with local file: {image_path}")
            
            # Verify image can be opened
            try:
                img = Image.open(image_path)
                logger.info(f"🖼️  Image info: {img.format} {img.size} {img.mode}")
                img.close()
            except Exception as e:
                logger.error(f"❌ Cannot open image: {e}")
                return None
            
            # Convert local file to base64 data URL
            import base64
            with open(image_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            # Determine MIME type
            suffix = image_path.suffix.lower()
            mime_types = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.bmp': 'image/bmp',
                '.webp': 'image/webp'
            }
            mime_type = mime_types.get(suffix, 'image/png')
            
            image_url = f"data:{mime_type};base64,{image_data}"
            
            return self.test_ocr_with_url(image_url, prompt)
            
        except Exception as e:
            logger.error(f"❌ Failed to process local file: {e}")
            return None
    
    def save_result(self, result: Dict[str, Any], output_path: Path):
        """Save OCR result to file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            logger.info(f"💾 Result saved to: {output_path}")
        except Exception as e:
            logger.error(f"❌ Failed to save result: {e}")


def main():
    """Main test function"""
    logger.info("🚀 Starting DeepSeek-OCR Inference Test")
    logger.info("=" * 60)
    
    # Initialize tester
    tester = DeepSeekOCRTester()
    
    # Check server health
    if not tester.check_server_health():
        logger.error("❌ Server is not available. Please start the vLLM server first:")
        logger.error("   docker run --runtime nvidia --gpus all -p 8000:8000 gsantopaolo/deepseek-ocr:latest")
        sys.exit(1)
    
    logger.info("")
    logger.info("=" * 60)
    
    # Test 1: OCR with online image URL
    logger.info("📋 Test 1: OCR with online image URL")
    logger.info("-" * 60)
    
    # Example receipt image from DeepSeek documentation
    test_url = "https://ofasys-multimodal-wlcb-3-toshanghai.oss-accelerate.aliyuncs.com/wpf272043/keepme/image/receipt.png"
    
    result = tester.test_ocr_with_url(test_url, prompt="Free OCR.")
    if result:
        output_path = Path("ocr_result_url.json")
        tester.save_result(result, output_path)
        
        # Save extracted text separately
        text_output = Path("ocr_result_url.txt")
        with open(text_output, 'w', encoding='utf-8') as f:
            f.write(result['text'])
        logger.info(f"📄 Extracted text saved to: {text_output}")
    
    logger.info("")
    logger.info("=" * 60)
    
    # Test 2: OCR with local image file
    logger.info("📋 Test 2: OCR with local image file")
    logger.info("-" * 60)
    
    # Check for test images in the same directory
    test_images = [
        Path("test_image.png"),
        Path("test_image.jpg"),
        Path("sample_receipt.png"),
        Path("sample_document.pdf"),
    ]
    
    local_image = None
    for img_path in test_images:
        if img_path.exists():
            local_image = img_path
            break
    
    if local_image:
        result = tester.test_ocr_with_local_file(local_image, prompt="Free OCR.")
        if result:
            output_path = Path(f"ocr_result_{local_image.stem}.json")
            tester.save_result(result, output_path)
            
            text_output = Path(f"ocr_result_{local_image.stem}.txt")
            with open(text_output, 'w', encoding='utf-8') as f:
                f.write(result['text'])
            logger.info(f"📄 Extracted text saved to: {text_output}")
    else:
        logger.warning("⚠️  No local test images found. Skipping local file test.")
        logger.info("💡 Tip: Place a test image in the src/ directory with one of these names:")
        for img in test_images:
            logger.info(f"   - {img.name}")
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("✅ All tests completed!")
    logger.info("📊 Check the generated files for results:")
    logger.info("   - ocr_result_*.json (full response)")
    logger.info("   - ocr_result_*.txt (extracted text only)")
    logger.info("   - deepseek_ocr_test.log (detailed logs)")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n⚠️  Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}", exc_info=True)
        sys.exit(1)
