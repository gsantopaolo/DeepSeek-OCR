# 🚀 DeepSeek-OCR vLLM Server - RunPod Template

## 🎯 What is This?

A **plug-and-play** RunPod template to deploy **DeepSeek-OCR** - a frontier OCR model that extracts text from images, PDFs, receipts, invoices, and complex documents with exceptional accuracy.

This template provides a **production-ready inference service** with an **OpenAI-compatible API** - just deploy and start making API calls!

---

## ✨ Why Use This Template?

### 🔥 Key Benefits

- **⚡ Zero Configuration** - Deploy in 1 click, ready in 5 minutes
- **🔌 Plug & Play** - OpenAI-compatible API, works with existing code
- **🎯 Production Ready** - Optimized for performance and reliability
- **💰 Cost Effective** - Pay only for GPU time you use
- **📦 Pre-configured** - All settings optimized for DeepSeek-OCR
- **🔒 HTTPS Enabled** - Secure API access out of the box

### 🎨 What Can It Do?

- ✅ **Extract text** from images (PNG, JPEG, TIFF, WebP)
- ✅ **Process receipts** and invoices with high accuracy
- ✅ **Parse tables** and structured documents
- ✅ **Read charts** and graphs
- ✅ **Recognize handwriting** (cursive, print)
- ✅ **Multi-language** support (100+ languages)
- ✅ **Complex layouts** (multi-column, mixed content)
- ✅ **Batch processing** for multiple documents

---

## 🚀 Quick Start

### 1️⃣ Deploy
```
Click "Deploy" → Select GPU → Wait 5 minutes
```

### 2️⃣ Get Your API URL
```
https://<your-pod-id>-8000.proxy.runpod.net
```

### 3️⃣ Start Using
```python
from openai import OpenAI

client = OpenAI(
    api_key="EMPTY",
    base_url="https://<your-pod-id>-8000.proxy.runpod.net/v1"
)

response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-OCR",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": "https://example.com/receipt.png"}},
            {"type": "text", "text": "Free OCR."}
        ]
    }],
    max_tokens=2048,
    temperature=0.0
)

print(response.choices[0].message.content)
```

---

## 💻 Technical Specifications

### 📦 What's Included

- **Model:** DeepSeek-OCR (~20GB)
- **Engine:** vLLM (high-performance inference)
- **API:** OpenAI-compatible REST API
- **Runtime:** NVIDIA GPU with CUDA support
- **Architecture:** x86_64 Linux

### 🎛️ Pre-configured Settings

| Setting | Value | Why? |
|---------|-------|------|
| Container Disk | 100 GB | Model + runtime + cache |
| Volume Disk | 50 GB | Persistent model cache |
| GPU Runtime | NVIDIA | CUDA acceleration (automatic) |
| Shared Memory | Auto | RunPod handles automatically |
| API Port | 8000 | vLLM default |

**Note:** RunPod automatically configures GPU runtime, shared memory, and IPC settings. No manual Docker args needed!

### 🖥️ GPU Requirements

| GPU | VRAM | Status | Best For |
|-----|------|--------|----------|
| RTX 3090 | 24GB | ✅ Minimum | Testing, light use |
| RTX 4090 | 24GB | ✅ Good | Development, moderate use |
| A100 40GB | 40GB | ⭐ Recommended | Production, high throughput |
| A100 80GB | 80GB | 🚀 Excellent | Batch processing, scaling |

---

## 📊 Performance Benchmarks

| GPU | Tokens/sec | Latency | Throughput |
|-----|------------|---------|------------|
| RTX 3090 | ~30 | Medium | 100-200 pages/hour |
| RTX 4090 | ~50 | Low | 200-400 pages/hour |
| A100 40GB | ~80 | Very Low | 400-800 pages/hour |

*Benchmarks based on typical receipt/invoice processing*

---

## 💰 Cost Estimation

### On-Demand Pricing (approximate)

| GPU | $/hour | Daily (24h) | Monthly |
|-----|--------|-------------|---------|
| RTX 3090 | $0.34 | $8.16 | $245 |
| RTX 4090 | $0.69 | $16.56 | $497 |
| A100 40GB | $1.89 | $45.36 | $1,361 |

### 💡 Cost Optimization Tips

- Use **Serverless** for intermittent workloads
- Use **Spot Instances** for 50-70% savings
- Enable **Auto-pause** when idle
- Use **Volume Mount** to avoid re-downloading model

---

## 🔧 Use Cases

### 📄 Document Processing
- Invoice extraction and parsing
- Receipt digitization
- Form data extraction
- Contract analysis

### 🏢 Business Automation
- Expense report automation
- Purchase order processing
- Identity document verification
- Insurance claim processing

### 📚 Content Digitization
- Book and manuscript scanning
- Archive digitization
- Historical document preservation
- Library catalog creation

