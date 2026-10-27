# VCU14 — estágio de curadoria e critérios de publicação

## O que foi produzido
- `curation/VCU14_EN_CANDIDATES_V1.json`: 1.000 **candidatos** selecionados entre 1.436 sementes editoriais de vocabulário cotidiano. Campos: `rank` **provisório**, `word`, `id` existente ou `null`, `topics`, `zipf`, `status`.
- Essa seleção **não é um corpus validado**: ainda não houve coleta e lematização de cinco textos reais por ambiente, nem avaliação de equilíbrio Brasil–Japão–EUA. A contagem e as frequências do arquivo não devem ser confundidas com evidência empírica dessa pesquisa.
- Não foram alterados `master/en-master-v1.json`, `v2/en-core-v2.json`, `v2/catalog.json` ou `frequency/en.json`: aplicar semântico novo diretamente poderia invalidar checksums e quebrar pares, grupos e backups. Não promover a produção até conclusão da fase abaixo.

## Próximos passos necessários para publicar
1. Elaborar/obter **cinco diálogos ou textos por ambiente**, com situações comuns e vocabulário natural de casa, família, férias, escola, viagens, comércio, transporte, cinema, roupas, escritório etc. Preferir textos originais ou corpora com licença explícita. Separar cenários EUA/Brasil/Japão, escritos/interpretados naturalmente, **sem considerar uma tradução literal como corpus independente**.
2. Tokenizar/lematizar, medir contagem e dispersão por ambiente e cultura; não deixar textos curtos ou pronomes repetidos anularem a presença de utensílios e vocabulário essencial. Comparar listas NGSL-Spoken (721) e New Dolch List (874) e, se licitamente disponível, frequência de legendas SUBTLEX-US.
3. Atribuir um `vcu14_rank` próprio, **não confundir com `frequency.rank` geral**, e `environments` múltiplos; preservar ID de palavra existente. Adicionar palavras essenciais realmente ausentes com ID novo; separar sentidos errados ou inadequados sem reatribuir IDs silenciosamente.
4. Excluir 5% de candidatos **realmente raros no corpus temático**, mas revisar manualmente itens essenciais que aparecem poucas vezes (por exemplo `broom`, `spoon`, `passport`) antes de excluí-los. O corte não pode eliminar objetos fundamentais por mera baixa frequência em um texto pequeno.
5. Manter os demais vocábulos de proficiência e dicionários complementares; atualizar pacotes mestre, V2, frequência editorial e catálogo/hash consistentemente com schema validado; teste de download, migração, backup.
6. Documento do app `docs/TAREFAS_TESTES_E_PERFIL.md` define persistência local de subdivisões, seleção da aba ativa e blocos salvos por perfil/curso. Backup `.imbak` deve conter essas seleções, IDs, origem, ordem, nomes, abas, preferências e progresso, sem credenciais secretas.

## Fontes externas para conferir e atribuir adequadamente
- NGSL Spoken: https://www.newgeneralservicelist.com/ngsl-spoken
- New Dolch List: https://www.newgeneralservicelist.com/word-lists
- SUBTLEX-US: https://github.com/chrplr/openlexicon/blob/master/datasets-info/SUBTLEX-US/README-SUBTLEXus.md

**Status:** primeiro índice gerado e commitado, aguarda corpus/revisão; não é biblioteca pronta para usuários.
