from firebase import firebase
 
 
firebase = firebase.FirebaseApplication('https://fakenews-app-d59dc.firebaseio.com/', None)
data1 =  { 'id_noticia': '1',
		  'noticia': 'O Novo Banco vai pedir ao Fundo de Resolução 1.037 milhões de euros por conta dos resultados de 2019. Em três anos, o banco que nasceu do fim do BES já foi buscar ao Mecanismo de Capital Contingente quase 3.000 milhões. Os resultados do Novo Banco referentes a 2019 vão ser apresentados na próxima sexta-feira [amanhã, dia 28 de fevereiro], mas um dos acionistas já revelou qual a fatura que será passada ao Estado. O banco que nasceu do fim do BES vai pedir ao Fundo de Resolução 1.037 milhões de euros, elevando para 2.978 milhões de euros o valor total injetado no Novo Banco ao abrigo do Mecanismo de Capital Contingente entre 2018 e 2020. O Bloco de Esquerda destaca que já há um \'buraco de 400 milhões\' no Orçamento do Estado (OE) para este ano.',
          'titulo': 'Centeno garantiu que não haveria injeção no Novo Banco acima do previsto no OE2020',
          'classificacao': 'true',
          'data': '27/02/2020',
          'Emotion': '26',
          'Subjectivity': '46',
          'Affectivity': '50',
          'Polarity': '44',
          'BP': '62',
          'source': 'Jornal Público',
          'verified': 'yes'
          }

data2 =  { 'id_noticia': '2',
		  'noticia': 'O PS não quer lembrar o seu próprio passado, porque levantou esta questão [do IVA da eletricidade] contra o Governo da troika. E bem. Que é: a passagem do IVA da taxa mínima para o valor dos 23% foi sempre entendida como provisória e excepcional para aquele período de aperto económico. Portanto é natural, como agora saímos da austeridade, entre aspas, é natural que haja maior maleabilidade para regressar a soluções de maior normalidade, principalmente discriminando positivamente quem tem menos recursos',
          'titulo': 'Aumento do IVA da eletricidade em 2011 foi uma medida "provisória" no âmbito do memorando da "troika"',
          'classificacao': 'true',
          'data': '06/02/2020',				
		  'Emotion': '59',
          'Subjectivity': '55',
          'Affectivity': '49',
          'Polarity': '43',
          'BP': '56',
          'source': 'TVI24',
          'verified': 'yes'
          }

data3 =  { 'id_noticia': '3',

		  'noticia': 'Bolsonaro é o terceiro governante mais popular do mundo nas redes sociais Quem segue na dianteira no ranking é o indiano Narendra Modi. Donald Trump, presidente dos EUA, aparece na segunda colocação O presidente Jair Bolsonaro é o terceiro chefe de governo mais popular do mundo nas redes sociais. O levantamento é do Estadão, elaborado pela consultoria Quaest. Foram analisados perfis de 18 líderes mundiais a partir das métricas de uso do Instagram, Twitter e Facebook. Nesse sentido, criou-se o Índice de Popularidade Digital (IPD), de 0 a 100. O período de análise foi de janeiro de 2019 e janeiro de 2020. Quem segue na dianteira no ranking é o indiano Narendra Modi, com 64,25 no IPD. Donald Trump, presidente dos EUA, aparece na segunda colocação, com 62,27. Jair Bolsonaro em terceiro, com 52.75. Outras duas figuras são Recep Tayyip Erdogan, da Turquia, com 44,65. No top 5 está Cristina Kirchner, da Argentina, com 32,48.',
          'titulo': 'Bolsonaro é "o terceiro governante mais popular do mundo nas redes sociais"',
          'classificacao': 'true',
          'data': '18/02/2020',				
		  'Emotion': '33',
          'Subjectivity': '43',
          'Affectivity': '46',
          'Polarity': '35',
          'BP': '47',
          'source': 'Facebook',
          'verified': 'no'
          }

