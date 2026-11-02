# ISHIDA MULTILANG — Ordem consolidada para Claude (2026-10-28)

## Contexto confirmado no GitHub
- `v2/en-core-v2.json`: 2.517 entradas, versão 2.0.0, `status=editorial-reviewed`.
- `v2/pt-BR-core-v2.json`: 2.517 entradas, versão 2.0.0.
- `v2/ja-core-v2.json`: 2.515 entradas, versão 2.0.0; 703 entradas ainda têm classificação JLPT.
- Revisão editorial 2.0 descrita nos próprios pacotes: definições inglesas reescritas individualmente e traduções PT-BR/JA refeitas a partir dos sentidos selecionados; IDs não devem ser reciclados.
- Apesar da revisão, os pacotes ainda contêm `frequency.zipf` com `source=wordfreq` (2.420 entradas EN, 2.420 PT-BR, 2.418 JA), `license` e `sources` antigos apontando para Wiktionary/Kaikki, WordNet, Argos, wordfreq. O gerador antigo também menciona e utiliza essas fontes. **Eliminar dados derivados que não integram a biblioteca editorial própria**.
- EN e PT-BR têm 2 entradas a mais que JA. Conferir as ausências intencionais antes de forçar equivalências inadequadas.
- `v2/catalog.json` conserva dados de descoberta e hashes; toda alteração de pacote exige atualização coerente do catálogo.

## PRIORIDADE A — Biblioteca editorial independente
1. Tomar a revisão editorial 2.0 feita sob instruções do proprietário como base autoral do ISHIDA MULTILANG. Não recuperar definições antigas inferiores nem reconverter silenciosamente a partir de Wiktionary/WordNet.
2. Auditar o conteúdo final e o processo de geração. Remover dos pacotes editoriais as marcas de proveniência obsoletas `Wiktionary`, `Kaikki`, `WordNet`, `Argos Translate`, `CC BY-SA` **quando não existir mais material sob essas licenças**. A simples reescrita não comprova por si a ausência de todo conteúdo derivado: verificar a origem dos campos remanescentes; não falsificar proveniência.
3. Remover campos `frequency` importados do wordfreq, se não forem indispensáveis ao funcionamento. Substituir dependências por metadados editoriais VCU14 onde aplicável; **preservar** `vcu14_rank`, `environments`, `vcu14_status`, níveis didáticos, etiquetas, IDs, ordem e `english_id`.
4. Preservar referências didáticas **aproximadas** JLPT, HSK, CEFR e semelhantes. Não tratar níveis como certificação oficial. Se níveis forem derivados de bases externas que exigem atribuição, conservar apenas o crédito específico necessário à respectiva fonte. Não apagar níveis JLPT/HSK por causa da limpeza das antigas referências lexicográficas.
5. Identificar quais dados ainda dependem de pacotes de terceiros (inclusive transcrição/romaji, traços de kanji/hanzi, UI e fontes), mantendo os avisos de licença realmente aplicáveis aos *componentes*, sem atribuir automaticamente licença copyleft a todo o dicionário próprio.
6. Atualizar o *gerador*, os metadados `license`/`sources` e os documentos para que a próxima compilação não restaure textos, frequências ou créditos desatualizados.
7. Rodar testes de schema, IDs únicos, integridade, compatibilidade, download e restauração; atualizar versões, contagens, tamanho e SHA-256 em `v2/catalog.json`. Manter pacote anterior recuperável.
8. Informar exatamente quantas entradas e metadados foram alterados, e indicar pendências verificadas. Não usar checklist superficial como substituto da validação.

## PRIORIDADE B — Pendências funcionais do APK
1. Corrigir backup no Google Drive HTTP 403. Google Drive API já habilitada; OAuth externo em produção e escopo `https://www.googleapis.com/auth/drive.appdata` cadastrado. Solicitar consentimento e token do escopo correto, guardar em `appDataFolder`, restaurar e exibir erro HTTP real. Preservar backup local.
2. Busca por lupa durante preparação e **durante** qualquer sessão Cards: procurar simultaneamente no idioma nativo, de treino **e inglês**; escrita nativa, romanização e transliteração (ex.: mizu → 水); distinguir resultados e sentidos homógrafos por idioma; seleção coloca Card imediatamente na sessão, aberto/virado no lado pesquisado, com escolha de posição inicial/final/antes/depois na fila. **Nunca salvar automaticamente no grupo atual**: comando separado para salvar em qualquer grupo ou criar novo, e opção de não salvar. Persistir sessão, progresso e ordem.
3. Detectar bibliotecas pelo catálogo; cerca de 1 minuto após abrir app verificar versões/hashes, perguntar antes de atualizar quando houver mudança; não interromper sessão; nunca descartar dados pessoais ou biblioteca válida por falha de rede.
4. Interface de temas e subtemas `environments`/VCU14, permitindo múltiplos ambientes por palavra e formação de grupos sem limite arbitrário.
5. Frases/chamadas culturais contextualizadas por idioma, desligáveis, sem interromper treino.
6. Clique nas bandeiras superiores abre janela **Languages**: idioma nativo/estudo, inverter direção, instaladas/disponíveis, baixar e atualizar.
7. Clique no nome da biblioteca abre página de histórico/estatísticas de palavras e caracteres treinados.
8. Treino de escrita: pequeno pincel na parte inferior esquerda dos Cards japoneses/mandarins; popup sobre a sessão com X; sombra-guia configurável, ordem/traços, dicas, animar, limpar, repetir, próximo; guardar histórico/pontos sem inflar por repetições. Kanji e Hanzi inicialmente, arquitetura para Hangul em fase posterior. Preservar modo offline e licenças de bibliotecas efetivamente incorporadas.
9. Refinamento visual sem reescrever o que já funciona; preparar APK de teste e AAB futuro; planejar assinatura de produção sem quebrar atualizações dos usuários atuais.

