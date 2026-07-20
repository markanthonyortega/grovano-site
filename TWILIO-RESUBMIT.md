# Twilio A2P 10DLC resubmission, round 2

Campaign SID `CM584c06c54571dba63e7f072002e105a9`
Rejected 2026-07-17 with **30909**, fixed. Rejected again with **30913**.

**Edit the existing campaign. Do not delete and recreate it.** The vetting fee is
charged once per campaign. In Console: **Messaging → Regulatory Compliance →
Campaigns**, open the campaign, **Edit Campaign**.

Do not resubmit until the updated site is deployed. Reviewers fetch the URLs.

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

This is the field 30913 is judging. Limit is 40 to 2049 characters.

> End users opt in in writing at https://grovano.com/messaging/signup. That page
> presents TWO SEPARATE consent checkboxes, both unchecked by default. A user may
> check either, both, or neither, and neither is a condition of purchase or sale.
> (1) TRANSACTIONAL CONSENT, its own checkbox, reads: "By checking this box, I
> agree to receive text messages from Grovano Inc at the mobile number I provided
> about my own transaction: confirmation of my cash offer request, cash offer
> details, follow-up questions about my property, walkthrough and showing
> scheduling, and closing status updates. Consent is not a condition of purchase
> or sale. Message frequency varies. Message and data rates may apply. Reply STOP
> to unsubscribe at any time, or HELP for help." (2) MARKETING CONSENT is a
> separate checkbox and reads: "Separately, by checking this box, I agree to
> receive marketing text messages from Grovano Inc about investment properties
> and deals matching my criteria, including new listings and price changes. This
> is a separate consent from the box above and is not required. Message frequency
> varies. Message and data rates may apply. Reply STOP to unsubscribe, or HELP
> for help." Marketing consent is collected only in writing. We never accept
> verbal consent for marketing. A user may alternatively opt in by texting our
> business number first or replying START, YES or SUBSCRIBE, and receives:
> "Grovano Inc: You're now opted in to receive property and cash offer updates.
> Msg frequency varies. Msg & data rates may apply. Reply HELP for help, STOP to
> opt out." Message frequency varies. Message and data rates may apply. Terms and
> Conditions: https://grovano.com/messaging/terms. Privacy Policy:
> https://grovano.com/messaging/privacy, which states that no mobile information
> or SMS opt-in data is shared with third parties or affiliates for marketing or
> promotional purposes. We do not purchase, rent, or import phone numbers from
> any third party or lead list.

### Campaign description

> Grovano Inc is a residential real estate investment company that buys homes
> directly from owners for cash and connects investors with off-market investment
> properties. This campaign sends SMS only to people who gave express written
> consent at https://grovano.com/messaging/signup or by texting our business
> number first. The signup page collects TWO SEPARATE consents with two separate
> unchecked checkboxes. The first covers informational and transactional messages
> to a seller or buyer about their own transaction: cash offer request
> confirmation, cash offer details, follow-up questions about the property,
> walkthrough and showing scheduling, and closing status updates. The second,
> separately, covers marketing messages about investment properties and deals
> matching a buyer's stated criteria, including new listings and price changes.
> Neither consent is a condition of purchase or sale, and consenting to one does
> not consent the user to the other. All conversations are two-way; recipients
> can reply with questions or to schedule, and our team responds directly.
> Message frequency varies by activity and stage. Message and data rates may
> apply. Reply STOP to unsubscribe and HELP for help. Terms and Conditions:
> https://grovano.com/messaging/terms. Privacy Policy:
> https://grovano.com/messaging/privacy. We do not share or sell mobile
> information or SMS opt-in data with third parties or affiliates for marketing
> or promotional purposes, and we do not purchase or import phone numbers from
> lead lists.

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
> call (210) 347-9018. Msg frequency varies. Msg & data rates may apply. Reply
> STOP to unsubscribe.

### Leave these alone

- Privacy Policy URL: `https://grovano.com/messaging/privacy`
- Terms and Conditions URL: `https://grovano.com/messaging/terms`
- Opt-out message and opt-out keywords, already compliant
- Help keywords HELP and INFO
- Messages contain phone numbers: No
- Messages contain embedded links: No
- Use case: LOW_VOLUME

---

## If this gets rejected a third time

The remaining structural option is to **split into two campaigns**: one
transactional, one marketing, each with its own consent record and its own
registration. That is the most bulletproof reading of "consent applies only to
the specific campaign and sender," and it removes any argument about mixing. It
costs a second vetting fee, which is why it is not the first move.

## Pre-submit checklist

- [ ] Updated site deployed and `/messaging/signup` shows two separate boxes
- [ ] Both checkboxes verified unchecked on page load in a private window
- [ ] Message flow field replaced
- [ ] Campaign description replaced
- [ ] Samples 2 and 5 updated
- [ ] OFFER and DEALS removed from opt-in keywords
- [ ] Help message updated

## Sources

- [30913: Marketing and informational consent must be separate](https://www.twilio.com/docs/api/errors/30913)
- [30909: Message Flow or Call to Action incomplete](https://www.twilio.com/docs/api/errors/30909)
- [30919: Website lacks sufficient business or messaging use case info](https://www.twilio.com/docs/api/errors/30919)
