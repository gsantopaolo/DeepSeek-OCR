# DeepSeek-OCR Testing Guide

Complete guide for testing DeepSeek-OCR inference with vLLM.

## 📁 Files Created

### Core Files
- **`test_inference.py`** - Main test script with error handling and logging
- **`requirements.txt`** - Python dependencies
- **`advanced_examples.py`** - Advanced OCR examples with different prompts
- **`download_test_images.sh`** - Script to download sample test images

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd src
pip install -r requirements.txt
```

### 2. Start vLLM Server
```bash
# Make sure you've built the Docker image first
cd ../deployment
./build.sh

# Run the container
docker run -d \
  --name deepseek-ocr \
  --runtime nvidia \
  --gpus all \
  -p 8000:8000 \
  --ipc=host \
  gsantopaolo/deepseek-ocr:latest

# Check logs (wait for "Application startup complete")
docker logs -f deepseek-ocr
```

### 3. Run Tests
```bash
cd src

# Basic test (uses online image)
python test_inference.py

# Advanced examples
python advanced_examples.py
```

## 📸 Test Images

### Option 1: Download Sample Images
```bash
chmod +x download_test_images.sh
./download_test_images.sh
```

This downloads:
- **sample_receipt.png** - Receipt with structured data
- **sample_document.png** - Text document
- **sample_table.png** - Table/spreadsheet

### Option 2: Use Your Own Images
Place any of these in the `src/` directory:
- `test_image.png`
- `test_image.jpg`
- `sample_receipt.png`
- `sample_document.pdf`

Supported formats: PNG, JPG, JPEG, GIF, BMP, WEBP

### Option 3: Use Online Images
The test script automatically uses this receipt image:
```
https://ofasys-multimodal-wlcb-3-toshanghai.oss-accelerate.aliyuncs.com/wpf272043/keepme/image/receipt.png
```

## 📝 Test Script Features

### `test_inference.py`
- ✅ Server health check
- ✅ Online image URL testing
- ✅ Local file testing
- ✅ Proper error handling
- ✅ Emoji-enhanced logging
- ✅ JSON and text output
- ✅ Performance metrics
- ✅ Base64 image encoding

### Output Files
After running tests:
- `ocr_result_url.json` - Full API response from URL test
- `ocr_result_url.txt` - Extracted text only
- `ocr_result_*.json` - Results from local file tests
- `deepseek_ocr_test.log` - Detailed execution logs

## 🎯 Use Cases & Prompts

### 1. Basic OCR
```python
prompt = "Free OCR."
```
Extracts all text from the image.

### 2. Markdown Conversion
```python
prompt = "Convert this image to markdown format, preserving structure and formatting."
```
Converts document to markdown with headers, lists, etc.

### 3. Table Extraction
```python
prompt = "Extract all tables from this image in markdown table format."
```
Extracts tables in structured markdown format.

### 4. Receipt Parsing
```python
prompt = """Extract the following information from this receipt:
- Store name
- Date
- Items purchased (name and price)
- Subtotal
- Tax
- Total amount
- Payment method"""
```

### 5. Form Field Extraction
```python
prompt = "Extract all form fields and their values from this image. Format as 'Field: Value' pairs."
```

### 6. Invoice Processing
```python
prompt = """Extract invoice information in this format:
Invoice Number: [number]
Date: [date]
Vendor: [name]
Line Items: [details]
Total: [amount]"""
```

### 7. Business Card
```python
prompt = """Extract contact information from this business card:
- Name
- Title/Position
- Company
- Email
- Phone
- Website"""
```

### 8. JSON Output
```python
prompt = """Extract all text and structure it as JSON with these fields:
{
  "title": "document title",
  "sections": [...],
  "tables": [...]
}"""
```

## 🔧 Configuration

### API Parameters
```python
response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-OCR",
    messages=messages,
    max_tokens=2048,          # Adjust based on document size
    temperature=0.0,          # 0.0 for deterministic output
    extra_body={
        "skip_special_tokens": False,
        "vllm_xargs": {
            "ngram_size": 30,
            "window_size": 90,
            "whitelist_token_ids": [128821, 128822],  # <td>, </td> for tables
        }
    }
)
```

### Adjustable Parameters
- **max_tokens**: Increase for longer documents (up to 8192)
- **temperature**: 0.0 for consistent results, higher for varied output
- **ngram_size**: Controls repetition prevention
- **window_size**: Context window for n-gram processor

## 🐛 Troubleshooting

### Server Not Responding
```bash
# Check if container is running
docker ps | grep deepseek-ocr

# View logs
docker logs deepseek-ocr

# Restart container
docker restart deepseek-ocr

# Check health endpoint
curl http://localhost:8000/health
```

### Connection Refused
- Ensure server is fully started (check logs for "Application startup complete")
- Verify port 8000 is not in use: `lsof -i :8000`
- Check firewall settings

### Out of Memory
- Reduce `max_tokens` parameter
- Use smaller images (resize before processing)
- Ensure GPU has sufficient VRAM (16GB+ recommended)
- Monitor GPU usage: `nvidia-smi -l 1`

### Slow Inference
- First request is slower (model loading)
- Subsequent requests are much faster
- GPU inference is significantly faster than CPU
- Large images take longer to process

### Image Format Issues
- Convert to PNG or JPG if using unusual formats
- Ensure image is not corrupted: `file test_image.png`
- Check image can be opened: `python -c "from PIL import Image; Image.open('test_image.png').show()"`

## 📊 Performance Tips

1. **Batch Processing**: Process multiple images in sequence to amortize model loading time
2. **Image Optimization**: Resize large images to ~2000px max dimension
3. **GPU Usage**: Always use GPU for production workloads
4. **Caching**: vLLM caches the model after first load
5. **Concurrent Requests**: vLLM supports multiple concurrent requests

## 🔗 Useful Links

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **OpenAPI Spec**: http://localhost:8000/openapi.json
- **DeepSeek-OCR GitHub**: https://github.com/deepseek-ai/DeepSeek-OCR
- **vLLM Documentation**: https://docs.vllm.ai/

## 📚 Additional Examples

See `advanced_examples.py` for:
- 10 different OCR use cases
- Various prompt templates
- Structured output examples
- Multi-language support
- Handwriting recognition
- Business document processing

Run with:
```bash
python advanced_examples.py
```

## 💡 Best Practices

1. **Clear Prompts**: Be specific about desired output format
2. **Image Quality**: Higher quality images = better results
3. **Preprocessing**: Crop/rotate images for optimal results
4. **Error Handling**: Always check response status
5. **Logging**: Enable detailed logging for debugging
6. **Testing**: Test with various image types before production
