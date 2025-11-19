#!/usr/bin/env python3
"""
DeepSeek-OCR File Type Test
Tests OCR with ALL supported files found in samples directory (no subdirectories).

Supported formats: JPEG/JPG, PNG, WEBP, BMP, GIF, TIFF, PDF

Usage:
    python test.py --base-url https://<pod-id>-8000.proxy.runpod.net
    python test.py --base-url http://localhost:8000
"""

import argparse
import base64
import sys
from pathlib import Path
from typing import List, Optional
import time

try:
    from openai import OpenAI
except ImportError:
    print("❌ Error: openai package not installed")
    print("Install with: pip install openai")
    sys.exit(1)


class FileTypeOCRTest:
    """Test DeepSeek-OCR with different file types."""
    
    # Supported file extensions (case-insensitive)
    SUPPORTED_EXTENSIONS = {
        'jpg', 'jpeg', 'png', 'webp', 'bmp', 'gif', 'tiff', 'pdf'
    }
    
    # MIME type mapping for data URLs
    MIME_TYPES = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'webp': 'image/webp',
        'bmp': 'image/bmp',
        'gif': 'image/gif',
        'tiff': 'image/tiff',
        'pdf': 'application/pdf'
    }
    
    # Simple prompt - DeepSeek-OCR works best with minimal prompts
    # OCR_PROMPT = "convert the document in md and latex if needed, it may contain text, math formulas, charts X and Y axis, stck price candle graph, diagrams, or any sort of graphs. If there are charts you can reproduce in a tabular format containing X, Y value and the actual data point value"

    # OCR_PROMPT = "Convert the document to markdown, use tables or LaTex when needed"

    OCR_PROMPT = "Microfiche scan, scan every cell, describe and ocr"

    def __init__(self, base_url: str, api_key: str = "EMPTY", debug: bool = False):
        """
        Initialize OCR processor.
        
        Args:
            base_url: Base URL of vLLM API
            api_key: API key (default: "EMPTY" for local vLLM)
            debug: Enable debug logging
        """
        # Ensure base_url ends with /v1
        original_url = base_url
        if not base_url.endswith('/v1'):
            base_url = base_url.rstrip('/') + '/v1'
        
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=300.0
        )
        
        self.base_url = base_url
        self.debug = debug
        
        print(f"🔗 API Configuration:")
        print(f"   Original URL: {original_url}")
        print(f"   Base URL:     {base_url}")
        print(f"   Timeout:      300 seconds")
        print(f"   Debug Mode:   {debug}")
    
    def find_sample_files(self, samples_dir: Path) -> List[Path]:
        """
        Find ALL supported files in the directory.
        Only searches in the specified directory (no subdirectories).
        
        Args:
            samples_dir: Directory to scan for sample files
            
        Returns:
            List of file paths with supported extensions
        """
        files = []
        
        # Only look at files directly in the samples directory (no subdirectories)
        for file_path in samples_dir.iterdir():
            # Skip directories - only process files in the root of samples dir
            if not file_path.is_file():
                continue
                
            ext = file_path.suffix.lower().lstrip('.')
            
            # Check if this extension is supported
            if ext in self.SUPPORTED_EXTENSIONS:
                files.append(file_path)
        
        return sorted(files)
    
    def encode_file_base64(self, file_path: Path) -> str:
        """Encode file to base64 string."""
        with open(file_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    
    def process_file(self, file_path: Path, file_type: str) -> Optional[str]:
        """
        Process a single file with OCR.
        
        Args:
            file_path: Path to file
            file_type: File extension/type
            
        Returns:
            OCR result text or None if error
        """
        print(f"\n📄 Processing {file_type.upper()} file: {file_path.name}")
        
        try:
            # Encode file to base64
            print(f"   📸 Encoding file to base64...")
            file_base64 = self.encode_file_base64(file_path)
            file_size_kb = len(file_base64) / 1024
            print(f"   📦 File size: {file_size_kb:.2f} KB (base64)")
            
            # Get MIME type
            mime_type = self.MIME_TYPES.get(file_type, 'application/octet-stream')
            file_url = f"data:{mime_type};base64,{file_base64}"
            
            # Create API request
            print(f"   🌐 Sending request to: {self.base_url}/chat/completions")
            start_time = time.time()
            
            if self.debug:
                print(f"   🔍 Request details:")
                print(f"      Model: deepseek-ai/DeepSeek-OCR")
                print(f"      MIME type: {mime_type}")
                print(f"      Max tokens: 4096")
                print(f"      Temperature: 0.0")
            
            response = self.client.chat.completions.create(
                model="deepseek-ai/DeepSeek-OCR",
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": file_url}
                        },
                        {
                            "type": "text",
                            "text": self.OCR_PROMPT
                        }
                    ]
                }],
                max_tokens=4096,
                temperature=0.0
            )
            
            elapsed = time.time() - start_time
            
            # Extract content
            result = response.choices[0].message.content
            
            # Get token usage
            usage = response.usage
            tokens = usage.completion_tokens if usage else 0
            
            # Debug: Show what we got
            if self.debug:
                print(f"   🔍 Response preview: {result[:200] if result else 'EMPTY/NULL'}")
            
            if not result or len(result.strip()) < 10:
                print(f"   ⚠️  WARNING: Response is empty or too short!")
                print(f"   ⚠️  Response length: {len(result) if result else 0} chars")
                print(f"   ⚠️  Tokens generated: {tokens}")
                return None
            
            print(f"   ✅ Completed in {elapsed:.2f}s ({tokens} tokens, {len(result)} chars)")
            
            return result
            
        except Exception as e:
            print(f"   ❌ Error processing {file_type.upper()}")
            print(f"   ❌ Error type: {type(e).__name__}")
            print(f"   ❌ Error message: {str(e)}")
            
            if hasattr(e, '__cause__') and e.__cause__:
                print(f"   ❌ Cause: {e.__cause__}")
            
            if self.debug:
                import traceback
                print(f"   ❌ Full traceback:")
                traceback.print_exc()
            
            # Check specific error types
            if "Connection" in str(e) or "connection" in str(e):
                print(f"   💡 Hint: Check your base URL and network connection")
            elif "timeout" in str(e).lower():
                print(f"   💡 Hint: Request timed out")
            elif "401" in str(e) or "403" in str(e):
                print(f"   💡 Hint: Authentication error")
            elif "404" in str(e):
                print(f"   💡 Hint: Endpoint not found")
            elif "500" in str(e):
                print(f"   💡 Hint: Server error - check logs")
            
            return None
    
    def run_tests(self, samples_dir: Path, output_file: Optional[Path] = None):
        """
        Run OCR tests on sample files.
        
        Args:
            samples_dir: Directory containing sample files
            output_file: Optional output file for results
        """
        # Find sample files
        print(f"\n🔍 Scanning for sample files in: {samples_dir}")
        files = self.find_sample_files(samples_dir)
        
        if not files:
            print(f"❌ No supported files found in {samples_dir}")
            print(f"   Supported types: {', '.join(sorted(self.SUPPORTED_EXTENSIONS))}")
            return
        
        print(f"\n📊 Found {len(files)} file(s) to test:")
        for file_path in files:
            ext = file_path.suffix.lower().lstrip('.')
            print(f"   • {ext.upper()}: {file_path.name}")
        
        # Process each file
        results = []
        successful = 0
        failed = 0
        
        for file_path in files:
            file_type = file_path.suffix.lower().lstrip('.')
            result = self.process_file(file_path, file_type)
            
            if result:
                results.append({
                    'file': file_path.name,
                    'type': file_type,
                    'result': result,
                    'status': 'success'
                })
                successful += 1
            else:
                results.append({
                    'file': file_path.name,
                    'type': file_type,
                    'result': None,
                    'status': 'failed'
                })
                failed += 1
        
        # Print summary
        print(f"\n{'='*60}")
        print(f"✨ Test Complete!")
        print(f"{'='*60}")
        print(f"✅ Successful: {successful}/{len(files)} files")
        if failed > 0:
            print(f"❌ Failed: {failed}/{len(files)} files")
        
        # Show results
        print(f"\n📋 Results Summary:")
        for data in results:
            status_emoji = "✅" if data['status'] == 'success' else "❌"
            print(f"   {status_emoji} {data['type'].upper()}: {data['file']}")
            if data['result']:
                preview = data['result'][:100].replace('\n', ' ')
                print(f"      Preview: {preview}...")
        
        # Save to file if specified
        if output_file:
            self._save_results(results, output_file)
    
    def _save_results(self, results: List, output_file: Path):
        """Save results to markdown file."""
        content = f"""# DeepSeek-OCR File Type Test Results

**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}
**Total File Types Tested:** {len(results)}

---

"""
        
        for data in results:
            status = "✅ SUCCESS" if data['status'] == 'success' else "❌ FAILED"
            content += f"\n## {data['type'].upper()} - {data['file']} - {status}\n\n"
            content += f"**File:** `{data['file']}`\n\n"
            
            if data['result']:
                content += f"**OCR Result:**\n\n```\n{data['result']}\n```\n\n"
            else:
                content += "**OCR Result:** Failed to process\n\n"
            
            content += "---\n"
        
        output_file.write_text(content, encoding='utf-8')
        print(f"\n💾 Results saved to: {output_file}")
        print(f"📊 File size: {output_file.stat().st_size / 1024:.2f} KB")


