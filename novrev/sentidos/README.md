# Passada de sentidos v2 (branch novrev/sentidos-v2)

Pedido do dono (26/11/2026): cada um dos 4 núcleos (en, pt-BR, ja, zh) tem que listar os sentidos principais de cada
palavra **do ponto de vista da própria língua**. A auditoria #512 foi rasa (ex.: "cara" sem rosto/moeda e com 3 IDs
de "homem informal"). Esta fila refaz tudo, idioma por idioma, sem pedir lote a lote.

## Regras
- Sinônimos e gírias do mesmo sentido = **variantes** (`alternatives`) dentro do ID, nunca IDs separados.
  "+ significados" (app) lista os IDs cujo `text` ou `alternatives` têm a palavra: então cada sentido real da palavra
  tem que ter um ID onde ela aparece como texto ou variante (cara → rosto, expressão, lado da moeda, homem informal).
- Sentido real que falta: se já existe ID com outro texto, só ligar (`alt+`); se não existe, criar ID nos 4 idiomas
  (`new`, com `vcu14` quando for vocabulário do dia a dia). Sem equivalente nos 4 → não criar; anotar em
  `pendencias.md` (id, idioma, problema).
- Variante errada, arcaica, regional ou de outro país (sítio = lugar é pt-PT) → `alt-`.
- ID duplicado (mesmo sentido, mesmo texto em inglês) → `drop` do duplicado nos 4 idiomas.
- Nada regional/britânico/de cidade no núcleo (lei do dono). Flexões e plurais não têm ID (só infinitivo/singular),
  exceto quando a forma vira outro significado. Comparativos/superlativos têm ID.
- Descrição sempre na própria língua, curta, com exemplo de uso; corrigir as ruins (`desc`).
- Antônimos só entre mesma classe e mesmo sentido. Masculino é a forma de estudo nas românicas.
- Planilha "Kanji Study" do dono: se chegar, ela manda nas traduções e na predominância dos sentidos.

## Ferramentas (rodar na raiz do repo)
- `python3 novrev/sentidos/dump.py LANG INICIO N n,v,adj` — palavras por prioridade VCU14 com todos os IDs que as usam.
- `python3 novrev/sentidos/find.py "en:turn on,dawn|pt-BR:sala"` — onde a palavra já existe.
- `python3 novrev/sentidos/apply.py novrev/sentidos/edits_NNN.jsonl` — aplica (ops no cabeçalho do script).
- Conferência: `python3 novrev/tools/check.py`, `python3 scripts/validate_vcu100_catalog.py`, `python3 -m pytest -q tests`.

## Execução de cada rodada
1. Ler `progress.json`. Para cada idioma, pegar as próximas ~120 palavras (`dump.py LANG <pos> 120 n,v,adj`;
   depois que n,v,adj acabarem, o resto das classes), julgar sentido por sentido, gravar `edits_NNN.jsonl`, aplicar.
2. Atualizar `progress.json`, commit e push na branch. Nada de mergear sem o dono autorizar.
3. Passes finais (`pending_passes`): flexões, duplicados, 4 planilhas de revisão (`revisao/LANG.xlsx`, colunas
   palavra | definição | variantes e outros sentidos | id oculto; ordem VCU14; suspeitas marcadas), versão nova dos
   núcleos + catálogo (guardar a anterior em `v2/previous`), PR para a main e avisar o dono.
