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

## Versão 2.1.0 — consolidação (28/10/2026)
Pacotes `en`, `pt-BR`, `ja`, `zh` passam a 2.1.0, gerados só por `scripts/build_editorial_core.py`:
- **Removido** `frequency` (Zipf/wordfreq): 2.420 entradas en, 2.420 pt-BR, 2.418 ja (e o equivalente em zh). O app não depende do campo (ordenação usa `vcu14_rank` e a ordem dos ids).
- **Metadados trocados** nos 4 pacotes: `license`, `sources`, `notes` (sem Wiktionary/Kaikki/WordNet/Argos/wordfreq/CC BY-SA genérico). O builder reescreve esses campos a cada execução, então reconstruções não trazem os antigos de volta.
- **Removido** o bloco `ui` do pacote zh (294 textos de interface traduzidos por máquina, com erros como 纸牌 para "Cards"); `has_ui=false` no catálogo. Interface em chinês: o app usa inglês até haver tradução revisada.
- **Mantidos**: ids, `english_id`, ordem, `kind`, `part_of_speech`, `level`, `vcu14_rank` (1.062 en/pt-BR; 1.060 ja/zh), `environments`, `vcu14_status`, `lemma` (133 en), leituras/romanização/pinyin (escritas na revisão), `speech` (40 ja).
- **JLPT** (703 entradas ja, campo `classifications`): vem das listas comunitárias OpenJLPT (CC BY-SA 4.0); a atribuição fica só em `third_party` do pacote ja e no próprio campo. Aproximado, não oficial.
- **level**: faixa aproximada estilo CEFR (A1–C2), estimada originalmente pela posição da palavra na lista de seleção (lista de frequência); nenhum valor de frequência é distribuído. Isso está declarado em `notes`.
- **HSK**: o zh antigo não tinha níveis HSK; nada foi apagado. Adicionar HSK exige uma fonte com licença compatível (pendência).
- Romanização japonesa: `scripts/kana_romaji.py` (próprio). Pinyin: escrito na revisão e conferido com pypinyin (apenas QA, não copiado).

### Diferença de 2 entradas (ja/zh × en/pt-BR)
`en:000000001` *the* e `en:000000028` *an* são artigos; japonês e mandarim não têm artigo, então não há par (sem card nesses idiomas). Não é perda de dados.

### Rollback
- Tag `libraries-v2.0.0`: pacotes 2.0.0 (com `frequency` e metadados antigos).
- Tag `libraries-pre-editorial`: última base antes da revisão editorial (definições Wiktionary).
Para restaurar: `git checkout <tag> -- v2/<pacote>.json v2/catalog.json` e publicar.

### Dependências de terceiros que continuam (componentes, não o dicionário)
- Pacotes de escrita `v2/writing/`: KanjiVG (CC BY-SA 3.0, Ulrich Apel) e hanzi-writer-data (Arphic Public License; dados derivados de Make Me a Hanzi) — licenças nos próprios pacotes.
- Outros idiomas (es, fr, it, de, ru, ko, ar, hi e gírias regionais) ainda são a base antiga e mantêm seus próprios créditos; não fazem parte desta consolidação.

## Pendências
- Revisão humana nativa (brasileiro e japonês), principalmente expressões/gírias.
- Divergências de leitura apontadas por `docs/EDITORIAL_QA.json` (pykakasi) devem ser conferidas uma a uma.
- `vcu14_rank` continua o provisório já publicado; outras línguas (es, fr…) ainda usam a base antiga e mantêm os ids excluídos.
