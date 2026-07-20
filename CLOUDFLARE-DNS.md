# DNS for grovano.com is in Cloudflare, not Route 53

## What I got wrong

I edited the Route 53 hosted zone for grovano.com. Those edits are correct in
content but have no effect, because grovano.com does not use Route 53 for DNS.

Public nameserver lookup for grovano.com returns:

```
luke.ns.cloudflare.com
jen.ns.cloudflare.com
```

Not the Route 53 nameservers (`ns-332.awsdns-41.com` and friends) listed inside
the AWS hosted zone. The registrar delegates this domain to Cloudflare, so
Cloudflare is authoritative and the Route 53 zone is an orphan. I should have
checked the NS delegation before touching anything. Nothing broke, because
nothing reads that zone.

Current live resolution:

```
grovano.com  A  104.21.13.188
grovano.com  A  172.67.201.170
```

Both are Cloudflare edge IPs. Cloudflare is proxying to a Heroku origin that is
returning "Application error" — that is the broken page a Twilio reviewer saw.

## What is already correct

The GitHub side is done and needs no further work:

- `markanthonyortega/grovano-site` is public, with all files and the `messaging/`
  directory structure intact
- Pages is set to deploy from `main` / `(root)`
- Custom domain is set to `grovano.com`
- Status reads "DNS Check in Progress" and will stay there until DNS points at
  GitHub

## What to change, in Cloudflare

Log in at https://dash.cloudflare.com, open the **grovano.com** zone, then go to
**DNS → Records**.

### 1. Apex A record

Edit the existing `A` record for `grovano.com` (or delete the Heroku/proxied
ones and create these). You need four A records on the root name, one per IP:

```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

Cloudflare creates these as four separate rows, unlike Route 53 which takes them
as one multi-value record.

### 2. Apex AAAA records

Four more rows on the root name:

```
2606:50c0:8000::153
2606:50c0:8001::153
2606:50c0:8002::153
2606:50c0:8003::153
```

### 3. www

```
Type:   CNAME
Name:   www
Target: markanthonyortega.github.io
```

### 4. The part that actually matters

**Set Proxy status to "DNS only" (grey cloud) on every record above.**

This is the most common way a GitHub Pages plus Cloudflare setup fails. If the
orange cloud is on, Cloudflare terminates TLS at its edge and GitHub can never
complete the Let's Encrypt challenge for grovano.com. GitHub's "Enforce HTTPS"
box stays permanently greyed out, and you can end up in a redirect loop. Grey
cloud on all eight A/AAAA rows and on the www CNAME.

### 5. Do not touch

Leave every `MX`, `TXT` (SPF, Google, Facebook verification), `_dmarc`, and
`_domainkey` record exactly as it is. Those carry your email. Changing the A and
AAAA records does not affect mail delivery.

## After the change

DNS propagation is fast on Cloudflare, usually under five minutes. Then GitHub
needs to run its DNS check and issue the certificate, typically 15 minutes to an
hour.

Verify:

```bash
dig +short grovano.com A
# expect the four 185.199.x.153 addresses, not 104.21.x or 172.67.x

for u in https://grovano.com/ \
         https://grovano.com/messaging/privacy \
         https://grovano.com/messaging/terms \
         https://grovano.com/messaging/signup ; do
  printf "%s -> %s\n" "$u" "$(curl -s -o /dev/null -w '%{http_code}' -L "$u")"
done
```

All four must return 200. Then tick **Enforce HTTPS** in the repo under
Settings → Pages, confirm the pages load clean in a private window, and only
then work through `TWILIO-RESUBMIT.md`.

## Loose end: the orphan Route 53 zone

The AWS hosted zone `Z003053915C5WAWDA9OLE` for grovano.com is not used by
anything. It still contains stale records, including an `A` record that pointed
at Shopify and MX records for privateemail.com that may or may not match what
Cloudflare actually serves. It bills at roughly $0.50/month.

My three edits to it were:

| Record | Was | Now |
|---|---|---|
| `grovano.com` A | `23.227.38.65` | four GitHub Pages IPs |
| `grovano.com` AAAA | did not exist | four GitHub Pages IPv6 |
| `www` CNAME | `shops.myshopify.com` | `markanthonyortega.github.io` |

None of it resolves. Reverting is optional. Deleting the zone entirely is
reasonable once you have confirmed Cloudflare holds everything you need, but
export it first so you do not lose a record you meant to keep.
