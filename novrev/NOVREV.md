# NOVREV — revisão dos quatro núcleos

## Ordem de execução vigente — 23/11/2026

Revisão editorial autorizada pelo proprietário em 23/11/2026. [LEXICON #88](https://github.com/arquitetoishida-max/LEXICON/issues/88) concentra as decisões editoriais. [IM-LIBRARIES #505](https://github.com/arquitetoishida-max/IM-LIBRARIES/issues/505) concentra os checkpoints e a entrega. O flip do APK é tratado em [ISHIDA-MULTILANG #122](https://github.com/arquitetoishida-max/ISHIDA-MULTILANG/issues/122).

1. Fixar a versão dos quatro núcleos e cruzar a matriz com os registros por `english_id` e sentido. A linha do XLS é o ponto de partida da revisão. Conferir presença e identidade antes de tomar decisões sobre os termos.
2. Revisar uma coluna inteira de cada vez, EN-US → PT-BR → JA → ZH. Manter boas descrições. Redigir alterações no próprio idioma, com o uso principal primeiro e até quatro usos cotidianos, com um quinto quando distinto e útil. Usar a referência editorial interna quando confirmar o mesmo sentido. Consultar outra fonte quando faltar evidência.
3. Encerradas as quatro colunas, comparar os quatro termos por ID e sentido. Preservar equivalências práticas. Corrigir a divergência clara e usar o estado editorial existente nos casos inconciliáveis.
4. Preservar VCU14, NHK e as classificações não afetadas. Informação JLPT ou da camada inglesa pode ser aproveitada quando a referência de fato trouxer dado equivalente. Registrar expressões fora do núcleo como Reservar ou Ignorar no XLS de pendências, ao lado da matriz.
5. Registrar o último bloco e o próximo ID no Git. Verificar os deltas, as classificações, os IDs, a ordem de cada pacote e os hashes antes de encaminhar os candidatos. A validação do APK segue suas issues e a regra de compilação da ISHIDA-MULTILANG #107.

## Registro da execução — 23/11/2026

- Base em `2e74688642dba1088f98a00536f00310f1c50ae4`: catálogo 1.5.3 e núcleos 2.5.3.
- Candidato nesta branch: catálogo 1.5.4 e núcleos 2.5.4. Os quatro mantêm 3.639 IDs, a sequência interna de cada arquivo e os níveis A1–C2 usados no inglês. O campo `study_priority` agora tem ordem única em cada idioma, preservando a prioridade relativa entre entradas ativas. Empates herdados seguem a ordem já presente no respectivo pacote. Pendências ficam depois das entradas elegíveis.
- [XLS de pendências e cobertura](NOVREV_pendencias.xlsx): 335 conceitos conferidos nos quatro idiomas, 40 recortes regionais reservados e 26 conceitos suspensos por falta de equivalência prática. Outros 6 IDs da matriz já estavam fora dos quatro pacotes desde a integração 2.4.0. Os 30 conceitos adicionados depois da matriz constam na aba Matriz atual. A fila de 423 relatos foi indexada. Um termo localizado no acervo ainda precisa ser conferido pelo sentido do relato.
- A matriz tem 3.238 conceitos com revisão semântica em aberto. As posições 1–266 foram percorridas. Retomar na posição 267, `en:000001984` (tired). O XLS indica os itens mais adiante já tratados e permite passá-los ao retomar. Após as quatro colunas, cruzar os casos ainda em aberto por ID e sentido.
- Conferências feitas: hashes, versões, contagens, ordem e IDs por língua, proteção dos vínculos e níveis, estados e prioridades. Passaram os 16 testes do repositório e o validador do catálogo. A homologação em Android fica para a fase de entrega.

## Registro anterior — 19/11/2026

Escopo novo e separado, que substitui as ordens de serviço antigas de revisão dos dicionários. Dono: Gabriel Noboru Ishida.

## Escopo
- Só **en, pt-BR, ja e zh** (núcleos). Os demais pacotes foram despublicados em `v2/catalog.json` 1.3.0 (arquivos preservados) e só voltam após passar pela NOVREV; depois serão refeitos a partir do esqueleto de IDs e descrições.
- Uma linha por **conceito** (`conceito_id` = `english_id`) em `NOVREV_matriz.xlsx`, com os 4 IDs. Os 4 dicionários terão exatamente as mesmas quantidades.
- Base = **VCU14** (grupo `VCU14`). O que sobra de JLPT/HSK vai para o fim da fila (`VCU14+`, preenchimento), organizado em suas próprias categorias. Pode ser enxugado: pacote grande com erros não serve.

## Regras decididas
1. **Sem equivalente num idioma** (partículas, objetos exclusivos): grupo/categoria próprios, ID próprio, sem paralelo nos outros, com explicação em inglês (o app traduz em tempo real para o idioma nativo).
2. **Palavra errada**: refazer do zero é preferível a reformar. Reserva fica fora da contagem de palavras.
3. **Descrição (T3)**: no idioma nativo, por sentido, distinguindo homônimos (ex.: cara = rosto / lado da moeda / produto caro / querida / gíria "sujeito").
4. **Dica (T4)**: início da palavra com chave para alternar o campo de origem entre kana/kanji/hanzi e romaji/pinyin (requer mudança no app).
5. **Antônimos (T6)**: ligação sempre pelo `conceito_id`, valendo nos 4 idiomas; vazio = "sem antônimo" ou pendente (campo de status).
6. **Listas JLPT/HSK**: manter como estão (comunitárias, aproximadas, atribuição em `third_party`).
7. Só o dono usa o app: sem preocupação com notificação de usuários.

## Tarefas (colunas de status: PENDENTE / OK / CORRIGIDO / NA)
T1 palavra principal correta por ID nos 4 idiomas · T1B compostas que são expressões/partícula · T2 edição por dicionário · T3 descrição nativa 100% · T4 dica 100% · T5 variantes (romaji, pinyin, kana, kanji, hanzi) · T6 antônimos · T7 formal/informal/conjugações (mover para o lugar certo).

Pronto = todas as linhas do grupo VCU14 com T1–T7 em OK/CORRIGIDO/NA.

## Campo `user_hint` (dica do usuário)
Campo reservado em todas as entradas dos 4 idiomas, vazio (`""`) por padrão. O app grava aqui a dica escrita pelo próprio usuário (botão ao lado da dica existente no Card). O dicionário publicado nunca preenche este campo; o app deve mantê-lo localmente e mesclar por `english_id`, para não perder a dica quando o pacote for atualizado.
