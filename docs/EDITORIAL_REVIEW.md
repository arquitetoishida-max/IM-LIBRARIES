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

## Mandarim (zh) — 28/10/2026
`curation/editorial/zh/z001–z007.txt` (`N|hanzi;alternativas|pinyin`): 2.515 entradas em chinês simplificado com pinyin com tons, traduzidas do mesmo sentido inglês de cada id (artigos *a/an* sem equivalente). Conferência com pypinyin: 199 divergências revisadas — tons neutros (喜欢 xǐhuan), sândi de 一/不 (yíyàng, búguò), erhua (一点儿), 地 adverbial = de e leituras que o pypinyin erra (干 gān, 长 cháng, 教 jiāo, 数 shǔ); 1 erro real corrigido (*parent* 家长).

## Pendências
- Revisão humana nativa (brasileiro e japonês), principalmente expressões/gírias.
- Divergências de leitura apontadas por `docs/EDITORIAL_QA.json` (pykakasi) devem ser conferidas uma a uma.
- `vcu14_rank` continua o provisório já publicado; outras línguas (es, fr…) ainda usam a base antiga e mantêm os ids excluídos.
