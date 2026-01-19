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
```bash
gh repo create <ORG_OR_USER>/meta3-canonical --public --source . --remote origin --push
```

If you want it private:
```bash
gh repo create <ORG_OR_USER>/meta3-canonical --private --source . --remote origin --push
```

## 3) Ongoing sync from the engine repo

From the engine repo root, re-export:
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

