# Twilio A2P 10DLC resubmission: what to change

Campaign SID `CM584c06c54571dba63e7f072002e105a9` — rejected 2026-07-17, error 30909.

**Edit the existing campaign. Do not delete and recreate it.** The vetting fee is
charged once per campaign; recreating it charges you again. In Console go to
**Messaging → Regulatory Compliance → Campaigns**, open the failed campaign, and
click **Edit Campaign**.

Do not resubmit until grovano.com is live over HTTPS. Reviewers fetch the URLs.

---

## Why it was rejected

Error 30909 means the reviewer could not verify how end users consent. Four
specific defects in your submission, mapped to Twilio's reviewer checklist:

### 1. Your policy URLs pointed at a parked domain — the fatal one

You submitted `https://grovano.com` for **both** the privacy policy and the terms
and conditions. That is not a policy page, it is a domain root, and nothing was
served there. The reviewer clicked, found no policy, and stopped. This alone
triggers 30933, 30934, 30908, and 30919.

Twilio requires the privacy policy to state, in substance, that mobile
information is not shared with third parties or affiliates for marketing or
promotional purposes. A reviewer cannot confirm language on a page that does not
exist.

**Fix:** the new site serves real pages at distinct URLs. Update both fields:

| Field | Old | New |
|---|---|---|
| Privacy Policy URL | `https://grovano.com` | `https://grovano.com/messaging/privacy` |
| Terms and Conditions URL | `https://grovano.com` | `https://grovano.com/messaging/terms` |

### 2. Your message flow described a website opt-in that did not publicly exist

You wrote that users opt in "by submitting a form on our website and checking a
dedicated, unchecked-by-default SMS consent box." The prose was accurate about
what a compliant flow looks like, but there was no such form anywhere a reviewer
could reach. Twilio's guidance is explicit: the flow must be publicly verifiable,
or you must host screenshots of it.

**Fix:** `/messaging/signup` is now a real, public page with a real unchecked
checkbox, and the message flow below names that exact URL.

### 3. The message flow did not link to the policy pages

Twilio's pre-submission checklist requires the `message_flow` field itself to
contain a link to the privacy policy and a link to the terms. Yours contained
neither. Their own passing example inlines both URLs directly in the field text.

**Fix:** both URLs are inlined in the replacement text below.

### 4. Your sample messages never said "Grovano"

The checklist requires sample messages to identify the brand by name. All five of
yours used `[agent name]` and never named the company. Sample 5 also omitted HELP
and dropped the trailing period. A recipient reading sample 2 has no way to tell
who is texting them.

**Fix:** rewritten samples below, each leading with the brand name.

---

## Field replacements — copy and paste

### Campaign description

> Grovano Inc is a residential real estate investment company that buys homes
> directly from owners for cash and connects investors with off-market investment
> properties. This campaign sends SMS only to clients and leads who explicitly
> opted in by submitting the consent form at
> https://grovano.com/messaging/signup, completing an in-person paper consent
> form, verbally requesting text updates from our team, or texting our business
> number first. The objective is to communicate with sellers and buyers
> throughout a property transaction. After opting in, a seller sends and receives
> messages such as confirmation of their cash offer request, follow-up questions
> about the property, cash offer details, scheduling of walkthroughs, and offer
> and closing status updates. A buyer receives investment property and deal
> alerts matching their stated criteria, price updates, and showing and closing
> coordination. All conversations are two-way; recipients can reply with
> questions or to schedule, and our team responds directly. Message frequency
> varies by activity and stage. Message and data rates may apply. Reply STOP to
> unsubscribe and HELP for help. Terms and Conditions:
> https://grovano.com/messaging/terms. Privacy Policy:
> https://grovano.com/messaging/privacy. We do not share or sell mobile
> information or SMS opt-in data with third parties or affiliates for marketing
> or promotional purposes, and we do not purchase or import phone numbers from
> lead lists.

### Message flow / How do end-users opt in

This is the field that got you rejected. It must be 40 to 2049 characters; the
text below is within range.

