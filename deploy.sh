#!/usr/bin/env bash
# Deploy grovano.com to GitHub Pages.
# Run:  bash "/Users/markortega/Library/CloudStorage/OneDrive-GrovanoInc/Software/grovano-site/deploy.sh"

set -euo pipefail

REPO_DIR="/Users/markortega/Library/CloudStorage/OneDrive-GrovanoInc/Software/grovano-site"
GH_USER="markanthonyortega"
REPO_NAME="grovano-site"

cd "$REPO_DIR"

echo "==> Checking for leftover placeholders"
if grep -rIn --exclude=deploy.sh --exclude=DEPLOY.md --exclude=TWILIO-RESUBMIT.md \
     "MAILING ADDRESS\|BUSINESS PHONE\|YOUR TWILIO NUMBER" . ; then
  echo "!! Placeholders above are still in the site files. Fix them, then re-run."
  exit 1
fi

if grep -rq "REPLACE_WITH_YOUR_FORM_ID" messaging/signup/index.html; then
  echo "!! WARNING: the signup form still posts to a placeholder Formspree URL."
  echo "   The page renders fine and Twilio can review it, but submissions will 404."
  echo "   Continuing anyway in 5 seconds. Ctrl-C to stop and fix it first."
  sleep 5
fi

echo "==> Preparing git repository"
if [ ! -d .git ]; then
  git init -b main
fi
git add -A
git commit -m "Grovano Inc site: A2P 10DLC privacy policy, SMS terms, and opt-in form" || \
  echo "   (nothing new to commit)"

echo "==> Checking GitHub CLI"
if ! command -v gh >/dev/null 2>&1; then
  cat <<'EOF'

The GitHub CLI (gh) is not installed. Two options:

  A) Install it, then re-run this script:
       brew install gh
       gh auth login

  B) Do it manually:
       1. Create a PUBLIC repo at https://github.com/new named "grovano-site".
          Do not add a README, .gitignore, or license.
       2. Then run:
            cd "/Users/markortega/Library/CloudStorage/OneDrive-GrovanoInc/Software/grovano-site"
            git remote add origin https://github.com/markanthonyortega/grovano-site.git
            git push -u origin main
       3. In the repo: Settings > Pages > Source: "Deploy from a branch",
          Branch: main, folder: / (root). Save.

EOF
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "!! gh is installed but not logged in. Run:  gh auth login"
  exit 1
fi

echo "==> Creating and pushing the repository"
if gh repo view "$GH_USER/$REPO_NAME" >/dev/null 2>&1; then
  echo "   Repo already exists, pushing to it."
  git remote get-url origin >/dev/null 2>&1 || \
    git remote add origin "https://github.com/$GH_USER/$REPO_NAME.git"
  git push -u origin main
else
  gh repo create "$REPO_NAME" --public --source=. --remote=origin --push
fi

echo "==> Enabling GitHub Pages"
gh api "repos/$GH_USER/$REPO_NAME/pages" \
  -X POST \
  -f "source[branch]=main" \
  -f "source[path]=/" >/dev/null 2>&1 && echo "   Pages enabled." || \
  echo "   Pages may already be enabled, or needs enabling by hand in Settings > Pages."

echo "==> Setting the custom domain"
gh api "repos/$GH_USER/$REPO_NAME/pages" \
  -X PUT \
  -f "cname=grovano.com" \
  -F "https_enforced=true" >/dev/null 2>&1 && echo "   Custom domain set to grovano.com." || \
  echo "   Set it by hand: Settings > Pages > Custom domain > grovano.com"

cat <<EOF

==> Done pushing.

DNS is already configured in Route 53:
  grovano.com      A     185.199.108-111.153
  grovano.com      AAAA  2606:50c0:8000-8003::153
  www.grovano.com  CNAME $GH_USER.github.io

GitHub still needs to issue the TLS certificate. That usually takes 15 minutes
to an hour. Check with:

  for u in https://grovano.com/ \\
           https://grovano.com/messaging/privacy \\
           https://grovano.com/messaging/terms \\
           https://grovano.com/messaging/signup ; do
    printf "%s -> %s\\n" "\$u" "\$(curl -s -o /dev/null -w '%{http_code}' -L "\$u")"
  done

All four must return 200 over HTTPS before you resubmit to Twilio.
Then follow TWILIO-RESUBMIT.md.

EOF