data4 =  { 'id_noticia': '4',
		  'noticia': 'SERA VERDADE???? Custa-me a acreditar numa coisa destas mas… Sem comentários, reencaminho como recebi, e como não é anónimo, teve a coragem de se identificar Lojas Chinesas - DIVULGUEM Isto é verdade pois já me tinham dito pessoalmente acerca da loja de Águeda. O estranho é não fecharem as lojas! Olá! Gostaria de partilhar convosco alguns episódios que me relataram e que de facto são impressionantes. Há algumas semanas atrás, numa loja de Chineses em ÁGUEDA: O pai deixou a filha à porta da loja porque de certo ela tinha alguma compra a fazer nesse estabelecimento e aguardou por ela no estacionamento dentro do carro. Após bastante tempo de espera, resolveu entrar na loja à procura da sua filha mas não a conseguiu encontrar lá dentro. Questionou alguns funcionários da loja que afirmavam não a terem visto, teimou de tal forma que a filha tinha entrado para a loja ao ponto de chamar a polícia, os polícias entraram e também não encontravam a jovem até que por fim chamaram reforço de colegas com cães-polícia que, através do seu faro, conseguiram detectar a presença da jovem numa zona mais retirada da loja dentro de um alçapão. A jovem já tinha o corpo marcado perto de alguns órgãos vitais e o destino dela seria ser MORTA PARA TRÁFICO DE ÓRGÃOS. Outro caso idêntico aconteceu na loja de Chineses no RETAIL PARK em AVEIRO: O marido ficou a fumar um cigarro à porta da loja enquanto que a esposa entrou. Quando o marido após alguns minutos entrou à procura da esposa também já não a viu. Após procurar por ela, esta também já estava amarrada nas traseiras da loja e o destino dela provavelmente seria o mesmo. Agora se entrarem numa loja dessas, tenham o cuidado de não irem sozinhos pois facilita-lhes o trabalho. Isto não é brincadeira, P.F. divulguem ao maior número de pessoas possível.',
          'titulo': 'Lojas de chineses dedicam-se ao tráfico de órgãos',
          'classificacao': 'false',
          'data': '6/10/2019',				
		  'Emotion': '46',
          'Subjectivity': '49',
          'Affectivity': '48',
          'Polarity': '43',
          'BP': '57',
          'source': 'Facebook',
          'verified': 'no'
          }

