# Publishing to GitHub

This folder is a ready-to-push standalone repo export of the canonical libraries + agent prompts + canonical graphs.

## 1) Initialize git
```bash
cd _export/meta3-canonical
git init
git add -A
git commit -m "chore: initial canonical seed"
```

## 2) Create the GitHub repo (via `gh`)

Pick your org/user and repo name, then:
This repo is published as:
`j-94/meta3`

## 3) Ongoing sync from the engine repo

From the engine repo root, re-export into your local checkout of `j-94/meta3`:
```bash
rsync -a --exclude='.DS_Store' canonical/ _export/meta3-canonical/
```

Then in the canonical repo:
```bash
cd _export/meta3-canonical
git add -A
git commit -m "sync: refresh canonical content"
git push
```