def main():
    parser = argparse.ArgumentParser(
        description='Test DeepSeek-OCR with different file types',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test with RunPod deployment
  python test.py --base-url https://abc123-8000.proxy.runpod.net
  
  # Test with local vLLM
  python test.py --base-url http://localhost:8000
  
  # Save results to file
  python test.py --base-url https://abc123-8000.proxy.runpod.net --output results.md
  
  # Enable debug mode
  python test.py --base-url https://abc123-8000.proxy.runpod.net --debug

Supported file types:
  JPEG/JPG, PNG, WEBP, BMP, GIF, TIFF, PDF
        """
    )
    
    parser.add_argument(
        '--base-url',
        required=True,
        help='Base URL of vLLM API'
    )
    
    parser.add_argument(
        '--samples-dir',
        type=Path,
        default=Path(__file__).parent / 'samples',
        help='Directory containing sample files (default: ./samples)'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='result.md',
        type=Path,
        help='Output file for results (optional)'
    )
    
    parser.add_argument(
        '--api-key',
        default='EMPTY',
        help='API key (default: EMPTY)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    args = parser.parse_args()
    
    # Validate samples directory
    if not args.samples_dir.exists():
        print(f"❌ Error: Samples directory not found: {args.samples_dir}")
        print(f"   Expected location: {args.samples_dir.absolute()}")
        return 1
    
    if not args.samples_dir.is_dir():
        print(f"❌ Error: Not a directory: {args.samples_dir}")
        return 1
    
    print("="*60)
    print("🚀 DeepSeek-OCR File Type Test")
    print("="*60)
    
    try:
        # Initialize tester
        tester = FileTypeOCRTest(
            base_url=args.base_url,
            api_key=args.api_key,
            debug=args.debug
        )
        
        # Test connection
        print("\n🔍 Testing API connection...")
        print(f"   📡 Attempting to list models at: {tester.base_url}/models")
        try:
            models = tester.client.models.list()
            print(f"   ✅ Connection successful!")
            print(f"   ✅ Available models: {len(models.data)}")
            if models.data:
                for model in models.data:
                    print(f"      - {model.id}")
        except Exception as e:
            print(f"   ⚠️  Warning: Could not list models")
            print(f"   ⚠️  Error: {str(e)}")
            print(f"   ⚠️  Continuing anyway...")
        
        # Run tests
        tester.run_tests(
            samples_dir=args.samples_dir,
            output_file=args.output
        )
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

# usage:
# Run the test
# python test.py --base-url https://your-pod-8000.proxy.runpod.net
#
# # Save results to file
# python test.py --base-url http://localhost:8000 --output results.md
#
# # Enable debug mode
# python test.py --base-url http://localhost:8000 --debug