### 🌐 Multi-language Applications
- International document processing
- Translation preparation
- Cross-border compliance
- Global business operations

---

## 🛠️ API Features

### ✅ OpenAI-Compatible
Works with any OpenAI SDK or tool:
- Python `openai` library
- JavaScript/TypeScript SDK
- LangChain integration
- LlamaIndex support
- REST API direct access

### 🔌 Endpoints Available

```
GET  /health              - Health check
GET  /v1/models           - List available models
POST /v1/chat/completions - OCR inference
GET  /docs                - API documentation
GET  /metrics             - Prometheus metrics
```

### 📸 Input Methods

- **URL:** Direct image URLs
- **Base64:** Embedded image data
- **Batch:** Multiple images per request

---

## 📖 Documentation & Support

### 📚 Learn More

- **📝 Blog Post:** [genmind.ch](https://genmind.ch) - Detailed guide and use cases
- **💻 GitHub Repo:** [github.com/gsantopaolo/DeepSeek-OCR](https://github.com/gsantopaolo/DeepSeek-OCR) - Full source code and examples
- **🔬 Model Card:** [DeepSeek-OCR on HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-OCR)
- **⚡ vLLM Docs:** [docs.vllm.ai](https://docs.vllm.ai)

### 🆘 Getting Help

1. Check the [GitHub Issues](https://github.com/gsantopaolo/DeepSeek-OCR/issues)
2. Read the [Setup Guide](./SETUP_GUIDE.md) in this template
3. Visit [genmind.ch](https://genmind.ch) for tutorials
4. Join RunPod Discord for community support

---

## 🎯 What Makes This Template Special?

### 🔧 Fully Optimized
- Pre-configured NVIDIA runtime
- Optimized shared memory settings
- Proper GPU allocation
- Volume mounting for persistence
- All environment variables set

### 🚀 Production Ready
- Health checks enabled
- Metrics endpoint available
- Error handling configured
- Logging optimized
- Auto-restart on failure

### 📦 Complete Package
- Model pre-downloaded (optional)
- All dependencies included
- No manual configuration needed
- Works out of the box
- HTTPS enabled by default

---

## 🔐 Security & Privacy

- ✅ **Private Deployment** - Your own isolated pod
- ✅ **No Data Logging** - Images not stored or logged
- ✅ **HTTPS Encryption** - Secure API communication
- ✅ **No External Calls** - Model runs locally on GPU
- ✅ **Full Control** - You own the infrastructure

---

## 🎓 Example Applications

### Python Script
```python
# Process a receipt
import openai

client = openai.OpenAI(
    api_key="EMPTY",
    base_url="https://<pod-id>-8000.proxy.runpod.net/v1"
)

result = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-OCR",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": "receipt.jpg"}},
            {"type": "text", "text": "Extract all items and prices."}
        ]
    }]
)

print(result.choices[0].message.content)
```

### cURL Command
```bash
curl https://<pod-id>-8000.proxy.runpod.net/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-ai/DeepSeek-OCR",
    "messages": [{
      "role": "user",
      "content": [
        {"type": "image_url", "image_url": {"url": "https://example.com/invoice.png"}},
        {"type": "text", "text": "Free OCR."}
      ]
    }]
  }'
```

### JavaScript/TypeScript
```typescript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: 'EMPTY',
  baseURL: 'https://<pod-id>-8000.proxy.runpod.net/v1'
});

const response = await client.chat.completions.create({
  model: 'deepseek-ai/DeepSeek-OCR',
  messages: [{
    role: 'user',
    content: [
      {type: 'image_url', image_url: {url: 'document.png'}},
      {type: 'text', text: 'Free OCR.'}
    ]
  }]
});

console.log(response.choices[0].message.content);
```

---

## 🎉 Ready to Get Started?

1. **Click "Deploy"** to launch your pod
2. **Wait 5 minutes** for model download (first time only)
3. **Copy your API URL** from the pod details
4. **Start making requests** with your favorite language/tool

### 🌟 That's It!

No configuration, no setup, no hassle. Just pure OCR power at your fingertips.

---

## 📞 Credits & Links

**Created by:** [Giuseppe Santopaolo](https://genmind.ch)

**Resources:**
- 📝 **Blog:** [genmind.ch](https://genmind.ch)
- 💻 **GitHub:** [github.com/gsantopaolo/DeepSeek-OCR](https://github.com/gsantopaolo/DeepSeek-OCR)
- 🤗 **Model:** [DeepSeek-OCR](https://huggingface.co/deepseek-ai/DeepSeek-OCR)
- ⚡ **Engine:** [vLLM](https://github.com/vllm-project/vllm)

---

## 📄 License

This template is provided as-is. Check the [DeepSeek-OCR model license](https://huggingface.co/deepseek-ai/DeepSeek-OCR) for usage terms.

---

**🚀 Happy OCR-ing! 🎯**