## PRIORIDADE C — Backups, continuidade, monetização futura
1. Manter Quick Backup atual e acrescentar **Full Offline Backup** `.imbak` em arquivo único: configurações, grupos, progresso, biblioteca(s) locais, dados de escrita, manifesto de versões/hashes, sem tokens OAuth/senhas. Compactação e criptografia autenticada; chave/senha controlada pelo usuário; restauração offline transacional. Exportar tamanho e progresso.
2. Arquitetura para **três URLs de catálogo embutidas** no APK (principal GitHub, duas reservas configuráveis); tentar sucessivamente em falhas, validando SHA; manter último catálogo válido. Reservas podem ficar vazias até ativação.
3. Importação/exportação de dicionários e catálogo por arquivo local, sem depender de servidores.
4. Preparar (sem ativar cobrança) uma futura **licença Premium Vitalícia**: compra única, direito de usar funcionalidades contratadas por prazo indeterminado, validação offline persistente, restauração da licença e opção de pacote de preservação (APK compatível + backup completo). Não prometer suporte/servidores perpétuos. Quando houver venda, registrar precisamente quais recursos foram adquiridos.
5. Gratuidade presente é experimental: recursos gratuitos podem tornar-se pagos, limitados ou retirados; não anunciar gratuidade permanente. Direitos pagos, ofertas e obrigações legais não podem ser retirados retroativamente.
6. Proposta contratual de garantia adicional: disponibilização de instalador/bibliotecas **por pelo menos 12 meses após a última venda vitalícia**; após isso, preservação pelos backups do usuário. Rever redação final antes da venda. Não confundir duração vitalícia da licença com prazo de hospedagem.
7. Fornecimento alternativo de APK por download/e-mail, mantendo package ID, assinatura e versionCode compatíveis. Explorar preservação do instalador antes de mudanças na chave de produção.

## PRIORIDADE D — Jurídico e distribuição
1. Criar repositório/site público GitHub Pages para Termos, Privacidade, Exclusão de conta e Licenças, com atualização dos textos aprovados. Termos devem mencionar caráter experimental gratuito e plano vitalício futuro sem alegar que aceite suprime direitos legais. Hospedar políticas em URL pública.
2. Integrar **Settings → Legal & Privacy** com links. Implementar **Account → Delete Account** com via externa, exclusão dos dados do Firebase controlados pelo projeto e instruções sobre Drive; cumprir requisitos Google Play.
3. Confrontar Política de Privacidade com dados realmente coletados por Firebase/Auth/Drive/Firestore e backup; não afirmar funções ainda inexistentes como ativas. Preencher nome/razão social e e-mail de suporte quando fornecidos.
4. Inventariar licenças abertas efetivamente incluídas no APK (Flutter, SDKs, KanjiVG, Hanzi Writer, fontes etc.). Separar **software e dados de terceiros** do conteúdo editorial próprio. Não remover atribuições obrigatórias desses componentes.
5. Preparar informações Google Play e fluxo de 12 testadores/14 dias para conta pessoal nova conforme regras aplicáveis.

## PRIORIDADE E — Revisão comunitária futura de dicionários
1. Módulo opcional **Dictionary Improvements**: enviar proposta de correção por Card ou verbete, indicando idioma, ID, campo, valor original, valor proposto e justificativa.
2. Fila pública com versões, alternativas, votos únicos por usuário, prevenção de abuso, moderação e histórico. Não publicar diretamente por mera maioria: validação final e controle administrativo.
3. Aprovação cria atualização versionada dos pacotes e hashes do catálogo; rollback e trilha de proveniência; manter grupos/IDs dos usuários.
4. Firebase/Firestore somente se custos e regras permitirem; implementar após lançamento, sem impedir a publicação Android atual.

## Restrições gerais
- Preservar o que já funciona, inclusive backups e dados locais.
- Não pedir validação do usuário para cada palavra; automatizar auditoria objetiva.
- Não iniciar versão Apple/iOS, não implementar Hangul ainda e deixar o mascote/gatinho adiado.
- Produzir entregas verificáveis por commits, testes e APK instalável; comunicar somente o que realmente foi concluído e pendências concretas.

