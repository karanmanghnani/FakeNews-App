from flask import Flask, render_template, url_for, request
from newspaper import Article
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import spacy
import get_lexicons as lex

STEMMER = nltk.stem.SnowballStemmer('portuguese')

app = Flask(__name__)



def desinfo2(website):
    article = Article(website)
    article.download()
    article.parse()
    article_text = article.text
    return article_text


def tokenize_sentences(document):
    sent_tokens = sent_tokenize(document)
    #print(sent_tokens)

    sentences = []
    for token in sent_tokens:
        sentences += token.split('\n')

    return sentences 

def stem_words(sentences):
    stems = []
    sp = spacy.load('pt_core_news_sm')
    for i in range(len(sentences)):
        for word in sp(sentences[i]):
            stems.append(STEMMER.stem(str(word)))
    return stems

def get_emotions(text):
	total_words = len(text.split())
	sentences = tokenize_sentences(text)
	list_of_words = stem_words(sentences)

	emotion_count = {'Happiness' : 0, 'Disgust' : 0, 'Fear' : 0, 'Anger':0, 'Surprise':0, 'Sadness':0}
	emotion_ratio = {'Happiness' : 0, 'Disgust' : 0, 'Fear' : 0, 'Anger':0, 'Surprise':0, 'Sadness':0}

	emotions = {'Happiness': ['abund', 'acalm', 'aceit', 'aclam', 'aconcheg', 'adesã', 'admir', 'ador', 'afeiçã', 'afet', 'afortun', 'afável', 'agrad', 'ajeit', 'altiv', 'altivez', 'alívi', 'amabil', 'amad', 'amar', 'amen', 'ameniz', 'amig', 'amist', 'amizad', 'amor', 'amável', 'anim', 'ansei', 'ansios', 'apaixon', 'apazigu', 'aplaus', 'apoi', 'apraz', 'aprec', 'aprov', 'aproveit', 'ardor', 'armir', 'arrum', 'atra', 'atraent', 'atraçã', 'avid', 'avidez', 'bel', 'belez', 'bem estar', 'benefic', 'beneficent', 'benefíci', 'benevocent', 'benign', 'benéf', 'benígn', 'boa intençã', 'bom', 'bom humor', 'bondad', 'bondos', 'bonit', 'bravur', 'bri', 'brilhant', 'brincadeir', 'calm', 'calor', 'carid', 'caridad', 'carinh', 'cativ', 'charm', 'chery', 'clam', 'cofort', 'colegu', 'comov', 'compaixã', 'companheir', 'compat', 'compatibil', 'complacent', 'complet', 'comprensã', 'coméd', 'conclusã', 'concretiz', 'condescendent', 'confianc', 'confort', 'congratul', 'conquist', 'consent', 'consider', 'consol', 'content', 'corag', 'cordial', 'cuidad', 'cumplic', 'cômic', 'dedic', 'deleit', 'delic', 'delicad', 'desej', 'despreocup', 'devot', 'devoçã', 'dignidad', 'diversã', 'divert', 'elogi', 'emocion', 'emot', 'emoçã', 'empat', 'empolg', 'empát', 'enamor', 'encant', 'encoraj', 'enfeit', 'engrac', 'entend', 'entusiasm', 'entusiást', 'esper', 'esplendor', 'estim', 'estimul', 'eufor', 'euforiz', 'eufór', 'exalt', 'excelent', 'excit', 'expans', 'extasi', 'exuber', 'exult', 'facilit', 'familiar', 'fascin', 'fascíni', 'favor', 'favorec', 'favorit', 'felic', 'feliz', 'fest', 'festej', 'festiv', 'fidel', 'fiel', 'filantrop', 'filantróp', 'fratern', 'ganh', 'gener', 'generos', 'gentil', 'glorific', 'glór', 'gost', 'gostos', 'goz', 'grat', 'gratidã', 'gratific', 'hilari', 'honr', 'humor', 'impression', 'incent', 'incentiv', 'inclin', 'incrível', 'inspir', 'inter', 'interess', 'irmandad', 'jovial', 'jubil', 'júbil', 'lealdad', 'legítim', 'levez', 'liberdad', 'louv', 'louvavel', 'louvável', 'lucr', 'lucrat', 'majest', 'maravilh', 'melhor', 'namor', 'nobr', 'obter', 'obtev', 'ode', 'orgulh', 'paixã', 'parabeniz', 'paz', 'piedos', 'posit', 'praz', 'prazenteir', 'predileçã', 'prefer', 'preferent', 'prench', 'promissor', 'prosper', 'proteg', 'protetor', 'proteçã', 'proveit', 'provilégi', 'quer', 'radiant', 'realiz', 'recomend', 'recompens', 'reconhec', 'recr', 'recreat', 'recreaçã', 'regozij', 'respeit', 'ressuscit', 'revigor', 'ris', 'risonh', 'romant', 'românt', 'sac', 'saciável', 'satisf', 'satisfatori', 'satisfatóri', 'satisfaz', 'satisfeit', 'seduz', 'seduçã', 'seren', 'simpat', 'simpát', 'sobreviv', 'sobrevivent', 'sort', 'sortud', 'sucess', 'surprend', 'tenr', 'ternur', 'torc', 'tranquil', 'triunf', 'triunfal', 'triunfant', 'vanglór', 'vantag', 'vantaj', 'vencedor', 'vener', 'ventur', 'vid', 'vigor', 'virtud', 'virtuos', 'vitori', 'vitór', 'viv', 'zel', 'zelos', 'ávid', 'ânim', 'ânsi'], 'Disgust': ['abelhud', 'abjet', 'abomin', 'aborrec', 'adoent', 'agon', 'amarg', 'antipat', 'antipát', 'apodrec', 'asco', 'asquer', 'aversã', 'chat', 'chateaçã', 'conden', 'decepçã', 'decepçõ', 'deprec', 'desagr', 'desagrad', 'desamor', 'desapeg', 'desaprec', 'descas', 'desconsider', 'desdém', 'desfavor', 'desgost', 'desord', 'desprez', 'detest', 'divórci', 'doenc', 'doent', 'enferm', 'enjo', 'enjoat', 'enjô', 'execr', 'falsidad', 'falt', 'fard', 'fei', 'fod', 'friez', 'fét', 'golf', 'grav', 'gravidad', 'gross', 'grosseir', 'heres', 'horror', 'horrível', 'ignóbil', 'ilegal', 'importun', 'imund', 'incomod', 'incômd', 'indecent', 'indecor', 'indiferenc', 'indign', 'indiscret', 'indisposiçã', 'indispost', 'inescrupul', 'insignific', 'invej', 'irregul', 'mal', 'maldad', 'maldos', 'malv', 'mau', 'menosprez', 'met', 'naus', 'nauseabund', 'nauseant', 'nauseos', 'noj', 'nojent', 'náus', 'obscen', 'obstru', 'obstruçã', 'ofens', 'patét', 'pavor', 'perig', 'perturb', 'problem', 'rejeiçã', 'repel', 'repelent', 'reprov', 'repugn', 'repuls', 'repulsã', 'rud', 'soberb', 'suj', 'sujeir', 'sórd', 'terrivel', 'terrível', 'torp', 'travess', 'travessur', 'tumult', 'tumultu', 'ultraj', 'vil', 'vomit', 'vômit', 'ânsi'], 'Fear': ['abomin', 'adapt', 'advers', 'afliçã', 'afugent', 'agon', 'alarm', 'alert', 'alien', 'ameac', 'amedront', 'angust', 'angusti', 'angúst', 'ansiedad', 'ansios', 'apavor', 'aprend', 'aprens', 'aprensã', 'arrepi', 'assombr', 'assust', 'assustador', 'atemoriz', 'aterroriz', 'brutal', 'calafri', 'calam', 'catástrof', 'choc', 'chocant', 'confrang', 'constern', 'covard', 'cruel', 'crueldad', 'cruelment', 'cuid', 'cuidad', 'defend', 'defensor', 'defes', 'derrot', 'desastr', 'desconfi', 'desconhec', 'desencoraj', 'desesper', 'desgrac', 'det', 'dor', 'envergonh', 'escandaliz', 'escuridã', 'espant', 'estremec', 'estremecedor', 'expuls', 'exót', 'fei', 'forasteir', 'friament', 'fug', 'hesit', 'horr', 'horripil', 'horrivel', 'horror', 'horroriz', 'horrível', 'impacient', 'impied', 'impiedad', 'indecisã', 'infortúni', 'inquiet', 'insegur', 'intimid', 'intrus', 'mal', 'martíri', 'Fearnh', 'medros', 'monstruos', 'mortalh', 'mortific', 'nervos', 'pavor', 'perturb', 'premoniçã', 'preocup', 'pressent', 'pressági', 'problem', 'pânic', 'rec', 'receat', 'recei', 'receos', 'ruim', 'separ', 'suplíci', 'suspeit', 'suspens', 'sust', 'tem', 'temer', 'temor', 'tens', 'tensã', 'terrific', 'terrivel', 'terror', 'terrível', 'timid', 'timidez', 'torment', 'tortur', 'tremor', 'tím', 'vigi', 'vigil'], 'Anger': ['abomin', 'aborrec', 'abus', 'adred', 'agred', 'agress', 'agressã', 'amaldiço', 'amargor', 'amargur', 'amol', 'angúst', 'animos', 'antipat', 'antipát', 'asco', 'assassin', 'assassinat', 'assedi', 'assédi', 'atorment', 'avar', 'avarent', 'aversã', 'beliger', 'bravej', 'chat', 'chateaçã', 'cobic', 'colér', 'complic', 'contraiedad', 'contrari', 'corrupt', 'corrupçã', 'cruxific', 'cól', 'demoníac', 'demôni', 'descas', 'descontent', 'descontrol', 'desengan', 'desgost', 'desgrac', 'despraz', 'desprez', 'destru', 'destruiçã', 'detest', 'diab', 'diaból', 'doid', 'encoleriz', 'energ', 'enfurec', 'enfuri', 'enlouquec', 'enraivec', 'escandaliz', 'escori', 'escândal', 'exasper', 'execr', 'fer', 'fod', 'frustr', 'frustraçã', 'furios', 'furor', 'fúr', 'gananc', 'ganânc', 'guerr', 'guerreador', 'guerrilh', 'hostil', 'humilh', 'implic', 'importun', 'incomod', 'incômod', 'indign', 'inferniz', 'inimig', 'inimizad', 'injuri', 'injustic', 'injúr', 'insolent', 'insult', 'invej', 'ira', 'irad', 'irasc', 'irascibil', 'irrit', 'louc', 'loucur', 'mago', 'mal', 'maldad', 'maldit', 'maldiz', 'maldiçã', 'maldos', 'maleficent', 'malevolent', 'malic', 'malign', 'maltrat', 'maluc', 'malv', 'malvad', 'maléf', 'malévol', 'malíc', 'malígn', 'mat', 'merd', 'mesquinh', 'misantrop', 'misantróp', 'molest', 'molést', 'mort', 'mortal', 'mortific', 'mortífer', 'nervos', 'odi', 'odios', 'odiável', 'ofend', 'ofens', 'opress', 'opressã', 'oprim', 'persegu', 'perseguiçã', 'perturb', 'pervers', 'provoc', 'rabugent', 'raivos', 'rancor', 'reclam', 'repressã', 'reprim', 'repuls', 'resmung', 'ressent', 'revolt', 'ridícul', 'segreg', 'tempestu', 'tiran', 'tol', 'tolic', 'torment', 'tortur', 'ultrag', 'ultraj', 'vexatóri', 'vigor', 'ving', 'vinganc', 'vingat', 'violent', 'violênc', 'zang', 'ódi'], 'Surprise': ['abasbac', 'admir', 'afeiçã', 'apavor', 'assombr', 'atordo', 'banz', 'boquiabr', 'brusc', 'casual', 'choc', 'chocant', 'choqu', 'desconcert', 'deslumbr', 'embasbac', 'emudec', 'encant', 'enorm', 'espant', 'estupef', 'estupefat', 'estupefaz', 'estupefic', 'estupor', 'eventual', 'expect', 'extraordinári', 'fantast', 'fantást', 'fortuit', 'horripil', 'imaginári', 'imens', 'impression', 'imprevist', 'improvis', 'inaudit', 'incrível', 'inesper', 'inopin', 'irreverent', 'maravilh', 'milagr', 'misteri', 'mistéri', 'pasm', 'perplex', 'prodígi', 'relanc', 'repentin', 'sensacional', 'sobressalt', 'subit', 'supetã', 'surprend', 'surprendent', 'surpres', 'suspens', 'sust', 'súbit', 'temor', 'trem', 'ótim'], 'Sadness': ['abandon', 'abat', 'abomin', 'aborrec', 'abort', 'aceit', 'advers', 'afast', 'aflig', 'aflit', 'afliçã', 'agoni', 'amarg', 'amargor', 'amargur', 'angusti', 'angúst', 'ansiedad', 'apart', 'arrepend', 'arrependid', 'atorment', 'atrit', 'azar', 'cabisbaix', 'carrancud', 'castig', 'chor', 'choros', 'chorã', 'circunspecçã', 'circunspeçã', 'coit', 'compass', 'compung', 'compunçã', 'constern', 'contrist', 'contrit', 'contriçã', 'culp', 'decepçã', 'decepçõ', 'defeitu', 'degrad', 'deplor', 'deposiçã', 'deprav', 'depress', 'depressã', 'deprim', 'depriment', 'derrot', 'derrub', 'desalent', 'desampar', 'desanim', 'desapont', 'desconsol', 'descontent', 'desculp', 'desencoraj', 'desentusiasm', 'desesper', 'desestimul', 'desg', 'desgost', 'desgrac', 'desilud', 'desincentiv', 'desist', 'desistent', 'desloc', 'desmoraliz', 'desmotiv', 'desol', 'desonr', 'despoj', 'despraz', 'desprez', 'desuman', 'desânim', 'discrimin', 'disfor', 'disfór', 'dissuad', 'divórci', 'dolor', 'dor', 'encobr', 'enegrec', 'enfad', 'enlut', 'entedi', 'entristec', 'entristecedor', 'envergonh', 'errant', 'erro', 'errôn', 'escald', 'escur', 'escurec', 'escuridã', 'esmorec', 'esquec', 'estrag', 'estranh', 'execr', 'extirp', 'fals', 'falsidad', 'falt', 'flagel', 'frac', 'fraquez', 'fri', 'fricçã', 'friez', 'funest', 'fúnebr', 'gel', 'grav', 'horror', 'humilh', 'importun', 'inconsol', 'indefes', 'infel', 'infeliz', 'infortúni', 'invej', 'isol', 'lacrim', 'lacrimej', 'lament', 'lastim', 'lut', 'lutos', 'lágrim', 'lástim', 'lúgubr', 'mago', 'martiriz', 'martíri', 'mau', 'melancol', 'melancól', 'menosprez', 'miser', 'misteri', 'mistéri', 'misér', 'morr', 'mort', 'mortific', 'mágo', 'negligent', 'nociv', 'nostalg', 'nubl', 'obscur', 'ofusc', 'opress', 'opressã', 'oprim', 'part', 'pen', 'penaliz', 'penitencial', 'penitent', 'penos', 'pensat', 'penumbr', 'perd', 'perturb', 'pervers', 'pervert', 'pes', 'pesar', 'pessim', 'piedad', 'pobr', 'porc', 'prejudic', 'prejudicial', 'prejuíz', 'pression', 'pressã', 'prostraçã', 'quebr', 'qued', 'queixos', 'rechac', 'remors', 'repress', 'repressã', 'reprim', 'retidã', 'retitud', 'ruim', 'saudad', 'secret', 'segreg', 'sent', 'separ', 'seriedad', 'servil', 'sisud', 'sisudez', 'sobrecarg', 'sobrecarreg', 'sofr', 'sofriment', 'solidã', 'solitári', 'sombri', 'soturn', 'sozinh', 'sucumb', 'suj', 'suplic', 'suplíci', 'timidez', 'torment', 'tortur', 'trev', 'trist', 'tristement', 'tristonh', 'tédi', 'tím', 'vazi', 'viúv']}


	for text_words in list_of_words:
	    for emotion_word in emotions['Happiness']:
	        if (emotion_word == text_words):
	            emotion_count['Happiness'] = emotion_count['Happiness'] + 1
	    for emotion_word in emotions['Disgust']:
	        if (emotion_word == text_words):
	            emotion_count['Disgust'] = emotion_count['Disgust'] + 1
	    for emotion_word in emotions['Fear']:
	        if (emotion_word == text_words):
	            emotion_count['Fear'] = emotion_count['Fear'] + 1
	    for emotion_word in emotions['Anger']:
	        if (emotion_word == text_words):
	            emotion_count['Anger'] = emotion_count['Anger'] + 1
	    for emotion_word in emotions['Surprise']:
	        if (emotion_word == text_words):
	            emotion_count['Surprise'] = emotion_count['Surprise'] + 1
	    for emotion_word in emotions['Sadness']:
	        if (emotion_word == text_words):
	            emotion_count['Sadness'] = emotion_count['Sadness'] + 1


	total_value = sum(emotion_count.values())

	emotion_ratio = emotion_count.copy()
	print(emotion_ratio)
	for i in emotion_ratio.keys():
	    if(total_value != 0):
	        emotion_ratio[i] = ('%.1f' % ((emotion_ratio[i]/total_value)*100))
	        print(type(emotion_ratio[i]))
	        
	        print(i)
	        print(emotion_ratio[i])

	emotion_total= round(total_value/total_words, 3)*100
	#print("Total number of emotions is: " + str(total_value))
	#print(emotion_count)
	print(emotion_ratio)
	#print(total_value)
	#print(total_words)
	#print(total_value/total_words)
	return emotion_count,emotion_ratio,emotion_total