data5 =  { 'id_noticia': '5', 
		  'noticia': 'Para não ofender muçulmanos, supermercado Lidl substitui a palavra “Natal” por “Festa” em seus produtos na Holanda Thaís Garcia A rede de supermercados alemã, Lidl, causou a indignação de muitos na Holanda. Para não ofender seus clientes muçulmanos, o supermercado substitui a palavra “Natal” por “festa” em seus produtos nos catálogos e prateleiras. Sem “estola de Natal”, mas “pão de festa”. Sem “café da manhã de Natal”, mas “café da manhã de festa”. Uma “guirlanda de Natal” é agora uma “guirlanda”. E as famílias celebrarão um “jantar festivo”, e não uma “Ceia de Natal”. No novo catálogo de produtos, não será mais encontrado a palavra Natal e muito menos um presépio. Um “suéter de Natal” virou uma “roupa de festa”, e outras roupas natalinas são agora apenas “fantasias”. Reações Na Holanda, o partido de direita, Fórum para a Democracia, publicou um vídeo no Facebook no qual é mostrado o novo catálogo do supermercado e a ausência da palavra “Natal”. Nas reações do vídeo, muitos criticaram a decisão polêmica do Lidl em optar pelo “politicamente correto” em seu catálogo. “Todas as nossas tradições estão sendo arrancadas. Tudo para não ofender os muçulmanos”, reagiu um holandês. “Você decora uma ‘árvore de festa’ com ‘bolas de festa’? No ‘Feriado’ vamos ao ‘jantar de festa’! Estamos caminhando para um futuro sombrio”, publicou Alexander ten Hoopen. “Boicote esse supermercado. Não compre mais nessa rede, porque ela não participam mais do Natal”, disse Willy Jacob. O político holandês de direita e líder do partido PVV, Geert Wilders, também publicou sua indignação no Twitter. “Nada de Natal, nada de Páscoa, mas produtos islâmicos Halal, Ramadã e celebração de sacrifício pode”, disse Wilders Politicamente correto O politicamente correto está aos poucos transformando a sociedade europeia. E infelizmente, não é uma transformação positiva. Em abril desse ano, cruzes foram cobertas com pano em um cemitério italiano em Bolonha, também para evitar “ofender muçulmanos”. O cemitério também instalou cortinas escuras motorizadas em uma capela local para esconder símbolos católicos romanos durante cerimônias envolvendo outras denominações. A líder do partido conservador Irmãos da Itália, Giorgia Meloni, também comentou o caso na época. “Usando a desculpa do respeito pelos outros, eles não têm respeito pela nossa cultura católica e nossas tradições. A esquerda está além do fanatismo. Isso é delírio ideológico”, disse Meloni. A celebração das festas cristãs continua sendo uma grande tradição na Holanda e em outros países europeus. Anteriormente, a loja de departamentos Hema recebeu muitas críticas porque trocou a “festa da Páscoa” por “banquete com coelhinhos e ovos”. Os holandeses então, descreveram que a atitude da Hema mostrava sua “queda” pelo Islã. A preocupação com o politicamento correto fez com que varejistas se sintam pressionados em não ofender muçulmanos. No entanto, acabam por ofender grande parte da população que por centenas de anos celebra festas cristãs na Europa. Afinal, o Natal é a data escolhida para a celebração do nascimento de Cristo e a Páscoa, para a celebração da Sua morte e ressurreição. As decorações natalinas, as luzes e os presépios, ainda podem ser vistos por toda a Europa nos meses de Novembro e Dezembro. Após o mar de críticas de consumidores holandeses nas redes sociais, o Lidl publicou uma nota informando que uma grande campanha de Natal está chegando.',
          'titulo': 'Para não ofender muçulmanos, supermercado Lidl substitui a palavra “Natal” por “Festa” em seus produtos na Holanda',
          'classificacao': 'false',
          'data': '11/11/2019',				
		  'Emotion': '66',
          'Subjectivity': '48',
          'Affectivity': '56',
          'Polarity': '36',
          'BP': '53',
          'source': 'conexaopolitica.com.br',
          'verified': 'no'
          }

data6 =  { 'id_noticia': '6',
		  'noticia': 'Última hora: Mega proposta por João Félix. João Félix tem interessados no seu passe, sendo que o Paris Saint-Germain estaria na linha da frente. O clube francês não desperdiça uma única oportunidade de ter do seu lado qualquer jovem talento e Félix é um dos que mais agrada, no atual panorama do futebol mundial. O Paris Saint-Germain tem milhões e força económica para se manter no topo do futebol europeu, mas numa altura em que se fala mais nas saídas de Neymar e de Mbappé, que poderiam estar à procura de ligas mais atrativas, o jogador português reentra nas contas do PSG. O PSG procura, então, alternativas e recursos para a milionária equipa de Thomas Tuchel. Este confronto João Felix / Diego Cholo Simeone poderia ser o gatilho que despoleta uma nova aquisição bombástica. Nasser Al-Khelaifi estaria já preparado para resgata uma das maiores promessas do futebol mundial, que parece perder-se no meio de todo o rigor de Simeone. Esse descontentamento é crucial para convencer João Félix. Além disso, o PSG tem a seu favor muitos milhões, que certamente podem compensar o Atlético de Madrid e o jovem prodígio português.',
          'titulo': 'Paris Saint-Germain prepara proposta milionária para contratar João Félix ao Atlético de Madrid',
          'classificacao': 'false',
          'data': '17/01/2020',				
		  'Emotion': '55',
          'Subjectivity': '53',
          'Affectivity': '51',
          'Polarity': '63',
          'BP': '57',
          'source': 'sonoticias.pt',
          'verified': 'no'
          }


firebase.post('/fakenews-app-d59dc/noticias/',data1)
firebase.post('/fakenews-app-d59dc/noticias/',data2)
firebase.post('/fakenews-app-d59dc/noticias/',data3)
firebase.post('/fakenews-app-d59dc/noticias/',data4)
firebase.post('/fakenews-app-d59dc/noticias/',data5)
firebase.post('/fakenews-app-d59dc/noticias/',data6)



