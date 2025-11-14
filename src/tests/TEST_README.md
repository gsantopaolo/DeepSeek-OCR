# 🧪 NVIDIA Financial Report OCR Test

Test script to process the NVIDIA annual report using DeepSeek-OCR and convert all pages to Markdown format with tables.

## 📋 What It Does

- ✅ Processes all 10 pages from `samples/NVIDIAAn_images/`
- ✅ Converts each page to clean Markdown
- ✅ Preserves tables in Markdown table format
- ✅ Maintains document structure and hierarchy
- ✅ Outputs a single combined Markdown file
- ✅ Shows progress and timing for each page

## 🚀 Quick Start

### 1. Make sure your RunPod deployment is running

```bash
# Get your pod URL from RunPod dashboard
# Example: https://abc123xyz-8000.proxy.runpod.net
```

### 2. Run the test

```bash
cd src/tests

# With RunPod deployment
python test.py --base-url https://<your-pod-id>-8000.proxy.runpod.net

# With local vLLM
python test.py --base-url http://localhost:8000

# Custom output file
python test.py --base-url https://<pod-id>-8000.proxy.runpod.net --output my_report.md
```

### 3. View the results

```bash
# View in terminal
cat nvidia_report_ocr.md

# Open in editor
open nvidia_report_ocr.md

# Or use your favorite markdown viewer
code nvidia_report_ocr.md
```

## 📊 Expected Output

```
==============================================================
🚀 NVIDIA Financial Report OCR Processing
==============================================================
🔗 Connected to: https://abc123xyz-8000.proxy.runpod.net/v1

🔍 Testing API connection...
   ✅ Connected! Available models: 1

📊 Found 10 pages to process
📁 Images directory: samples/NVIDIAAn_images
💾 Output file: nvidia_report_ocr.md

📄 Processing page 1: page_0001.png
   ✅ Completed in 12.34s (2048 tokens)

📄 Processing page 2: page_0002.png
   ✅ Completed in 15.67s (2456 tokens)

... (continues for all pages)

💾 Saved to: nvidia_report_ocr.md
📊 File size: 156.78 KB

==============================================================
✨ Processing Complete!
==============================================================
✅ Successful: 10/10 pages
📝 Total markdown length: 160,543 characters

🎉 Success! Report processed and saved.
```

## 🎯 Features

### Optimized Prompt
The script uses a specialized prompt for financial documents:
- Extracts ALL text accurately
- Preserves document structure
- Converts tables to Markdown format
- Maintains numerical precision
- Keeps heading hierarchy
- Preserves lists and bullet points

### Smart Processing
- Base64 image encoding for API compatibility
- Proper timeout handling (5 minutes per page)
- Progress tracking with timing
- Error handling and retry logic
- Token usage reporting

### Output Format
```markdown
# NVIDIA Annual Report - OCR Extraction

**Processed by:** DeepSeek-OCR via vLLM
**Date:** 2025-01-13 18:45:00
**Total Pages:** 10
**Successful:** 10
**Failed:** 0

---

# Page 1

[Extracted content with tables in Markdown format]

---

# Page 2

[Extracted content...]
```

## 📁 File Structure

```
src/tests/
├── test.py                          # Main test script
├── samples/
│   ├── NVIDIAAn.pdf                # Original PDF
│   └── NVIDIAAn_images/            # Extracted pages
│       ├── page_0001.png           # Page 1
│       ├── page_0002.png           # Page 2
│       └── ...                     # Pages 3-10
└── nvidia_report_ocr.md            # Output (generated)
```

## ⚙️ Command-Line Options

```bash
python test.py [OPTIONS]

Required:
  --base-url URL          Base URL of vLLM API
                          Examples:
                            https://abc123-8000.proxy.runpod.net
                            http://localhost:8000

Optional:
  --output FILE, -o FILE  Output markdown file
                          Default: nvidia_report_ocr.md
  
  --images-dir DIR        Directory with page images
                          Default: samples/NVIDIAAn_images
  
  --api-key KEY          API key for authentication
                          Default: EMPTY (for local vLLM)
```

## 🔧 Advanced Usage

### Process Specific Pages Only

If you want to test with fewer pages first:

```bash
# Process only first 3 pages (manually copy them to a test folder)
mkdir -p samples/test_pages
cp samples/NVIDIAAn_images/page_000{1,2,3}.png samples/test_pages/
python test.py --base-url https://pod-8000.proxy.runpod.net --images-dir samples/test_pages
```

### Custom API Configuration

```bash
# With authentication
python test.py --base-url https://api.example.com --api-key your-api-key

# With custom timeout (edit script)
# Change: timeout=300.0 to timeout=600.0 in OpenAI client init
```

### Batch Processing Multiple Reports

```bash
# Process multiple reports
for report in samples/*/; do
    name=$(basename "$report")
    python test.py --base-url https://pod-8000.proxy.runpod.net \
        --images-dir "$report" \
        --output "${name}_ocr.md"
done
```

## 📊 Performance Metrics

### Typical Processing Times

| GPU | Time per Page | Total (10 pages) |
|-----|---------------|------------------|
| RTX 3090 | 15-20s | ~3 minutes |
| RTX 4090 | 10-15s | ~2 minutes |
| A100 40GB | 8-12s | ~1.5 minutes |

### Output Size
- **Input:** 10 PNG images (~4.5 MB total)
- **Output:** 1 Markdown file (~150-200 KB)
- **Tokens:** ~2000-3000 per page

## 🐛 Troubleshooting

### Connection Error
```
❌ Error: Connection refused
```
**Solution:** Check your base URL and ensure the pod is running

### Timeout Error
```
❌ Error: Request timeout
```
**Solution:** Increase timeout in script or use faster GPU

### No Images Found
```
❌ Error: No page images found
```
**Solution:** Check the images directory path:
```bash
ls -la samples/NVIDIAAn_images/
```

### Poor Table Formatting
**Solution:** The prompt is already optimized for tables. If tables are still not formatted well, check the original image quality.

## 💡 Tips

1. **Test with 1-2 pages first** to verify everything works
2. **Use HTTPS URLs** for RunPod deployments (automatic)
3. **Monitor GPU usage** in RunPod dashboard during processing
4. **Check output quality** after first page before processing all
5. **Save intermediate results** if processing large documents

## 📖 Example Output

Here's what a typical page looks like after OCR:

```markdown
# Page 3

## Financial Highlights

| Metric | 2024 | 2023 | Change |
|--------|------|------|--------|
| Revenue | $26.97B | $26.91B | +0.2% |
| Net Income | $4.37B | $4.37B | 0% |
| EPS | $1.76 | $1.74 | +1.1% |

### Key Points

- **Data Center revenue** increased 217% year-over-year
- **Gaming revenue** grew 15% year-over-year
- **Professional Visualization** revenue up 105%
```

## 🔗 Related Files

- **[pdf_to_image.py](./pdf_to_image.py)** - Convert PDFs to images
- **[batch_process.py](./batch_process.py)** - Batch processing script
- **[test_inference.py](./test_inference.py)** - Basic inference test

## 📞 Support

For issues or questions:
- Check [GitHub Issues](https://github.com/gsantopaolo/DeepSeek-OCR/issues)
- Visit [genmind.ch](https://genmind.ch) for tutorials
- Read the main [README.md](../../README.md)

---

**Happy OCR-ing! 🚀**
