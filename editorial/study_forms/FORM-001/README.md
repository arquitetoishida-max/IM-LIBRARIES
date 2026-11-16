# FORM-001 — six reviewed English alternatives

Refs IM-LIBRARIES #7 and MULTILANG #47. Candidate editorial data only; not in the public catalog.

- car → automobile (passenger road vehicle, not a railway car)
- fridge → refrigerator (same household appliance)
- bye → goodbye (farewell expression, not the noun)
- grandpa → grandfather (relationship reference; formal direct address is different in tone)
- grandma → grandmother (relationship reference; formal direct address is different in tone)
- cell phone → mobile phone (UK wording, not restricted to smartphones)

Each alternative has its own stable `:sf:1` ID, speech text, register/context, original example, PT-BR translation and dictionary source URLs. Primary IDs `:sf:0` retain their legacy anchors and default selection. Sources were checked on 2026-11-10 through indexed dictionary text where full-page access returned 403. Cambridge is the publisher of the cited dictionary entries; no examples or dictionary definitions were copied into the alternatives.

No measured age or frequency evidence was found, so alternative age bands and numeric study priorities are omitted. No automatic preference change is made. The English texts are used directly for TTS; no invented romanization is needed. Grammatical inflections remain in the existing contract.

## Verification

`en-source.fixture.json` snapshots the six real entries from en-core-v2 2.2.1; their IDs and meanings were inspected before assignment. It is test-only, not a downloadable language package. Build with the existing exporter and this registry; 6 concepts produce 12 forms. The same registry was also tested against the complete 3,615-entry source package, producing 3,313 eligible concepts and 3,319 forms.

Seven existing tests passed. Additional checks passed for full-package validation, idempotent rebuilding, reordering, identical legacy content after removing the extension, unchanged entry IDs, inactive new alternatives and absent inferred age/priority. Hashes are in `manifest.json`; the generated full candidate is not published.

Reproduce:
```sh
python -m unittest discover -s tests -p 'test_study_forms.py'
python scripts/study_forms.py editorial/study_forms/FORM-001/en-source.fixture.json --registry editorial/study_forms/FORM-001/registry.json --output /tmp/form-001-fixture.json
python scripts/study_forms.py v2/en-core-v2.json --registry editorial/study_forms/FORM-001/registry.json --output /tmp/form-001-en-candidate.json
python scripts/study_forms.py /tmp/form-001-en-candidate.json
```

## Remaining

Android acceptance for primary-grade preservation, independent sibling grades, preferences/backup and concept-to-card counts is pending. Public release still needs an approved package version, catalog hashes and rollback.

Pairs already represented by distinct legacy entries (bike/bicycle, plane/airplane, TV/television, mom/mother, dad/father, big/large, hi/hello and film/movie) were deliberately not merged or re-added. They need a separate semantic/migration decision. Smartphone is narrower than cell phone; phone is broader, so neither was made an unrestricted equivalent. Japanese and Mandarin forms still need their own readings and grammatical review.
