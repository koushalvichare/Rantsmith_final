#!/bin/bash
# Vercel build script for RantSmith frontend
echo "🔧 Starting RantSmith build process..."

# Make sure we have the right permissions
chmod +x node_modules/.bin/vite 2>/dev/null || true

# Try different build approaches
if command -v npx >/dev/null 2>&1; then
  echo "📦 Using npx to build..."
  npx vite build --mode production
elif [ -x "node_modules/.bin/vite" ]; then
  echo "🔧 Using direct vite binary..."
  node_modules/.bin/vite build --mode production
else
  echo "🔄 Using node directly..."
  node node_modules/vite/bin/vite.js build --mode production
fi

echo "✅ Build completed successfully!"
