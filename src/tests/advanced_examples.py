#!/usr/bin/env python3
"""
Advanced DeepSeek-OCR Examples
Demonstrates various OCR use cases and prompts
"""

import logging
from pathlib import Path
from typing import List, Dict
from test_inference import DeepSeekOCRTester

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdvancedOCRExamples:
    """Advanced OCR examples with different prompts and use cases"""
    
    def __init__(self):
        self.tester = DeepSeekOCRTester()
    
    def example_1_basic_ocr(self, image_path: str):
        """Example 1: Basic OCR - Extract all text"""
        logger.info("📋 Example 1: Basic OCR")
        logger.info("-" * 60)
        
        prompt = "Free OCR."
        result = self.tester.test_ocr_with_url(image_path, prompt)
        
        if result:
            logger.info(f"✅ Extracted text:\n{result['text']}\n")
        return result
    
    def example_2_markdown_conversion(self, image_path: str):
        """Example 2: Convert image to markdown format"""
        logger.info("📋 Example 2: Markdown Conversion")
        logger.info("-" * 60)
        
        prompt = "Convert this image to markdown format, preserving structure and formatting."
        result = self.tester.test_ocr_with_url(image_path, prompt)
        
        if result:
            logger.info(f"✅ Markdown output:\n{result['text']}\n")
            # Save markdown to file
            with open("output_markdown.md", "w", encoding="utf-8") as f:
                f.write(result['text'])
            logger.info("💾 Saved to: output_markdown.md\n")
        return result
    
    def example_3_table_extraction(self, image_path: str):
        """Example 3: Extract tables in structured format"""
        logger.info("📋 Example 3: Table Extraction")
        logger.info("-" * 60)
        
        prompt = "Extract all tables from this image in markdown table format."
        result = self.tester.test_ocr_with_url(image_path, prompt)
        
        if result:
            logger.info(f"✅ Table data:\n{result['text']}\n")
        return result
    
    def example_4_receipt_parsing(self, image_path: str):
        """Example 4: Parse receipt with specific fields"""
        logger.info("📋 Example 4: Receipt Parsing")
        logger.info("-" * 60)
        
        prompt = """Extract the following information from this receipt:
- Store name
- Date
- Items purchased (name and price)
- Subtotal
- Tax
- Total amount
- Payment method

Format the output as a structured list."""
        
        result = self.tester.test_ocr_with_url(image_path, prompt)
        
        if result:
            logger.info(f"✅ Parsed receipt:\n{result['text']}\n")
        return result
    
    def example_5_form_extraction(self, image_path: str):
        """Example 5: Extract form fields and values"""
        logger.info("📋 Example 5: Form Field Extraction")
        logger.info("-" * 60)
        
        prompt = "Extract all form fields and their values from this image. Format as 'Field: Value' pairs."
        result = self.tester.test_ocr_with_url(image_path, prompt)
        
        if result:
            logger.info(f"✅ Form data:\n{result['text']}\n")
        return result
    
    def example_6_multilingual_ocr(self, image_path: str):
        """Example 6: OCR with multiple languages"""
        logger.info("📋 Example 6: Multilingual OCR")
        logger.info("-" * 60)
        
        prompt = "Extract all text from this image, preserving the original language. If multiple languages are present, identify them."
        result = self.tester.test_ocr_with_url(image_path, prompt)
        
        if result:
            logger.info(f"✅ Multilingual text:\n{result['text']}\n")
        return result
    
    def example_7_invoice_processing(self, image_path: str):
        """Example 7: Process invoice with line items"""
        logger.info("📋 Example 7: Invoice Processing")
        logger.info("-" * 60)
        
        prompt = """Extract invoice information in this format:
Invoice Number: [number]
Date: [date]
Vendor: [name]
Line Items:
  - [item] | [quantity] | [unit price] | [total]
Subtotal: [amount]
Tax: [amount]
Total: [amount]"""
        
        result = self.tester.test_ocr_with_url(image_path, prompt)
        
        if result:
            logger.info(f"✅ Invoice data:\n{result['text']}\n")
        return result
    
    def example_8_handwriting_recognition(self, image_path: str):
        """Example 8: Recognize handwritten text"""
        logger.info("📋 Example 8: Handwriting Recognition")
        logger.info("-" * 60)
        
        prompt = "Transcribe all handwritten text from this image. Maintain line breaks and structure."
        result = self.tester.test_ocr_with_url(image_path, prompt)
        
        if result:
            logger.info(f"✅ Transcribed handwriting:\n{result['text']}\n")
        return result
    
    def example_9_business_card(self, image_path: str):
        """Example 9: Extract business card information"""
        logger.info("📋 Example 9: Business Card Extraction")
        logger.info("-" * 60)
        
        prompt = """Extract contact information from this business card:
- Name
- Title/Position
- Company
- Email
- Phone
- Address
- Website"""
        
        result = self.tester.test_ocr_with_url(image_path, prompt)
        
        if result:
            logger.info(f"✅ Contact info:\n{result['text']}\n")
        return result
    
    def example_10_json_output(self, image_path: str):
        """Example 10: Request structured JSON output"""
        logger.info("📋 Example 10: JSON Structured Output")
        logger.info("-" * 60)
        
        prompt = """Extract all text and structure it as JSON with these fields:
{
  "title": "document title if present",
  "sections": [
    {
      "heading": "section heading",
      "content": "section text"
    }
  ],
  "tables": [
    {
      "headers": ["col1", "col2"],
      "rows": [["val1", "val2"]]
    }
  ]
}"""
        
        result = self.tester.test_ocr_with_url(image_path, prompt)
        
        if result:
            logger.info(f"✅ JSON output:\n{result['text']}\n")
        return result


def main():
    """Run all examples"""
    logger.info("🚀 DeepSeek-OCR Advanced Examples")
    logger.info("=" * 60)
    
    examples = AdvancedOCRExamples()
    
    # Check server health
    if not examples.tester.check_server_health():
        logger.error("❌ Server not available. Start it first!")
        return
    
    # Example receipt image
    receipt_url = "https://ofasys-multimodal-wlcb-3-toshanghai.oss-accelerate.aliyuncs.com/wpf272043/keepme/image/receipt.png"
    
    # Run examples
    logger.info("\n" + "=" * 60)
    examples.example_1_basic_ocr(receipt_url)
    
    logger.info("=" * 60)
    examples.example_2_markdown_conversion(receipt_url)
    
    logger.info("=" * 60)
    examples.example_3_table_extraction(receipt_url)
    
    logger.info("=" * 60)
    examples.example_4_receipt_parsing(receipt_url)
    
    logger.info("=" * 60)
    logger.info("✅ Examples completed!")
    logger.info("\n💡 Tip: Modify the prompts in this script to test different use cases")
    logger.info("💡 Tip: Use your own images by changing the image_path variable")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n⚠️  Interrupted by user")
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
