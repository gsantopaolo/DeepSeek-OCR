# PDF to Image Converter for DeepSeek-OCR

Convert PDF documents to high-quality PNG images optimized for OCR processing.

## Features

- ✅ **High-Quality Conversion** - Uses PyMuPDF for best results
- ✅ **OCR-Optimized** - Default 300 DPI (industry standard for OCR)
- ✅ **Flexible DPI** - Presets or custom DPI (72-600)
- ✅ **Page Selection** - Convert specific pages or ranges
- ✅ **Multiple Formats** - PNG (default) or JPEG output
- ✅ **Batch Processing** - Convert entire PDFs at once
- ✅ **Progress Tracking** - Real-time conversion feedback

## Installation

```bash
pip install PyMuPDF>=1.23.0
# or
pip install -r requirements.txt
```

## Quick Start

```bash
# Convert entire PDF at 300 DPI (recommended)
python pdf_to_image.py document.pdf

# Convert with high quality (400 DPI)
python pdf_to_image.py document.pdf --dpi 400

# Use preset
python pdf_to_image.py document.pdf --preset high

# Convert specific pages
python pdf_to_image.py document.pdf --pages "1,5-10,15"

# Convert to JPEG
python pdf_to_image.py document.pdf --format jpg

# Custom output directory
python pdf_to_image.py document.pdf --output-dir ./my_images
```

## DPI Presets

| Preset | DPI | Use Case |
|--------|-----|----------|
| `low` | 150 | Fast preview, draft quality |
| `medium` | 200 | Balanced speed/quality |
| `high` | 300 | **Recommended for OCR** ⭐ |
| `ultra` | 400 | Maximum quality, large files |

## Usage Examples

### 1. Basic Conversion
```bash
python pdf_to_image.py invoice.pdf
```
Output: `invoice_images/page_0001.png`, `page_0002.png`, etc.

### 2. High-Quality Conversion
```bash
python pdf_to_image.py scan.pdf --preset ultra
```

### 3. Convert First 10 Pages
```bash
python pdf_to_image.py report.pdf --pages "1-10"
```

### 4. Convert Specific Pages
```bash
python pdf_to_image.py book.pdf --pages "1,5,10,20-25"
```

### 5. JPEG for Smaller Files
```bash
python pdf_to_image.py large_doc.pdf --format jpg
```

### 6. Get PDF Info
```bash
python pdf_to_image.py document.pdf --info
```

## Integration with DeepSeek-OCR

After converting, use the images with DeepSeek-OCR:

```bash
# Single image
python test_inference.py --image invoice_images/page_0001.png

# Batch process all pages
python batch_process.py invoice_images/
```

## Output Format

### PNG (Default)
- **Pros**: Lossless, best quality, supports transparency
- **Cons**: Larger file sizes
- **Best for**: Text documents, diagrams, forms

### JPEG
- **Pros**: Smaller file sizes, faster processing
- **Cons**: Lossy compression, no transparency
- **Best for**: Photos, scanned documents with images

## DPI Guidelines

| DPI | Quality | File Size | Use Case |
|-----|---------|-----------|----------|
| 150 | Low | Small | Quick preview |
| 200 | Medium | Medium | General use |
| **300** | **High** | **Large** | **OCR (Recommended)** ⭐ |
| 400+ | Ultra | Very Large | Archival, fine print |

## Technical Details

- **Library**: PyMuPDF (fitz) - Fastest and most accurate
- **Default DPI**: 300 (optimal for OCR)
- **Max DPI**: 600 (prevents excessive file sizes)
- **Output Format**: PNG (lossless) or JPEG (95% quality)
- **Color Space**: RGB (required by DeepSeek-OCR)

## Command-Line Options

```
usage: pdf_to_image.py [-h] [--dpi DPI] [--preset {low,medium,high,ultra}]
                       [--output-dir OUTPUT_DIR] [--pages PAGES]
                       [--format {png,jpg}] [--info]
                       pdf_file

positional arguments:
  pdf_file              Input PDF file path

optional arguments:
  -h, --help            show this help message and exit
  --dpi DPI             Resolution in DPI (default: 300)
  --preset {low,medium,high,ultra}
                        Use DPI preset (overrides --dpi)
  --output-dir OUTPUT_DIR, -o OUTPUT_DIR
                        Output directory for images
  --pages PAGES, -p PAGES
                        Page range (e.g., "1,3,5-10")
  --format {png,jpg}, -f {png,jpg}
                        Output format (default: png)
  --info, -i            Show PDF info and exit
```

## Tips for Best OCR Results

1. **Use 300 DPI** - Industry standard for OCR
2. **PNG format** - Lossless quality preserves text clarity
3. **Clean PDFs** - Better source = better OCR results
4. **Page selection** - Convert only needed pages to save time
5. **Check output** - Verify image quality before OCR processing

## Troubleshooting

### PDF is encrypted
```bash
# Error: PDF is password protected
# Solution: Decrypt PDF first or provide password
```

### Out of memory
```bash
# Use lower DPI or convert fewer pages at once
python pdf_to_image.py large.pdf --dpi 200 --pages "1-10"
```

### Poor OCR results
```bash
# Increase DPI for better quality
python pdf_to_image.py scan.pdf --dpi 400
```

## Performance

Typical conversion speeds (on modern hardware):

| Pages | DPI | Time | Output Size |
|-------|-----|------|-------------|
| 10 | 300 | ~5s | ~50 MB |
| 50 | 300 | ~25s | ~250 MB |
| 100 | 300 | ~50s | ~500 MB |

## License

This tool is part of the DeepSeek-OCR project.
