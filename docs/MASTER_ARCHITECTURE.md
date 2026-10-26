# ISHIDA MULTILANG — MASTER LEXICAL ARCHITECTURE (v1)

## Core principle

An **ISHIDA concept ID** is a permanent, language-neutral identifier for one tightly specified meaning. English is the **pivot for the initial editorial order and default explanations**, not a required translation and not an assertion that all concepts exist in English.

The same form can have distinct senses: `bank` (financial institution) and `bank` (river edge) require two IDs. A single concept can have several forms in one language, including standard synonyms, colloquialisms and slang; forms retain their **own IDs** even when linked to the same concept.

**Do not infer equivalence from shared English gloss, word position, text similarity, or frequency rank.** Incomplete/uncertain mapping stays unlinked until reviewed.

## Distinct identifiers

- `concept_id`: `imc:000000001` — permanent, never recycled.
- `lexeme_id`: `iml:en:000000001` — specific word/phrase in an explicit locale/language.
- `sense_id`: `ims:en:000000001` — meaning of that lexeme, linked to a concept after review.
- `source_id`: unaltered upstream dictionary identifier; informational and traceable.

When a local slang form means the same underlying concept as the standard form, map both senses to one `concept_id` and distinguish the lexemes, register, region, domain, age and connotations. **If slang changes the underlying meaning, use another concept ID** and link a related concept if useful.

## Locale codes

`pt-BR` display **Port. (Brasileiro)**; `pt-PT` display **Portugues**; also `en`, `ja`, `fr`, `it`, `es`, `de`, `zh`, `ko`, `ru`. Regional varieties are tags, e.g. `en-US`, `en-GB`, `en-US-NY`, `en-US-CA`, `en-US-TX`; those are app-internal geo-tags, not all formal BCP47 language tags.

## Data model

- `concepts/`: sense-level concept records, description in English when possible.
- `languages/`: words and expressions with stable lexeme IDs, spellings, examples, pronunciation, linked concept IDs, register, regional labels, notes, and source status.
- `frequency/`: frequency per language/variety, source, period, measure, rank, corpus domain (spoken/written). Ranking is **NOT** a permanent concept ID.
- `proficiency/`: CEFR (estimated or source-attributed and language/sense-specific), JLPT/HSK/TOPIK separately. CEFR is not a universal official word-by-word list.
- `raw/`: imported sources retained with upstream IDs and attribution, pending semantic mapping.
- `catalog.json`: lists **only** actually published usable files and their accurate statuses.

## Study condition

For chosen locales A and B, present a concept only if it has at least one validated lexeme or expression linked to the same concept in A **and** one in B. English may be empty. Incomplete data are retained without being falsely displayed as valid study pairs.

## Expressions and slang

Store `kind: word|expression`, `register: neutral|informal|slang|vulgar|formal`, `regions: []` (not mutually exclusive), attested meaning, examples, approximate dates of relevance, `confidence`, and `review_status`. Region is only a claim when supported by a source; US slang is not necessarily exclusive to NY/CA/TX. Distinguish meaning-equivalent alternatives from near-synonyms and context-specific substitutions.

## Explanations

Store short editable English explanations in the master data. Do **not** machine-translate on every app launch: that requires connectivity, may incur fees, introduces inconsistent results and makes offline study fail. Instead prepare and cache versioned translations offline or translate once during data curation and mark `review_status`. No translated explanations are authoritative until checked.

## Sorting and pedagogy

Assign IDs independent of display order. Frequency may change between corpus versions, so the ranking must be a separate field. Draft CEFR levels as **estimates**, not official accreditation; slang often has register/use guidance rather than a meaningful fixed CEFR label. Provide separate spoken-frequency and general-frequency when available.

## Migration

Preserve all previously published source-specific IDs and vocabulary. Build a new semantic crosswalk without automatically linking a source's English gloss to a master concept. Existing 2,000-record packages remain raw source material, **not** automatically international concept dictionaries.

## Release gate

Automated generation can be large, but production eligibility requires: licensing and attribution, no empty study pairs, IDs unique/immutable, source-specific provenance, deduplication, reviewed or explicitly provisional sense mapping, actual import/parser tests, and checksums.
