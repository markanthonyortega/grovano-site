# Deployment status

Last checked: August 1, 2026

grovano.com is live over HTTPS with a valid certificate.

## Where this site is actually hosted

**ortega-host, not GitHub Pages.** Cloudflare fronts a tunnel to the server,
Caddy serves the files out of `/srv/stack/sites/grovano`, and the deploy is:

```bash
ssh ortega
sudo /srv/stack/tools/deploy.sh grovano
```

Earlier versions of this file described a GitHub Pages setup with a Cloudflare
CNAME to `markanthonyortega.github.io`. That was true in July and is not true
now. `.github/workflows/static.yml` is left in the repo but is not the path
anything reaches the public through — Caddy's response headers on the live site
are the proof.

**This means a merge to `main` does not publish anything.** It has to be
deployed. That is how the 30896 form fix sat merged and un-live.

| URL | Status |
|---|---|
| https://grovano.com/ | live, 200 |
| https://grovano.com/messaging/signup | live, 200, both boxes unchecked |
| https://grovano.com/messaging/terms | live, 200 |
| https://grovano.com/messaging/privacy | live, 200 |
| https://grovano.com/messaging/opt-in-evidence | live, 200 |

## Remaining items

1. **Enforce HTTPS on GitHub Pages** — moot. Pages is no longer the origin.
   Cloudflare and Caddy handle the redirect.

2. **README.md.** Committed through GitHub's web editor, whose autoindent
   mangled the list indentation. Cosmetic, no effect on the site.

3. **The orphan Route 53 zone** `Z003053915C5WAWDA9OLE`. Nothing resolves
   through it, and it bills around $0.50/month. Safe to delete after exporting,
   once you have confirmed Cloudflare holds everything you need.

## History worth keeping

**DNS was not where we thought.** grovano.com is authoritative on **Cloudflare**,
not Route 53. The Route 53 hosted zone is an orphan that nothing reads. Public
NS lookup returns `luke.ns.cloudflare.com` and `jen.ns.cloudflare.com`. The dead
Heroku app behind the old apex CNAME is what served "Application error" to
Twilio's first reviewer.

**The legacy Pages builder was broken.** Three `pages-build-deployment` runs
ended in "Startup failure" with no job ever assigned to a runner. Switching the
Pages source to GitHub Actions with the Static HTML starter workflow fixed it at
the time. Since superseded by the move to ortega-host.

## Next

Work through `TWILIO-RESUBMIT.md`. Register a **new** campaign — the rejected
one cannot be edited, which is why three reviews all read the original text.
