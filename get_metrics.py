from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import spacy
import get_metrics as metrics
import get_lexicons as lex
import statistics 
from urllib.parse import urlparse
import re
import xlrd 
import pickle

import get_lexicons as lex

STEMMER = nltk.stem.SnowballStemmer('portuguese')
sp = spacy.load('pt_core_news_sm')


####################################################
#		Prepare and Load get_lexicons              #
####################################################

def prepare_lexicons():

    liwc_pt_path = 'lexicons/LIWC2007_Portugues_win.dic.txt'
    oplexicon_path = 'lexicons/oplexico_v3.0.txt'
    sentilex_path = 'lexicons/SentiLex-flex-PT02.txt'
    filename_anew = 'lexicons/anew-pt.csv'
    filename_anew_extended = 'lexicons/BRM-emot-submit-pt.csv'
    filename_emotions = 'lexicons/emotions'
    filename_subjectivity = 'lexicons/subjectivity-clues-pt.csv'

    liwc_tags = lex.load_liwc(liwc_pt_path)
    with open('proc_lexicons/liwc.pkl', 'wb') as f:
        pickle.dump(liwc_tags,f)
    print('Done LIWC.')

    oplexicon = lex.load_valence_emotions_from_oplexicon(oplexicon_path)
    sentilex = lex.load_valence_emotions_from_sentilex(sentilex_path)
    sentilex = lex.complement_sentilex(sentilex,oplexicon)
    with open('proc_lexicons/sentilex.pkl', 'wb') as f:
        pickle.dump(sentilex,f)
    print('Done Sentilex.')
    
    anew = lex.load_anew_pt(filename_anew)
    anew_extended = lex.load_anew_extended_pt(filename_anew_extended)
    anew_extended.update(anew)
    with open('proc_lexicons/anew.pkl', 'wb') as f:
        pickle.dump(anew_extended,f)
    print('Done ANEW.')

    emotion_words = lex.load_six_emotions(filename_emotions)
    with open('proc_lexicons/emotion_words.pkl', 'wb') as f:
        pickle.dump(emotion_words,f)
    print('Done Emotion words.')

    subjective_words = lex.load_subjectivity_lexicon(filename_subjectivity)
    with open('proc_lexicons/subjective_words.pkl', 'wb') as f:
        pickle.dump(subjective_words,f)
    print('Done Subjective words.')

def load_lexicons():
    with open('proc_lexicons/liwc.pkl', 'rb') as f:
        liwc_tags = pickle.load(f)
    print('Done LIWC.')

    with open('proc_lexicons/sentilex.pkl', 'rb') as f:
        sentilex = pickle.load(f)
    print('Done Sentilex.')
    
    with open('proc_lexicons/anew.pkl', 'rb') as f:
        anew_extended = pickle.load(f)
    print('Done ANEW.')

    with open('proc_lexicons/emotion_words.pkl', 'rb') as f:
        emotion_words = pickle.load(f)
    print('Done Emotion words.')

    with open('proc_lexicons/subjective_words.pkl', 'rb') as f:
        subjective_words = pickle.load(f)
    print('Done Subjective words.')

    return liwc_tags, sentilex, anew_extended, emotion_words, subjective_words

def tokenize_sentences(document):
    sent_tokens = sent_tokenize(document)
    #print(sent_tokens)

    sentences = []
    for token in sent_tokens:
        sentences += token.split('\n')

    return sentences 

def tokenize_words(sentences):
    tokens = []

    for i in range(len(sentences)):
        for word in sp(sentences[i]):
            #print(word.text, word.pos_, word.dep_, )
            if word.pos_ != 'PUNCT':
                tokens += [word.text.lower()]
    return tokens


def stem_words(sentences):
    stems = []
    sp = spacy.load('pt_core_news_sm')
    for i in range(len(sentences)):
        for word in sp(sentences[i]):
            stems.append(STEMMER.stem(str(word)))
    return stems

def lemmatize_words(sentences):
    lemmas = []

    for i in range(len(sentences)):
        for word in sp(sentences[i]):
            if word.pos_ != 'PUNCT':
                lemmas += [word.lemma_.lower()]
    return lemmas

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



