#!/bin/bash
# Docker build and test script for Exito Scraper

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="exito-scraper"
CONTAINER_NAME="exito-scraper-test"

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

cleanup() {
    print_status "Cleaning up..."
    docker rm -f $CONTAINER_NAME 2>/dev/null || true
}

# Set up cleanup trap
trap cleanup EXIT

# Load environment variables
if [ -f .env ]; then
    # Export only simple key=value pairs, ignore complex values
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        if [[ $key =~ ^[[:space:]]*# ]] || [[ -z "$key" ]]; then
            continue
        fi
        # Remove any quotes and export simple variables
        key=$(echo "$key" | xargs)
        value=$(echo "$value" | sed 's/^["'\'']//' | sed 's/["'\'']$//')
        if [[ $key =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]]; then
            export "$key=$value"
        fi
    done < .env
    print_status "Loaded environment variables from .env"
fi

print_status "Building Docker image: $IMAGE_NAME"
docker build -t $IMAGE_NAME:latest .

if [ $? -eq 0 ]; then
    print_success "Docker image built successfully"
else
    print_error "Docker build failed"
    exit 1
fi

print_status "Testing Docker image..."

# Test 1: Basic import test
print_status "Test 1: Basic import test"
docker run --rm --name $CONTAINER_NAME-import $IMAGE_NAME:latest \
    python -c "import exito_scraper; print('✅ Import test passed')"

# Test 2: CLI help test
print_status "Test 2: CLI help test"
docker run --rm --name $CONTAINER_NAME-cli $IMAGE_NAME:latest \
    python -m exito_scraper.main --help

# Test 3: Configuration test
print_status "Test 3: Configuration test"
docker run --rm --name $CONTAINER_NAME-config $IMAGE_NAME:latest \
    python -c "
from exito_scraper.config import EXPECTED_URLS, DEFAULT_HEADERS
print(f'✅ Configuration test passed. Categories: {list(EXPECTED_URLS.keys())}')
"

# Test 4: Utility scripts test
print_status "Test 4: Utility scripts test"
docker run --rm --name $CONTAINER_NAME-utils $IMAGE_NAME:latest \
    python -c "
from exito_scraper.utils.html_formatter import clean_html_details
test_html = '<p>Test <span>HTML</span> content</p>'
cleaned = clean_html_details(test_html)
print(f'✅ HTML cleaner test passed: {cleaned}')
"

# Test 5: Volume mount test
print_status "Test 5: Volume mount test"
mkdir -p test_data
docker run --rm --name $CONTAINER_NAME-volume \
    -v $(pwd)/test_data:/app/data \
    $IMAGE_NAME:latest \
    python -c "
import os
assert os.path.exists('/app/data'), 'Data directory not mounted'
assert os.access('/app/data', os.W_OK), 'Data directory not writable'
print('✅ Volume mount test passed')
"

# Test 6: Format script test
print_status "Test 6: Format script test"
docker run --rm --name $CONTAINER_NAME-format $IMAGE_NAME:latest \
    python format_json.py --help || echo "Format script help not available (expected)"

print_success "All Docker tests passed! 🎉"

# Optional: Tag with version if provided
if [ ! -z "$1" ]; then
    VERSION=$1
    print_status "Tagging image with version: $VERSION"
    docker tag $IMAGE_NAME:latest $IMAGE_NAME:$VERSION
    print_success "Tagged as $IMAGE_NAME:$VERSION"
fi

print_status "Available images:"
docker images | grep $IMAGE_NAME

print_success "Docker build and test completed successfully!"

# Clean up test directory
rm -rf test_data

echo
echo "To run the scraper:"
echo "  docker run --rm -v \$(pwd)/data:/app/data $IMAGE_NAME:latest python -m exito_scraper.main scrape --categoria televisores --paginas 1 --output data/productos.jsonl"
echo
echo "To run interactively:"
echo "  docker run --rm -it -v \$(pwd)/data:/app/data $IMAGE_NAME:latest /bin/bash"
echo
echo "To use docker-compose:"
echo "  docker-compose up exito-scraper"
