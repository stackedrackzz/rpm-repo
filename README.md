# rpm-repo

A GPG-signed yum/dnf repository built from `.spec` files in this repo and
published as static files on GitHub Pages by a GitHub Actions workflow.

Site once deployed: https://stackedrackzz.github.io/rpm-repo/

## Layout

```
specs/                 .spec files to build (one package per file)
SOURCES/                source files referenced by the specs (tarballs, scripts, patches, ...)
packages/               built + signed .rpm files and repodata/ (committed by the workflow, don't hand-edit)
index.html              Pages landing page
stackedrackzz.repo      .repo file end users install
.github/workflows/publish.yml   build -> sign -> createrepo -> publish pipeline
```

## One-time setup

### 1. Push this to GitHub

```
git init
git add .
git commit -m "Initial rpm-repo scaffold"
git branch -M main
git remote add origin git@github.com:stackedrackzz/rpm-repo.git
git push -u origin main
```

### 2. Enable GitHub Pages via Actions

Repo Settings -> Pages -> Build and deployment -> Source: **GitHub Actions**.
(No `gh-pages` branch needed — `actions/deploy-pages` handles deployment directly.)

### 3. Generate a GPG signing key

```
gpg --batch --gen-key <<EOF
%no-protection
Key-Type: RSA
Key-Length: 4096
Name-Real: stackedrackzz rpm-repo
Name-Email: noreply@example.com
Expire-Date: 2y
EOF
```

Use a real passphrase-protected key instead if you prefer (drop `%no-protection`
and set `GPG_PASSPHRASE` below to match).

Export the private key as ASCII-armored text:

```
gpg --list-secret-keys --with-colons | awk -F: '/^sec/ {print $5}'   # note the key id
gpg --armor --export-secret-keys <KEY_ID> > private.asc
```

### 4. Add repo secrets

Repo Settings -> Secrets and variables -> Actions -> New repository secret:

- `GPG_PRIVATE_KEY_ASCII` — full contents of `private.asc`
- `GPG_PASSPHRASE` — the key's passphrase (any non-empty value if you used `%no-protection`; the workflow always passes `--passphrase-file`, so this must be set even for a passphrase-less key — use a placeholder value in that case)

Then delete `private.asc` locally — it's not needed again once the secret is set,
and the workflow re-derives the key id from the imported key each run.

### 5. Trigger a run

Push to `main` (e.g. edit `specs/hello-repo.spec` or add a new spec) or run the
workflow manually from the Actions tab (**workflow_dispatch**).

## Adding a new package

1. Add `specs/<name>.spec`.
2. Add any source files it needs under `SOURCES/`.
3. Commit and push to `main`.

The workflow builds every `.spec` under `specs/`, signs the resulting RPMs,
copies new ones into `packages/` (existing files are never overwritten — bump
`Version`/`Release` for updates), regenerates and signs `repodata/`, commits
the new packages back to `main`, and republishes Pages.

## Notes

- Packages accumulate in `packages/` via git, so old versions stay available —
  binary `.rpm` files do bloat repo/history size over time; for a high-volume
  registry consider Git LFS or pruning old releases.
- `repo_gpgcheck=1` in `stackedrackzz.repo` verifies `repodata/repomd.xml`'s
  detached signature; `gpgcheck=1` verifies each package's embedded signature.
- The example `specs/hello-repo.spec` just proves the pipeline end-to-end —
  delete it once you have real packages.
