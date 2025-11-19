# DeepSeek-OCR Quick Start Guide

## 🚀 Choose Your Deployment

### Option A: Pre-Built Docker Image (Fastest - No Build Required)
```bash
# Pull and run directly from Docker Hub
docker run -d \
  --name deepseek-ocr \
  --runtime nvidia \
  --gpus all \
  -p 8000:8000 \
  --ipc=host \
  gsantopaolo/deepseek-ocr:latest

# Check logs
docker logs -f deepseek-ocr
# Wait for: "Application startup complete"
```

### Option B: RunPod Cloud Deployment (No Local GPU)
```
1. Go to: https://www.runpod.io/console/templates
2. Create template with image: gsantopaolo/deepseek-ocr:latest
3. Choose GPU: RTX 4090 or A100 (24GB+ VRAM)
4. Deploy - Get endpoint: http://<pod-id>-8000.proxy.runpod.net
```

**Full RunPod guide**: See [`src/runpod-template/QUICK_START.md`](src/runpod-template/QUICK_START.md)

### Option C: Build From Source
```bash
cd deployment
chmod +x build.sh
./build.sh  # Takes 30-60 min first time
```

## 🧪 Test Your Deployment

### Quick Test
```bash
cd src/tests
pip install openai

# Test local Docker
python test.py --base-url http://localhost:8000

# Test RunPod deployment
python test.py --base-url https://<pod-id>-8000.proxy.runpod.net

# Save results to markdown
python test.py --base-url http://localhost:8000 --output results.md
```

This will test all supported file types (JPEG, PNG, PDF, etc.) in the `samples/` directory.

## 📝 Common Commands

### Container Management
```bash
# Start container
docker start deepseek-ocr

# Stop container
docker stop deepseek-ocr

# View logs
docker logs -f deepseek-ocr

# Restart container
docker restart deepseek-ocr

# Remove container
docker rm -f deepseek-ocr
```

### Testing
```bash
cd src

# Basic test
python test_inference.py

# Advanced examples
python advanced_examples.py

# Batch processing
python batch_process.py test_images/

# Download test images
./download_test_images.sh
```

### Health Check
```bash
# Check if server is healthy
curl http://localhost:8000/health

# View API docs
open http://localhost:8000/docs
```

## 🎯 Quick API Test

### Python
```python
from openai import OpenAI

client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")

response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-OCR",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": "https://example.com/image.png"}},
            {"type": "text", "text": "Free OCR."}
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
        {"type": "image_url", "image_url": {"url": "https://example.com/receipt.png"}},
        {"type": "text", "text": "Free OCR."}
      ]
    }],
    "max_tokens": 2048
  }'
```

## 🎨 Common Prompts

| Use Case | Prompt |
|----------|--------|
| Basic OCR | `"Free OCR."` |
| Markdown | `"Convert to markdown format."` |
| Tables | `"Extract all tables in markdown format."` |
| Receipt | `"Extract store name, date, items, and total."` |
| Form | `"Extract all form fields and values."` |
| JSON | `"Extract text as JSON with title and sections."` |

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Container won't start | Check logs: `docker logs deepseek-ocr` |
| Connection refused | Wait for startup, check: `docker logs -f deepseek-ocr` |
| Out of memory | Ensure 16GB+ GPU VRAM, close other apps |
| Slow inference | First request is slow, subsequent are fast |
| Port in use | Change port: `-p 8001:8000` |

## 📊 Expected Performance

- **First Request**: 10-30 seconds (model loading)
- **Subsequent**: 1-5 seconds per image
- **GPU Memory**: 14-16GB VRAM
- **Throughput**: 10-20 requests/minute

## 🔗 Quick Links

- **API Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health
- **Full Guide**: [README.md](README.md)
- **Testing Guide**: [src/TESTING_GUIDE.md](src/TESTING_GUIDE.md)

## 💡 Tips

1. **First build is slow** - Model download takes time, be patient
2. **Use GPU** - 10-50x faster than CPU
3. **Batch process** - Use `batch_process.py` for multiple images
4. **Test images** - Run `./download_test_images.sh` for samples
5. **Check logs** - Always check logs if something fails
