# RunPod Template for DeepSeek-OCR

This directory contains the RunPod template configuration for deploying DeepSeek-OCR vLLM server.

## Quick Deploy

### Option 1: Create Template via RunPod UI

1. **Go to RunPod Console**
   - Navigate to https://www.runpod.io/console/templates

2. **Click "New Template"**

3. **Fill in the following settings:**

   ```
   Template Name: DeepSeek-OCR vLLM Server
   
   Container Image: gsantopaolo/deepseek-ocr:1.0.1
   
   Container Disk: 100 GB
   
   Volume Disk: 50 GB (for persistent model cache)
   
   Volume Mount Path: /root/.cache/huggingface
   
   Expose HTTP Ports: 8000
   
   Expose TCP Ports: (leave empty)
   
   Container Start Command: (leave empty)
   
   Environment Variables:
     NVIDIA_VISIBLE_DEVICES = all
     NVIDIA_DRIVER_CAPABILITIES = compute,utility
     HF_HOME = /root/.cache/huggingface
     PYTHONUNBUFFERED = 1
     VLLM_WORKER_MULTIPROC_METHOD = spawn
   
   Docker Command: (leave empty - uses default from Dockerfile)
   
   Category: AI/ML
   ```

4. **Add Description:**
   ```
   DeepSeek-OCR frontier OCR model served via vLLM with OpenAI-compatible API. 
   Supports images, PDFs, receipts, invoices, and complex documents.
   ```

5. **Click "Save Template"**

6. **Deploy:**
   - Go to "Pods" → "Deploy"
   - Select your template
   - Choose GPU (minimum 24GB VRAM)
   - Click "Deploy On-Demand" or "Deploy Serverless"

---

### Option 2: Use Template JSON (Advanced)

The `template.json` file contains the complete template configuration. You can:

1. Import it via RunPod API
2. Use it as reference for manual setup
3. Share it with your team

---

## GPU Recommendations

| GPU | VRAM | Status | Notes |
|-----|------|--------|-------|
| RTX 3090 | 24GB | ✅ Minimum | Works but tight on memory |
| RTX 4090 | 24GB | ✅ Good | Better performance than 3090 |
| A5000 | 24GB | ✅ Good | Enterprise option |
| A6000 | 48GB | ✅ Excellent | Plenty of headroom |
| A100 40GB | 40GB | ✅ Excellent | Best price/performance |
| A100 80GB | 80GB | ✅ Overkill | For batch processing |
| H100 | 80GB | ✅ Overkill | Fastest but expensive |

**Recommendation:** RTX 4090 or A100 40GB for best value.

---

## Deployment Steps

### 1. Deploy Pod

```bash
# Via RunPod UI:
1. Select template: "DeepSeek-OCR vLLM Server"
2. Choose GPU: RTX 4090 or A100
3. Select region: Closest to you
4. Deploy
```

### 2. Wait for Model Download

First startup takes **5-10 minutes** to download the model (~20GB).

Check logs:
```bash
# In RunPod UI, click "Logs" on your pod
# You should see:
# "Downloading model deepseek-ai/DeepSeek-OCR..."
# "Model loaded successfully"
# "vLLM server started on port 8000"
```

### 3. Get Your API Endpoint

Your pod will have a URL like:
```
http://<pod-id>-8000.proxy.runpod.net
```

Example:
```
http://abc123xyz-8000.proxy.runpod.net
```

### 4. Test the API

```bash
# Health check
curl http://<pod-id>-8000.proxy.runpod.net/health

# List models
curl http://<pod-id>-8000.proxy.runpod.net/v1/models

# API documentation
open http://<pod-id>-8000.proxy.runpod.net/docs
```

---

## Usage Examples

### Python (OpenAI SDK)

```python
from openai import OpenAI

# Replace with your pod URL
client = OpenAI(
    api_key="EMPTY",
    base_url="http://<pod-id>-8000.proxy.runpod.net/v1"
)

# OCR from URL
response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-OCR",
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://example.com/receipt.png"
                }
            },
            {
                "type": "text",
                "text": "Free OCR."
            }
        ]
    }],
    max_tokens=2048,
    temperature=0.0,
    extra_body={
        "skip_special_tokens": False,
        "vllm_xargs": {
            "ngram_size": 30,
            "window_size": 90,
            "whitelist_token_ids": [128821, 128822]  # <td>, </td>
        }
    }
)

print(response.choices[0].message.content)
```

### cURL

