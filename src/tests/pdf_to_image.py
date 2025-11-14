#!/usr/bin/env python3
"""
PDF to Image Converter for DeepSeek-OCR
Converts PDF pages to high-quality PNG images optimized for OCR processing.

Usage:
    python pdf_to_image.py input.pdf
    python pdf_to_image.py input.pdf --dpi 300
    python pdf_to_image.py input.pdf --output-dir ./images
    python pdf_to_image.py input.pdf --pages 1,3,5-10
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional, Tuple
import fitz  # PyMuPDF


class PDFToImageConverter:
    """Convert PDF pages to images optimized for OCR."""
    
    # Recommended DPI settings for OCR
    DPI_PRESETS = {
        'low': 150,      # Fast, lower quality
        'medium': 200,   # Balanced
        'high': 300,     # Recommended for OCR (default)
        'ultra': 400,    # Best quality, slower
    }
    
    DEFAULT_DPI = 300  # Optimal for OCR according to industry standards
    MAX_DPI = 600      # Maximum to prevent excessive file sizes
    
    def __init__(self, pdf_path: str, output_dir: Optional[str] = None, dpi: int = DEFAULT_DPI):
        """
        Initialize PDF converter.
        
        Args:
            pdf_path: Path to input PDF file
            output_dir: Directory for output images (default: same as PDF)
            dpi: Resolution in dots per inch (default: 300)
        """
        self.pdf_path = Path(pdf_path)
        
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"❌ PDF file not found: {pdf_path}")
        
        if not self.pdf_path.suffix.lower() == '.pdf':
            raise ValueError(f"❌ File must be a PDF: {pdf_path}")
        
        # Set output directory
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = self.pdf_path.parent / f"{self.pdf_path.stem}_images"
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Validate and set DPI
        if dpi < 72:
            print(f"⚠️  DPI too low ({dpi}), using minimum: 72")
            self.dpi = 72
        elif dpi > self.MAX_DPI:
            print(f"⚠️  DPI too high ({dpi}), using maximum: {self.MAX_DPI}")
            self.dpi = self.MAX_DPI
        else:
            self.dpi = dpi
        
        # Calculate zoom factor (DPI / 72, since PDF default is 72 DPI)
        self.zoom = self.dpi / 72.0
        
        print(f"📄 PDF: {self.pdf_path.name}")
        print(f"📁 Output: {self.output_dir}")
        print(f"🎯 DPI: {self.dpi} (zoom: {self.zoom:.2f}x)")
    
    def parse_page_range(self, page_spec: Optional[str], total_pages: int) -> List[int]:
        """
        Parse page specification string.
        
        Args:
            page_spec: Page specification (e.g., "1,3,5-10" or None for all)
            total_pages: Total number of pages in PDF
            
        Returns:
            List of 0-indexed page numbers
        """
        if not page_spec:
            return list(range(total_pages))
        
        pages = set()
        for part in page_spec.split(','):
            part = part.strip()
            if '-' in part:
                start, end = part.split('-')
                start = int(start.strip()) - 1  # Convert to 0-indexed
                end = int(end.strip())
                pages.update(range(max(0, start), min(total_pages, end)))
            else:
                page = int(part.strip()) - 1  # Convert to 0-indexed
                if 0 <= page < total_pages:
                    pages.add(page)
        
        return sorted(list(pages))
    
    def convert(self, pages: Optional[str] = None, format: str = 'png') -> List[Path]:
        """
        Convert PDF pages to images.
        
        Args:
            pages: Page specification (e.g., "1,3,5-10" or None for all)
            format: Output format ('png' or 'jpg')
            
        Returns:
            List of created image file paths
        """
        format = format.lower()
        if format not in ['png', 'jpg', 'jpeg']:
            raise ValueError(f"❌ Unsupported format: {format}. Use 'png' or 'jpg'")
        
        # Normalize format
        if format == 'jpeg':
            format = 'jpg'
        
        output_files = []
        
        try:
            # Open PDF
            doc = fitz.open(self.pdf_path)
            total_pages = len(doc)
            
            print(f"📖 Total pages: {total_pages}")
            
            # Parse page range
            page_list = self.parse_page_range(pages, total_pages)
            
            if not page_list:
                print("⚠️  No valid pages to convert")
                return output_files
            
            print(f"🔄 Converting {len(page_list)} page(s)...")
            print()
            
            # Convert each page
            for i, page_num in enumerate(page_list, 1):
                page = doc[page_num]
                
                # Create transformation matrix for DPI scaling
                mat = fitz.Matrix(self.zoom, self.zoom)
                
                # Render page to pixmap (image)
                pix = page.get_pixmap(matrix=mat, alpha=False)
                
                # Generate output filename
                output_file = self.output_dir / f"page_{page_num + 1:04d}.{format}"
                
                # Save image
                if format == 'png':
                    pix.save(output_file)
                else:  # jpg
                    pix.save(output_file, jpg_quality=95)
                
                output_files.append(output_file)
                
                # Get image dimensions
                width, height = pix.width, pix.height
                size_mb = output_file.stat().st_size / (1024 * 1024)
                
                print(f"  ✅ Page {page_num + 1:3d} → {output_file.name} "
                      f"({width}x{height}px, {size_mb:.2f} MB)")
            
            doc.close()
            
            print()
            print(f"✨ Successfully converted {len(output_files)} page(s)")
            print(f"📁 Images saved to: {self.output_dir}")
            
            return output_files
            
        except Exception as e:
            print(f"❌ Error converting PDF: {e}")
            raise
    
    def get_pdf_info(self) -> dict:
        """Get PDF metadata and information."""
        try:
            doc = fitz.open(self.pdf_path)
            info = {
                'pages': len(doc),
                'metadata': doc.metadata,
                'encrypted': doc.is_encrypted,
            }
            
            # Get first page dimensions
            if len(doc) > 0:
                page = doc[0]
                info['page_size'] = {
                    'width': page.rect.width,
                    'height': page.rect.height,
                    'unit': 'points (1/72 inch)'
                }
            
            doc.close()
            return info
        except Exception as e:
            print(f"❌ Error reading PDF info: {e}")
            return {}


def main():
    parser = argparse.ArgumentParser(
        description='Convert PDF to images optimized for DeepSeek-OCR',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert all pages at default 300 DPI (recommended)
  python pdf_to_image.py document.pdf
  
  # Convert with specific DPI
  python pdf_to_image.py document.pdf --dpi 400
  
  # Use DPI preset
  python pdf_to_image.py document.pdf --preset high
  
  # Convert specific pages
  python pdf_to_image.py document.pdf --pages "1,3,5-10"
  
  # Convert to JPEG instead of PNG
  python pdf_to_image.py document.pdf --format jpg
  
  # Specify output directory
  python pdf_to_image.py document.pdf --output-dir ./my_images
  
  # Show PDF info without converting
  python pdf_to_image.py document.pdf --info

DPI Presets:
  low    = 150 DPI (fast, lower quality)
  medium = 200 DPI (balanced)
  high   = 300 DPI (recommended for OCR) ⭐
  ultra  = 400 DPI (best quality, slower)
        """
    )
    
    parser.add_argument('pdf_file', help='Input PDF file path')
    parser.add_argument('--dpi', type=int, default=PDFToImageConverter.DEFAULT_DPI,
                        help=f'Resolution in DPI (default: {PDFToImageConverter.DEFAULT_DPI})')
    parser.add_argument('--preset', choices=PDFToImageConverter.DPI_PRESETS.keys(),
                        help='Use DPI preset (overrides --dpi)')
    parser.add_argument('--output-dir', '-o', help='Output directory for images')
    parser.add_argument('--pages', '-p', help='Page range (e.g., "1,3,5-10")')
    parser.add_argument('--format', '-f', choices=['png', 'jpg'], default='png',
                        help='Output format (default: png)')
    parser.add_argument('--info', '-i', action='store_true',
                        help='Show PDF info and exit')
    
    args = parser.parse_args()
    
    # Determine DPI
    if args.preset:
        dpi = PDFToImageConverter.DPI_PRESETS[args.preset]
        print(f"📊 Using preset '{args.preset}': {dpi} DPI")
    else:
        dpi = args.dpi
    
    try:
        converter = PDFToImageConverter(args.pdf_file, args.output_dir, dpi)
        
        # Show info and exit if requested
        if args.info:
            print("\n📋 PDF Information:")
            info = converter.get_pdf_info()
            for key, value in info.items():
                print(f"  {key}: {value}")
            return 0
        
        # Convert PDF to images
        print()
        output_files = converter.convert(pages=args.pages, format=args.format)
        
        if output_files:
            print()
            print("🚀 Ready for DeepSeek-OCR!")
            print(f"   Use: python test_inference.py --image {output_files[0]}")
            print(f"   Or:  python batch_process.py {converter.output_dir}")
            return 0
        else:
            return 1
            
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
