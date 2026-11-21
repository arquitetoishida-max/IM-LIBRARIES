# Revisão T5 — 100% dos 4 dicionários (en, pt-BR, ja, zh)

Cada linha do seu slice é UM conceito (id) com a palavra nos 4 idiomas. O conceito é definido pelo inglês (en + en_desc).
Leia TODAS as linhas do seu slice, uma por uma (em partes de ~120 linhas com o Read, offset/limit). Não pule nenhuma.

## O que é erro (corrigir)
1. Tradução errada, absurda ou de outro sentido (ex.: "its" → ja その; "jawn" → あれ/"troço"; "bodega" → コンビニ).
   A palavra de cada idioma tem que ser a palavra comum, do dia a dia, que um nativo usa para ESSE sentido.
2. Registro errado: gíria, regionalismo ou palavra rara no lugar da palavra comum.
3. Classe errada: verbo traduzido por substantivo, adjetivo por advérbio etc. (respeite o pos).
4. Japonês: leitura (kana) errada ou que não bate com o texto; romaji que não bate com a leitura (Hepburn: shi, chi, tsu, ō → use "ou"/"oo" como no resto: siga o padrão existente do arquivo); kanji raro quando o normal é kana (ex.: 出来る→できる; 有難う→ありがとう).
5. Chinês: simplificado sempre; pinyin com marcas de tom, correto, sílabas separadas por espaço só entre palavras como já está no arquivo; palavra errada.
6. Português do Brasil: palavra de Portugal, gênero/número errado, falso cognato.
7. Descrição (pt_desc, ja_desc, zh_desc, en_desc): tem que estar NO PRÓPRIO IDIOMA, curta (1 frase), correta, descrevendo o sentido do conceito e não outro; nunca só repetir a palavra (ex.: zh "大约。" para 大约 é ruim). A ja_desc deve ser simples (kana/kanji básicos).
8. Alternativas (alt) erradas, de outro sentido, ou duplicadas da palavra principal.
9. Conceito que é gíria/regionalismo/nome próprio/sigla que não serve para núcleo de vocabulário cotidiano → marque "retire":true.
10. Antônimo errado (lista de ids em "antonyms") → informe em "why" (não edite).

## O que NÃO fazer
- Não "melhore" o que está certo. Só corrija erro real. Na dúvida razoável entre duas palavras boas, deixe.
- Não invente ids, não mude o id.

## Saída
Escreva no arquivo indicado (JSON Lines, um objeto por conceito corrigido), SÓ os campos que mudam:
{"i":"000001234","w":{"pt":{"t":"palavra","a":["alt1"]},"ja":{"t":"漢字","r":"かな","ro":"romaji","a":[]},"zh":{"t":"汉字","r":"pīnyīn","a":[]},"en":{"t":"word"}},"d":{"pt":"desc","ja":"説明","zh":"说明","en":"desc"},"why":"motivo curto em português"}
Para aposentar: {"i":"000001234","retire":true,"why":"..."}
Ao final, responda só: número de linhas lidas, número de correções, e 5 exemplos das piores.
