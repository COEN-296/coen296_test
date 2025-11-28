#!/bin/bash

# Sync UI files from /UI to /project/static

echo "📁 Syncing UI files..."

SOURCE_DIR="/Users/suraj/Desktop/ai_goverance/coen296-main/project/ui"
DEST_DIR="/Users/suraj/Desktop/ai_goverance/coen296-main/project/static"

# Copy HTML files
cp "$SOURCE_DIR/index.html" "$DEST_DIR/index.html"
cp "$SOURCE_DIR/login.html" "$DEST_DIR/login.html"

# Copy USER_GUIDE if it exists
if [ -f "$SOURCE_DIR/USER_GUIDE.md" ]; then
    cp "$SOURCE_DIR/USER_GUIDE.md" "$DEST_DIR/USER_GUIDE.md"
fi

echo "✅ UI files synced successfully!"
echo ""
echo "Updated files:"
echo "  - index.html"
echo "  - login.html"
echo "  - USER_GUIDE.md (if exists)"
echo ""
