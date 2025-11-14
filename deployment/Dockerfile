# Use official vLLM NIGHTLY image (required for DeepSeek-OCR until v0.11.1)
FROM vllm/vllm-openai:nightly

# Install system tools and monitoring utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    vim \
    htop \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install GPU monitoring tools
RUN pip install --no-cache-dir \
    nvitop \
    gpustat

# TODO: Resolution Mode Configuration
# Currently using GUNDAM mode (base_size=1024, image_size=640, crop_mode=True)
# This is HARDCODED in vLLM and cannot be changed via environment variables yet.
# 
# Why Gundam mode is optimal for our use case:
# - Dynamic resolution: n×640×640 + 1×1024×1024
# - Adapts automatically to image complexity
# - Best for financial reports with mixed content (tables, text, charts)
# - Balances quality and performance
#
# Available modes:
# - Tiny:   base_size=512,  image_size=512,  crop_mode=False (64 tokens)
# - Small:  base_size=640,  image_size=640,  crop_mode=False (100 tokens)
# - Base:   base_size=1024, image_size=1024, crop_mode=False (256 tokens)
# - Large:  base_size=1280, image_size=1280, crop_mode=False (400 tokens)
# - Gundam: base_size=1024, image_size=640,  crop_mode=True  (variable tokens) ← CURRENT
#
# To change mode: Fork vLLM and modify constants in:
# https://github.com/vllm-project/vllm/blob/main/vllm/transformers_utils/processors/deepseek_ocr.py#L10-L13
#
# vLLM plans to expose this as mm_processor_kwargs in the future:
# https://github.com/vllm-project/vllm/blob/main/vllm/transformers_utils/processors/deepseek_ocr.py#L15
# (See comment: "TODO(Isotr0py): Expose as mm_kwargs")

# Environment optimizations
ENV VLLM_IMAGE_FETCH_TIMEOUT=30
ENV TORCH_CUDNN_V8_API_ENABLED=1
ENV HF_HUB_ENABLE_HF_TRANSFER=1

# Expose vLLM API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start vLLM server with DeepSeek-OCR optimized settings
# Model will be downloaded on first run to /root/.cache/huggingface
# Using GUNDAM resolution mode (dynamic: n×640×640 + 1×1024×1024)
CMD ["deepseek-ai/DeepSeek-OCR", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--no-enable-prefix-caching", \
     "--mm-processor-cache-gb", "0", \
     "--logits-processors", "vllm.model_executor.models.deepseek_ocr:NGramPerReqLogitsProcessor", \
     "--trust-remote-code", \
     "--max-model-len", "8192"]
