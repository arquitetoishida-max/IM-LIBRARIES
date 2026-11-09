# Study forms implementation evidence — 09 November 2026

Source snapshot is the IM-LIBRARIES main tree `b4e9097fcb17678f144b678cb4289066c831ea31`, catalog 1.2.0, core package versions 2.2.0. The builder was run on each full package with an empty reviewed-alternative registry. All original entries and fields were retained; only eligible lexical entries gained the extension. Existing retired records, examples and grammatical-form entries received no lexical form cards.

- EN: 3,615 source entries, 3,313 primary forms exported.
- PT-BR: 3,612 source entries, 3,495 primary forms exported.
- JA: 3,611 source entries, 3,342 primary forms exported; reading required for every exported form.
- ZH: 3,610 source entries, 3,320 primary forms exported; pinyin required for every exported form.

Six unittest cases passed, including legacy package validation, idempotent regeneration, identity after spelling correction, independently identified tokoro in the test-only context, exclusion of unreviewed alternatives/grammatical duplicates, and failures for foreign IDs, duplicate recommendations, missing readings, unapproved forms, private state and removed alternative identities.

The full generated packages were temporary candidates. Their SHA-256 values for this builder run are EN `ab921d568b0908897307d1e5c390e5d525a2996191123969e3d276ee222376df`, PT-BR `9339d4da889fd425b6bf598fab53c5ef9aa57d6f3378450ce88d1e7000401537`, JA `747feecb3d6460ab3044c64e9d004fc87a198738b27c0daaa9ba8245370d6428` and ZH `e35bdfa4f50fde5f482aa988789f00f6c8584629772a54a92cd68e6391d609dc`.

Publication is pending integration of the reader, migration and independent form progress in MULTILANG #47, with the Android update/backup/offline checks in #50. This evidence covers the data implementation and Python checks. The fixture does not approve all existing alternative strings as independent lexical equivalents. Additional production alternatives require individual contextual review and explicit registry IDs.
