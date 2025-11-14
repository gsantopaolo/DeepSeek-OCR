#!/bin/bash
# ============================================================================
# Build script for DeepSeek-OCR with vLLM
# ============================================================================
# remember to: chmod +x build.sh
set -e

# Version configuration
VERSION="${VERSION:-1.0.6}"
IMAGE_NAME="gsantopaolo/deepseek-ocr"

echo "🏗️  Building DeepSeek-OCR with vLLM Container..."
echo "📦 Image: ${IMAGE_NAME}:${VERSION}"
echo "⚠️  Note: This build will download ~20GB+ model during build"
echo ""

# Build the image with multiple tags
echo "📦 Building Docker image..."
cd "$(dirname "$0")/.."

# Detect if running on Apple Silicon and force x86_64 platform
ARCH=$(uname -m)
if [ "$ARCH" = "arm64" ]; then
  echo "🍎 Detected Apple Silicon (ARM64)"
  echo "🔧 Building for linux/amd64 platform (required for NVIDIA CUDA)"
  docker buildx build --platform linux/amd64 \
    -f deployment/Dockerfile \
    -t ${IMAGE_NAME}:${VERSION} \
    -t ${IMAGE_NAME}:latest \
    --load \
    .
else
  echo "🖥️  Detected x86_64 architecture"
  docker build -f deployment/Dockerfile \
    -t ${IMAGE_NAME}:${VERSION} \
    -t ${IMAGE_NAME}:latest \
    .
fi

echo ""
echo "✅ Build complete!"
echo ""
echo "🚀 To run the container:"
echo ""
echo "   docker run -d \\"
echo "     --name deepseek-ocr \\"
echo "     --runtime nvidia \\"
echo "     --gpus all \\"
echo "     -p 8000:8000 \\"
echo "     -v ~/.cache/huggingface:/root/.cache/huggingface \\"
echo "     --ipc=host \\"
echo "     ${IMAGE_NAME}:${VERSION}"
echo ""
echo "   ⚠️  Note: Model (~20GB) will download on first run to ~/.cache/huggingface"
echo ""
echo "   Or without GPU (CPU only - slower):"
echo "   docker run -d \\"
echo "     --name deepseek-ocr \\"
echo "     -p 8000:8000 \\"
echo "     -v ~/.cache/huggingface:/opt/hf-cache \\"
echo "     --ipc=host \\"
echo "     ${IMAGE_NAME}:${VERSION}"
echo ""
echo "🌐 Access URLs:"
echo "   vLLM API:     http://localhost:8000/v1"
echo "   API Docs:     http://localhost:8000/docs"
echo "   Health Check: http://localhost:8000/health"
echo ""
echo "📝 Example API usage:"
echo "   curl http://localhost:8000/v1/chat/completions \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{"
echo "       \"model\": \"deepseek-ai/DeepSeek-OCR\","
echo "       \"messages\": [{"
echo "         \"role\": \"user\","
echo "         \"content\": ["
echo "           {\"type\": \"image_url\", \"image_url\": {\"url\": \"https://example.com/image.png\"}},"
echo "           {\"type\": \"text\", \"text\": \"Free OCR.\"}"
echo "         ]"
echo "       }],"
echo "       \"max_tokens\": 2048,"
echo "       \"temperature\": 0.0"
echo "     }'"
echo ""