### Limites obrigatórios para contribuições comunitárias
- **Descrição/definição proposta:** máximo de **240 caracteres Unicode** por acepção, contados como caracteres visíveis (grapheme clusters), não bytes. Preferir texto curto e objetivo.
- **Tradução proposta:** máximo de **100 caracteres** por campo.
- **Exemplo de uso:** máximo de **160 caracteres** por exemplo, até **2 exemplos** por acepção.
- **Justificativa da correção:** máximo de **500 caracteres**; não é texto publicado no Card.
- Exibir contador `usados/limite` em todos os campos e impedir envio acima do limite. Validar também no backend para não aceitar requisições adulteradas.
- Se houver vários sentidos, abrir entradas/acepções separadas: **não ampliar o limite concatenando definições**. Não permitir anexos, HTML, links ou textos extensos em definições.
- Aplicar aos envios e edições comunitárias; não truncar silenciosamente definições já existentes na biblioteca. Interface e validação aceitam idiomas com caracteres combinados e ideogramas.

## Revisão futura — Sensibilidade do treino de escrita Kanji/Hanzi (28/10/2026)
- Teste real do usuário: treinador Kanji **funciona bem**, porém a validação dos traços está **excessivamente rígida**; pequenos desvios de posição/forma no toque são rejeitados, dificultando a aprendizagem em tela sensível ao toque.
- **Aumentar moderadamente a tolerância padrão** de reconhecimento para a prática inicial, sem deixar de avaliar o sentido e a sequência dos traços quando aplicável.
- Adicionar opção persistente em **Settings → Writing Practice → Stroke Recognition Sensitivity / Tolerância dos traços** (por exemplo: Estrita, Normal [padrão mais flexível], Flexível), com descrição simples e efeito imediato na validação.
- Se a biblioteca tiver controles diferentes para precisão geométrica, direção e sequência, priorizar tolerância geométrica; não desativar a verificação da sequência por acidente.
- Aplicar também ao Hanzi se usar o mesmo motor; preservar configurações em backups e não comprometer progresso/sessão atual.
- Incluir testes com dedo e stylus, incluindo traços curtos e caracteres complexos, para evitar aprovação indiscriminada.

## Revisão futura — Velocidade da animação dos traços Kanji/Hanzi (28/10/2026)
- Teste no celular: o botão **Play/Animate** executa a animação rápida demais (percebida como menos de meio segundo), impedindo observar a sequência dos traços.
- **Reduzir significativamente a velocidade padrão** para uma demonstração didática legível, com intervalo perceptível entre os traços e animação gradual de cada um.
- Adicionar em **Settings → Writing Practice → Animation Speed / Velocidade da animação** controle persistente, com pelo menos **Lenta / Normal (padrão) / Rápida**; permitir ajuste imediatamente sem sair do treino.
- A duração deve considerar o **número de traços** do caractere: não usar uma duração total fixa que comprima caracteres complexos; idealmente duração por traço e pausa breve entre eles.
- Permitir repetir o Play quantas vezes desejar; não mexer no progresso ou pontuação ao apenas assistir à animação.
- Aplicar ao Hanzi se compartilhar motor de animação, sem alterar a verificação dos traços.

## Revisão futura — Qualidade visual/caligrafia dos traços Kanji/Hanzi (28/10/2026)
- Relato de teste: Kanji funciona, pacote pequeno e download rápido, porém os traços são visivelmente **quadrados, grosseiros e feios**. Melhorar representação sem aumentar significativamente os downloads.
- Diagnóstico no código atual do APK (`ISHIDA-MULTILANG/lib/writing.dart`): `_StrokePainter` usa polilinhas de pontos normalizados em 0..1000, `lineTo` e largura fixa de ~48 unidades, inclusive na animação e no fantasma. Apesar de `StrokeCap.round` e `StrokeJoin.round`, a forma fica uniforme e grosseira. `lib/strokes.dart` pode continuar usando centerlines para reconhecimento: separar visualização e avaliação.
- **Prioridade:** substituir a visualização do caractere por curvas vetoriais com contorno de traço mais natural, variável na espessura, pontas/terminações corretas e antialiasing. Preferir usar caminhos SVG originais de KanjiVG para a visualização onde disponíveis, preservando metadados de ordem, e, em Hanzi, contornos `strokes` nativos de Hanzi Writer; nunca extrapolar automaticamente curvas malformadas a partir de amostras muito grosseiras.
- Manter as centerlines/polilinhas existentes para checagem de ordem/sensibilidade, sem regressão. Sincronizar a animação com o novo desenho sem perder sequência. Testar formas em caracteres simples e complexos, em diferentes tamanhos e densidades Android.
- Opcional: oferecer aparência **Natural (padrão)** e **Traçado simples** nas preferências do treino. Preservar velocidade/tolerância configuráveis já solicitadas.
- Avaliar tamanho extra real do pacote, cache e licenças dos dados vetoriais; manter disponibilidade offline, sem dependência de CDN. **Não trocar todo o motor por solução pesada sem necessidade**.

