# Deploying grovano.com on GitHub Pages + Route 53

Replace `markanthonyortega` throughout with your actual GitHub username.

---

## Step 0. Fill in the placeholders first

Search the repo for `[` and replace every highlighted placeholder. If any of these
ship to production, a Twilio reviewer sees a broken page and rejects you again.

| Placeholder | Appears in | What to put |
|---|---|---|
| `[MAILING ADDRESS — street, city, state, ZIP]` | index, privacy, terms | Your real business address. A PO box is acceptable; "Austin, TX" alone is not. |
| `(210) 347-9018` | index, privacy, terms | A number a reviewer could actually call. |
| `[YOUR TWILIO NUMBER]` | signup | The 10DLC number attached to this campaign. |
| `REPLACE_WITH_YOUR_FORM_ID` | signup | Your form endpoint. See Step 1b. |
| `support@grovano.com` | all pages | Keep it, but make sure the mailbox actually exists and is monitored. |

Quick check that nothing was missed:

```bash
cd grovano-site
grep -rn "MAILING ADDRESS\|BUSINESS PHONE\|YOUR TWILIO NUMBER\|REPLACE_WITH" .
```

That command should print nothing before you go live.

---

## Step 1. Create the repo and push

The repo must be **public** — GitHub Pages on a private repo requires a paid plan.

```bash
cd "/Users/markortega/Library/CloudStorage/OneDrive-GrovanoInc/Software/grovano-site"

git init -b main
git add -A
git commit -m "Grovano Inc site: A2P 10DLC privacy policy, SMS terms, and opt-in form"

# Using the GitHub CLI (brew install gh, then gh auth login):
gh repo create grovano-site --public --source=. --remote=origin --push

# Or, if you created the repo in the GitHub web UI instead:
# git remote add origin https://github.com/markanthonyortega/grovano-site.git
# git push -u origin main
```

### Step 1b. Wire up the form endpoint

GitHub Pages is static, so the form needs a third-party endpoint. Free options:

- **Formspree** — sign up, create a form, paste the given URL into the `action`
  attribute in `messaging/signup/index.html`.
- **Web3Forms** — no account needed; swap the `action` for their endpoint and add
  a hidden `access_key` input.

For the Twilio review, what matters is that the page renders publicly with the
unchecked consent box and the disclosures. But make it actually deliver, because
you are legally required to retain proof of consent.

---

## Step 2. Turn on GitHub Pages

In the repo: **Settings → Pages**

- Source: **Deploy from a branch**
- Branch: **main**, folder: **/ (root)**
- Custom domain: **grovano.com** → Save

The `CNAME` file in this repo already sets the custom domain, so GitHub should
pick it up on first deploy. Leave **Enforce HTTPS** unchecked for now; you will
enable it in Step 4 once the certificate is issued.

Confirm the build succeeded under the **Actions** tab before moving on.

---

## Step 3. Point Route 53 at GitHub

Open **Route 53 → Hosted zones → grovano.com**.

### 3a. Apex A record

- Record name: leave blank (this is the apex, `grovano.com`)
- Type: **A**
- TTL: 300
- Value — all four IPs, one per line:

```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

### 3b. Apex AAAA record

- Record name: blank
- Type: **AAAA**
- TTL: 300
- Value — all four, one per line:

```
2606:50c0:8000::153
2606:50c0:8001::153
2606:50c0:8002::153
2606:50c0:8003::153
```

### 3c. www CNAME

- Record name: **www**
- Type: **CNAME**
- TTL: 300
- Value: `markanthonyortega.github.io`

> Delete any pre-existing A, AAAA, ALIAS, or CNAME records at the apex or on
> `www` left over from the parked page. Stale records pointing at a parking
> service will keep grovano.com resolving to the old placeholder, and the
> reviewer will see that instead of your site.

### Same thing via the AWS CLI

Get your zone ID, then apply a change batch:

```bash
aws route53 list-hosted-zones-by-name --dns-name grovano.com \
  --query 'HostedZones[0].Id' --output text
# -> /hostedzone/ZXXXXXXXXXXXXX ; use just the ZXXXXXXXXXXXXX part below
```

```bash
cat > /tmp/grovano-dns.json <<'JSON'
{
  "Comment": "Point grovano.com at GitHub Pages",
  "Changes": [
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "grovano.com.",
        "Type": "A",
        "TTL": 300,
        "ResourceRecords": [
          {"Value": "185.199.108.153"},
          {"Value": "185.199.109.153"},
          {"Value": "185.199.110.153"},
          {"Value": "185.199.111.153"}
        ]
      }
    },
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "grovano.com.",
        "Type": "AAAA",
        "TTL": 300,
        "ResourceRecords": [
          {"Value": "2606:50c0:8000::153"},
          {"Value": "2606:50c0:8001::153"},
          {"Value": "2606:50c0:8002::153"},
          {"Value": "2606:50c0:8003::153"}
        ]
      }
    },
    {
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "www.grovano.com.",
        "Type": "CNAME",
        "TTL": 300,
        "ResourceRecords": [
          {"Value": "markanthonyortega.github.io"}
        ]
      }
    }
  ]
}
JSON

aws route53 change-resource-record-sets \
  --hosted-zone-id ZXXXXXXXXXXXXX \
  --change-batch file:///tmp/grovano-dns.json
```

### 3d. Optional but recommended: verify the domain

**GitHub → Settings → Pages → Add a domain.** GitHub gives you a TXT record named
`_github-pages-challenge-markanthonyortega.grovano.com`. Add it in Route 53.
This prevents anyone else from claiming grovano.com on GitHub Pages later.

---

## Step 4. Wait, then enable HTTPS

DNS propagation plus certificate issuance usually takes 15 minutes to an hour,
occasionally up to 24 hours. Check progress:

```bash
dig +short grovano.com A
dig +short www.grovano.com
```

Once the A records return the GitHub IPs, go back to **Settings → Pages** and
tick **Enforce HTTPS**. Do not submit to Twilio until this is on — the campaign
URLs must be HTTPS and must not throw certificate warnings.

---

## Step 5. Verify before you resubmit

Every one of these must return `200`:

```bash
for u in https://grovano.com/ \
         https://grovano.com/messaging/privacy \
         https://grovano.com/messaging/terms \
         https://grovano.com/messaging/signup ; do
  printf "%s -> %s\n" "$u" "$(curl -s -o /dev/null -w '%{http_code}' -L "$u")"
done
```

Then open each page in a private browsing window — no login, no VPN — and confirm:

- [ ] Pages load over HTTPS with a valid certificate, no warnings
- [ ] Business name, mailing address, and phone are real and visible
- [ ] The privacy policy contains the no-sharing paragraph verbatim
- [ ] The consent checkbox on `/messaging/signup` is **unchecked** on page load
- [ ] Consent text names Grovano Inc, states frequency, rates, STOP, and HELP
- [ ] Terms and Privacy links work from the signup page
- [ ] No `[BRACKETED]` placeholders anywhere

Now go to `TWILIO-RESUBMIT.md` for the campaign field changes.
