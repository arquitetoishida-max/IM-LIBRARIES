"""Artigos (singular,plural) dos substantivos do pt-BR-core-v2. Regras + listas de exceção revisadas à mão."""
import re, unicodedata
M,F,C='o,os','a,as','o/a,os/as'
MP,FP='os,os','as,as'
SKIP=set('''muitos vocês fumar onze doze treze quatorze quinze dezesseis dezessete dezoito dezenove trinta quarenta cinquenta
sessenta setenta oitenta noventa pop ex info muito pouquinho máximo mínimo'''.split())
# substantivos por palavra exata (primeira palavra), revisados
EXACT={
# -e feminino
**{w:F for w in '''parte noite mente morte série arte frente chance fonte chave base rede parede sorte pele espécie árvore superfície
ponte tarde neve tempestade corrente fase carne frase gangue torre sede greve equipe alface fome pirâmide semente enchente
hipótese gente classe aeronave febre ave estante catástrofe maré fé internet web mãe lei vez voz luz paz foz noz raiz flor dor cor
colher mulher nuvem ordem origem vovó maçã irmã manhã lã rã startup análise crise cal'''.split()},
# -e / outros masculino
**{w:M for w in '''nome time telefone clube filme presente interesse leste oeste norte sul parque sangue ataque estoque crime peixe café
volume esporte estresse limite acidente restaurante transporte leite pacote debate romance detalhe índice tanque basquete combate
golfe incidente sabonete tomate uniforme legume alarme poste corte dente tigre elefante lanche sorvete chocolate passaporte continente
trompete saxofone eclipse fertilizante reagente asteroide pronome recife caule regime empate chifre serrote cofre frete iogurte desfile
sanduíche bife refrigerante creme teste mestre leque arco-íris esconde-esconde andar jantar poder dever prazer colar par cachecol
sutiã talismã vice comitê karaokê bebê-x pé chá sofá chapéu troféu céu museu baú peru bambu táxi abacaxi açaí tsunami pai rei grau
homem jardim trem item rim álbum fim som garçom país mês deus lápis ônibus tênis gás inglês francês português japonês chinês atlas
oásis status campus nariz giz juiz xadrez arroz zíper link blog marketing software notebook tablet mouse design show site rock jazz
surf curry tofu futon udon lámen tempurá matchá mangá judô vôlei caratê kung habitat pH cupcake cheesecake shopping iene yuan diesel
câncer açúcar álcool ar mar sol bar lugar valor calor senhor amor computador professor diretor jogador autor trabalhador treinador
vencedor governador escritor ator fator setor morador editor interruptor senador consumidor cantor vapor comandante-x corredor cobertor
apontador marcador tambor programador curador investidor empreendedor seguidor ventilador terror elevador pôster contêiner repórter
caráter placar motor favor dólar interior equador apresentador hotel hospital papel tribunal nível casal sinal canal anel festival
jornal sal aluguel quintal painel metal perfil túnel combustível animal material total futebol fóssil mineral pinguim girassol
coral carnaval decimal moral natal plural litoral comercial celular militar vovô vapor zero baú'''.split()},
# comum de dois
**{w:C for w in '''presidente gerente agente assistente cliente paciente estudante representante comandante adolescente chefe hóspede fã
policial profissional jovem líder colega camarada democrata artista motorista dentista especialista cientista jornalista estilista
astronauta atleta turista guia gêmeo personagem ex-x indivíduo-x'''.split()},
# -a / -o com gênero fora da regra
**{w:M for w in '''dia mapa problema sistema programa tema clima planeta drama esquema diploma pijama cinema poema idioma telefonema cometa
guarda-chuva mapa-múndi quebra-cabeça pega-pega delta papa pirata pião'''.split()},
**{w:F for w in 'foto moto tribo libido'.split()},
# -ão
**{w:M for w in '''coração furacão pão avião cão chão irmão cidadão campeão capitão anfitrião dragão vilão verão feijão algodão botão balcão
cartão salão caminhão tubarão pulmão vulcão trovão alemão mamão limão macarrão sabão portão órgão'''.split()},
**{w:F for w in 'mão'.split()},
}
EXACT.update({**{w:M for w in '''ser pessoal bebê abril por capital-x príncipe vale e-mail final herói beisebol boné toque controle ciúme lótus
variável ph ciclone afluente atol poliéster náilon alicate predador pólen bem-estar oficial trimestre espanhol cachorro-quente aspirador
cartão-postal bilhete filhote dez'''.split()},
 **{w:F for w in 'saúde metade van amizade manchete planície fotossíntese higiene filial estrela-do-mar capital'.split()}})
EXACT['bebê']=C; EXACT['oficial']=C
SKIP.update({'si','deixar','pular','dez','por'})
EXACT.update({'quilograma':M,'prisma':M,'soba':M,'guarda':C,'moral':F,'ex':C})
SKIP.discard('ex')
ID_OVERRIDE={'en:000000373':M,'en:000001594':M,'en:000003642':M}
PLURAL_ONLY={'óculos':MP,'férias':FP,'juros':MP,'damas':FP,'finanças':FP,'bens':MP,'fones':MP,'fogos':MP,'pauzinhos':MP,'economias':FP,
 'compras':FP,'maneiras':FP,'mercadorias':FP,'estatísticas':FP,'estudos':MP,'direitos':MP,'dados':MP,'ações':FP,'valores':MP,'armas':FP,
 'tropas':FP,'gêmeos':MP,'luzes':FP,'pessoas':FP,'mulheres':FP,'vezes':FP,'homens':MP,'crianças':FP,'amigos':MP,'minutos':MP,'olhos':MP,
 'pais':MP,'coisas':FP,'milhas':FP,'pés':MP,'esportes':MP,'braços':MP,'filmes':MP,'cartas':FP,'roupas':FP,'sentimentos':MP,'soldados':MP,
 'artes':FP,'pernas':FP,'sapatos':MP,'flores':FP,'senhoras':FP,'autoridades':FP,'ferramentas':FP,'dentes':MP,'funcionários':MP,
 'graus':MP,'libras':FP,'ovos':MP,'dedos':MP,'cientistas':MP,'meninos':MP}

def strip_acc(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn')

def head(text):
    t=text.split('(')[0].strip()
    return t.split()[0] if t else ''

def articles_for(entry):
    return ID_OVERRIDE.get(entry.get('english_id')) or articles(entry.get('text') or '')

def articles(text):
    if not text or text[0].isupper() or text[0].isdigit() or text.startswith(('o ','a ','um ')): return None
    h=head(text).lower()
    if h=='não': h=text.split()[1].lower()  # "não ficção"
    if h in SKIP or h=='monte': return None
    if text.lower() in ('fones de ouvido','fogos de artifício','direitos humanos','pirâmides de gizé'): return MP if not text.lower().startswith('pir') else None
    if h in PLURAL_ONLY: return PLURAL_ONLY[h]
    if h in EXACT: return EXACT[h]
    # regras por terminação
    if re.search(r'(dade|tude|ção|são|stão|xão|idão|gião|nião|gem|ise|ice|eza)$',h): return F
    if h.endswith('ão'): return M
    if h.endswith('ã'): return F
    if h.endswith('o') or h.endswith('ô'): return M
    if h.endswith('a') or h.endswith('ó'): return F
    return 'REVIEW'
