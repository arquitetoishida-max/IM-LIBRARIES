# Revisão T6 — linha por linha, 100% dos conceitos (en, pt-BR, ja, zh)

Cada linha = UM conceito (id), definido pelo inglês (en + en_desc). Leia TODAS as linhas do seu slice (Read em partes de ~100 linhas). Para CADA conceito faça esta lista, nesta ordem, e só então passe ao próximo:

1. CONCEITO: o conceito existe e é comum nas 4 línguas/culturas? Regra do dono: conceito tem que existir no próprio idioma e cultura. Gíria, regionalismo (EUA, Reino Unido, Brasil, Japão, China), nome de lugar/monumento, sigla, marca → aposente ("retire").
2. PALAVRA de cada idioma: é a palavra comum do dia a dia para ESSE sentido? Classe gramatical certa (pos)? Nuance obrigatória do idioma aplicada? Ex.: brother/sister → ja 兄弟/姉妹 genérico, mas existem 兄 (irmão mais velho), 弟, 姉, 妹; zh 哥哥/弟弟/姐姐/妹妹; se o conceito é genérico, a palavra ja/zh tem que ser a genérica e a descrição deve citar as formas mais velho/mais novo; se faltar conceito para 兄/姉 etc., anote em issues. Aplique a mesma ideia a tudo (tio/tia materno-paterno em zh, formal/informal em ja, 你/您, tu/você etc.).
3. LEITURA/ROMANIZAÇÃO: ja reading (kana) correta para ESTE sentido; romaji Hepburn igual ao padrão do arquivo (ou/oo, sem mácron, partículas separadas: "hontou ni", "~ shinai"); zh pinyin com tons corretos (多音字!), simplificado.
4. DESCRIÇÕES (en/pt/ja/zh): no próprio idioma, 1 frase curta, correta, sem repetir a palavra; ja simples.
5. ALTERNATIVAS: só sinônimos do MESMO sentido e classe.
6. ANTÔNIMO: o antônimo listado está certo? Falta um antônimo óbvio que exista na lista? (só anote em issues, não edite).
7. FLEXÕES (forms): as formas listadas estão certas (ja conjugação, en plural/passado, pt, zh)? Errada → corrija se tiver certeza; senão issues.

Quando não tiver CERTEZA, consulte a internet (WebSearch / WebFetch: jisho.org, wiktionary, mdbg.net, dicio.com.br, dictionary.cambridge.org). Não chute.

## Resultado por conceito
- Certo → nada.
- Erro que você sabe corrigir → linha em fix{N}.jsonl.
- Erro que você NÃO consegue resolver com certeza → marque pendente (o termo some do app): {"i":"000001234","pending":true,"why":"..."} E escreva linha(s) em issues{N}.tsv.

## Formato fix{N}.jsonl (só campos que mudam)
{"i":"000001234","pos":"v","w":{"pt":{"t":"..","a":[..]},"ja":{"t":"..","r":"..","ro":"..","a":[..]},"zh":{"t":"..","r":"..","a":[..]},"en":{"t":".."}},"d":{"pt":"..","ja":"..","zh":"..","en":".."},"forms":{"ja":{"GRAMMATICAL_KEY":{"t":"..","r":"..","ro":".."}}},"why":"motivo curto em pt"}
Aposentar: {"i":"000001234","retire":true,"why":"..."}

## Formato issues{N}.tsv (sem cabeçalho, TAB entre colunas, uma linha por problema)
id<TAB>idioma (en|pt-BR|ja|zh|todos)<TAB>problema descrito em português claro, com sua dúvida/pergunta para o dono<TAB>campo(s) com erro (text, reading, romanization, alternatives, description, antonyms, forms:CHAVE, pos, concept)

Não edite outros arquivos, não rode git. Ao final responda só: linhas lidas, nº de fixes, nº retire, nº pending, nº issues, 5 piores exemplos.