### Decisão visual do proprietário — ESTILO PINCEL PRIORITÁRIO (28/10/2026)
- O usuário **prefere explicitamente a aparência caligráfica de pincel japonesa (kaisho)** mostrada como exemplo à direita, e rejeita a atual representação de “boneco de palito”: poucas amostras, segmentos retos unidos e pontas arredondadas.
- Alterar a meta do item anterior: **estilo pincel/kaisho é o alvo e padrão**, não somente pequenas melhorias cosméticas. Curvas realmente suaves, largura variável e terminais orgânicos; não simular com apenas `quadraticBezierTo` em poucos nós e espessura fixa.
- Inspecionar os dados: KanjiVG fornece essencialmente trajetórias/ordem dos traços, não necessariamente contorno caligráfico completo. **Não prometer fidelidade idêntica a fotografia de pincel com os centerlines atuais**. Para visual bonito, usar fonte japonesa de estilo escolar/kaisho licenciada e máscaras de revelação por traço, ou gerar geometria variável de largura com suavização suficiente; para chinês priorizar contornos vetoriais de `Hanzi Writer` quando disponível. Selecionar técnica por qualidade, desempenho e licenças.
- Separar sempre **motor geométrico de reconhecimento** (pontos/sensibilidade/ordem) do **renderizador estético**. A animação Play deve revelar progressivamente os traços caligráficos, em vez de simplesmente alongar um segmento tubular uniforme.
- Testar visualmente antes/depois com kanji simples e complexo e confirmar que o resultado realmente parece escrita japonesa tradicional escolar de pincel, não hastes retas com bolinhas. Manter dados offline e tamanho de download razoável. Se for impossível obter fidelidade total com a fonte de dados atual, priorizar a melhor aproximação perceptível e registrar limitações concretas.

### Escolha visual definitiva — japonesa/chinesa versus coreana (28/10/2026)
- O proprietário **retificou a preferência anterior por pincel forte/kaisho muito bold**. A referência aprovada é **a imagem da ESQUERDA do último par mostrado**: traçado japonês intermediário entre técnico e caligráfico, visual limpo, elegante, leve, legível, com linhas curvas suaves e terminações discretas — **não** o pincel grosso, preto e carregado da direita, nem o atual esqueleto poligonal de linhas retas.
- Aplicar esse estilo **a japonês (kanji) E chinês (hanzi)**, de maneira coerente. Espessura moderada, curvatura natural, geometria escolar refinada, não caligrafia pesada.
- Para **coreano (hangul)**, em fase posterior, preferir estilo **técnico/geométrico limpo**, com traços mais regulares e cantos cuidadosamente desenhados; não forçar estilo pincel japonês/chinês. Não implementar Hangul agora.
- A referência visual da imagem é orientação estética; recriar resultado por renderização vetorial adequada, mantendo ordem/animação, reconhecimento e compatibilidade offline. Testar visualmente caracteres japoneses e chineses simples e complexos. **Esta decisão prevalece sobre a instrução anterior de pincel forte como padrão.**

## Revisão futura — STT mandarim indisponível + mensagem cortada (28/10/2026)
**Teste do usuário no Android:** reconhecimento de voz em mandarim mostra “Idioma não disponível no reconhecimento de voz do Android”, e a mensagem de retorno aparece com a segunda linha parcialmente cortada.

**Diagnóstico confirmado no código atual do app:**
- `ISHIDA-MULTILANG/lib/study.dart`, `listen()`: após `speech.locales()`, compara `locale(target)` (esperado `zh-CN`) com `localeId` normalizado, depois busca prefixo linguístico; se nenhum corresponder, retorna mensagem e não inicia captação. É erro de disponibilidade/anúncio do mecanismo STT instalado, **não prova incapacidade geral do Android para mandarim**.
- `lib/cards.dart` linha aproximada 221: mensagem `Text(feedback, maxLines: 2, overflow: TextOverflow.ellipsis, fontSize:12)`; verificar também as restrições verticais do contêiner, pois o usuário vê apenas parte da segunda linha.

**Ajustes pedidos:**
1. Mapear corretamente BCP-47 e variantes do mandarim: `zh-CN`, `zh_CN`, `cmn-Hans-CN` e variantes `zh`/ `cmn` efetivamente anunciadas. Não confundir automaticamente `zh-TW` com `zh-CN` sem explicar a diferença.
2. Verificar disponibilidade do mecanismo Android/Google Speech Services e idioma solicitado; diagnosticar no app se o idioma não está instalado/ativado ou se o reconhecedor não o oferece. Oferecer mensagem clara e atalho/ajuda de configuração; não presumir nem inventar instalação automática do idioma. Solicitar permissões necessárias.
3. Preservar funcionamento de outros idiomas; se STT nativo não oferecer mandarim, apresentar alternativa segura ou configurar motor STT local/offline compatível como melhoria opcional, avaliando tamanho e licenciamento, sem bloquear a sessão.
4. Remover o truncamento de feedback e permitir mensagem **integral**, com texto multilinha, contêiner expansível ou rolável e padding suficiente; não cortar meia altura da segunda linha. Garantir boa visualização em celulares menores, fontes maiores e orientação diversa.
5. Testar com aparelho que tenha e que não tenha STT mandarim disponível, inclusive erro de rede e falta de permissão; manter microfone, feedback, sessões e backup funcionando.