> End users opt in to receive text messages from Grovano Inc through four paths,
> all of which are used for this campaign. (1) WEBSITE: the user visits
> https://grovano.com/messaging/signup, enters their name, email, mobile number
> and property details, and checks a dedicated SMS consent box that is unchecked
> by default. The box reads: "By checking this box, I agree to receive recurring
> text messages from Grovano Inc at the mobile number I provided, including
> confirmation of my cash offer request, cash offer details, follow-up questions
> about the property, walkthrough and showing scheduling, closing status updates,
> and investment property and deal alerts matching my criteria. Consent is not a
> condition of purchase or sale. Message frequency varies. Message and data rates
> may apply. Reply STOP to unsubscribe at any time, or HELP for help." (2) PAPER
> FORM: the user completes an in-person paper form containing that same written
> consent language. (3) VERBAL: the user verbally requests text updates from a
> Grovano Inc team member, and we log the date, time, and staff member who took
> the request. (4) KEYWORD: the user texts our business number first, or replies
> START, YES, SUBSCRIBE, OFFER or DEALS, and receives the auto-reply "Grovano
> Inc: You're now opted in to receive property and cash offer updates. Msg
> frequency varies. Msg & data rates may apply. Reply HELP for help, STOP to opt
> out." Message frequency varies. Message and data rates may apply. Terms and
> Conditions: https://grovano.com/messaging/terms. Privacy Policy:
> https://grovano.com/messaging/privacy, which states that no mobile information
> or SMS opt-in data is shared with third parties or affiliates for marketing or
> promotional purposes. We do not purchase, rent, or import phone numbers from
> any third party or lead list.

### Sample messages

Each now names the brand and carries opt-out plus help language.

**Sample 1**
> Grovano Inc: Hi {Name}, this is {agent} following up on the cash offer request
> for your property at 123 Main St. Is now a good time to talk? Reply STOP to opt
> out, HELP for help.

**Sample 2**
> Grovano Inc: New investment property in 78704, 3BR, $220K, ARV $340K. Want the
> details? Reply STOP to unsubscribe, HELP for help.

**Sample 3**
> Grovano Inc: Confirming your walkthrough at 456 Oak Dr tomorrow at 2pm. Reply
> YES to confirm. Reply STOP to opt out, HELP for help.

**Sample 4**
> Grovano Inc: Hi {Name}, {agent} here. We've prepared your cash offer for 123
> Main St. Want me to text or email the details? Reply STOP to opt out, HELP for
> help.

**Sample 5**
> Grovano Inc: Price drop on the 78704 deal you asked about, now $205K. Still
> interested? Reply STOP to unsubscribe, HELP for help.

### Opt-in message

Add the brand name here too.

> Grovano Inc: You're now opted in to receive property and cash offer updates.
> Msg frequency varies. Msg & data rates may apply. Reply HELP for help, STOP to
> opt out.

### Help message

Yours was thin at 47 characters. The field wants 20 to 320 and reviewers expect
actual support options.

> Grovano Inc: For help with your property or offer, email support@grovano.com or
> call (210) 347-9018. Msg frequency varies. Msg & data rates may apply. Reply
> STOP to unsubscribe.

### Leave these alone

- **Opt-out message** — already compliant.
- **Opt-out keywords** — full standard set present.
- **Help keywords** — HELP and INFO are fine.
- **Messages contain phone numbers: No** — still true of the samples.
- **Messages contain embedded links: No** — still true of the samples. Keep it
  that way; if you later start texting links, update this field first.
- **Use case: LOW_VOLUME** — appropriate.

### One judgment call: opt-in keywords

You listed START, YES, SUBSCRIBE, OFFER, DEALS. START, YES, and SUBSCRIBE are
standard. OFFER and DEALS are unusual as opt-in keywords and invite a reviewer
question about whether they are really promotional triggers. They are defensible
given your use case, and I left them in and documented them in the terms page. If
you get a second rejection that cites the keyword set, drop OFFER and DEALS.

---

## Pre-submit checklist

- [ ] All four URLs return 200 over HTTPS in a private window
- [ ] No bracketed placeholders remain on any page
- [ ] Privacy Policy URL field updated to `/messaging/privacy`
- [ ] Terms and Conditions URL field updated to `/messaging/terms`
- [ ] Campaign description replaced
- [ ] Message flow replaced
- [ ] All five sample messages replaced
- [ ] Opt-in message and help message updated
- [ ] `support@grovano.com` mailbox exists and is monitored
- [ ] Consent checkbox verified unchecked on page load

## Sources

- [30909: Message Flow or Call to Action incomplete/unverified](https://www.twilio.com/docs/api/errors/30909)
- [30908: Compliant Privacy Policy Required](https://www.twilio.com/docs/api/errors/30908)
- [30919: Website lacks sufficient business or messaging use case info](https://www.twilio.com/docs/api/errors/30919)
- [Why Was My A2P 10DLC Campaign Registration Rejected?](https://help.twilio.com/articles/15778026827291-A2P-10DLC-Campaign-Registration-Rejected)
- [Troubleshooting and rectifying A2P Campaigns](https://www.twilio.com/docs/messaging/compliance/a2p-10dlc/troubleshooting-a2p-brands/troubleshooting-and-rectifying-a2p-campaigns)
- [Managing a custom domain for your GitHub Pages site](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
