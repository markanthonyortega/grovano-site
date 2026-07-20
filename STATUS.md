# Deployment status: LIVE, redeploy pending

Last checked: July 19, 2026

grovano.com is serving over HTTPS with a valid certificate.

**Pending:** the site was rewritten to split SMS consent into two separate
opt-ins after Twilio rejection 30913. Those changes are on disk but not yet
pushed. Run the publish command in `TWILIO-RESUBMIT.md` before resubmitting.

| URL | Status |
|---|---|
| https://grovano.com/ | live |
| https://grovano.com/messaging/privacy | live, verified in browser |
| https://grovano.com/messaging/terms | live |
| https://grovano.com/messaging/signup | live, consent box confirmed unchecked |

## What it took

**DNS was not where we thought.** grovano.com is authoritative on **Cloudflare**,
not Route 53. The Route 53 hosted zone is an orphan that nothing reads. I edited
it first, which had no effect. Public NS lookup returns `luke.ns.cloudflare.com`
and `jen.ns.cloudflare.com`.

The real records, changed in Cloudflare:

| Name | Type | Was | Now | Proxy |
|---|---|---|---|---|
| grovano.com | CNAME | dead Heroku app | markanthonyortega.github.io | DNS only |
| www | CNAME | did not exist | markanthonyortega.github.io | DNS only |

Both are grey-cloud on purpose. With Cloudflare's orange-cloud proxy on, GitHub
cannot complete its certificate challenge and Enforce HTTPS stays permanently
unavailable. Cloudflare flattens the apex CNAME, so grovano.com now resolves to
the four GitHub Pages addresses. MX, SPF, DKIM, DMARC, autodiscover, and the
SendGrid records were untouched. Email is unaffected.

The dead Heroku app behind the old CNAME is what served "Application error" to
Twilio's reviewer.

**The legacy Pages builder was broken.** Three attempts at
`pages-build-deployment` all ended in "Startup failure" with a generic GitHub
error and no job ever assigned to a runner, while GitHub's status page reported
everything operational and repo Actions permissions allowed all workflows.

Fix: switched Pages source from "Deploy from a branch" to **GitHub Actions** and
added GitHub's own **Static HTML** starter workflow at
`.github/workflows/static.yml`. It succeeded in 20 seconds on the first run.
That workflow is now the deployment path, and any push to `main` redeploys.

## Remaining items

1. **The signup form endpoint.** `messaging/signup/index.html` still posts to
   `https://formspree.io/f/REPLACE_WITH_YOUR_FORM_ID`. The page renders correctly
   and Twilio can review it, but real submissions will 404. Create a form at
   formspree.io and replace that ID. You are required to retain proof of consent,
   so this matters beyond the review.

2. **Enforce HTTPS.** Not yet ticked. GitHub disables the control while its
   periodic DNS re-check is running. HTTPS already works with a valid
   certificate, so this only adds an HTTP to HTTPS redirect. Tick it later at
   Settings, Pages.

3. **README.md.** Committed through GitHub's web editor, whose autoindent
   mangled the list indentation. Cosmetic, no effect on the site.

4. **The orphan Route 53 zone** `Z003053915C5WAWDA9OLE`. Nothing resolves
   through it, and it bills around $0.50/month. Safe to delete after exporting,
   once you have confirmed Cloudflare holds everything you need.

## Next

Work through `TWILIO-RESUBMIT.md`. Edit the existing campaign rather than
recreating it, or you pay the vetting fee twice.
