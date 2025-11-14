# DeepSeek-OCR Inference Testing

This directory contains test scripts for DeepSeek-OCR inference via vLLM.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the vLLM server:**
   ```bash
   # Using Docker
   docker run -d \
     --name deepseek-ocr \
     --runtime nvidia \
     --gpus all \
     -p 8000:8000 \
     --ipc=host \
     gsantopaolo/deepseek-ocr:latest
   
   # Or using the build script
   cd ../deployment
   ./build.sh
   docker run -d --name deepseek-ocr --runtime nvidia --gpus all -p 8000:8000 --ipc=host gsantopaolo/deepseek-ocr:latest
   ```

3. **Wait for server to be ready** (check logs):
   ```bash
   docker logs -f deepseek-ocr
   ```

## Running Tests

### Basic test (uses online image):
```bash
python test_inference.py
```

### With your own images:
Place test images in this directory with one of these names:
- `test_image.png`
- `test_image.jpg`
- `sample_receipt.png`
- `sample_document.pdf`

Then run:
```bash
python test_inference.py
```

## Test Images Suggestions

### 1. **Receipt Image**
Download a sample receipt:
```bash
curl -o sample_receipt.png "https://ofasys-multimodal-wlcb-3-toshanghai.oss-accelerate.aliyuncs.com/wpf272043/keepme/image/receipt.png"
```

### 2. **Document/Text Image**
Any image containing text works well:
- Scanned documents
- Screenshots of text
- Photos of books/papers
- Business cards
- Forms and invoices

### 3. **Table/Structured Data**
DeepSeek-OCR excels at structured data:
- Spreadsheet screenshots
- Tables from PDFs
- Financial statements
- Data reports

### 4. **Handwritten Notes**
Test with handwritten content:
- Notes
- Forms
- Signatures

## Output Files

After running tests, you'll get:
- `ocr_result_*.json` - Full API response with metadata
- `ocr_result_*.txt` - Extracted text only
- `deepseek_ocr_test.log` - Detailed execution logs

## Prompts

DeepSeek-OCR supports various prompts:

### Basic OCR:
```python
"Free OCR."
```

### Structured Output (Markdown):
```python
"Convert the image to markdown format."
```

### Table Extraction:
```python
"Extract all tables from this image in markdown format."
```

### Specific Information:
```python
"Extract the total amount and date from this receipt."
```

## Troubleshooting

### Server not responding:
```bash
# Check if container is running
docker ps | grep deepseek-ocr

# Check logs
docker logs deepseek-ocr

# Restart container
docker restart deepseek-ocr
```

### Out of memory:
- Reduce `max_tokens` in the script
- Use smaller images
- Ensure GPU has enough VRAM (16GB+ recommended)

### Slow inference:
- First inference is slower (model loading)
- Subsequent requests are faster
- Use GPU for best performance

## API Documentation

Once the server is running, access:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- OpenAPI Spec: http://localhost:8000/openapi.json
