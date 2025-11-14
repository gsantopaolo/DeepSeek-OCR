#!/bin/bash
# Quick test runner for NVIDIA report OCR

set -e

echo "🚀 NVIDIA Report OCR Test Runner"
echo ""

# Check if base URL is provided
if [ -z "$1" ]; then
    echo "❌ Error: Base URL required"
    echo ""
    echo "Usage:"
    echo "  ./run_test.sh https://<pod-id>-8000.proxy.runpod.net"
    echo "  ./run_test.sh http://localhost:8000"
    echo ""
    exit 1
fi

BASE_URL="$1"
OUTPUT_FILE="${2:-nvidia_report_ocr.md}"

echo "📡 API URL: $BASE_URL"
echo "💾 Output: $OUTPUT_FILE"
echo ""

# Check if images exist
if [ ! -d "samples/NVIDIAAn_images" ]; then
    echo "❌ Error: samples/NVIDIAAn_images directory not found"
    exit 1
fi

PAGE_COUNT=$(ls -1 samples/NVIDIAAn_images/page_*.png 2>/dev/null | wc -l)
if [ "$PAGE_COUNT" -eq 0 ]; then
    echo "❌ Error: No page images found in samples/NVIDIAAn_images/"
    exit 1
fi

echo "✅ Found $PAGE_COUNT pages to process"
echo ""

# Run the test
python test.py --base-url "$BASE_URL" --output "$OUTPUT_FILE"

# Check if successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✨ Test completed successfully!"
    echo ""
    echo "📖 View the report:"
    echo "   cat $OUTPUT_FILE"
    echo "   open $OUTPUT_FILE"
else
    echo ""
    echo "❌ Test failed"
    exit 1
fi
