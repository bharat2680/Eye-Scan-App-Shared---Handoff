# Google Play Monetization Plan

Last updated: 2026-03-17 21:33 AEDT

## Goal

Monetize the Android EyeScan app on Google Play without making unsafe medical
claims or adding a payment model that feels predatory for a health-related app.

## Current product facts this plan uses

From the current shared app status:

- the app already shows screening summaries and quality scores
- saved history already stores screening metadata
- individual PDF export already includes screening results
- multi-result PDF export already includes screening results
- the current pipeline is still `evaluation_only`

These existing features are the cleanest premium surfaces to sell first.

## Recommended model

### Primary offer: subscription

Create one subscription for premium workflow features rather than charging per
scan.

Suggested subscription:

- product ID: `eyescan_plus`
- name: `EyeScan Plus`

Suggested base plans:

- `monthly`
- `yearly`

Suggested paid benefits:

- unlimited saved history
- PDF export
- multi-result PDF export
- future premium report templates or clinic workflow tools

### Optional secondary offer: one-time unlock

If you want a non-recurring option, add one non-consumable one-time product:

- product ID: `pdf_export_lifetime`
- title: `PDF Export Lifetime`

This should unlock:

- individual PDF export
- multi-result PDF export

## Why this is the best first monetization path

This is the safest fit for the current EyeScan product because:

- the app is still evaluation-only, so charging directly for a diagnosis-like
  result would create trust and policy risk
- history and PDF export are already implemented, so they can be paywalled
  quickly
- subscriptions on Google Play are charged a 15% service fee for
  auto-renewing subscriptions, and many developers are also eligible for 15%
  on the first USD 1M of other revenue
- this keeps the scan experience accessible while monetizing reporting and
  record-keeping value

## Free vs paid structure

Recommended launch split:

- free:
  - run scans
  - view current result
  - save only the most recent limited history
- paid:
  - unlimited history
  - individual PDF export
  - batch or multi-result PDF export
  - future premium workflow features

## What not to launch first

Avoid these at first launch:

- per-scan consumable credits
- charging just to reveal a health-related screen result
- multiple subscriptions or complex tiering

Reason:

- higher support burden
- more billing edge cases
- weaker user trust for a health-related product
- harder entitlement logic for very little added upside at the current stage

## Play Console steps from your current screen

You are already on `Monetize with Play`.

### 1. Finish payments setup first

Go to:

- `Settings > Payments profile`

Then:

- add your bank payment method
- complete verification if Google asks for it

Notes:

- only the account owner can manage merchant payment accounts
- payment method verification can take up to 5 days

### 2. Create the subscription

From the screen in your screenshot:

- click `Get started` under `Subscriptions`

Then create:

- product ID: `eyescan_plus`
- name: `EyeScan Plus`

Suggested benefit text for Play Console:

- `Unlimited saved history`
- `PDF report export`
- `Batch PDF reports`
- `Premium workflow tools`

Then add base plans:

- `monthly`
- `yearly`

Suggested first pricing:

- monthly: keep simple and accessible
- yearly: 15% to 25% cheaper than 12 monthly payments

You can add a free trial later, but it is better to launch without one until
purchase flow and entitlement handling are stable.

### 3. Create the optional one-time unlock

From `Monetize with Play > Products > One-time products`, create:

- product ID: `pdf_export_lifetime`
- title: `PDF Export Lifetime`

Use this only if you want a non-subscription option for users who mainly want
reports.

## In-app entitlement design

Gate these features behind Play Billing entitlements:

- unlimited history
- single PDF export
- multi-result PDF export

Keep these free:

- taking a scan
- viewing the immediate screening summary
- viewing the current quality feedback

## Android implementation checklist

The Android app will need:

- Play Billing integration
- the `com.android.vending.BILLING` permission
- product IDs that exactly match Play Console
- local entitlement checks plus restored purchase handling
- purchase acknowledgement
- a paywall screen that clearly explains what is free and what is paid
- a subscription management link or settings entry

## Policy guardrails for EyeScan

Because EyeScan is health-related, do all of the following before launch:

- complete the Health apps declaration in Play Console
- keep a public privacy policy in-app and on the store listing
- include a store listing disclaimer that the app is not a medical device and
  does not diagnose, treat, cure, or prevent any medical condition
- remind users to consult a healthcare professional for medical advice
- do not imply regulatory approval unless you actually have it

Recommended listing-safe positioning:

- `EyeScan provides evaluation-only eye screening support and is not a medical device.`

## Billing and compliance notes

- if users pay for digital features inside the Play-distributed app, Google
  Play Billing must be used for those transactions
- subscription names and offer text must be transparent
- the app must clearly explain how users manage or cancel a subscription
- product IDs and base plan IDs cannot be changed or reused after activation,
  so name them carefully before you click through

## Recommended launch order

1. Set up payments profile and merchant payout details.
2. Launch one subscription only: `eyescan_plus`.
3. Gate unlimited history and PDF exports behind that subscription.
4. Test with Google Play license testers.
5. Publish the monetization update.
6. Add `pdf_export_lifetime` only if recurring conversion is weak.

## Assumption

This plan assumes the Android app will expose the same core user-facing
features already documented for the current iPhone build, especially history and
PDF export.

## Official references

- Google Play payments requirements:
  https://support.google.com/googleplay/android-developer/answer/9858738
- Create subscriptions:
  https://support.google.com/googleplay/android-developer/answer/140504
- Understand subscriptions and base plans:
  https://support.google.com/googleplay/android-developer/answer/12154973
- Create one-time products:
  https://support.google.com/googleplay/android-developer/answer/1153481
- Payment profile and merchant setup:
  https://support.google.com/googleplay/android-developer/answer/13628312
- Test Play Billing:
  https://developer.android.com/google/play/billing/test
- Health content and services policy:
  https://support.google.com/googleplay/android-developer/answer/16679511
- Service fees:
  https://support.google.com/googleplay/android-developer/answer/112622
