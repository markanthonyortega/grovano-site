# Twilio A2P 10DLC resubmission, round 2

Campaign SID `CM584c06c54571dba63e7f072002e105a9`
Rejected 2026-07-17 with **30909**, fixed. Then **30913**. Live status: **30896**.

## Edit this campaign. Do NOT register a new one.

An earlier version of this file said the campaign could not be edited and had to
be re-registered. **That was wrong.** Acting on it would have cost a second $15
vetting fee and required deleting the campaign first.

Verified in the Console on August 1, 2026:

- The campaign page carries an **Edit & resubmit** button in the red error
  banner. It works, and opens an editable form headed **"Revise errors and
  resubmit your A2P Campaign registration"**.
- The stored campaign already holds **most** of the corrected copy. The campaign
  description and all five sample messages match this document. There is no
  PAPER FORM or VERBAL consent language anywhere in the stored record.
- So earlier edits DID save. The claim that all three reviews read the original
  text is not supported.

What the earlier note got right is that stale content reached reviewers — just
not all of it, and not for the stated reason. Three fields never got updated:

- **Opt-in keywords still read `START,YES,SUBSCRIBE,OFFER,DEALS`.** OFFER and
  DEALS are still there.
- **Help message is still the original** unbranded `Reply STOP to unsubscribe.
  Msg&Data Rates May Apply.`
- **Opt-in message** is missing the `Grovano Inc:` prefix.

**Action: open the campaign, click Edit & resubmit, fix the fields below,
resubmit.** Nothing is deleted, the number never moves, and there is no second
vetting fee.

### The registration is blocked if you try to create a new campaign anyway

The messaging service holding (830) 355-0900,
`MG7ee02390f22ff32b0d6a6dac6b8e036f`, is listed under **"Connected with an
existing A2P campaign (not available to select)"** in the create-campaign modal.
A second campaign cannot attach to it while this one exists. Creating a new
campaign would mean deleting this one first, or moving the number to another
service. Another reason to edit rather than recreate.

Do not submit until the updated site is deployed. Reviewers fetch the URLs.

## Field length limits, verified in the form

| Field | Limit | Our text |
|---|---|---|
| Campaign description | **1024** | 1011 |
| Message flow | 2048 (assumed — **confirm before pasting**) | 1824 |

The description limit is the tight one and it is easy to miss: an earlier
1506-character draft could not have fit. If a verification pass reports that a
too-long value "matches exactly", distrust it and re-read the field.

## The most recent rejection was 30896, not 30913

Error 30896 is *"Compliance reviewers were unable to submit your website's
opt-in form"*, with the note **"Form not foun[d]"**. The form posted to the
literal placeholder `formspree.io/f/REPLACE_WITH_YOUR_FORM_ID`, so every
reviewer who filled it in and pressed Submit landed on a 404.

This is a separate failure from the consent-structure problems below, and it
outranks them: a reviewer who cannot complete the form never evaluates the
consent language at all. The consent-splitting work for 30913 is still correct
and still needed — it was simply never reachable.

**Fixed:** `forms/` is a self-hosted, dependency-free endpoint on ortega-host.
The form posts same-origin to `/messaging/signup/submit`, so a reviewer never
leaves grovano.com, and each submission writes a consent record holding the
disclosure text as shown, the two consents as separate booleans, the IP, the
user agent, and a UTC timestamp. See `forms/` for how to read the records.

---

## Why it was rejected this time

Error 30913: *"Marketing and informational consent must be separate."*

The first rejection was about a flow reviewers could not verify. That is fixed:
grovano.com is live and the opt-in page is public. This rejection is a different
and more specific problem, and Twilio's docs name the exact cause.

### 1. One checkbox covered two kinds of message

Twilio's listed cause: *"A single checkbox, form, or agreement covers both
marketing messages and informational or transactional messages."*

Your consent box bundled these together:

| Message type | Twilio classifies it as |
|---|---|
| Cash offer request confirmation | transactional |
| Cash offer details | transactional |
| Walkthrough and showing scheduling | transactional |
| Closing status updates | transactional |
| **Investment property and deal alerts** | **marketing** |
| **Price drop notifications** | **marketing** |

Deal alerts and price drops promote inventory to a buyer who is not yet in a
transaction on that property. That is marketing, and marketing consent has to be
its own affirmative act.

**Fix:** `/messaging/signup` now has **two separate checkboxes**, both unchecked
by default, visually separated, each with its own full disclosure block. One is
labeled "Transaction updates (informational and transactional)" and the other
"Property and deal alerts (marketing)." A user can check either, both, or
neither.

### 2. You claimed verbal consent, which cannot support marketing

Twilio's listed cause: *"The campaign uses a Marketing use case, but the opt-in
process relies on verbal consent instead of written consent."*

Your message flow listed verbal opt-in as one of four paths. Marketing consent
must be written. A logged phone call does not qualify no matter how well you
document it.

**Fix:** the flow below claims only two paths, both written: the website form and
a text-in keyword. The paper form and verbal paths are removed from the
application and from the site.

