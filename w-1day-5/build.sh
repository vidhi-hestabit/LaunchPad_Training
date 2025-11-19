#!/bin/bash

TIMESTAMP=$(date '+%Y%m%d-%H%M%S')
BUILD_DIR="artifacts"
LOG_FILE="logs/validate.log"
TARBALL="$BUILD_DIR/build-$TIMESTAMP.tgz"
CHECKSUM_FILE="$BUILD_DIR/build-$TIMESTAMP.sha256"

mkdir -p $BUILD_DIR

# Package logs, config, and src
tar -czf $TARBALL src config.json logs

# Generate checksum
sha256sum $TARBALL > $CHECKSUM_FILE
echo "✅ Build artifact created: $TARBALL"
echo "🔑 Checksum saved to: $CHECKSUM_FILE"

