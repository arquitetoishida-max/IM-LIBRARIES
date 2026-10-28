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