def get_vad_features(lemmas, anew):

	V, A, D = [], [], []
	total_vad = 0

	for lemma in lemmas:

	    if lemma in anew.keys():
	        #print(lemma, ' lemma found')
	        #print(lemma)
	        V += [anew[lemma]['V']]
	        A += [anew[lemma]['A']]
	        D += [anew[lemma]['D']]
	        total_vad += 1
	    #else:
	    #    print(lemma, ' lemma not found')
	vad_features = {
		'total_vad': round(total_vad/len(lemmas), 3)*100,
	    'valence_avg': round(statistics.mean(V) , 3),
	    'valence_std': round(statistics.stdev(V), 4),
	    'valence_max': round(max(V), 4),
	    'valence_min': round(min(V), 4),
	    'valence_dif': round(max(V) - min(V), 4),
	    'arousal_avg': round(statistics.mean(A), 3),
	    'arousal_std': round(statistics.stdev(A), 4),
	    'arousal_max': round(max(A), 4),
	    'arousal_min': round(min(A), 4),
	    'arousal_dif': round(max(A) - min(A), 4),
	    'dominance_avg': round(statistics.mean(D), 3),
	    'dominance_std': round(statistics.stdev(D), 4),
	    'dominance_max': round(max(D), 4),
	    'dominance_min': round(min(D), 4),
	    'dominance_dif': round(max(D) - min(D), 4),
	}

	#print(V,A,D)
	print(vad_features)
	return  vad_features

def sentiment_polarity(words, sentilex):

	polarity = {}
	total_pos, polarity['positive_ratio'] = get_positive_words_ratio(sentilex, words)
	total_neg, polarity['negative_ratio'] = get_negative_words_ratio(sentilex, words)
	polarity['positive_contrast'] = get_positive_contrast(sentilex, words)
	polarity['negative_contrast'] = get_negative_contrast(sentilex, words)
	#print(polarity)
	total_pol = round((total_pos + total_neg)/len(words), 3)
	polarity['total_pol'] = total_pol*100
	return polarity


def behavioral_physiological(words, liwc_tags):

	doc_stats = {}
	n_perceptual_words, doc_stats['perceptuality'] = get_perceptuality(liwc_tags, words)
	n_relativity_words, doc_stats['relativity'] = get_relativity(liwc_tags, words)
	n_cognitive_words, doc_stats['cognitivity'] = get_cognitivity(liwc_tags, words)
	n_personal_concerns_words, doc_stats['personal_concerns'] = get_personal_concerns(liwc_tags, words)
	n_biological_words, doc_stats['biological_processes'] = get_biological_processes(liwc_tags, words)
	n_social_words, doc_stats['social_processes'] = get_social_processes(liwc_tags, words)
	print((n_perceptual_words + n_relativity_words + n_cognitive_words + n_personal_concerns_words + n_biological_words + n_social_words)/len(words))
	print(n_perceptual_words + n_relativity_words + n_cognitive_words + n_personal_concerns_words + n_biological_words + n_social_words)
	print(len(words))
	total_words = n_perceptual_words + n_relativity_words + n_cognitive_words + n_personal_concerns_words + n_biological_words + n_social_words
	total_bp = (total_words/(len(words)*6))*100
	doc_stats['total_bp'] = round(total_bp,1)
	return doc_stats

def get_subjective_ratio(words, subjective_words):

	total_subj_words = 0
	totalsubj = 0
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

	total_subj_ratio = (round(total_subj_words/n_words, 3))*100

	#Regra 3 simples para calculo de % em relaçao ao total e depois *100 (para meter em %)
	total_strongsubj_ratio = (((subj_feats.get('strongsubj')/n_words)*100)/total_subj_ratio)*100
	total_weeksubj_ratio = (((subj_feats.get('weaksubj')*100)/n_words)/total_subj_ratio)*100

	subj_feats['strongsubj'] = round(total_strongsubj_ratio, 1)
	subj_feats['weaksubj'] = round(total_weeksubj_ratio, 1)

	print(total_subj_words, n_words)
	print(subj_feats)
	return total_subj_ratio, subj_feats

def source(url):
	hostname = urlparse(url).hostname 
	absolute_url = re.sub('www.', '', hostname)

	loc = ("Entidades registadas.xlsx") 
	  
	wb = xlrd.open_workbook(loc) 
	sheet = wb.sheet_by_index(0) 

	value = False
	for i in range(2,sheet.nrows):
	    if(absolute_url in sheet.cell_value(i, 12)):
	    	value = True

	return value, absolute_url

#######################################
#          Auxiliar Functions		  #
#######################################

def get_perceptuality(liwc_tags, words):
    '''sensorial experiences, such as sounds, smells, physical sensations, and visual details over the number of words'''
    # zhou et al: perceptual information
    # liwc categories: [140] perceptual processes, [141] see, [142] hear, [143] feel

    n_words = len(words)

    n_perceptual_words = 0
    for word in words:
        if (word in liwc_tags['140']['words'] or 
            word in liwc_tags['141']['words'] or 
            word in liwc_tags['142']['words'] or 
            word in liwc_tags['143']['words']):
            #print(word) 
            n_perceptual_words += 1

    return n_perceptual_words, round(n_perceptual_words/n_words, 3)*100


