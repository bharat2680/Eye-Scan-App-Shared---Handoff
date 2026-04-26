# Google Play Monetization Plan

Last updated: 2026-03-18 17:33 AEDT

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

This plan now assumes EyeScan is being positioned as a clinic workflow product,
not a casual consumer wellness app.

## Recommended model

### Primary offer: clinic subscription

Create one clinic subscription for workflow access rather than charging per
scan or per individual user.

Suggested subscription:

- product ID: `eyescan_plus`
- name: `EyeScan Plus`

Suggested base plans:

- `monthly`
- `yearly`

Suggested paid benefits:

- clinic-level access beyond the trial
- PDF export and multi-result PDF export
- future clinic workflow tools
- future multi-user clinic features

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
- it matches how clinics actually evaluate software: by testing a workflow
  across a small team and then subscribing at the organisation level

## Recommended trial model

Use a backend-managed hybrid trial:

- `14` days
- `100` scans
- up to `2` authorised users
- one trial per clinic or organisation
- optionally tied to one registered device or installation later

This should be enforced per clinic or workspace, not per username.

## Trial vs paid structure

Recommended launch split:

- trial:
  - full workflow evaluation for one clinic
  - limited by time, scan count, and user count
  - enough access to test exports and reporting in realistic usage
- paid:
  - ongoing clinic access after trial expiry
  - PDF export and batch or multi-result PDF export
  - future multi-user and clinic workflow features

## What not to launch first

Avoid these at first launch:

- per-scan consumable credits
- charging just to reveal a health-related screen result
- one free trial per email address
- a one-time lifetime export unlock as the default path
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

- `Clinic workflow access`
- `PDF report export`
- `Batch PDF reports`
- `Evaluation trial and clinic tools`

Then add base plans:

- `monthly`
- `yearly`

Suggested first pricing:

- monthly: keep simple and accessible
- yearly: 15% to 25% cheaper than 12 monthly payments

The clinic trial itself should be controlled by your backend, not by Play's
subscription configuration alone.

## In-app entitlement design

Gate these features behind Play Billing entitlements:

- ongoing clinic access after trial expiry
- PDF export
- multi-result PDF export

Keep these free:

- taking a scan
- viewing the immediate screening summary
- viewing the current quality feedback

## Backend trial enforcement design

The app alone should not decide whether a clinic still has a free trial.

The backend should track at least:

- clinic or organisation ID
- clinic name
- email domain
- trial start date
- trial end date
- scan limit
- scans used
- max authorised users
- optional registered device or installation ID
- paid status

Recommended rule before each scan:

1. if clinic is paid, allow
2. else if trial is active and both time and scan limits remain, allow
3. else require subscription or activation

This is the main anti-abuse control. It prevents the same clinic from creating
fresh free trials under new usernames.

## Android implementation checklist

The Android app will need:

- Play Billing integration
- the `com.android.vending.BILLING` permission
- product IDs that exactly match Play Console
- local entitlement checks plus restored purchase handling
- purchase acknowledgement
- a paywall screen that clearly explains what is free and what is paid
- a subscription management link or settings entry

## Current implementation status on the Mac app

As of the latest Mac-side billing pass:

- Flutter Play Billing integration has been added using `in_app_purchase`
- Android now declares `com.android.vending.BILLING`
- the app includes a clinic access screen and purchase restore flow
- the app includes a settings entry and about-screen entry for clinic access
- the default product IDs compiled into the app are:
  - subscription: `eyescan_plus`
- this product ID currently maps to the clinic-access strategy so the app can
  match the live Play Console setup without creating a second subscription
- PDF export and multi-result PDF export can now be access-gated, but the
  gating switch currently defaults to off via:
  `EYESCAN_PREMIUM_GATING_ENABLED=false`
- current purchase entitlement handling is still local-device based and
  suitable for first-party testing only
- a true clinic-level trial and multi-user entitlement model still requires
  backend implementation
- latest billing-enabled Android bundle built on the Mac:
  - version: `1.1.7+17`
  - local output:
    `/Users/bharatsharma/FlutterProjects/eye_scan_app/build/app/outputs/bundle/release/app-release.aab`
  - backend target:
    `https://eyescan-backend-beta-66791987039.australia-southeast2.run.app`
  - current Play state:
    production release `17 (1.1.7)` uploaded and sent for review

## Immediate next operational steps

1. create the Play Console subscription product using the ID in this file
2. upload the billing-enabled clinic-access bundle
3. publish that build to internal testing
4. return to `Monetize with Play > Products > Subscriptions`
5. verify the subscription page now unlocks with the billing-enabled build
6. keep trial enforcement backend-controlled instead of trusting local device
   state alone
7. only turn premium gating on in release builds after the billing flow is
   confirmed stable with testers

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
3. Run the free trial at the clinic level in your backend.
4. Gate ongoing PDF/report workflow access behind that subscription.
5. Test with Google Play license testers and at least one real clinic workflow.
6. Add other product types only after the clinic trial and conversion path are
   stable.

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
