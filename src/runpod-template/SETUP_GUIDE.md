# RunPod Template Setup Guide - Step by Step

## 📝 Complete Configuration Checklist

Follow these exact steps to create your RunPod template.

---

## Step 1: Navigate to Templates

1. Go to https://www.runpod.io/console/templates
2. Click **"New Template"** button (top right)

---

## Step 2: Basic Information

### Template Name
```
DeepSeek-OCR vLLM Server
```

### Container Image
```
gsantopaolo/deepseek-ocr:1.0.1
```

### Description
```
DeepSeek-OCR frontier OCR model served via vLLM with OpenAI-compatible API. Supports images, PDFs, receipts, invoices, and complex documents. Runs on x86_64 with NVIDIA GPU.
```

---

## Step 3: Storage Configuration

### Container Disk
```
100 GB
```
**Why:** Model (~20GB) + vLLM runtime + system overhead

### Volume Disk
```
50 GB
```
**Why:** Persistent model cache across pod restarts

### Volume Mount Path
```
/root/.cache/huggingface
```
**Why:** HuggingFace model cache location

---

## Step 4: Network Configuration

### Expose HTTP Ports
```
8000
```
**Why:** vLLM API server port

### Expose TCP Ports
```
(leave empty)
```

---

## Step 5: Container Start Command

### Container Start Command
```
(leave empty)
```

**Why:** 
- RunPod automatically configures NVIDIA GPU runtime
- RunPod handles shared memory (`--ipc=host`) automatically
- Your Dockerfile CMD is used by default
- No manual Docker args needed!

**Note:** RunPod's GPU pods automatically include:
- ✅ NVIDIA runtime (`--runtime=nvidia`)
- ✅ GPU access (`--gpus=all`)
- ✅ Shared memory (`--ipc=host`)
- ✅ Large shared memory allocation

### Docker Command
```
(leave empty)
```
**Why:** Uses CMD from Dockerfile

---

## Step 6: Environment Variables

Click **"Add Environment Variable"** for each:

### Variable 1: NVIDIA GPU Access
```
Key:   NVIDIA_VISIBLE_DEVICES
Value: all
```

### Variable 2: NVIDIA Capabilities
```
Key:   NVIDIA_DRIVER_CAPABILITIES
Value: compute,utility
```

### Variable 3: HuggingFace Cache
```
Key:   HF_HOME
Value: /root/.cache/huggingface
```

### Variable 4: Python Unbuffered
```
Key:   PYTHONUNBUFFERED
Value: 1
```

### Variable 5: vLLM Worker Method
```
Key:   VLLM_WORKER_MULTIPROC_METHOD
Value: spawn
```

---

## Step 7: Advanced Settings (Optional)

### Category
```
AI/ML
```

### Is Serverless
```
☐ Unchecked (use On-Demand)
```

---

## Step 8: Save Template

1. Review all settings
2. Click **"Save Template"**
3. Template is now ready to use!

---

## Step 9: Deploy Pod

### From Template
1. Go to **Pods** → **Deploy**
2. Select **"DeepSeek-OCR vLLM Server"** template
3. Choose GPU:
   - **Minimum:** RTX 3090 (24GB)
   - **Recommended:** RTX 4090 or A100 40GB
4. Select region (closest to you)
5. Click **"Deploy On-Demand"**

### Wait for Startup
- **First run:** 5-10 minutes (model download)
- **Subsequent runs:** 30-60 seconds

---

## Step 10: Verify Deployment

### Get Pod URL
Your pod will have a URL like:
```
http://<pod-id>-8000.proxy.runpod.net
```

### Test Health Endpoint
```bash
curl http://<pod-id>-8000.proxy.runpod.net/health
```

Expected response:
```json
{"status": "ok"}
```

### Test Models Endpoint
```bash
curl http://<pod-id>-8000.proxy.runpod.net/v1/models
```

Expected response:
```json
{
  "object": "list",
  "data": [
    {
      "id": "deepseek-ai/DeepSeek-OCR",
      "object": "model",
      ...
    }
  ]
}
```

### View API Documentation
```
http://<pod-id>-8000.proxy.runpod.net/docs
```

---

## Troubleshooting

### ❌ Template won't save
- Check all required fields are filled
- Verify Docker image name is correct
- Ensure environment variables have no typos

### ❌ Pod won't start
- Check logs in RunPod UI
- Verify GPU has minimum 24GB VRAM
- Ensure container disk is 100GB

### ❌ Model download stuck
- Wait 10-15 minutes (large model)
- Check network connectivity
- Restart pod if stuck >15 minutes

### ❌ API returns 404
- Wait for model to load (check logs)
- Verify port 8000 is exposed
- Check health endpoint first

### ❌ Out of memory
- Use larger GPU (A100 recommended)
- Check shared memory (--shm-size=8g)
- Verify --ipc=host is set

---

## Quick Reference Card

**Copy-paste this into RunPod UI:**

```
=== BASIC ===
Name: DeepSeek-OCR vLLM Server
Image: gsantopaolo/deepseek-ocr:1.0.1
Container Disk: 100 GB
Volume Disk: 50 GB
Volume Mount: /root/.cache/huggingface
HTTP Port: 8000

=== CONTAINER START COMMAND ===
(leave empty - RunPod handles GPU runtime automatically)

=== ENV VARS ===
NVIDIA_VISIBLE_DEVICES=all
NVIDIA_DRIVER_CAPABILITIES=compute,utility
HF_HOME=/root/.cache/huggingface
PYTHONUNBUFFERED=1
VLLM_WORKER_MULTIPROC_METHOD=spawn

=== GPU ===
Min: RTX 3090 (24GB)
Recommended: RTX 4090 or A100 40GB
```

---

## Next Steps

1. ✅ Template created
2. ✅ Pod deployed
3. ✅ API tested
4. 📝 Integrate into your application
5. 📊 Monitor usage and costs
6. 🚀 Scale as needed

**Need help?** Check the main README.md or QUICK_START.md in this directory.
