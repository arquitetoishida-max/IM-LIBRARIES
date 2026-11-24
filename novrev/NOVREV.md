# NOVREV — revisão dos quatro núcleos

## Ordem de execução vigente — 23/11/2026

Revisão editorial autorizada pelo proprietário em 23/11/2026. [LEXICON #88](https://github.com/arquitetoishida-max/LEXICON/issues/88) concentra as decisões editoriais. [IM-LIBRARIES #505](https://github.com/arquitetoishida-max/IM-LIBRARIES/issues/505) concentra os checkpoints e a entrega. O flip do APK é tratado em [ISHIDA-MULTILANG #122](https://github.com/arquitetoishida-max/ISHIDA-MULTILANG/issues/122).

1. Fixar a versão dos quatro núcleos e cruzar a matriz com os registros por `english_id` e sentido. A linha do XLS é o ponto de partida da revisão. Conferir presença e identidade antes de tomar decisões sobre os termos.
2. Revisar uma coluna inteira de cada vez, EN-US → PT-BR → JA → ZH. Manter boas descrições. Redigir alterações no próprio idioma, com o uso principal primeiro e até quatro usos cotidianos, com um quinto quando distinto e útil. Usar a referência editorial interna quando confirmar o mesmo sentido. Consultar outra fonte quando faltar evidência.
3. Encerradas as quatro colunas, comparar os quatro termos por ID e sentido. Preservar equivalências práticas. Corrigir a divergência clara e usar o estado editorial existente nos casos inconciliáveis.
4. Preservar VCU14, NHK e as classificações não afetadas. Informação JLPT ou da camada inglesa pode ser aproveitada quando a referência de fato trouxer dado equivalente. Registrar expressões fora do núcleo como Reservar ou Ignorar no XLS de pendências, ao lado da matriz.
5. Registrar o último bloco e o próximo ID no Git. Verificar os deltas, as classificações, os IDs, a ordem de cada pacote e os hashes antes de encaminhar os candidatos. A validação do APK segue suas issues e a regra de compilação da ISHIDA-MULTILANG #107.

Quando a mesma palavra abranger sentidos cotidianos que exigem equivalentes diferentes em outro idioma, desambiguar os verbetes e espelhar a forma no idioma em que ela se repete. Reaproveitar um conceito já cadastrado para aquele sentido. Se faltar, criar um ID próprio nos quatro núcleos quando houver equivalência prática. Preservar o vínculo do ID legado e usar a descrição nativa para distinguir os sentidos. Manter as classificações dos verbetes existentes e conferir as do novo sentido separadamente. Se o novo sentido não tiver quatro equivalentes práticos, registrar o caso no XLS de pendências. Aplicar esta regra a toda a revisão, inclusive aos lotes anteriores quando houver um caso semelhante.

## Registro da execução — 23/11/2026

- Base em `2e74688642dba1088f98a00536f00310f1c50ae4`: catálogo 1.5.3 e núcleos 2.5.3.
- Candidato nesta branch: catálogo 1.5.4 e núcleos 2.5.4. São 3.718 IDs por núcleo. Mantidas a sequência interna dos IDs preexistentes, as classificações e a prioridade relativa de estudo. As pendências ficam depois das entradas elegíveis.
- [XLS de pendências e cobertura](NOVREV_pendencias.xlsx): 1.058 conceitos conferidos nos quatro idiomas, 40 recortes regionais reservados e 26 conceitos suspensos por falta de equivalência prática. Outros 6 IDs da matriz já estavam fora dos quatro pacotes desde a integração 2.4.0. Os 109 conceitos adicionados depois da matriz constam na aba Matriz atual. A fila de 423 relatos foi indexada. Um termo localizado no acervo ainda precisa ser conferido pelo sentido do relato.
- A matriz tem 2.594 conceitos com revisão semântica em aberto. As posições 1–1250 foram percorridas. Retomar na posição 1251, `en:000003288` (próximo ID da fila). O XLS indica os itens mais adiante já tratados e permite passá-los ao retomar. Após as quatro colunas, cruzar os casos ainda em aberto por ID e sentido.
- Conferências feitas: hashes, versões, contagens, ordem e IDs por língua, proteção dos vínculos e níveis, estados e prioridades. Passaram os 16 testes do repositório e o validador do catálogo. A homologação em Android fica para a fase de entrega.

### Lote 267–283

- 16 conceitos conferidos, de `en:000001984` (tired) a `en:000000137` (that's). A posição 268 já estava revisada. Comparação por `english_id` e sentido em EN-US, PT-BR, JA e ZH.
- Kanji Study, abas de kanji, consultada para 森, 疲, 言, 開 e os caracteres dos compostos. Para os compostos, o sentido foi conferido no contexto do verbete. O sentido comercial de *order* foi confirmado no [Cambridge Dictionary](https://dictionary.cambridge.org/us/dictionary/english/order). Em mandarim, foram conferidas as formas e alternativas vigentes. Nos quatro pacotes, o ID de *order* fica no sentido de pedido comercial. As colocações gramaticais de *you're* e *that's* tiveram as explicações locais corrigidas, com os estados existentes preservados.
- Mantidos os 3.639 IDs por pacote, a ordem física, as prioridades, as classificações e os estados. Atualizados os hashes e tamanhos do catálogo 1.5.4 para o candidato 2.5.4.

### Lote 285–305

- 20 conceitos conferidos, de `en:000000329` a `en:000000156`. Cruzamento de EN-US, PT-BR, JA e ZH por ID e sentido.
- Conferidos os sentidos espaciais de [*upon*](https://dictionary.cambridge.org/dictionary/english/upon) e políticos de [*state*](https://dictionary.cambridge.org/dictionary/english/state). O ID de *state* mantém a divisão administrativa, sem a glosa chinesa de condição. A definição de 駅 foi ajustada ao uso ferroviário. *Am* conserva o estado de busca, com notas locais para as formas japonesa e chinesa.
- Validação dos IDs, ordenação, prioridades, estados, camadas, contagens, tamanhos e hashes. Os 16 testes locais passaram.

### Lote 306–325

- 19 conceitos conferidos, de `en:000001109` a `en:000002360`. Cruzamento de EN-US, PT-BR, JA e ZH por ID e sentido.
- *Class* mantém o sentido de turma e *floor*, o de piso interno. A definição de [*during*](https://dictionary.cambridge.org/dictionary/english/during) distingue um acontecimento dentro do período da duração pelo período inteiro. O campo japonês de 電車 explicita a tração elétrica, e 列車 permanece como alternativa mais abrangente.
- Validação dos IDs, ordenação, prioridades, estados, camadas, contagens, tamanhos e hashes. Os 16 testes locais passaram.

### Lote 326–345

- 19 conceitos conferidos, de `en:000002362` a `en:000000197`. Cruzamento de EN-US, PT-BR, JA e ZH por ID e sentido.
- O ID de [*address*](https://dictionary.cambridge.org/pt/dicionario/learner-english/address) mantém o endereço físico. Em *appointment*, as glosas de encontro social foram retiradas das entradas de consulta agendada. As descrições de *fish* e *foot* foram ajustadas para delimitar os conceitos, e a de *ourselves* passou a mostrar os usos reflexivo e enfático.
- Validação dos IDs, ordenação, prioridades, estados, camadas, contagens, tamanhos e hashes. Os 16 testes locais passaram.

### Lote 346–370

- 25 conceitos conferidos, de `en:000002639` a `en:000000644`. Cruzamento de EN-US, PT-BR, JA e ZH por ID e sentido.
- O sentido material de [*board*](https://dictionary.cambridge.org/dictionary/english/board) foi separado de quadro escolar. A entrada de *play* corresponde a brincar e jogar, sem equivalentes de tocar um instrumento. As quatro descrições de *money* passaram a incluir valores em conta.
- Validação dos IDs, ordenação, prioridades, estados, camadas, contagens, tamanhos e hashes. Os 16 testes locais passaram.

### Lote 371–400

- 28 conceitos conferidos, de `en:000001677` a `en:000000759`. Cruzamento de EN-US, PT-BR, JA e ZH por ID e sentido.
- Kanji Study confirma 読 no sentido de ler. O texto de 読む foi corrigido, pois descrevia a ação de apoiar. [*Volume*](https://dictionary.cambridge.org/pt/dicionario/learner-english/volume) mantém a intensidade sonora. O ID de *whom* preserva o estado de busca, com explicações locais sobre a função de objeto.
- Validação dos IDs, ordenação, prioridades, estados, camadas, contagens, tamanhos e hashes. Os 16 testes locais passaram.

### Lote 401–435

- 32 conceitos conferidos de `en:000000764` (page) a `en:000000933` (card), na sequência EN-US, PT-BR, JA e ZH e por ID e sentido. Três posições já estavam cobertas.
- Kanji Study conferida para 線, 通, 雨, 海 e 雪. [*Line*](https://dictionary.cambridge.org/dictionary/english/line) tem um ID para traço, `en:000000296` (linha, 線, 线), e um espelho para fila, `en:000004193` (fila, 行列, 队伍). O segundo foi acrescido depois da matriz e antes das pendências na ordem de estudo. As prioridades numéricas das 26 pendências avançaram uma posição em cada núcleo. *Pass* compartilha o sentido de passar por um lugar, com explicações locais sobre aprovação onde aplicável. A definição de *card* contempla peças de papel firme ou plástico.
- Mantidos IDs, sequências, estados, prioridades e camadas. Validados o XLS, os quatro pacotes e os hashes do catálogo. Passaram os 16 testes locais.

### Lote 436–470

- 32 conceitos conferidos na sequência EN-US, PT-BR, JA e ZH, com cruzamento por ID e sentido. Os sentidos de [*officer*](https://dictionary.cambridge.org/pt/dicionario/ingles/officer) e *ticket* foram desdobrados. Os IDs legados mantêm policial e ingresso. Os espelhos `en:000004194` e `en:000004195` correspondem a oficial das forças armadas e passagem de transporte terrestre, respectivamente.
- *Least* recupera a separação em relação ao ID de *at least*. *Single* mantém o sentido de único, separado do ID de solteiro. O ID de [*post*](https://dictionary.cambridge.org/us/dictionary/english/post) conserva o uso digital. O sentido postal em EN-US tem o verbete *mail* e o substantivo de poste tem um ID separado de *post*. O sentido informal de *funny* como estranho foi registrado no conceito existente de *weird*. A descrição de *feet* distingue a flexão inglesa dos usos sem marca de número de 足 e 脚.
- Mantidos os IDs, a sequência física e as classificações legadas. As prioridades das 26 pendências avançaram duas posições para acomodar os espelhos. Validados o XLS, os quatro pacotes, os hashes do catálogo e os 16 testes locais.

### Lote 471–505

- 32 conceitos conferidos na sequência EN-US, PT-BR, JA e ZH e cruzados por ID e sentido. O sentido de *lost* para objeto desaparecido reaproveita o conceito de *missing*. O sentido de *nice* para pessoa atenciosa reaproveita o conceito de *kind*. A saudação *excuse me* permanece no seu ID próprio e *excuse* fica com o sentido de justificativa.
- Quatro espelhos acrescentados, de `en:000004196` a `en:000004199`: *sale* como promoção, *remember* como trazer de volta à memória, *move* como mudar de residência e *ask* como pedir. Conferidas as formas do japonês e mandarim, incluindo [引っ越す](https://www.japandict.com/%E5%BC%95%E8%B6%8A%E3%81%99).
- Mantidos os IDs, ordem física e classificações anteriores. As prioridades das 26 pendências avançaram quatro posições. Validados o XLS, os IDs e os hashes do catálogo. Passaram os 16 testes locais.

### Lote 506–535

- 27 conceitos conferidos em EN-US, PT-BR, JA e ZH, com cruzamento por ID e sentido. Os sentidos de *fan* para fã, leque e ventilador ficam em verbetes distintos. *Form* como formato reaproveita o conceito de *shape*. *Living* como adjetivo reaproveita *alive*. O ID de *living* como sustento passou de 生活 a [生計](https://www.japandict.com/%E7%94%9F%E8%A8%88), com leitura e romaji atualizados.
- Três espelhos acrescentados, de `en:000004200` a `en:000004202`: *stay* como ficar hospedado, *heart* no sentido de sentimentos e *shower* no sentido de chuveiro. Mantidos os vínculos preexistentes.
- Validados os IDs, a ordem dos pacotes, o XLS, as classificações, os tamanhos e os hashes do catálogo. As prioridades das 26 pendências avançaram três posições. Os 16 testes locais passaram.

### Lote 536–600

- 61 conceitos conferidos em EN-US, PT-BR, JA e ZH e cruzados por ID e sentido. Foram reaproveitados os verbetes existentes de *plant* (instalação industrial), *application* (aplicativo), *glass* (copo de vidro), *square* (praça) e *date* (encontro). *Chance* e *site* reaproveitam os conceitos de possibilidade e local físico quando cabível.
- Criados quatro espelhos, de `en:000004203` a `en:000004206`: *clear* como transparente, *exchange* como intercâmbio estudantil, [*mobile*](https://dictionary.cambridge.org/pt/dicionario/ingles/mobile) como móvel e *ring* como toque. O ID de telefone usa a forma plena *mobile phone*.
- Validados os IDs, ordem dos pacotes, XLS, classificações, tamanhos e hashes do catálogo. As prioridades das 26 pendências avançaram quatro posições. Os 16 testes locais passaram.

### Lote 601–665 e retomada de sentidos legados

- 61 conceitos conferidos no intervalo em EN-US, PT-BR, JA e ZH. *Present* como presente e como tempo atual já tem IDs distintos. *File* fica no sentido de arquivo digital, com o verbete existente de *folder* para pasta.
- Seis espelhos novos, de `en:000004207` a `en:000004212`: *play* como jogar e como tocar instrumento, *star* como pessoa famosa, *fly* como viajar de avião, *oil* como petróleo e *serious* como grave. O ID anterior de *play* conserva o sentido de brincar.
- Quatro IDs históricos reativados após conferir que o vínculo como duplicata juntava sentidos diferentes: [*pass*](https://dictionary.cambridge.org/dictionary/english/pass) como passar numa prova (`en:000003962`) e entregar algo a alguém (`en:000003963`), *patient* como pessoa em tratamento (`en:000004010`) e *volume* como livro de uma coleção (`en:000004013`). Mantidos os IDs, prioridades e classificações dessas quatro entradas.
- Validados os IDs, ordem, XLS, classificações, tamanhos e hashes. As prioridades das 26 pendências avançaram seis posições. Os 16 testes locais passaram.

### Lote 666–695

- 29 conceitos conferidos em EN-US, PT-BR, JA e ZH nesse intervalo. A posição 678 já estava revisada. Também foram conferidos dois IDs posteriores relacionados a *platform* e *sign*.
- O ID de [*platform*](https://dictionary.cambridge.org/dictionary/english/platform) mantém o sentido ferroviário e a forma japonesa [ホーム](https://www.japandict.com/%E3%83%9B%E3%83%BC%E3%83%A0). Reativado o ID `en:000004027` para o sentido digital, com プラットフォーム e 平台, mantendo sua prioridade e classificações. Os sentidos de superfície elevada e programa político têm espelhos próprios.
- Outros espelhos separam *update* (novas informações e ato de atualizar), *lose* (perder uma disputa), *pick* (colher), *sign* (assinar), *pool* (sinuca), *safe* (cofre) e *writing* (texto produzido). O ID `en:000001977` de *sign* corresponde a indício, separado da placa. [*Holiday*](https://dictionary.cambridge.org/dictionary/english/holiday) fica em feriado no núcleo EN-US, com 祝日 e 法定节假日. *Vacation* já tem ID próprio.
- A Kanji Study foi consultada para 月, 髪, 選, 難, 靴, 聞, 払, 嵐, 章 e caracteres dos compostos afetados. Mantidas as camadas e a ordem relativa de estudo. Passaram os 16 testes do repositório, o validador do catálogo e as conferências da planilha, dos IDs e dos hashes.

### Lote 696–730

- 35 conceitos conferidos no intervalo em EN-US, PT-BR, JA e ZH. Também foram conferidos três registros posteriores, relativos a nota escolar, objeto perdido e carne de frango.
- Reativados os IDs históricos `en:000003937` para *lost* (objeto perdido) e `en:000004033` para [*chicken*](https://dictionary.cambridge.org/dictionary/english/chicken) (carne). Os IDs de *lost* para quem perdeu o caminho e de *chicken* para a ave conservam os sentidos próprios. *Mark* fica no sentido de marca física e o ID de *grade* foi delimitado ao desempenho escolar.
- *Rock* (música), *charge* (cobrar), *table* (tabela) e *sleep* (sono) já têm IDs próprios. Criados espelhos para *offer* (oferta), *note* (nota musical escrita), *visit* (visitar lugar), *network* (rede de contatos) e *charge* (acusar formalmente). [*Shall*](https://dictionary.cambridge.org/dictionary/english/shall) permanece no uso de convite. O futuro formal e o uso normativo foram registrados na planilha para decisão editorial.
- A Kanji Study foi consultada para 旅, 印, 寝, 眠, 建, 親, 箱, 訪, 鳥, 鶏, 痛, 岩, 話, 書 e outros caracteres dos compostos. Mantidas as camadas, os IDs, a ordem física e a prioridade relativa. Passaram os 16 testes, o validador do catálogo e as conferências da planilha e dos hashes.

### Lote 731–770

- 39 conceitos conferidos em EN-US, PT-BR, JA e ZH. A posição 766 permanece reservada por conter a grafia britânica *centre*.
- *Stream* (transmissão), *gas* (estado gasoso), *branch* (filial) e *sentence* (pena judicial) já têm IDs distintos. Os IDs da faixa revisada ficam em riacho, gasolina, galho e frase, respectivamente.
- Criados 12 espelhos, de `en:000004228` a `en:000004239`, para [*track*](https://dictionary.cambridge.org/dictionary/english/track) (faixa, trilha, via férrea e rastrear), *ahead* (futuro), *text* (texto escrito), *credit* (reconhecimento), *contact* (pessoa), *guest* (hóspede), *spend* (passar tempo), *button* (comando) e *counter* (bancada). As acepções de pintura e desenho preservam 絵 e 画 nas duas entradas, com as definições locais distinguindo os processos.
- A Kanji Study foi consultada para 川, 絵, 画, 文, 枝, 品, 客, 夫, 氷, 誤 e outros caracteres dos compostos. Passaram os 16 testes, o validador do catálogo e as verificações da planilha, dos IDs, das camadas e dos hashes.

### Lote 771–815

- 44 conceitos conferidos em EN-US, PT-BR, JA e ZH. A posição 812 já estava revisada. O ID de *letter* conserva letra do alfabeto, *degree* fica em unidade de medida e *tie* em gravata. Carta, diploma universitário e empate já têm IDs próprios.
- Criados 13 espelhos, de `en:000004240` a `en:000004252`, para *bathroom* (banheiro público), *seriously?* (pedido de confirmação), *burn* (lesão na pele), *ship* (despachar), *chest* (baú), *shipping* (valor do frete), [*cap*](https://dictionary.cambridge.org/dictionary/english/cap) (tampa e teto), *sweet* (afetuoso), *tie* (amarrar), *drink* (bebida) e *division* (separação e departamento).
- A Kanji Study foi consultada para 皿, 姉, 妹, 度, 印, 刷, 焼, 船, 胸, 着, 甘, 触, 飲, 割 e os demais caracteres pertinentes. Passaram os 16 testes, o validador do catálogo e as conferências da planilha, dos IDs, das camadas e dos hashes.

### Lote 816–875

- 59 conceitos conferidos em EN-US, PT-BR, JA e ZH, incluindo a reativação de `en:000002651` para *partner* em relacionamento amoroso. O ID de maior prioridade conserva *partner* como pessoa com quem se trabalha ou colabora. Retiradas as glosas de ano escolar do ID de nota escolar. O ano escolar já tem verbete próprio.
- *Arms* mantém um ID de busca para o plural anatômico e outro ID para armas. *Iron* mantém o metal em um ID e o ferro de passar em outro. *Bear* já tem o verbo aguentar, em ID próprio. *Ride* mantém a carona registrada como pendente no XLS.
- Criados 12 espelhos, de `en:000004253` a `en:000004264`, para *ride* (como passageiro), *worry* (preocupação), *smart* (dispositivos), *profile* (vista lateral), *enter* (inserir dados), *host* (apresentador), *fix* (estabelecer), *iron* (passar a ferro), *plane* (plano geométrico e plaina) e *quarter* (15 minutos e trimestre).
- A Kanji Study foi consultada para 場, 距, 受, 乗, 底, 腕, 引, 入, 石, 危, 鉄, 茶, 郵, 空, 熊 e outros caracteres pertinentes. Passaram os 16 testes, o validador do catálogo e as conferências da planilha, dos IDs, das camadas e dos hashes.

### Lote 876–930

- 57 conceitos conferidos em EN-US, PT-BR, JA e ZH, incluindo três posições posteriores. *Teach* já estava revisado.
- Reativados os IDs históricos `en:000004026` para [*exercise*](https://dictionary.cambridge.org/dictionary/english/exercise) (atividade de prática), `en:000004035` para *cream* (creme para a pele) e `en:000004036` para *orange* (cor). Os demais IDs mantêm exercício físico, creme de leite e a fruta.
- Criados sete espelhos, de `en:000004265` a `en:000004271`, para *exercise* (exercitar-se), *fault* (defeito), *display* (exposição e exibir), *novel* (inédito), *chat* (conversar por chat) e *index* (indicador numérico). O ID de *aircraft* passou a usar 航空器, que também abrange helicópteros e planadores.
- A Kanji Study foi consultada para 月, 芸, 術, 運, 動, 花, 画, 面, 責, 任, 塩, 泣, 枠, 索 e outros caracteres pertinentes. Passaram os 16 testes, o validador do catálogo e as verificações da planilha, dos IDs, das camadas e dos hashes.

### Lote 931–990

- 57 conceitos conferidos em EN-US, PT-BR, JA e ZH (posições 931–990; 934, 953 e 972 já revisadas). Retiradas glosas de outros sentidos: *tip* (gorjeta) ficou sem a acepção de dica, que tem ID próprio; *mouse* (animal) ficou sem o mouse do computador; *rice* (grão) ficou sem o arroz cozido. Em *paint*, o japonês passou a incluir 絵の具 e 塗料. Em *loud*, o chinês manteve 吵 com a nuance de incômodo.
- Criado o espelho `en:000004272` para *tap* (torneira): torneira, 蛇口, 水龙头. A Kanji Study foi consultada para 親, 米, 蛇, 口, 絵, 録, 描, 妊, 衝, 突 e 穏. Passaram os 16 testes, o validador do catálogo e as conferências de IDs, prioridades e hashes.

### Lote 991–1050

- 57 conceitos conferidos em EN-US, PT-BR, JA e ZH (posições 991–1050; 997, 1018 e 1027 já tratadas ou reservadas). *Collar* ficou no colarinho, pois a coleira tem ID próprio. *Tablet* ficou no computador, pois o comprimido tem ID próprio. *Gate* ficou no portão de cerca ou muro.
- Corrigido o lote anterior: o espelho de *tap* (torneira) criado em `en:000004272` duplicava o ID de *faucet* (`en:000003124`) e foi removido. No lugar, `en:000004272` passou a ser *gate* no aeroporto: portão de embarque, 搭乗口, 登机口. Em *sink*, o japonês passou a usar シンク, com 流し e 洗面台 como alternativas. Em *assignment*, o japonês passou a usar 課題, distinto de 宿題 (*homework*).
- A Kanji Study foi consultada para 襟, 門, 蛇, 口, 流, 洗, 課, 題 e 搭. Passaram os 16 testes, o validador do catálogo e as conferências de IDs, prioridades e hashes.

### Lote 1051–1110

- 57 conceitos conferidos em EN-US, PT-BR, JA e ZH (posições 1051–1110; 1061, 1093 e 1108 já tratadas). Em *earth*, o ID de maior prioridade ficou no planeta. Criado o espelho `en:000004273` para *earth* (solo): terra, 土, 泥土. O japonês de *bathtub* passou a incluir バスタブ e 湯船. As descrições de *guys* e *kids* foram escritas no idioma de cada verbete.
- A Kanji Study foi consultada para 土, 球 e 泥. Passaram os 16 testes, o validador do catálogo e as conferências de IDs, prioridades e hashes.

### Lote 1111–1170

- 57 conceitos conferidos em EN-US, PT-BR, JA e ZH (posições 1111–1170; 1128 e 1134 já tratadas). O ID `en:000001269` de *dream* passou a ensinar o sentido de desejo para o futuro (sonho, 夢, 梦想), pois o ID `en:000002493` já cobre o sonho durante o sono. Em *bright*, retirada a glosa de inteligente, que o japonês 明るい não cobre. *Hurt* passou a incluir sentir dor. O chinês de *lovely* passou a usar 美好, pois 可爱 já traduz *cute*.
- A Kanji Study foi consultada para 夢, 傷, 痛 e 偽. Passaram os 16 testes, o validador do catálogo e as conferências de IDs, prioridades e hashes.

### Lote 1171–1250

- 79 conceitos conferidos em EN-US, PT-BR, JA e ZH (posições 1171–1250; 1189 e 1207 já tratadas ou sem pendência). As descrições de *be*, *right*, *light*, *good*, *turn* e *of course* usavam exemplos em inglês e passaram a trazer exemplos no idioma de cada verbete. *Spoon* passou a incluir sobremesa e o ato de mexer.
- A Kanji Study foi consultada para 豚, 膝, 肘 e 箸. Passaram os 16 testes, o validador do catálogo e as conferências de IDs, prioridades e hashes.

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
