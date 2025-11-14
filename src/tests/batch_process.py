#!/usr/bin/env python3
"""
Batch OCR Processing Script
Process multiple images in a directory with DeepSeek-OCR
"""

import sys
import logging
from pathlib import Path
from typing import List
import json
from datetime import datetime
from test_inference import DeepSeekOCRTester

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BatchOCRProcessor:
    """Batch process multiple images"""
    
    def __init__(self, output_dir: Path = None):
        self.tester = DeepSeekOCRTester()
        self.output_dir = output_dir or Path("batch_results")
        self.output_dir.mkdir(exist_ok=True)
        
    def find_images(self, directory: Path) -> List[Path]:
        """Find all supported images in directory"""
        supported_formats = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
        images = []
        
        for ext in supported_formats:
            images.extend(directory.glob(f"*{ext}"))
            images.extend(directory.glob(f"*{ext.upper()}"))
        
        return sorted(images)
    
    def process_batch(self, image_dir: Path, prompt: str = "Free OCR."):
        """Process all images in a directory"""
        images = self.find_images(image_dir)
        
        if not images:
            logger.warning(f"⚠️  No images found in {image_dir}")
            return
        
        logger.info(f"📁 Found {len(images)} images to process")
        logger.info(f"💾 Results will be saved to: {self.output_dir}")
        logger.info("")
        
        results_summary = {
            "timestamp": datetime.now().isoformat(),
            "total_images": len(images),
            "processed": 0,
            "failed": 0,
            "results": []
        }
        
        for idx, image_path in enumerate(images, 1):
            logger.info(f"📸 [{idx}/{len(images)}] Processing: {image_path.name}")
            
            try:
                result = self.tester.test_ocr_with_local_file(image_path, prompt)
                
                if result:
                    # Save individual result
                    output_name = f"{image_path.stem}_ocr"
                    
                    # Save JSON
                    json_path = self.output_dir / f"{output_name}.json"
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(result, f, indent=2, ensure_ascii=False)
                    
                    # Save text
                    txt_path = self.output_dir / f"{output_name}.txt"
                    with open(txt_path, 'w', encoding='utf-8') as f:
                        f.write(result['text'])
                    
                    logger.info(f"   ✅ Saved to: {output_name}.*")
                    
                    results_summary["processed"] += 1
                    results_summary["results"].append({
                        "image": image_path.name,
                        "status": "success",
                        "elapsed_time": result["elapsed_time"],
                        "output_files": [str(json_path), str(txt_path)]
                    })
                else:
                    logger.error(f"   ❌ Failed to process {image_path.name}")
                    results_summary["failed"] += 1
                    results_summary["results"].append({
                        "image": image_path.name,
                        "status": "failed"
                    })
                
            except Exception as e:
                logger.error(f"   ❌ Error processing {image_path.name}: {e}")
                results_summary["failed"] += 1
                results_summary["results"].append({
                    "image": image_path.name,
                    "status": "error",
                    "error": str(e)
                })
            
            logger.info("")
        
        # Save summary
        summary_path = self.output_dir / "batch_summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(results_summary, f, indent=2, ensure_ascii=False)
        
        logger.info("=" * 60)
        logger.info("📊 Batch Processing Summary")
        logger.info(f"   Total images: {results_summary['total_images']}")
        logger.info(f"   ✅ Processed: {results_summary['processed']}")
        logger.info(f"   ❌ Failed: {results_summary['failed']}")
        logger.info(f"   📁 Results saved to: {self.output_dir}")
        logger.info(f"   📄 Summary: {summary_path}")
        logger.info("=" * 60)


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Batch process images with DeepSeek-OCR",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all images in test_images directory
  python batch_process.py test_images
  
  # Process with custom prompt
  python batch_process.py test_images --prompt "Convert to markdown format"
  
  # Specify output directory
  python batch_process.py test_images --output results_2024
        """
    )
    
    parser.add_argument(
        'image_dir',
        type=str,
        help='Directory containing images to process'
    )
    
    parser.add_argument(
        '--prompt',
        type=str,
        default='Free OCR.',
        help='OCR prompt to use (default: "Free OCR.")'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='batch_results',
        help='Output directory for results (default: batch_results)'
    )
    
    args = parser.parse_args()
    
    image_dir = Path(args.image_dir)
    if not image_dir.exists():
        logger.error(f"❌ Directory not found: {image_dir}")
        sys.exit(1)
    
    if not image_dir.is_dir():
        logger.error(f"❌ Not a directory: {image_dir}")
        sys.exit(1)
    
    logger.info("🚀 DeepSeek-OCR Batch Processor")
    logger.info("=" * 60)
    logger.info(f"📁 Input directory: {image_dir}")
    logger.info(f"💬 Prompt: {args.prompt}")
    logger.info(f"📂 Output directory: {args.output}")
    logger.info("")
    
    processor = BatchOCRProcessor(output_dir=Path(args.output))
    
    # Check server health
    if not processor.tester.check_server_health():
        logger.error("❌ Server not available. Start vLLM server first!")
        sys.exit(1)
    
    logger.info("")
    
    # Process batch
    processor.process_batch(image_dir, args.prompt)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n⚠️  Batch processing interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}", exc_info=True)
        sys.exit(1)
