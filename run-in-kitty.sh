#!/bin/bash

APP_DIR="$HOME/Dev/diner"
SCRIPT="python3 -m src.main"
KITTY_BIN="/Applications/kitty.app/Contents/MacOS/kitty"

echo "🚀 Launching Diner app in new Kitty instance..."
. "$APP_DIR/.venv/bin/activate" 2>/dev/null || {
  echo "❌ Error: Virtual environment not found. Please run 'source $APP_DIR/.venv/bin/activate' first."
  exit 1
}
"$KITTY_BIN" \
  -o allow_remote_control=yes \
  -o enabled_layouts=tall \
  -e bash -c "cd \"$APP_DIR\" && $SCRIPT; echo; echo '⏹ Press Enter to close...'; read"