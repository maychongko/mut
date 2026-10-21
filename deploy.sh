#!/bin/bash
# FoundHer — deploy to GitHub Pages
# Usage: GITHUB_TOKEN=xxx ./deploy.sh
# Creates repo (if needed), pushes, enables Pages, prints the live URL.
set -e

TOKEN="${GITHUB_TOKEN:?Paste your GitHub token first: GITHUB_TOKEN=xxx ./deploy.sh}"
API="https://api.github.com"
AUTH="Authorization: token $TOKEN"
cd "$(dirname "$0")"

# --- 1. Who are you? ---
USER=$(curl -s -H "$AUTH" $API/user | python3 -c "import sys,json; print(json.load(sys.stdin)['login'])")
REPO="mut"
echo "✓ GitHub user: $USER"

# --- 2. Create repo if it doesn't exist ---
if ! curl -sf -H "$AUTH" $API/repos/$USER/$REPO > /dev/null 2>&1; then
  echo "→ Creating repo $USER/$REPO (public)…"
  curl -sf -X POST -H "$AUTH" $API/user/repos \
    -d '{"name":"foundher","description":"FoundHer — 6-week entrepreneurship bootcamp for women in Germany","private":false,"homepage":""}' > /dev/null
  echo "✓ Repo created"
else
  echo "✓ Repo exists"
fi

# --- 3. Git init + commit + push ---
git init -q 2>/dev/null || true
git add -A   # .gitignore keeps .token out
git commit -qm "FoundHer landing page" 2>/dev/null || echo "  (nothing new to commit)"
git branch -M main
git remote remove origin 2>/dev/null || true
git remote add origin "https://$USER:$TOKEN@github.com/$USER/$REPO.git"
git push -qfu origin main
echo "✓ Pushed to GitHub"
# keep token out of the remote URL on disk
git remote set-url origin "https://github.com/$USER/$REPO.git"

# --- 4. Enable GitHub Pages ---
if ! curl -sf -H "$AUTH" $API/repos/$USER/$REPO/pages > /dev/null 2>&1; then
  echo "→ Enabling GitHub Pages…"
  curl -sf -X POST -H "$AUTH" $API/repos/$USER/$REPO/pages \
    -d '{"source":{"branch":"main","path":"/"}}' > /dev/null
  echo "✓ Pages enabled"
else
  echo "✓ Pages already on"
fi

# --- 5. Verify build status ---
echo "→ Waiting for Pages build (can take ~1 min)…"
for i in $(seq 1 12); do
  sleep 10
  STATUS=$(curl -s -H "$AUTH" $API/repos/$USER/$REPO/pages/builds/latest | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',''))" 2>/dev/null || echo "")
  echo "  build: $STATUS"
  [ "$STATUS" = "built" ] && break
done

URL="https://$USER.github.io/$REPO/"
echo ""
echo "🌍 LIVE: $URL"
