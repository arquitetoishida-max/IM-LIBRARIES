# Synthetic missing-word compatibility fixtures

These three JA/ZH/PT-BR requests exercise the already existing v1 contract, including `new:` markers, `english_id: "-"`, Unicode and original captured spelling. Their words/hints do not assert actual dictionary absence or approved equivalence. Versions identify them as test fixtures. Never submit them live or count them as editorial vocabulary.

`node community/receiver/test_receiver.cjs` checks the original service behaviors and these fixtures: successful mocked receipt, same-ID/property-order retry with one GitHub POST, metadata/message/time preservation, version mutation conflict and rejection of an overlong marker. No source change to `Code.gs` or `report.schema.json` is necessary.

On November 16, 2026, `jsonschema.Draft202012Validator` with `FormatChecker` also validated all three fixtures against `report.schema.json`; removing each required field was rejected. These checks validate the payload, not Claude's Android normalizer/outbox. Live POST, durable receipt, lost response/offline recovery and device acceptance remain pending in #9/#55/#70.