### 3. Opt-in keywords did not match the flow

You listed START, YES, SUBSCRIBE, OFFER, DEALS. OFFER and DEALS are not standard
opt-in keywords and read as promotional triggers, which invites exactly the
marketing-consent scrutiny that just failed. They also were not all explained in
the message flow, and a mismatch between declared keywords and the described flow
is its own review risk.

**Fix:** drop OFFER and DEALS. Keep **START, YES, SUBSCRIBE**.

---

## Field replacements, copy and paste

### Opt-in keywords

Remove `OFFER` and `DEALS`. Leave:

> START, YES, SUBSCRIBE

### Message flow / How do end-users opt in

This is the field the reviewer judges. It leads with the exact PUBLIC signup
URL, states there is no login or paywall, links a hosted page that reproduces
the checkbox area, and contains no verbal opt-in path. 1824 of 2048 characters.

The opt-in confirmation quoted inside it is **verbatim identical** to the
Opt-in message field below. It previously quoted a shortened version, so the
two fields contradicted each other.

> End users opt in in writing at https://grovano.com/messaging/signup. This form is fully public: no login, account, paywall, or client portal is required to view or use it. A public hosted page reproducing the opt-in and its checkbox area is at https://grovano.com/messaging/opt-in-evidence. The form has TWO SEPARATE consent checkboxes, both unchecked by default; a user may check either, both, or neither, and neither is a condition of purchase or sale. (1) TRANSACTIONAL checkbox reads: "I agree to receive text messages from Grovano Inc about my own transaction: cash offer request confirmation, cash offer details, follow-up questions about my property, walkthrough and showing scheduling, and closing status updates. Consent is not a condition of purchase or sale. Msg frequency varies. Msg and data rates may apply. Reply STOP to opt out, HELP for help." (2) MARKETING checkbox, separate, reads: "Separately, I agree to receive marketing texts from Grovano Inc about investment properties and deals matching my criteria, including new listings and price changes. This is a separate consent from the box above and is not required. Msg frequency varies. Msg and data rates may apply. Reply STOP to opt out, HELP for help." All consent is collected in writing. A user may alternatively text our business number first or reply START, YES, or SUBSCRIBE, and receives: "Grovano Inc: You're now opted in to receive property and cash offer updates. Msg frequency varies. Msg & data rates may apply. Reply HELP for help, STOP to opt out." Terms: https://grovano.com/messaging/terms. Privacy: https://grovano.com/messaging/privacy, which states no mobile information or SMS opt-in data is shared with third parties or affiliates for marketing. We do not purchase, rent, or import phone numbers from any third party or lead list.

### Campaign description

**Hard limit 1024 characters. This is 1011.** Paste as one line.

The long version this replaced was 1506 characters and could never have been
saved. What was cut is duplicated verbatim in the message flow field above — the
enumerated transactional message types, the two-way-conversation sentence, and
the trailing periods after the two URLs, which some parsers swallow into the
link. Every compliance clause survives: the public signup URL, TWO SEPARATE
consents unchecked by default, not a condition of purchase or sale, one consent
not implying the other, frequency and rate disclosures, STOP and HELP, both
policy URLs, no sharing with third parties or affiliates, and no lead lists.

> Grovano Inc is a residential real estate investment company that buys homes from owners for cash and connects investors with off-market properties. We text only people who gave express written consent at https://grovano.com/messaging/signup or who text our business number first. That page collects TWO SEPARATE consents using two separate checkboxes, both unchecked by default: one for transactional messages about the user's own transaction, and one, separately, for marketing messages about investment properties matching a buyer's criteria. Neither is a condition of purchase or sale, and consenting to one does not consent the user to the other. Message frequency varies. Message and data rates may apply. Reply STOP to unsubscribe, HELP for help. Terms: https://grovano.com/messaging/terms Privacy: https://grovano.com/messaging/privacy We do not share or sell mobile information or SMS opt-in data with third parties or affiliates for marketing, and we do not buy or import phone numbers from lead lists.

### Sample messages

Samples 1, 3 and 4 are transactional. Samples 2 and 5 are marketing and go only
to recipients who checked the second box. Each names the brand and carries
opt-out and help language.

**Sample 1** (transactional)
> Grovano Inc: Hi {Name}, this is {agent} following up on the cash offer request
> for your property at 123 Main St. Is now a good time to talk? Reply STOP to opt
> out, HELP for help.

**Sample 2** (marketing)
> Grovano Inc: New investment property in 78704, 3BR, $220K, ARV $340K. You asked
> for deal alerts. Want the details? Reply STOP to unsubscribe, HELP for help.

**Sample 3** (transactional)
> Grovano Inc: Confirming your walkthrough at 456 Oak Dr tomorrow at 2pm. Reply
> YES to confirm. Reply STOP to opt out, HELP for help.

