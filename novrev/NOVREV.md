# NOVREV — revisão global (19/11/2026)

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
