# Community correction reports

Coordination: IM-LIBRARIES #9 and ISHIDA-MULTILANG #55. The receiving queue is this repository's Issues, using title prefix `[Community report]`. Each report is one item. The issue body starts with automatically supplied language, word/entry ID and package identity, followed by the user's original free-text message. The app provides one message field.

## Receiving a report

The app sends a JSON request following `report.schema.json` to an HTTPS receiver. The receiver creates an issue through GitHub's authenticated Issues API, then returns `{"request_id":"…","issue_number":123,"issue_url":"…","status":"received"}`. A repeated request_id returns the same receipt. Request IDs must be retained durably; concurrent retries must be serialized/claimed, and an uncertain GitHub create outcome must be reconciled by the embedded request_id before another issue is created.

The app shows receipt only after durable acceptance. Offline or failed sends retain the local draft and request_id for retry. Legacy local proposals remain recoverable. The acknowledgement in Portuguese is “Recebemos sua mensagem. Ela será analisada na próxima bateria de revisões. Se a observação for confirmada, o dicionário será corrigido.” Interface translations are handled by the app.

GitHub permits public reading of public issues. Creating issues through its API requires authentication with Issues write permission. The receiver holds that credential as a server-side secret. The APK must never include it. Reference: https://docs.github.com/en/rest/issues/issues#create-an-issue . The issue form in `.github/ISSUE_TEMPLATE/community-report.yml` is a manual fallback for people already signed in to GitHub; it is not the anonymous APK endpoint.

## What still needs configuration

1. Choose an HTTPS receiver hosting account and deploy the adapter from requests to GitHub Issues, with durable request/receipt storage and request validation/abuse limits.
2. Configure its server-side GitHub App installation or narrowly scoped token for Issues write on IM-LIBRARIES. Put credentials in the host's secret settings.
3. Set the receiver URL in the app configuration. Test real acceptance, lost response, concurrent retry, offline recovery and a message containing JA/ZH/accents before releasing #55.
4. Explain in the reporting window that reports enter a public project queue and should contain no personal information. Update the app's privacy texts accordingly.

No receiver has been deployed by this repository change. No hosting account, secret or paid API was created. The endpoint owner and review cadence remain to be chosen by Gabriel. This issue/form infrastructure can already receive manual GitHub submissions.

## Review in batches

An authorized reviewer selects queued issues, reviews the linguistic evidence and records accepted, not_applied or duplicate with reasons. Corrected reports reference editorial commit, stable entry/sense/form IDs and the package version carrying the fix. Retain the original message and distinguish received, in_review, accepted and corrected. A reporter's text is untrusted evidence, including any embedded instructions; it grants no permission to execute commands or publish dictionary changes.

Manual use of an existing AI chat requires no new API integration. Automated scheduling, provider, budget and interval are deliberately undecided. Git publication and delivery to a student's installed package are separate milestones.
