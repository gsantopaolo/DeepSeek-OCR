# RunPod Quick Start - DeepSeek-OCR

## 🚀 5-Minute Setup

### 1. Create Template
```
RunPod Console → Templates → New Template

Name: DeepSeek-OCR vLLM Server
Image: gsantopaolo/deepseek-ocr:1.0.1
Container Disk: 100 GB
Volume Disk: 50 GB (for model cache)
Volume Mount: /root/.cache/huggingface
Port: 8000
Container Start Command: (leave empty)

Environment Variables:
  NVIDIA_VISIBLE_DEVICES=all
  NVIDIA_DRIVER_CAPABILITIES=compute,utility
  HF_HOME=/root/.cache/huggingface
  PYTHONUNBUFFERED=1
  VLLM_WORKER_MULTIPROC_METHOD=spawn
```

### 2. Deploy Pod
```
Pods → Deploy → Select Template
GPU: RTX 4090 or A100
Region: Closest to you
Deploy On-Demand
```

### 3. Wait for Startup
```
⏱️ First run: 5-10 minutes (model download)
📊 Check logs for: "vLLM server started"
```

### 4. Get API URL
```
Your pod URL: http://<pod-id>-8000.proxy.runpod.net
```

### 5. Test
```bash
# Health check
curl http://<pod-id>-8000.proxy.runpod.net/health

# OCR test
curl http://<pod-id>-8000.proxy.runpod.net/v1/chat/completions \
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
    "max_tokens": 2048,
    "temperature": 0.0
  }'
```

---

## 📋 Template Settings Cheat Sheet

| Setting | Value |
|---------|-------|
| **Container Image** | `gsantopaolo/deepseek-ocr:1.0.1` |
| **Container Disk** | `100 GB` |
| **Volume Disk** | `50 GB` |
| **Volume Mount** | `/root/.cache/huggingface` |
| **Expose HTTP Ports** | `8000` |
| **Container Start Command** | (leave empty) |
| **Min GPU** | 24GB VRAM (RTX 3090/4090) |
| **Recommended GPU** | A100 40GB |
| **Architecture** | x86_64 with NVIDIA GPU |

### Required Environment Variables:
```bash
NVIDIA_VISIBLE_DEVICES=all
NVIDIA_DRIVER_CAPABILITIES=compute,utility
HF_HOME=/root/.cache/huggingface
PYTHONUNBUFFERED=1
VLLM_WORKER_MULTIPROC_METHOD=spawn
```

---

## 💰 Cost Calculator

| GPU | $/hour | Daily | Monthly |
|-----|--------|-------|---------|
| RTX 4090 | $0.69 | $16.56 | $497 |
| A100 40GB | $1.89 | $45.36 | $1,361 |

**Tip:** Use Serverless for intermittent workloads!

---

## 🔗 Important URLs

Once deployed, access:

- **API Base:** `http://<pod-id>-8000.proxy.runpod.net/v1`
- **Health:** `http://<pod-id>-8000.proxy.runpod.net/health`
- **Docs:** `http://<pod-id>-8000.proxy.runpod.net/docs`
- **Models:** `http://<pod-id>-8000.proxy.runpod.net/v1/models`

---

## 🐍 Python Example

```python
from openai import OpenAI

client = OpenAI(
    api_key="EMPTY",
    base_url="http://<pod-id>-8000.proxy.runpod.net/v1"
)

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

---

## ⚠️ Common Issues

| Issue | Solution |
|-------|----------|
| Pod won't start | Increase disk to 40GB |
| Model download stuck | Wait 10 min, then restart |
| API 404 | Wait for model load (check logs) |
| Out of memory | Use larger GPU (min 24GB) |
| Slow inference | Use A100 or reduce image size |

---

## 📊 Performance

| GPU | Tokens/sec | Latency |
|-----|------------|---------|
| RTX 3090 | ~30 | Medium |
| RTX 4090 | ~50 | Low |
| A100 40GB | ~80 | Very Low |

---

## 🎯 Next Steps

1. ✅ Deploy pod
2. ✅ Test API
3. ✅ Integrate into your app
4. ✅ Monitor usage
5. ✅ Scale as needed

**Need help?** Check the full README.md in this directory!