def get_subjective_ratio(text):

    total_subj_words = 0
    totalsubj = 0
    words = text.split()
    subjective_words = lex.load_subjectivity_lexicon('lexicons/subjectivity-clues-pt.csv')
    subj_feats = {'strongsubj':0, 'weaksubj':0}
    n_words = len(words)

    for word in words:
        stem = STEMMER.stem(word)
        if stem in subjective_words['strongsubj']:
        	subj_feats['strongsubj'] += 1
        	total_subj_words += 1
        	#print('strongsubj', word, stem)
        elif stem in subjective_words['weaksubj']:
        	subj_feats['weaksubj'] += 1
        	total_subj_words += 1
        	#print('weaksubj', word, stem)

    total_subj_ratio = (total_subj_words/n_words)*100

    #Regra 3 simples para calculo de % em relaçao ao total e depois *100 (para meter em %)
    total_strongsubj_ratio = (((subj_feats.get('strongsubj')/n_words)*100)/total_subj_ratio)*100
    total_weeksubj_ratio = (((subj_feats.get('weaksubj')*100)/n_words)/total_subj_ratio)*100

    totalsubj = round(total_subj_ratio, 1)
    subj_feats['strongsubj'] = round(total_strongsubj_ratio, 1)
    subj_feats['weaksubj'] = round(total_weeksubj_ratio, 1)
    
    print(total_subj_words, n_words)
    print(subj_feats)
    return totalsubj, subj_feats



