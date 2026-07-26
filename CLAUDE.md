# grovano-site — guide for Claude Code

Live at **https://grovano.com**

## Deployment (ortega-host — self-hosted)

This app **no longer deploys to AWS**. It runs as a Docker container on Mark's
own server (`ortega-host`), reached through a Cloudflare Tunnel. There are no
open inbound ports; the server dials out.

The old GitHub Actions deploy workflows are **disabled** — do not re-enable
them, and do not add new ones without asking. They were turned off deliberately
(Actions minutes cost, and hung builds on metered runners).

### How to deploy

```bash
ssh ortega                                    # LAN;  ssh ortega-ts from anywhere
sudo /srv/stack/tools/deploy.sh grovano
```

That single command pulls the latest commit, builds an image tagged with that
commit, swaps only this app's container, health-checks the real site through
Caddy, and **rolls back automatically if the check fails**.

Useful flags:

```bash
sudo /srv/stack/tools/deploy.sh grovano --dry-run          # show, don't do
sudo /srv/stack/tools/deploy.sh grovano --ref <sha|branch> # specific commit
sudo /srv/stack/tools/deploy.sh grovano --no-pull          # rebuild as-is
```

Rolling back is just deploying an older commit:

```bash
sudo /srv/stack/tools/deploy.sh grovano --ref <older-sha>
```

Full guide: `/srv/stack/DEPLOYING.md` on the server.

### 🚦 Rule for Claude Code sessions — read this before deploying

**Never deploy to production unless Mark explicitly grants permission in the
current session.**

- Permission is **per-session and per-deploy**. Approval given in an earlier
  conversation, or for an earlier deploy, does **not** carry over.
- "Deploy this" from Mark in this session **is** permission for that deploy.
- Absent that, stop and ask. Do not infer permission from the fact that the
  work is finished, tested, or obviously ready.
- **Staging needs no permission** — deploy there freely to test.

```bash
sudo /srv/stack/tools/deploy.sh grovano-staging     # no permission needed
sudo /srv/stack/tools/deploy.sh grovano             # ASK FIRST, every time
```

If you are unsure whether you have permission, you do not have it.

### Checking your work

```bash
cd /srv/stack && docker compose ps           # what is running
sudo /srv/stack/tools/healthcheck.sh         # containers, sites, disk, backups
docker logs --tail 50 -f <CONTAINER>         # this app's logs
tail -50 /tmp/deploy-grovano.log          # why a build failed
```

### Backups

Nightly at 02:30 — every database plus the stack config, verified, kept 7 daily
/ 4 weekly / 12 monthly, with an encrypted copy pushed offsite to S3. Take one
on demand before anything risky:

```bash
sudo /srv/stack/tools/backup.sh
```


---

## Branch hygiene

Dead branches accumulate fast when several sessions work in parallel. The rule:

**Work on a branch → open a PR → merge → delete the branch.** Same session,
every time. Do not leave a merged branch behind for someone else to clean up.

```bash
git checkout -b feat/short-description        # never commit directly to main
# ... work, commit ...
git push -u origin feat/short-description
gh pr create --fill
gh pr merge --squash --delete-branch          # merges AND removes the branch
```

`--delete-branch` is the part people skip. Use it.

If you finish work but the PR is not ready to merge, say so plainly rather
than leaving an orphan branch with no explanation.

**Before starting new work, check what is already there:**

```bash
gh pr list                                    # open PRs
git branch -r --merged origin/main            # merged, deletable
```

**Naming:** `feat/`, `fix/`, `chore/`, `ci/`, `docs/` followed by a few words
in kebab-case. Avoid auto-generated names like `claude/reverent-swirles-41d09c`
— they say nothing about the work six weeks later.

**Never force-push to `main`**, and never delete a branch that is not merged
without asking first — an unmerged branch is somebody's unfinished work.
