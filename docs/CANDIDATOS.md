# Pacotes candidatos (IM-LIBRARIES #2)

Contrato: LEXICON `docs/CONTRATO_UNIDADES_ESTUDO_v1.md` e `docs/UNIDADES_FORMATO_v1.md`. Schema continua **2**:
`forms[]` por entrada (já lido pelo app) e, no topo, `constructions`, `grammar_units`, `unit_aliases` — leitores
antigos ignoram esses arrays.

## Gerar um candidato (não publica nada)
```sh
python scripts/build_candidate.py --lang ja --delta <LEXICON>/editorial/candidates/ja-<rodada>.delta.json --lexicon <LEXICON>
```
Saída em `candidates/<lang>/`: `<pacote>-<versão>-candidate.<rodada>.json` (só se todos os gates passarem) e
`manifest.json` (hash da base para reversão, hash do candidato, contagens separadas de lemas/formas/construções/
unidades gramaticais, erros e avisos). `v2/catalog.json` e `v2/<lang>-core-v2.json` **não são tocados**.

Gates: nenhum ID existente some; `english_id` e `kind` de IDs existentes não mudam (mudança = ID novo + alias);
entrada nova só com `approved_new: true`; fixtures `test-only` recusadas; validadores de unidades do LEXICON sem erro.

## Promoção (somente com autorização explícita do proprietário)
1. Teste de importação no app (Android real) com o candidato servido localmente: grupos, notas 0–7, direção,
   offline, atualização sobre a versão ativa.
2. Copiar o candidato para `v2/<lang>-core-v2.json`, atualizar `version`, `sha256`, `size_bytes`, `entry_count` do
   catálogo **no mesmo commit**.
3. Reversão: restaurar o arquivo e os campos do catálogo a partir de `manifest.json → base` (hash conferido).

Estado: ferramenta pronta e testada com dados de teste fora do repositório; nenhum candidato real ainda
(aguarda os pilotos LEXICON #2/#3).