posts = [
	{
	    'author': 'Corey Schafer',
	    'title': 'Blog Post 1',
	    'content': 'First post content',
	    'date_posted': 'April 20, 2018'
	},
	{
	    'author': 'Jane Doe',
	    'title': 'Blog Post 2',
	    'content': 'Second post content',
	    'date_posted': 'April 21, 2018'
	}
]


@app.route("/")
@app.route("/HomePage",methods = ['POST', 'GET'])
def HomePage():
    if request.method == 'POST': 
        if('url' in request.values ):
            url = request.form['url']
            article_text = desinfo2(url)
            emotion_count,emotion_ratio,total_emotion = get_emotions(article_text)
            totalsubj, subj_feats = get_subjective_ratio(article_text)
            return render_template('result.html', title='FakeNews',posts=posts, article_text=article_text, emotion_count=emotion_count, emotion_ratio=emotion_ratio, total_emotion=total_emotion, totalsubj=totalsubj, subj_feats=subj_feats)
        else:
            article_text = request.form['ArticleText']
            emotion_count,emotion_ratio,total_emotion = get_emotions(article_text)
            totalsubj, subj_feats = get_subjective_ratio(article_text)
            return render_template('result.html', title='FakeNews',posts=posts, article_text=article_text, emotion_count=emotion_count, emotion_ratio=emotion_ratio, total_emotion=total_emotion, totalsubj=totalsubj, subj_feats=subj_feats)

    else:
        return render_template('HomePage.html', title='FakeNews')


@app.route("/result",methods = ['POST', 'GET'])
def result():
    return render_template('result.html', posts=posts)




if __name__ == '__main__':
    app.run(debug=True)