## Próxima revisão — Card deve sempre entrar na direção definida pelas bandeiras (30/10/2026)
**Relato do proprietário (teste no Android, visto em chinês; provavelmente todos os idiomas):** ao passar para o próximo card, ele às vezes já entra **virado** (mostrando o verso). O card está “lembrando” o lado em que foi deixado.

**Regra pedida:** todo card que entra na tela começa **sempre na frente**, isto é, no idioma que está por cima na ordem das bandeirinhas do topo (ex.: sempre português → outro idioma, ou sempre outro idioma → inglês). O card **não guarda memória** do lado em que foi deixado. Para estudar ao contrário, o usuário usa o botão das bandeiras (inverter direção), que vale para todos os cards seguintes.

**Diagnóstico no código atual (`ISHIDA-MULTILANG/lib/study.dart`):**
- `navigate()`: grava `faces[pos] = revealed` ao sair do card e, ao chegar, aplica `revealed = faces[pos]` — ao voltar e avançar pelo histórico, o card reaparece virado.
- Troca de par de idiomas / retomada de sessão (`sessions[...]['faces']`, ~linha 352): restaura `revealed` a partir de `faces[pos]`, então um card pode abrir virado ao reabrir o app.
- Cards inseridos pela busca (`revealFor(lang)` em `navigation.dart` / `faces.add(... revealFor(...))`): abrem virados quando o termo foi pesquisado no idioma de trás. Isso foi pedido antes (“aberto no lado pesquisado”); decidir na revisão se vale **só no momento da inserção (“Mostrar agora”)** e nunca depois, para não conflitar com a regra acima.

**Correção prevista:** ao exibir qualquer card (avançar, voltar, retomar sessão, trocar idiomas), definir `revealed = false`; deixar de usar `faces` para restaurar o lado (pode continuar existindo só para compatibilidade de backups). Opcional, desligado por padrão: preferência “Lembrar o lado de cada card”. Testar avançar/voltar, retomar após fechar o app, inverter bandeiras no meio da sessão e cards vindos da busca, em pelo menos zh, ja e en.

## Próxima revisão — Frases faladas durante a lição (Laboratório de vozes → função real) (30/10/2026)
**Situação atual:** existe a aba *Laboratório de vozes (teste)* (`ISHIDA-MULTILANG/lib/voicelab.dart`, `assets/voice_lab/lab.json` + clipes `.m4a` Kokoro-82M, 8 frases f01…f31 em en/ja/pt-BR, vozes mother/father/sister). Ali só se ouve a frase apertando *play*; **não está integrado ao treino**.

**Pedido do proprietário:** durante a sessão de Cards, de tempos em tempos, o app **fala uma frase simples** no idioma estudado, de forma aleatória e não previsível.
1. **Intervalo aleatório configurável:** o usuário define um mínimo e um máximo de cards (ex.: 25 a 30). Após cada frase, sorteia-se um número inteiro nesse intervalo; quando o contador de cards chega a ele, toca uma frase sorteada (sem repetir as recentes). Opção liga/desliga (padrão a decidir; antes a ordem era “não interromper o estudo normal” — agora o proprietário pede a função, então ela deve ser opcional e configurável).
2. **Sem bloquear o treino:** a frase toca e aparece **suspensa no topo** (faixa/“balão” discreto, como as chamadas culturais) sem abrir diálogo nem pausar a sessão. Não tocar se o microfone estiver gravando ou outro áudio/TTS estiver tocando; esperar o próximo card.
3. **Interação com a frase suspensa:** tocar nela → **replay** do áudio; mostra o **texto** no idioma estudado (com leitura/pinyin/romaji quando houver) e a **tradução** no idioma nativo. Botão fechar. A frase some no card seguinte ou ao fechar (decidir; manter acessível ao menos até o próximo card).
4. **Frases simples e graduadas:** gerar **mais frases**, curtas e do dia a dia, para cada idioma estudado (ja, zh, en, pt-BR e os demais conforme haja voz). Classificar por **nível** (ex.: 1 = 2–4 palavras muito comuns; 2 = frases curtas com verbos básicos; 3 = frases com conectores). Usar de preferência palavras que o usuário **já treinou** (scores/viewed) para que entenda; o nível padrão pode seguir o progresso (quantidade de palavras estudadas/dominadas), com **configuração manual de nível** nas preferências.
5. **Áudio:** usar clipes pré-gerados offline quando existirem (Kokoro, como hoje; sem clonagem de voz, sem serviço pago) e, para frases sem clipe, o TTS do aparelho. Frases e traduções revisadas editorialmente, ligadas aos ids dos dicionários quando possível; pacote separado (ex.: `v2/phrases/<lang>-phrases.json` no catálogo) para não inflar o APK.
6. **Configurações (Opções → Frases durante a lição):** ligar/desligar, mínimo e máximo de cards, nível (automático/1/2/3), voz preferida, mostrar tradução automaticamente ou só ao tocar. Persistir no perfil e no backup.
7. **Integração:** reaproveitar a faixa das chamadas culturais (`lib/community.dart`, `culturalStrip`) ou unificar as duas num mesmo espaço no topo, sem empilhar faixas. Não mexer em progresso, pontuação nem ordem dos cards.
8. **Testes:** intervalo aleatório dentro dos limites (teste unitário), não repetir frase recente, não tocar durante gravação, replay/tradução, idiomas com e sem clipes, e funcionamento offline.

