# Trainable lexical forms — schema-2 extension v1

Implementation of IM-LIBRARIES #7 for the MULTILANG #47 reader. Package schema stays 2. `study_forms_version: 1` announces the optional extension. Old readers ignore it and keep the existing `text`, `alternatives`, `forms`, IDs and descriptions.

## Identity and fields

Each eligible entry has a `study_forms` array. `form_id` is scoped to package and language, remains stable across spelling corrections and sorting, and must begin with the owning entry ID plus `:sf:`. The primary uses `:sf:0`. Additional suffixes are explicitly allocated in the reviewed registry, never regenerated from text, pronunciation, list position or a translation. An alternative is another way to express the same contextual meaning. Readings, transliterations and spelling representations share that form's identity. Grammatical inflections remain in the existing `forms`/typed-unit contract.

Every form contains `form_id`, `entry_id`, `english_id`, nullable `english_sense_id`, `text`, `speech`, `usage_en`, boolean `recommended` and `include_by_default`. The primary also contains `legacy_entry_id`. Optional fields are `reading`, `romanization`, `register`, `region_tags`, `context_en`, `examples`, `representations`, `sources`, `study_priority`, `study_tier` and `age_band`. An example is an object with `text` and a map `translations` keyed by locale. A representation is an object with `text` and an explanatory `usage_en`.

Age bands, when individually evidenced, are 3, 5, 7, 10 or 14. Omission means unknown. Neither curriculum tiers nor frequency estimates prove an age of acquisition. A different lexical form inherits no reading, age or register from its sibling. Priority on the primary inherits the entry's existing study priority. New alternatives require their own explicit metadata.

Exactly one form is recommended and included initially. The legacy primary is the fallback recommendation. An explicitly reviewed alternative may declare `recommended: true`, making it the initial recommendation while the primary retains its legacy grade anchor. Other alternatives are exported with `include_by_default: false`. The user's choice and automatic admission of everyday siblings belong to the app. `grade`, history, schedules, selected states and profile identities are private and never enter package data. An entry without a lexical equivalent stays absent in that language. Retired entries, examples and grammatical-form entries receive no trainable lexical forms.

## App integration and migration

Persist each form's state using the tuple `(profile, studied_language, stable_package_or_course_scope, english_id, english_sense_id-or-null, form_id)`. Serialize the tuple without ambiguous string concatenation. Reordering does not affect it. The owning entry ID alone is insufficient across courses. Keep the distinction between a missing sense ID and a named sense.

The legacy grade can migrate only to the primary carrying the matching `legacy_entry_id`, within the same existing course/language/direction scope. Siblings start with no history. Ambiguous legacy matches remain saved as legacy records for explicit resolution. The app owns an idempotent migration marker and must include form preferences/state in backup and restore. Dropping an alternative's identity is rejected by the builder; withdrawal requires a separately reviewed retirement/mapping strategy.

The reader uses `study_forms` when extension version 1 is present, otherwise its existing legacy behavior. Grammatical `forms` retain their current meaning. Displaying a representation or rotating for consultation changes no grade. Selection, independent grades, active/paused/dominated filters, contextual acceptance, concept-to-card expansion and session recomputation are MULTILANG #47 responsibilities. Counter examples include 15 concepts producing 20 active form cards, grade 7 on basho with tokoro still ungraded, and an explicit unchecked sibling staying excluded.

## Build and validation

`python scripts/study_forms.py v2/en-core-v2.json --output /tmp/en-candidate.json`

Add `--registry editorial/study_forms/approved.json` to export individually approved alternatives. This command writes a separate candidate atomically. Existing catalog hashes and public package files are untouched. The registry has `version: 1` and a `packages` map from package ID to entry ID to a list of alternative records. Each record needs an explicit stable `form_id`, `approved: true`, `sources`, `context_en`, `text`, `speech`, `usage_en`, and the reading/pinyin required by its language. No alternative is promoted merely because it occurs in the old unstructured `alternatives` array.

`python scripts/study_forms.py /tmp/en-candidate.json` validates without writing. Unknown registry entries, malformed IDs, missing required readings, duplicate forms, invalid defaults and student-state leakage fail the command. `python -m unittest discover -s tests -p 'test_study_forms.py'` checks stability, legacy fallback, contextual alternatives and rejected input.

`fixtures/study_forms/ja-place.json` and its registry exercise basho/tokoro in a physical-location context. These fixtures are test-only. The equivalence does not extend to tokoro as a grammatical construction or basho as a sumo tournament. Public release needs a version bump, regenerated hashes and counts, plus the reader/migration acceptance evidence under MULTILANG #47/#50.
