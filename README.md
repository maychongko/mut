# FoundHer

Landing page for a 6-week entrepreneurship bootcamp for women in Germany.

**Live site:** https://maychongko.github.io/foundher/

## Edit workflow
The whole site is one file: `index.html` (design, content, logic — no build step).

After editing, push:
```bash
git add index.html && git commit -m "update" && git push
```
GitHub Pages redeploys automatically (~1 min).

## Deploy / redeploy
```bash
GITHUB_TOKEN=<token> ./deploy.sh
```
Creates the repo, pushes, enables GitHub Pages, waits for the build.

## Structure
- `index.html` — everything: hero, curriculum, mentors, pricing, application form, FAQ
- `deploy.sh` — one-command deployment
- Form submissions are stored in the visitor's browser (localStorage) — see "next steps" for hooking up a real form backend