```bash
curl http://<pod-id>-8000.proxy.runpod.net/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-ai/DeepSeek-OCR",
    "messages": [{
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://example.com/receipt.png"
          }
        },
        {
          "type": "text",
          "text": "Free OCR."
        }
      ]
    }],
    "max_tokens": 2048,
    "temperature": 0.0
  }'
```

### JavaScript/TypeScript

```typescript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: 'EMPTY',
  baseURL: 'http://<pod-id>-8000.proxy.runpod.net/v1'
});

const response = await client.chat.completions.create({
  model: 'deepseek-ai/DeepSeek-OCR',
  messages: [{
    role: 'user',
    content: [
      {
        type: 'image_url',
        image_url: {
          url: 'https://example.com/receipt.png'
        }
      },
      {
        type: 'text',
        text: 'Free OCR.'
      }
    ]
  }],
  max_tokens: 2048,
  temperature: 0.0
});

console.log(response.choices[0].message.content);
```

---

## Advanced Configuration

### Persistent Model Cache (Optional)

To avoid re-downloading the model on each pod restart:

1. **Create a Network Volume:**
   - Go to RunPod → Storage → Network Volumes
   - Create volume: 25 GB
   - Name: `deepseek-ocr-models`

2. **Update Template:**
   - Volume Disk: 25 GB
   - Volume Mount Path: `/root/.cache/huggingface`

3. **First Run:**
   - Model downloads to volume
   - Subsequent runs use cached model

### Environment Variables

Add these if needed:

```bash
# HuggingFace token (for private models)
HUGGING_FACE_HUB_TOKEN=hf_xxxxxxxxxxxxx

# Custom cache directory
HF_HOME=/workspace/models

# Logging level
VLLM_LOGGING_LEVEL=INFO
```

---

## Cost Estimation

### On-Demand Pricing (approximate)

| GPU | $/hour | 24h Cost | Monthly Cost |
|-----|--------|----------|--------------|
| RTX 3090 | $0.34 | $8.16 | $245 |
| RTX 4090 | $0.69 | $16.56 | $497 |
| A100 40GB | $1.89 | $45.36 | $1,361 |
| A100 80GB | $2.49 | $59.76 | $1,793 |

### Serverless Pricing

- **Idle:** $0.0003/sec (~$0.018/min)
- **Active:** Varies by GPU
- **Best for:** Intermittent use

---

## Troubleshooting

### Pod won't start
```bash
# Check logs in RunPod UI
# Common issues:
# - Insufficient disk space (increase to 40GB)
# - GPU out of memory (use larger GPU)
# - Image pull failed (check Docker Hub)
```

### Model download stuck
```bash
# Check logs for:
# "Downloading model..."
# If stuck >15 min, restart pod
```

### API returns 404
```bash
# Wait for model to load (5-10 min first run)
# Check health endpoint:
curl http://<pod-id>-8000.proxy.runpod.net/health
```

### Out of memory
```bash
# Use larger GPU (minimum 24GB VRAM)
# Or reduce max_tokens in requests
```

### Slow inference
```bash
# Use faster GPU (A100 > RTX 4090 > RTX 3090)
# Reduce image resolution
# Use batch processing for multiple images
```

---

## Monitoring

### Check Pod Status
```bash
# In RunPod UI:
# - CPU/GPU usage
# - Memory usage
# - Network traffic
# - Logs
```

### API Metrics
```bash
# Check vLLM metrics endpoint
curl http://<pod-id>-8000.proxy.runpod.net/metrics
```

---

## Scaling

### Horizontal Scaling
- Deploy multiple pods
- Use load balancer
- Distribute requests

### Vertical Scaling
- Use larger GPU (A100 80GB)
- Increase batch size
- Enable tensor parallelism (for multi-GPU)

---

## Security

### API Access
- RunPod provides HTTPS by default
- No authentication required (add your own if needed)
- Use environment variables for secrets

### Network
- Pods are isolated
- Only exposed ports are accessible
- Use RunPod's built-in firewall

---

## Support

- **RunPod Docs:** https://docs.runpod.io/
- **DeepSeek-OCR:** https://github.com/deepseek-ai/DeepSeek-OCR
- **vLLM Docs:** https://docs.vllm.ai/
- **Issues:** Create issue in your GitHub repo

---

## Template Updates

To update the template:

1. Build new Docker image version
2. Push to Docker Hub: `gsantopaolo/deepseek-ocr:1.0.2`
3. Update template in RunPod UI
4. Redeploy pods

---

## License

This template is for deploying the DeepSeek-OCR model. Check model license for usage terms.
