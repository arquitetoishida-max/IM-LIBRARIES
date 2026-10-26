# ISHIDA — English monolingual dictionary v1

The English master is **monolingual** and is the editorial pivot for future locale dictionaries. English lexical IDs are stable and must never be renumbered. The independent frequency file may be re-ranked.

## Published files
- `master/en-master-v1.json`: 3,000 English high-frequency headwords + 25 drafted regional slang/expressions; English definitions and documented WordNet senses for headwords found in WordNet. Each English headword has its original reserved ID. Some headwords may have several meanings; their WordNet sense IDs are separate and must be selected before a translation is linked.
- `frequency/en.json`: independently ranked entries with Zipf scores, joined via `english_id`. The slang records do not yet have independently verified regional frequency rankings.

**Important:** `concept_id` fields in v1 are legacy reserved slots from the first draft. They are **not approved international concept identities**. The operative key for mapping future languages is `english_id` plus the *specific English sense ID* where multiple meanings exist. The first locale mapping must introduce a stable mapping table and may introduce new concepts with no English equivalent. Never align words merely by shared index.

## English definitions
The preferred short summary is `short_description_en`, alongside `senses[].definition_en` and `definitions_en` (where found). The meanings are sourced from **Princeton WordNet 3.0**. License and attribution are required on redistribution; consult the original WordNet license at https://wordnet.princeton.edu/license-and-commercial-use .

Some spelling variants, colloquial forms and high-frequency grammatical words are not defined in WordNet. Marked `definition_status: missing-dictionary-definition`, not silently fabricated. Several common words have multiple WordNet senses: do not presume the first sense is the most frequent sense or the only possible translation.

## CEFR preliminary annotations
The `cefr` values are **heuristic frequency bands only** (500 A1, 600 A2, 700 B1, 600 B2, 600 C1), not research-backed proficiency labels. `cefr_status=heuristic-frequency-only-unreviewed`. Revise with a language-specific lexical CEFR source or expert review before using for official proficiency training. Regional slang carries no CEFR level.

## Slang and regions
Slang entries store their own English IDs and a separate short explanation, as well as provisional region tags. Regional tags are non-exclusive. New York, northern California, Texas, Boston, Britain, etc. will be expanded after checking actual attestation. An equivalent slang form can map to the same sense as a standard word, but only where context and pragmatic register allow.

## Brazilian Portuguese next
For each English lexeme/sense: find Brazilian Portuguese translation(s) **for the exact intended meaning**; store original English ID and sense identifier as a foreign key, Brazilian localized form and meaning, examples, regional use and separate Brazilian frequency. Where no exact PT-BR translation exists, retain a note and mark the association non-equivalent or absent. Additional PT-BR concepts without English counterpart receive native stable IDs and can still be paired with other languages.

The ISHIDA app may provide **on-demand translation of the English explanatory text** when the user requests it, with local caching and an offline English fallback. Do not translate every record upon app launch and do not confuse translated explanations with validated lexical translation fields.

## Publication status
The data is a **draft source dictionary**, not approved automatic cross-language pairs. Dictionary sense alignment, CEFR validation, slang evidence, and missing WordNet coverage remain editorial tasks. Keep these statuses explicit in the catalog.

## Refinamento funcional (2026-10-26)

O objetivo pedagógico é ser utilizável, sem reivindicar certificação oficial. O gerador cobre os níveis de estudo **A1–C2 por aproximação de frequência**, com aviso ao usuário: *Níveis aproximados para orientar o estudo; não são classificações oficiais.* Níveis de homógrafos variam com o sentido e devem ser refinados quando possível. Registros sem WordNet recebem glossário editorial breve apenas quando a definição é conhecida e sustentada, e os demais mantêm um marcador de revisão, não definições inventadas.

Toda entrada utiliza `description_short_english` com no máximo 12 palavras, quando existe material definicional; `short_description_en` pode preservar a definição mais longa. Gírias usam definição curta e múltiplas regiões, com status provisório. Frequência segue isolada em `frequency/en.json`, e o ID inglês não deve ser reordenado.

**Nota de licença:** dados de WordNet 3.0 exigem crédito e a reprodução do aviso de licença nas cópias distribuídas. Referência: https://wordnet.princeton.edu/license-and-commercial-use .
