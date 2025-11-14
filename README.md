# DeepSeek-OCR with vLLM

Production-ready Docker container for serving DeepSeek-OCR via vLLM with OpenAI-compatible API.

## 🚀 Features

- ✅ **Pre-downloaded Model**: Model baked into Docker image (~20GB+)
- ✅ **vLLM Serving**: High-performance inference with OpenAI-compatible API
- ✅ **GPU Optimized**: CUDA 12.1 with cuDNN support
- ✅ **Health Checks**: Built-in Docker health monitoring
- ✅ **Production Ready**: Proper error handling and logging
- ✅ **Test Suite**: Comprehensive testing scripts included

## 📋 Prerequisites

- Docker with NVIDIA GPU support
- NVIDIA GPU with 16GB+ VRAM (recommended)
- NVIDIA Container Toolkit installed

## 🏗️ Building the Container

```bash
cd deployment
chmod +x build.sh
./build.sh
```

This will:
1. Build the Docker image with all dependencies
2. Download the DeepSeek-OCR model (~20GB+)
3. Tag the image as `gsantopaolo/deepseek-ocr:latest`

**Note**: First build takes 30-60 minutes due to model download.

## 🚀 Running the Container

### With GPU (Recommended)
```bash
docker run -d \
  --name deepseek-ocr \
  --runtime nvidia \
  --gpus all \
  -p 8000:8000 \
  --ipc=host \
  gsantopaolo/deepseek-ocr:latest
```

### CPU Only (Slower)
```bash
docker run -d \
  --name deepseek-ocr \
  -p 8000:8000 \
  --ipc=host \
  gsantopaolo/deepseek-ocr:latest
```

### Check Logs
```bash
docker logs -f deepseek-ocr
```

Wait for: `Application startup complete`

## 🧪 Testing

### Quick Test
```bash
cd src
pip install -r requirements.txt
python test_inference.py
```

### Download Test Images
```bash
cd src
chmod +x download_test_images.sh
./download_test_images.sh
```

### Advanced Examples
```bash
cd src
python advanced_examples.py
```

### Batch Processing
```bash
cd src
python batch_process.py test_images/
```

## 📚 Documentation

- **[Testing Guide](src/TESTING_GUIDE.md)** - Complete testing documentation
- **[Source README](src/README.md)** - Test scripts overview
- **[API Docs](http://localhost:8000/docs)** - OpenAPI documentation (when server is running)

## 🌐 API Endpoints

Once running, access:
- **API Base**: http://localhost:8000/v1
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **OpenAPI Spec**: http://localhost:8000/openapi.json

## 📝 Example Usage

### Python (OpenAI Client)
```python
from openai import OpenAI

client = OpenAI(
    api_key="EMPTY",
    base_url="http://localhost:8000/v1"
)

response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-OCR",
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {"url": "https://example.com/image.png"}
            },
            {
                "type": "text",
                "text": "Free OCR."
            }
        ]
    }],
    max_tokens=2048,
    temperature=0.0
)

print(response.choices[0].message.content)
```

### cURL
```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-ai/DeepSeek-OCR",
    "messages": [{
      "role": "user",
      "content": [
        {"type": "image_url", "image_url": {"url": "https://example.com/image.png"}},
        {"type": "text", "text": "Free OCR."}
      ]
    }],
    "max_tokens": 2048,
    "temperature": 0.0
  }'
```

## 🎯 Use Cases

- **Document OCR**: Extract text from scanned documents
- **Receipt Processing**: Parse receipts and invoices
- **Table Extraction**: Convert tables to markdown/JSON
- **Form Processing**: Extract form fields and values
- **Business Cards**: Extract contact information
- **Handwriting**: Recognize handwritten text
- **Multi-language**: Support for multiple languages
- **Markdown Conversion**: Convert documents to markdown

## 📁 Project Structure

```
DeepSeek-OCR/
├── deployment/
│   ├── Dockerfile          # Production Dockerfile with model pre-download
│   └── build.sh           # Build script
├── src/
│   ├── test_inference.py  # Main test script
│   ├── advanced_examples.py # Advanced OCR examples
│   ├── batch_process.py   # Batch processing script
│   ├── requirements.txt   # Python dependencies
│   ├── download_test_images.sh # Download sample images
│   ├── TESTING_GUIDE.md   # Complete testing guide
│   └── README.md          # Testing overview
└── README.md              # This file
```

## 🔧 Configuration

### vLLM Server Arguments
The container runs with these optimized settings:
- `--no-enable-prefix-caching` - Disabled for OCR workloads
- `--mm-processor-cache-gb 0` - No multimodal cache
- `--logits-processors` - Custom n-gram processor for better OCR

### Environment Variables
- `HF_HOME=/opt/hf-cache` - Model cache location
- `VLLM_WORKER_MULTIPROC_METHOD=forkserver` - Process spawning method

## 🐛 Troubleshooting

### Container won't start
```bash
# Check logs
docker logs deepseek-ocr

# Verify GPU access
docker run --rm --gpus all nvidia/cuda:12.1.1-base-ubuntu22.04 nvidia-smi
```

### Out of memory
- Ensure GPU has 16GB+ VRAM
- Reduce `max_tokens` in API requests
- Close other GPU applications

### Slow inference
- First request is slower (model loading)
- Use GPU for best performance
- Subsequent requests are much faster

### Connection refused
- Wait for "Application startup complete" in logs
- Check port 8000 is not in use: `lsof -i :8000`

## 📊 Performance

- **First Request**: ~10-30s (model loading)
- **Subsequent Requests**: ~1-5s (depending on image size)
- **GPU Memory**: ~14-16GB VRAM
- **Throughput**: ~10-20 requests/minute (single GPU)

## 🔗 Links

- **DeepSeek-OCR**: https://github.com/deepseek-ai/DeepSeek-OCR
- **vLLM**: https://docs.vllm.ai/
- **vLLM DeepSeek-OCR Guide**: https://docs.vllm.ai/projects/recipes/en/latest/DeepSeek/DeepSeek-OCR.html

## 📄 License

See [LICENSE](LICENSE) file.

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## ⚠️ Notes

- Model size: ~20GB+ (included in Docker image)
- First build takes 30-60 minutes
- Requires NVIDIA GPU with 16GB+ VRAM for optimal performance
- CPU inference is supported but significantly slower