def get_relativity(liwc_tags, words):
    ''' number of locations of people or objects or information about when the event happened over the number of words'''
    # zhou et al: space-temporal information
    # liwc: [250] relativity, [251] motion, [252] space, [253] time
    
    n_words = len(words)

    n_relativity_words = 0
    for word in words:
        if (word in liwc_tags['250']['words'] or 
            word in liwc_tags['251']['words'] or 
            word in liwc_tags['252']['words'] or 
            word in liwc_tags['253']['words']):
            #print(word) 
            n_relativity_words += 1

    return n_relativity_words, round(n_relativity_words/n_words, 3)*100


def get_cognitivity(liwc_tags, words):
    ''' number of cognitive words over the number of words'''
    # liwc categories: [131] cognitive processes, [132] insight, [133] causation, [134] discrepancy, [135] tentative, 
    # [136] certainty, [137] inhibition, [138] inclusive, [139] exclusive

    n_words = len(words)

    n_cognitive_words = 0
    for word in words:
        if (word in liwc_tags['131']['words'] or 
            word in liwc_tags['132']['words'] or 
            word in liwc_tags['133']['words'] or
            word in liwc_tags['134']['words'] or
            word in liwc_tags['135']['words'] or
            word in liwc_tags['136']['words'] or
            word in liwc_tags['137']['words'] or
            word in liwc_tags['138']['words'] or
            word in liwc_tags['139']['words']):

            #print(word) 
            n_cognitive_words += 1

    return n_cognitive_words, round(n_cognitive_words/n_words, 3)*100

    
def get_personal_concerns(liwc_tags, words):
    '''personal concerns over the number of words'''
    # liwc categories: [354] work, [355] achievement, [356] leisure, [357] home, 
    # [358] money, [359] religion, [360] death

    n_words = len(words)

    n_personal_concerns_words = 0
    for word in words:
        if (word in liwc_tags['354']['words'] or 
            word in liwc_tags['355']['words'] or 
            word in liwc_tags['356']['words'] or 
            word in liwc_tags['357']['words'] or 
            word in liwc_tags['358']['words'] or 
            word in liwc_tags['359']['words'] or 
            word in liwc_tags['360']['words']):
            #print(word) 
            n_personal_concerns_words += 1

    return n_personal_concerns_words, round(n_personal_concerns_words/n_words, 3)*100


def get_social_processes(liwc_tags, words):
    '''social processes over the number of words'''
    # liwc categories: [121] social, [122] family, [123] friends, [124] humans

    n_words = len(words)

    n_social_words = 0
    for word in words:
        if (word in liwc_tags['121']['words'] or 
            word in liwc_tags['122']['words'] or 
            word in liwc_tags['123']['words'] or 
            word in liwc_tags['124']['words']):
            #print(word) 
            n_social_words += 1

    return n_social_words, ('%.1f' % ((n_social_words/n_words)*100))


def get_biological_processes(liwc_tags, words):
    '''biological processes over the number of words'''
    # liwc categories: [146] bio, [147] body, [148] health, [149] sexual, [150] ingestion

    n_words = len(words)

    n_biological_words = 0
    for word in words:
        if (word in liwc_tags['146']['words'] or 
            word in liwc_tags['147']['words'] or 
            word in liwc_tags['148']['words'] or 
            word in liwc_tags['149']['words'] or 
            word in liwc_tags['150']['words']):
            #print(word) 
            n_biological_words += 1
 
    return n_biological_words, ('%.1f' % ((n_biological_words/n_words)*100))

def get_positive_words_ratio(sentilex, words):
    '''number of potentially positive words over the number of words'''

    n_words = len(words)
    text = ' ' + ' '.join(words) + ' '

    n_pos = 0
    for pos in sentilex['POSITIVO']:
        if ' ' + pos + ' ' in text:
            n_pos += 1
    
    return n_pos, round(n_pos/n_words, 3)*100

def get_negative_words_ratio(sentilex, words):
    '''number of potentially negative words over the number of words'''

    n_words = len(words)
    text = ' ' + ' '.join(words) + ' '

    n_neg = 0
    for neg in sentilex['NEGATIVO']:
        if ' ' + neg + ' ' in text:
            n_neg += 1

    return n_neg, ('%.1f' % ((n_neg/n_words)*100))


def get_positive_contrast(sentilex, words):
    '''number of sequences where a positive word (unigram) is followed by a negative word'''

    n_pos_contrast = 0
    for i in range(len(words)-1):
        if words[i] in sentilex['POSITIVO'] and words[i+1] in sentilex['NEGATIVO']:
            #print(words[i], words[i+1])
            n_pos_contrast += 1

    return n_pos_contrast


def get_negative_contrast(sentilex, words):
    '''number of sequences where a negative word (unigram) is followed by a positive word'''

    n_neg_contrast = 0
    for i in range(len(words)-1):
        if words[i] in sentilex['NEGATIVO'] and words[i+1] in sentilex['POSITIVO']:
            #print(words[i], words[i+1])
            n_neg_contrast += 1

    return n_neg_contrast