**Sample 4** (transactional)
> Grovano Inc: Hi {Name}, {agent} here. We've prepared your cash offer for 123
> Main St. Want me to text or email the details? Reply STOP to opt out, HELP for
> help.

**Sample 5** (marketing)
> Grovano Inc: Price drop on the 78704 deal you asked about, now $205K. Still
> interested? Reply STOP to unsubscribe, HELP for help.

### Opt-in message

> Grovano Inc: You're now opted in to receive property and cash offer updates.
> Msg frequency varies. Msg & data rates may apply. Reply HELP for help, STOP to
> opt out.

### Help message

> Grovano Inc: For help with your property or offer, email support@grovano.com or
> call (830) 355-0900. Msg frequency varies. Msg & data rates may apply. Reply
> STOP to unsubscribe.

### Messages contain phone numbers: YES

This file used to say **No**. That was wrong, and the checkbox in the Console is
already correctly ticked — do not untick it.

The Help message above reads "…or call (830) 355-0900." That is a phone number,
inside a message this campaign sends. Declaring No while shipping it is an
internal contradiction, and internal contradictions between declared fields are
exactly what has been sinking these submissions.

The alternative would be stripping the number out of the Help message. Don't:
HELP is where a confused recipient should find a human, and a reply that offers
only an email address is a worse reply.

### Leave these alone

- Privacy Policy URL: `https://grovano.com/messaging/privacy`
- Terms and Conditions URL: `https://grovano.com/messaging/terms`
- Opt-out message and opt-out keywords, already compliant. The terms page at
  grovano.com quotes the opt-out message verbatim, so site and campaign agree.
- Help keywords HELP and INFO
- Messages contain embedded links: No
- Use case: LOW_VOLUME

---

## If this gets rejected again

First, read the error code before assuming it is about consent structure. The
last three rejections were three different problems — 30909, then 30913, then
30896 — and treating the newest one as a repeat of the last is how this file
ended up telling you to re-register a campaign that was editable all along.

If it is genuinely 30913 again, the remaining structural option is to **split
into two campaigns**: one transactional, one marketing, each with its own
consent record and its own registration. That is the most bulletproof reading of
"consent applies only to the specific campaign and sender," and it removes any
argument about mixing. It costs a second $15 vetting fee, which is why it is not
the first move.

## Pre-submit checklist

### Site, verified against the live URLs

- [x] `/messaging/signup` public, two separate checkboxes, neither carrying a
      `checked` attribute
- [x] `/`, `/messaging/terms`, `/messaging/privacy`, `/messaging/opt-in-evidence`
      all return 200
- [x] Terms section 6 quotes the same HELP message this campaign declares. It
      previously quoted a different, unbranded one.
- [x] Every `tel:` link dials (830) 355-0900. Three pages displayed the new
      number while the link still dialed the old one.
- [x] "We do not accept verbal consent for marketing messages" removed from
      terms and privacy. Both already say all consent is written, which is the
      same claim without raising verbal consent at all.
- [x] **The opt-in form actually accepts a submission.** Verified from outside on
      August 1, 2026: `POST https://grovano.com/messaging/signup/submit` returns
      303 to `/messaging/signup/thank-you/` and writes a consent record. This is
      the 30896 fix.

### Console: edit the EXISTING campaign

Open `CM584c06c54571dba63e7f072002e105a9`, click **Edit & resubmit**. Verified
already correct in the stored record, leave alone: campaign description content,
all five sample messages, both policy URLs, help keywords, embedded-links = No.

Four fields still need changing:

- [ ] **Opt-in keywords** — currently `START,YES,SUBSCRIBE,OFFER,DEALS`. Set to
      `START,YES,SUBSCRIBE`. This is the single most likely repeat-rejection
      cause still live in the record.
- [ ] **Help message** — currently the unbranded `Reply STOP to unsubscribe.
      Msg&Data Rates May Apply.` Replace with the version above.
- [ ] **Opt-in message** — add the missing `Grovano Inc:` prefix and unhyphenate
      "cash offer".
- [ ] **Message flow** — the confirmation quoted inside it is the shortened
      variant. Make it character-identical to the Opt-in message field.
- [ ] Description re-pasted only if it is over 1024 or differs from the version
      above
- [ ] **Do NOT untick "messages contain phone numbers"** — see above
- [ ] Nothing deleted, no new campaign, no second vetting fee

## Sources

- [30896: Reviewers could not submit the website's opt-in form](https://www.twilio.com/docs/api/errors/30896) — the live rejection
- [30913: Marketing and informational consent must be separate](https://www.twilio.com/docs/api/errors/30913)
- [30909: Message Flow or Call to Action incomplete](https://www.twilio.com/docs/api/errors/30909)
- [30919: Website lacks sufficient business or messaging use case info](https://www.twilio.com/docs/api/errors/30919)

Campaign fees, read off the Console's own table on August 1, 2026: **$15 per
vetting request**, all campaign types, non-refundable. Low Volume Mixed carries
**$1.50/month**. Editing and resubmitting this campaign does not incur a second
$15; registering a replacement would.
