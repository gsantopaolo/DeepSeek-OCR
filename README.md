# DeepSeek-OCR Production Deployment

Production-ready Docker container for serving [DeepSeek-OCR](https://github.com/deepseek-ai/DeepSeek-OCR) via vLLM with OpenAI-compatible API. 
This repository provides everything you need to deploy and test DeepSeek-OCR in production environments.

## 📦 What This Repo Provides

### 1. Ready-to-Use Docker Image
Pre-built Docker image with DeepSeek-OCR and vLLM, optimized for production deployment:
- **Docker Hub**: `gsantopaolo/deepseek-ocr:latest` (pull and run immediately)
- **Build yourself**: Full Dockerfile and build scripts included
- **vLLM optimized**: High-performance inference with OpenAI-compatible API
- **GPU ready**: CUDA 12.1 with cuDNN support

### 2. RunPod Cloud Deployment
One-click deployment template for [RunPod](https://www.runpod.io/) cloud GPUs:
- **Template config**: Pre-configured template in `src/runpod-template/`
- **5-minute setup**: From template creation to running API
- **Cost-effective**: ~$0.69/hour (RTX 4090) to ~$1.89/hour (A100)
- **Documentation**: Complete setup guide with troubleshooting

### 3. Comprehensive Testing Suite
- **test script** in [`src/tests/test.py`](/src/tests/)


## ✅ Validated OCR Performance

This deployment has been extensively tested on diverse document types with **outstanding results**:

- ✅ **Financial reports** - Complex multi-page documents with tables and charts
- ✅ **Simple text OCR** - Clean document scans and digital PDFs
- ✅ **Complex pages** - Documents with graphs, diagrams, and mixed content
- ✅ **Handwritten text** - Cursive and printed handwriting
- ✅ **Receipts & invoices** - Structured business documents
- ✅ **Multi-language** - 100+ languages supported

**Test it yourself** with the included test suite to validate on your specific use cases.

## 🚀 Quick Start

Choose your deployment method:

### Option A: Use Pre-Built Image (Fastest)
```bash
docker run -d \
  --name deepseek-ocr \
  --runtime nvidia \
  --gpus all \
  -p 8000:8000 \
  --ipc=host \
  gsantopaolo/deepseek-ocr:latest
```

### Option B: Deploy on RunPod (No Local GPU Required)
See detailed guide in [`src/runpod-template/QUICK_START.md`](src/runpod-template/QUICK_START.md)

1. Use template: `gsantopaolo/deepseek-ocr:latest`
2. Choose GPU: RTX 4090 or A100 (24GB+ VRAM)
3. Deploy in 5 minutes
4. Get your API endpoint: `http://<pod-id>-8000.proxy.runpod.net`

### Option C: Build From Source
```bash
cd deployment
chmod +x build.sh
./build.sh
```

## 🧪 Testing Your Deployment

Once deployed (local or RunPod), test with the included script:

```bash
cd src/tests
pip install openai

# Test local deployment
python test.py --base-url http://localhost:8000

# Test RunPod deployment
python test.py --base-url https://<pod-id>-8000.proxy.runpod.net

# Save results to file
python test.py --base-url http://localhost:8000 --output results.md
```

**What it does:**
- Scans `samples/` directory for all supported file types
- Sends OCR request for each file
- Outputs results with success/failure status
- Saves formatted markdown report

**Supported formats**: JPEG/JPG, PNG, WEBP, BMP, GIF, TIFF, PDF

## 🚀 Features

- ✅ **Pre-downloaded Model**: Model baked into Docker image (~20GB+)
- ✅ **vLLM Serving**: High-performance inference with OpenAI-compatible API
- ✅ **GPU Optimized**: CUDA 12.1 with cuDNN support
- ✅ **Health Checks**: Built-in Docker health monitoring
- ✅ **Production Ready**: Proper error handling and logging
- ✅ **Test Suite**: Comprehensive testing scripts included
- ✅ **RunPod Template**: One-click cloud deployment

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



## 🎯 Use Cases

- **Document OCR**: Extract text from scanned documents
- **Receipt Processing**: Parse receipts and invoices
- **Table Extraction**: Convert tables to markdown/JSON
- **Form Processing**: Extract form fields and values
- **Business Cards**: Extract contact information
- **Handwriting**: Recognize handwritten text
- **Multi-language**: Support for multiple languages
- **Markdown Conversion**: Convert documents to markdown






## 🔗 Links
- [**GenMind blog post about DeepSeek-OCR88**](https://genmind.ch/posts/DeepSeek-OCR-Beyond-Traditional-OCR/)
- [**DeepSeek-OCR**](https://github.com/deepseek-ai/DeepSeek-OCR)
- [**vLLM DeepSeek-OCR Guide**](https://docs.vllm.ai/projects/recipes/en/latest/DeepSeek/DeepSeek-OCR.html)



## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## ⚠️ Notes

- Model size: ~20GB+ (included in Docker image)
- First build takes 30-60 minutes
- Requires NVIDIA GPU with 16GB+ VRAM for optimal performance
- CPU inference is supported but significantly slower
