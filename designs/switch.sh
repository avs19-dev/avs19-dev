#!/bin/sh
# ─────────────────────────────────────────────────────────────
#  Design switcher — apna profile README kisi bhi stored design
#  par set karein.
#
#  Usage:   ./designs/switch.sh <design-name>
#  Designs: dashboard | professional | hybrid
#
#  Example: ./designs/switch.sh dashboard
# ─────────────────────────────────────────────────────────────
set -e
name="${1:-hybrid}"
if [ ! -f "designs/$name/README.md" ]; then
  echo "❌ Design '$name' nahi mila. Available:"
  for d in designs/*/; do echo "   - $(basename "$d")"; done
  exit 1
fi
cp "designs/$name/README.md" README.md
echo "✅ README ab '$name' design par hai. Publish karne ke liye commit + push karein."
