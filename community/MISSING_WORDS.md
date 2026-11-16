# Missing-word intake — schema v1 convention

Coordination: IM-LIBRARIES #9 and MULTILANG #55/#70. The existing JSON schema and receiver accept this convention without changing fields or runtime code. These are intake markers, never production dictionary IDs.

- `language`: actual studied-language code (`ja`, `zh`, `en`, `pt-BR`, etc.).
- `entry_id`: `new:<language>:<normalized word>`.
- `english_id`: literal `-`, meaning no verified concept link. Never guess an ID.
- `package_id` / `package_version`: actual installed package used for lookup. Resolve missing package context before sending; do not invent a future package/version.
- `word`: recommended existing optional field, preserving readable original spelling/case.
- `message`: `Palavra ausente no dicionário (importação por captura). Dica lida na captura: <translation hint>`. If no hint exists, say so. The hint is unverified evidence, not accepted translation.
- `english_sense_id` / `form_id`: null or omitted until verified. Existing course/message-language/time fields work normally.

Normalize only the marker: Unicode NFC, trim and collapse whitespace to a single space; use the studied language's lowercase convention for cased writing. Preserve accents, meaningful punctuation, word boundaries and kana/kanji/hanzi. Do not strip particles, guess lemmas or transliterate to force a match. `PÔR` may produce `new:pt-BR:pôr` while `word` retains `PÔR`.

Existing adapter limits remain: `entry_id` at most 256 JavaScript UTF-16 code units including prefix/language, no CR/LF/NUL; message at most 10,000 Unicode code points. The schema does not express every adapter limit. Never silently truncate identities. Overlong items stay local for correction; a hash-marker convention would require coordination in #9. No extra user form fields are needed.

All metadata stays single-line without CR/LF/NUL. The optional `word` field allows at most 512 JavaScript UTF-16 code units; preserve spelling/case, not OCR line breaks. The 256-unit marker limit may be reached first.

Generate one UUID per queued submission. Preserve the entire payload, original creation time, package/app versions and request ID through offline storage, response loss, app updates and retries. Retry when connectivity returns, with backoff. Editing a sent/uncertain payload under the same request ID causes a conflict; retain the original record and create a separate submission only for an explicit user edit.

Only JSON `status: received` with matching request ID and positive integer `issue_number` counts as sent. HTTP 200 or health GET is insufficient. `pending`/`retry` stay queued; diagnose `rejected`. Identical retries must return the same receipt. The current adapter validates syntax/limits; it does not prove absence, language/package consistency or correctness of the OCR hint. Check these during editorial triage. Identical spellings may have different senses; preserve originals and mark duplicates only after context review.

`new:*` and `-` must never enter released packages as stable IDs. Search entries, forms, master and central allocations before requesting new concepts. Preserve existing IDs, notes, groups and per-form progress. The OCR flow sends no image through this contract; the word/message is sent only when the user chooses to suggest it. Otherwise OCR stays local.

Fixtures in `community/fixtures/missing-word-*.json` are synthetic offline compatibility samples, not vocabulary assertions or live submissions. The Node receiver mocks cover Unicode metadata, same-payload retries, version-change conflicts and the existing length limit. Real POST/retry/Android acceptance remains pending. Publication rules: [REVIEW_BATCHES.md](REVIEW_BATCHES.md).