## Nota de teste — Hanzi: velocidade da animação (02/11/2026)
- Usuário testou o treinador **Hanzi (chinês)** e constatou que a animação Play está **aproximadamente 3 vezes mais rápida do que gostaria**.
- **Ação pendente, não executar nesta anotação:** reduzir a velocidade padrão de animação do Hanzi para **1/3 da atual** (duração de cada traço ~3x maior), com pausa perceptível entre traços. Não confundir velocidade com atraso inicial.
- Integrar com a tarefa anterior de configuração persistente **Settings → Writing Practice → Animation Speed** (Lenta / Normal / Rápida), aplicável a Kanji e Hanzi; preservar ordem dos traços e controles do treino.
- Validar visualmente com caracteres simples e complexos, mantendo duração por traço e sem afetar pontuação.
- Esta nota **soma-se às demais correções pendentes do treinador**: tolerância configurável, melhoria visual dos traços para japonês e chinês, ajuste da animação do Kanji, e às outras pendências no documento. **Não marcar nenhuma como concluída sem testar.**

## Situação em 02/11/2026 — APK v0.9.113 (compilado no CI; testes automáticos aprovados; NÃO testado no aparelho)
Implementado nesta versão (aguarda teste do proprietário):
- **Card sempre entra pela frente** (idioma de cima nas bandeiras): `revealed = false` ao avançar, voltar, retomar sessão ou trocar idiomas; o lado de cada card não é mais lembrado. Card vindo da busca com “Mostrar agora” ainda abre no lado pesquisado só nesse momento.
- **Frases durante a lição:** liga/desliga (padrão ligado), intervalo sorteado entre mínimo e máximo de cards (padrão 25–30, ajustável 5–80), nível Auto/1/2/3 (Auto pelo nº de palavras com nota ≥ 4), 35 frases simples em pt-BR/en/ja/zh (leitura kana/pinyin) + as frases do laboratório com clipes Kokoro em en/ja/pt-BR; toca ~2 s após o card (não toca gravando nem se o card mudou), fica numa faixa no topo (mesma das chamadas culturais), toque = leitura + tradução, botão de replay e fechar. Banco embutido no app (pequeno); pacote baixável separado fica para quando houver mais frases.
- **Opções:** nova linha “Idiomas de estudo” com a bandeira do idioma alvo, logo abaixo do rigor do reconhecimento e antes de Dicas, abrindo a mesma janela das bandeiras; “Adicionar idioma” removido da lista (está dentro de Idiomas); linhas divisórias entre todas as configurações de primeiro nível; ícones coloridos.
- **Animação Kanji/Hanzi ~3× mais lenta** em todas as velocidades (Normal: ~2,5 s por traço + 0,65 s de pausa; Lenta ~3,6 s; Rápida ~1,3 s).

Ainda pendente (depende de teste ou do proprietário): teste no aparelho de tudo acima e das versões 0.9.110–0.9.112 (mandarim no microfone, treino de escrita, backup completo, arquivo único de backup); Drive HTTP 403 (enviar o texto de “Detalhes do último erro” se ocorrer); site jurídico (caminho da exclusão de conta “Opções → Legal e privacidade → Excluir conta e dados”, menção a MyMemory e reconhecimento de voz na privacidade, pasta `temp`); tradução revisada da interface em chinês; fila pública Firestore das sugestões (pós-lançamento); applicationId e chave de produção para o Google Play.

## Teste v0.9.113 (02/11/2026) — direção dos cards e seta das bandeiras: NÃO resolvido
**Relato do proprietário:** os cards continuam entrando **invertidos**, mostrando primeiro o idioma alvo em vez do nativo. A prioridade deve **sempre seguir a ordem das bandeiras** no topo. Além disso, o topo mostra uma **seta do idioma alvo apontando de volta para o nativo**, o que não faz sentido para quem fala o nativo e aprende o alvo.

