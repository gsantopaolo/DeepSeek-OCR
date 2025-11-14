# 📚 RunPod Template Documentation Index

Welcome to the DeepSeek-OCR RunPod template documentation!

## 📄 Files in This Directory

### 🎯 For Template Creation

1. **[TEMPLATE_README.md](./TEMPLATE_README.md)** ⭐
   - **Use this as the template description in RunPod UI**
   - Beautiful, emoji-rich README with all features
   - Links to blog and GitHub repo
   - Complete usage examples

2. **[template.json](./template.json)**
   - Complete JSON configuration
   - Can be imported via RunPod API
   - All settings pre-configured

3. **[.runpod-settings](./.runpod-settings)**
   - Quick reference for manual setup
   - Copy-paste values for RunPod UI

### 📖 Setup Guides

4. **[QUICK_START.md](./QUICK_START.md)**
   - 5-minute deployment guide
   - Essential settings only
   - Perfect for experienced users

5. **[SETUP_GUIDE.md](./SETUP_GUIDE.md)**
   - Step-by-step visual guide
   - Every field explained
   - Perfect for first-time users

6. **[README.md](./README.md)**
   - Comprehensive documentation
   - Advanced configuration
   - Troubleshooting guide
   - Cost estimation

## 🚀 Quick Navigation

### I want to...

**Create the template in RunPod UI**
→ Follow [SETUP_GUIDE.md](./SETUP_GUIDE.md)
→ Copy description from [TEMPLATE_README.md](./TEMPLATE_README.md)

**Get a quick reference**
→ Check [QUICK_START.md](./QUICK_START.md)
→ Or use [.runpod-settings](./.runpod-settings)

**Import via API**
→ Use [template.json](./template.json)

**Learn about features**
→ Read [TEMPLATE_README.md](./TEMPLATE_README.md)

**Troubleshoot issues**
→ See [README.md](./README.md) troubleshooting section

## ⚙️ Template Configuration Summary

```
Image: gsantopaolo/deepseek-ocr:1.0.1
Container Disk: 100 GB
Volume Disk: 50 GB
Port: 8000
Container Start Command: --runtime=nvidia --gpus=all --ipc=host --shm-size=24g

Environment Variables:
  NVIDIA_VISIBLE_DEVICES=all
  NVIDIA_DRIVER_CAPABILITIES=compute,utility
  HF_HOME=/root/.cache/huggingface
  PYTHONUNBUFFERED=1
  VLLM_WORKER_MULTIPROC_METHOD=forkserver
```

## 🔗 External Resources

- **📝 Blog:** [genmind.ch](https://genmind.ch)
- **💻 GitHub:** [github.com/gsantopaolo/DeepSeek-OCR](https://github.com/gsantopaolo/DeepSeek-OCR)
- **🤗 Model:** [DeepSeek-OCR](https://huggingface.co/deepseek-ai/DeepSeek-OCR)
- **⚡ vLLM:** [docs.vllm.ai](https://docs.vllm.ai)

## 📞 Support

For help:
1. Check the documentation files above
2. Visit [genmind.ch](https://genmind.ch) for tutorials
3. Open an issue on [GitHub](https://github.com/gsantopaolo/DeepSeek-OCR/issues)
4. Join RunPod Discord community

---

**Created by Giuseppe Santopaolo** | [genmind.ch](https://genmind.ch)
