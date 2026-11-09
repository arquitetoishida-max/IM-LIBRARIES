# Optional Google Apps Script receiver

This adapter uses an owner-controlled Apps Script web app, a private receipt spreadsheet and GitHub Issues. It has no AI API dependency and creates no paid account or deployment by itself. Google quotas and availability apply; check https://developers.google.com/apps-script/guides/services/quotas before deployment. Service and deployment references are https://developers.google.com/apps-script/guides/web and https://developers.google.com/apps-script/guides/content .

## Owner setup

1. Open https://script.google.com and choose **New project**. Paste `Code.gs` from this directory into the editor's `Code.gs` file.
2. Create a fine-grained GitHub token limited to **IM-LIBRARIES**, with repository permission **Issues → Read and write**. In Apps Script, open **Project Settings → Script properties → Add script property**. Set `GITHUB_TOKEN` to that token. Never paste the token in an issue, the app code or chat. The receiver posts to the fixed `arquitetoishida-max/IM-LIBRARIES` repository.
3. Select `setupReceiver` in the editor and click **Run**. Approve access for the owner account. This creates a private Google spreadsheet for receipts and adds `QUEUE_SPREADSHEET_ID` in Script properties. Keep the spreadsheet private.
4. Choose **Deploy → New deployment → Web app**. Set **Execute as → Me** and **Who has access → Anyone**. Deploy and copy the URL ending in `/exec`. Account/administrator restrictions may hide the anonymous option; deployment is blocked until the owner can enable that access or chooses another receiver host.
5. Give the `/exec` URL to Claude for MULTILANG #55. Test with a synthetic report first. Confirm an issue appears in IM-LIBRARIES, retry the same request_id and verify that it returns the same issue number. Then test Android, a lost response, Unicode text, offline recovery and update with old local proposals before release.

## App response handling

POST the `report.schema.json` request as JSON. Follow the ContentService redirect to `script.googleusercontent.com`. Apps Script ContentService responses use a JSON envelope; HTTP 200 alone is not proof of acceptance.

- `status: received` includes `request_id`, `issue_number` and `issue_url`. Only this state triggers the “Recebemos sua mensagem…” acknowledgement.
- `status: retry` means retain the same local draft, request_id, payload and original creation time. Retry with backoff or let the user retry later.
- `status: pending` means the server may already have created the issue. Preserve the request and check again later using exactly the same payload. Do not generate a fresh request_id. An operator may need reconciliation.
- `status: rejected` requires correcting an invalid request; `request_id_conflict` means that an existing ID was reused with a different payload. Preserve the original queued record while diagnosing.

The technical message limit is 10,000 Unicode code points; all UI remains one field. Metadata is attached automatically. Private profile/account identifiers are not accepted by this contract. The receiver serializes sends, writes a durable posting record before GitHub creation, and returns an existing receipt for identical retries.

## Uncertain outcomes and review

Run `reconcilePendingReports` manually from the Apps Script editor after a lost network response. It searches GitHub for the request ID and accepts exactly one issue with the full expected body. A zero/multiple match remains pending, so the receiver never blindly duplicates an uncertain submission. GitHub search indexing can lag; retry reconciliation later. If no issue was created, the owner can verify that in GitHub and change that receipt row from `uncertain`/`posting` to `failed` to permit resending. Never change a confirmed `received` row to `failed`.

The spreadsheet is an intake receipt journal. Actual editorial review happens on the IM-LIBRARIES issues in the batches Gabriel will define. This adapter creates no timer, automated AI review or dictionary edits. For high-volume anonymous traffic, abuse controls/host capacity need a separate deployment decision; this small-project adapter is not an unlimited public ticket service.

Local tests use Node service mocks for success, retries, failures, conflict, message validation, receipt reconciliation and text rendering. They do not prove a live Google/GitHub deployment. Run `node community/receiver/test_receiver.cjs` from repository root.