**Diagnóstico no código (`ISHIDA-MULTILANG/lib/main.dart`):**
- O topo desenha sempre `bandeira nativa`, depois a seta, depois `bandeira alvo`; quando `reversed = true` a seta vira `arrow_back` (← ). Ou seja, as bandeiras **não mudam de lugar** ao inverter; só a seta muda. A frente do card segue `srcL` (`reversed ? studyL : nativeL`), então com `reversed = true` o card abre no idioma alvo enquanto a bandeira nativa continua à esquerda — exatamente o que o usuário viu.
- `reversed` é persistido e pode ter sido ligado pelo botão ⇄ do cabeçalho do card ou pelo interruptor “Inverter direção” na janela Idiomas; a correção da v0.9.113 (`revealed = false`) só garante a frente do card, não a direção.

**Correção pedida:**
1. O topo mostra as bandeiras **na ordem real de estudo**: à esquerda o idioma da frente do card (`srcL`), à direita o do verso (`tgtL`), sempre com seta **→** (da esquerda para a direita). Inverter a direção **troca as bandeiras de lugar**, sem seta para trás.
2. A frente de todo card = bandeira da esquerda. Sem exceções ao avançar, voltar, retomar sessão ou trocar idiomas.
3. Revisar todos os lugares que mostram a direção (cabeçalho do card ⇄, janela Idiomas “Inverter direção dos cards”, linha “Idiomas de estudo” em Opções) para usarem a mesma representação `frente → verso`.
4. Avaliar se a direção padrão ao escolher um novo par deve ser **nativo → alvo** (reversed = false) e se a inversão deve ser lembrada por par de idiomas; não deixar um estado invertido antigo “escondido”.
5. Testar: abrir o app, avançar/voltar cards, inverter pelas bandeiras, inverter pelo botão do card, trocar idioma de estudo, fechar e reabrir — em zh, ja e en.

### Complemento do proprietário (02/11/2026, 14:00)
- Regra confirmada: bandeira do **nativo à esquerda**, **alvo à direita**, seta **→ apontando para o alvo**. A leitura automática (voz) é sempre do idioma alvo — está correta. Os cards **pararam de girar com o histórico** (correção da v0.9.113 aprovada).
- Logo depois, o proprietário relatou que “agora está funcionando certo” na v0.9.113 (provavelmente após desfazer a inversão salva). Manter a regra acima como referência para testes.
- Já enviado (commit `ee5c8e0`, v0.9.114 em compilação): o topo passa a mostrar as bandeiras na ordem real `frente → verso` (sem seta para trás; inverter troca as bandeiras de lugar); a inversão salva é zerada uma vez na atualização; trocar o par de idiomas volta para nativo → alvo. Com a direção normal, o topo fica idêntico ao descrito pelo proprietário.

### Direção invertida: começo limpo e aviso visual forte (02/11/2026, 14:04)
**Causa provável confirmada pelo proprietário:** a inversão tinha sido ligada sem querer pelo botão ⇄ do cabeçalho do card e ficou salva da sessão anterior.
1. **Começar sempre resetado:** ao configurar pela primeira vez um par nativo/alvo (ou trocar qualquer um dos dois), a direção começa **nativo → alvo** (sem inversão). A inversão continua possível, mas nunca deve “vir de herança” de outra sessão/par. *(Já incluído no commit `ee5c8e0` / v0.9.114: `switchLanguages` zera `reversed` e há um reset único na atualização — confirmar no teste.)*
2. **Indicativo dramático quando invertido:** além das bandeiras trocarem de lugar, a **barra superior inteira inverte as cores** enquanto a direção estiver invertida — o fundo (hoje claro/branco, onde fica o nome do login) passa a usar a cor escura/de destaque do tema e os textos/ícones (nome do login, bandeiras, engrenagem) ficam claros. Opcional: o contorno do card também muda de cor. Ao desinverter, tudo volta ao normal. Deve funcionar em todos os temas (inclusive escuro: usar contraste invertido do próprio tema) e ser perceptível de relance.
3. Testar: inverter pelo ⇄ do card, pela janela Idiomas e trocar o par; fechar e reabrir o app; conferir a barra em temas claro e escuro.

### Bandeiras do topo × botão de inversão (02/11/2026, 14:05)
- **Decisão do proprietário:** são duas coisas diferentes. As **bandeiras do topo** representam o **par de idiomas** (nativo à esquerda × alvo à direita, seta → para o alvo) e **não se invertem**. A **inversão** (normal × invertido) aparece no **mini botão ⇄ do cabeçalho do card**, cujas bandeirinhas trocam de lugar.
- Código ajustado (commit após `ee5c8e0`): o topo voltou a mostrar sempre nativo → alvo, agora com a seta **sempre →** (sem a seta para trás). A linha “Idiomas de estudo” das Opções mostra o par nativo → alvo. Mantidos: reset da inversão ao trocar o par e reset único na atualização.
- O aviso forte de “invertido” continua sendo a **inversão de cores da barra superior** (item anterior), a implementar.

