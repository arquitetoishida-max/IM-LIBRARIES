# Receiver deployment record

Owner report, November 16, 2026: the receiver was deployed in the owner's Google Apps Script account. Public service URL (not a credential):

https://script.google.com/macros/s/AKfycbwnbrntKuW9u5GyUTCrCdlkvOlTeRlPuOvVEF2M9WnhZcCytFmbdwmVCqEfFNPThiYQww/exec

A read-only GET on November 16 followed the ContentService redirect to `script.googleusercontent.com` and returned HTTP 200 with `{"service":"ishida-community-reports","schema_version":1}`. This verifies service metadata only, not GitHub-token scope, receipt persistence, live POST/retry, Android behavior or the exact deployed source revision.

The owner reports that the token stays only in Script properties. No token is recorded here, in fixtures or in the APK. No live POST was made during this verification; no synthetic issue/production receipt was created. Offline service mocks and schema checks are separate evidence. #9/#55 remain open for live and Android acceptance.

The missing-word convention in [MISSING_WORDS.md](MISSING_WORDS.md) needs no schema or receiver-code change; documentation/test additions alone require no owner redeployment. Setup instructions remain in [receiver/SETUP.md](receiver/SETUP.md).
