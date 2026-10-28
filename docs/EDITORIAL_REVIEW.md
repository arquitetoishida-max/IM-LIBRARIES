# Revisão editorial 2.0 — inglês (pivô), brasileiro e japonês

**Fonte:** `curation/editorial/batches/b001–b011.txt` (uma linha por id inglês). **Gerador:** `scripts/build_editorial_core.py` → `v2/{en,pt-BR,ja}-core-v2.json` 2.0.0 e `v2/catalog.json`. A reconstrução geral (`build_monolingual_v2.py`) aplica esta revisão no fim, para não sobrescrevê-la.

Formato: `N|classe|explicação curta EN|brasileiro;alternativas|japonês;alternativas|leitura[=pronúncia]` ou `N|-|motivo`.

## Critérios
- Inglês é o pivô: headword e id preservados; escolhido **um sentido cotidiano** por id (ex.: *awesome* = "incrível", não "aterrador"; *kind* = "tipo"; *re* removido).
- Explicação curta em inglês para todos os ids (traduzida no app para a língua nativa).
- Excluídos (ids nunca reutilizados): nomes próprios, nomes de letras/códigos, fragmentos e prefixos, sentidos raros/vagos, gírias hiperlocais, flexões regulares cujo lema existe (*faces*, *doctors*, *years*). Flexões irregulares comuns ficam (*went* → "foi; fui", 行った).
- Brasileiro: homônimos de sentido diferente recebem desambiguação no próprio texto ("canto (de cantar)", "rosa (flor)", "conta (a pagar)"); sinônimos do inglês (big/large) podem compartilhar tradução — a explicação distingue.
- Japonês: kanji + leitura em kana + romanização Hepburn; partículas pronunciadas corretamente (は→wa, へ→e, を→o) com campo `speech` para a voz. Artigos (*a/an*) não têm equivalente japonês: sem par, sem card.

## Resultado
3.140 ids revisados: 2.517 mantidos, 623 excluídos; 2.517 em brasileiro, 2.515 em japonês.

## Conferência das leituras
`docs/EDITORIAL_QA.json` (pykakasi, gerado no GitHub Actions): divergências conferidas uma a uma — eram leituras alternativas ou erradas do pykakasi (人=ひと, お金=おかね, 小さい=ちいさい, 年下=としした, 通り=とおり); 1 erro real corrigido (*ourselves* 私たち自身 = わたしたちじしん).

## Pendências
- Revisão humana nativa (brasileiro e japonês), principalmente expressões/gírias.
- Divergências de leitura apontadas por `docs/EDITORIAL_QA.json` (pykakasi) devem ser conferidas uma a uma.
- `vcu14_rank` continua o provisório já publicado; outras línguas (es, fr…) ainda usam a base antiga e mantêm os ids excluídos.