### Idioma nativo não deve aparecer como idioma estudado (02/11/2026, 14:10)
- **Regra do proprietário:** o idioma **nativo nunca entra como idioma estudado** (estatísticas, “Seus idiomas”, listas de progresso, seleção de cursos etc.). **Exceção:** se a pessoa, em algum momento, escolheu esse idioma como **idioma de estudo (alvo)**, praticou e há progresso salvo nessa direção, aí ele pode aparecer como estudado (com os dados daquela prática).
- **Onde verificar (`ISHIDA-MULTILANG/lib/account.dart`, `languageStats()`):** hoje o idioma de cada nota é deduzido da chave `id:origem:destino` (`lang = src == nativeLang ? tgt : (tgt == nativeLang ? src : tgt)`), e `viewed` também é contado por idioma; há tratamento especial `s.lang.code == nativeLang` para “disponíveis”. Com cards invertidos (alvo → nativo) ou trocas de nativo, o nativo pode acabar listado como idioma estudado.
- **Correção prevista:** contar um idioma como estudado somente quando ele foi o **idioma de estudo** (`studyLang`) da sessão/nota — independentemente da direção do card (normal ou invertida, o idioma estudado é o alvo do par). O nativo atual só aparece se houver notas/vistos registrados com ele como `studyLang` em algum par anterior. Revisar também outros lugares que listam idiomas estudados (janela Idiomas, página da biblioteca, backup/estatísticas de escrita).
- Testar: estudar pt→zh normal e invertido (nativo não aparece), depois escolher pt como alvo de outro nativo e praticar (pt aparece com os dados dessa prática).

### Treino de escrita: barras deslizantes para velocidade e tolerância (02/11/2026, 14:12)
- **Velocidade da animação:** o proprietário pede animação **3 a 6 vezes mais lenta** (referência: versão anterior à v0.9.113). Na v0.9.113 já entrou ~3× (Normal ≈ 2,5 s por traço + 0,65 s de pausa); confirmar no teste e ampliar a faixa para chegar a ~6×.
- **Trocar os 3 estados por barras deslizantes** (Opções → Treino de escrita e ajustes dentro do treino):
  - **Velocidade:** slider contínuo, do mais lento (~6× a referência antiga: ≈ 5 s por traço) ao mais rápido (~1,3 s por traço), padrão no meio-lento (~3×); pausa entre traços proporcional. Mostrar o valor (ex.: “2,5 s por traço”).
  - **Tolerância:** slider contínuo de Estrita a Flexível (leniência ≈ 1,0 a 2,0), padrão ≈ 1,35; ordem e direção continuam sempre conferidas.
  - Migrar os valores salvos dos 3 estados para o slider (strict/normal/flexible e slow/normal/fast → posições equivalentes); persistir no perfil e no backup; efeito imediato no treino.
- Aplicar a japonês e chinês. Testes unitários: limites do slider, migração dos valores antigos, duração por traço crescente com o comprimento.
- **Confirmação no teste da v0.9.113 (02/11, 14:12):** a animação de kanji/hanzi **ainda está muito veloz**. Reduzir **mais 3 a 6×** em relação à v0.9.113 (ou seja, Normal passa de ≈ 2,5 s para ≈ 7,5–15 s por traço?). Atenção: se a percepção de “rápido” vier de outro fator (ex.: o controlador animar o caractere inteiro numa duração única, a animação não usar o agendamento por traço, ou o Play reiniciar), **conferir no código antes de só multiplicar os tempos**. Faixa do slider a definir no teste: do mais lento ≈ 15 s por traço ao mais rápido ≈ 2 s, padrão perto de 6–8 s, pausa entre traços proporcional.
- **Sem migração (02/11, 14:13):** não é preciso converter os valores salvos dos 3 estados para os sliders — ainda não há usuários. Usar novas chaves com o padrão novo e ignorar as antigas. (Regra geral nesta fase: migrações de configurações só quando houver usuários; dados de estudo e backups continuam protegidos.)
- **Meta definida pelo proprietário (02/11, 14:14):** no **Normal**, cada traço leva **0,3 a 0,9 s conforme a complexidade** (comprimento/curvas do traço), **média ≈ 0,6 s**; o slider escala esses tempos para mais lento/mais rápido. Pausa curta entre traços.
- **Inconsistência a investigar antes de ajustar:** pelos números do código, a v0.9.113 já deveria animar a ≈ 2,5 s por traço no Normal (bem **mais lento** que a meta), mas o proprietário a percebe como **muito rápida**. Logo, o tempo programado provavelmente **não está sendo aplicado**: verificar se o aparelho está mesmo na v0.9.113 (Opções → Sobre), se `animate()`/`animationSchedule()` estão em uso pelo pintor durante o Play, se a duração do `AnimationController` está correta, e se há escala de animação do sistema (Opções do desenvolvedor → escala de duração do animador) afetando. Medir no aparelho o tempo real de um caractere com N traços antes e depois da correção.
- **Slider de velocidade (02/11, 14:14):** o valor **Normal (0,3–0,9 s por traço, média 0,6 s) fica no meio da barra**; para um lado fica mais lento, para o outro mais rápido (ex.: extremos ≈ 3× mais lento e ≈ 3× mais rápido que o Normal). O padrão inicial é o meio.
