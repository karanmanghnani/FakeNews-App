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
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression

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
    original_words = []

    for i in range(len(sentences)):
        for word in sp(sentences[i]):
            #print(word.text, word.pos_, word.dep_, )
            if word.pos_ != 'PUNCT':
                tokens += [word.text.lower()]
                original_words.append(word)
    return tokens, original_words


def stem_words(sentences):
    stems = []
    sp = spacy.load('pt_core_news_sm')
    for i in range(len(sentences)):
        for word in sp(sentences[i]):
            stems.append(STEMMER.stem(str(word)))
    return stems

def lemmatize_words(sentences):
    lemmas = []
    original_words = []

    for i in range(len(sentences)):
        for word in sp(sentences[i]):
            if word.pos_ != 'PUNCT':
                lemmas += [word.lemma_.lower()]
                original_words.append(word)
    return lemmas, original_words

def get_emotions(words, emotion_words):
    six_emotions = list(emotion_words.keys())
    emotion_feats = {k:0 for k in six_emotions}
    n_emotions = 0
    emotions_list = {}

    for emo in six_emotions:
        emotions_list[emo] = []

    for word in words:
        stem = STEMMER.stem(word)
        for emo in six_emotions:
            if stem in emotion_words[emo]:
                #print(word, stem, emo)
                emotion_feats[emo] += 1
                n_emotions +=1
                emotions_list[emo].append(word) 

    if n_emotions:
        emotion_feats.update({k:round(emotion_feats[k]/n_emotions, 4) for k in six_emotions})

    return emotion_feats, round(n_emotions/len(words),3 )*100, emotions_list



def get_vad_features(lemmas, anew):

    V, A, D = [], [], []
    total_vad = 0
    vad_list = []

    for lemma in lemmas:

        if lemma in anew.keys():
            V += [anew[lemma]['V']]
            A += [anew[lemma]['A']]
            D += [anew[lemma]['D']]
            total_vad += 1
            vad_list.append(lemma)
    
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
    return  vad_features, vad_list

def sentiment_polarity(words, sentilex):

	polarity = {}
	total_pos, polarity['positive_ratio'], polarity['pos_list'] = get_positive_words_ratio(sentilex, words)
	total_neg, polarity['negative_ratio'], polarity['neg_list'] = get_negative_words_ratio(sentilex, words)
	polarity['positive_contrast'], polarity['pos_cons_list'] = get_positive_contrast(sentilex, words)
	polarity['negative_contrast'], polarity['neg_cons_list'] = get_negative_contrast(sentilex, words)
	#print(polarity)
	total_pol = round((total_pos + total_neg)/len(words), 3)
	polarity['total_pol'] = total_pol*100
	return polarity


def behavioral_physiological(words, liwc_tags):

	doc_stats = {}
	n_perceptual_words, doc_stats['perceptuality'], doc_stats['perc_list'] = get_perceptuality(liwc_tags, words)
	n_relativity_words, doc_stats['relativity'], doc_stats['rel_list'] = get_relativity(liwc_tags, words)
	n_cognitive_words, doc_stats['cognitivity'], doc_stats['cog_list'] = get_cognitivity(liwc_tags, words)
	n_personal_concerns_words, doc_stats['personal_concerns'], doc_stats['pers_list'] = get_personal_concerns(liwc_tags, words)
	n_biological_words, doc_stats['biological_processes'], doc_stats['soc_list'] = get_biological_processes(liwc_tags, words)
	n_social_words, doc_stats['social_processes'], doc_stats['bio_list'] = get_social_processes(liwc_tags, words)
	#print((n_perceptual_words + n_relativity_words + n_cognitive_words + n_personal_concerns_words + n_biological_words + n_social_words)/len(words))
	#print(n_perceptual_words + n_relativity_words + n_cognitive_words + n_personal_concerns_words + n_biological_words + n_social_words)
	#print(len(words))
	total_words = n_perceptual_words + n_relativity_words + n_cognitive_words + n_personal_concerns_words + n_biological_words + n_social_words
	total_bp = (total_words/(len(words)*6))*100
	doc_stats['total_bp'] = round(total_bp,1)
	return doc_stats

def get_subjective_ratio(words, subjective_words):

    total_subj_words = 0
    totalsubj = 0
    subj_feats = {'strongsubj':0, 'weaksubj':0}
    n_words = len(words)
    subj_list = {}
    subj_list['strongsubj'] = []
    subj_list['weaksubj'] = []
	
    for word in words:
        stem = STEMMER.stem(word)
        if stem in subjective_words['strongsubj']:
            subj_feats['strongsubj'] += 1
            total_subj_words += 1
            subj_list['strongsubj'].append(word)
            #print('strongsubj', word, stem)
        elif stem in subjective_words['weaksubj']:
            subj_feats['weaksubj'] += 1
            total_subj_words += 1
            subj_list['weaksubj'].append(word)
            #print('weaksubj', word, stem)
    total_subj_ratio = (round(total_subj_words/n_words, 3))*100

    #Regra 3 simples para calculo de % em relaçao ao total e depois *100 (para meter em %)
    total_strongsubj_ratio = ((subj_feats.get('strongsubj'))/n_words)*100
    total_weeksubj_ratio = ((subj_feats.get('weaksubj'))/n_words)*100

    #print(total_subj_words, n_words)
    #print(subj_feats)
    return total_subj_ratio, subj_feats, subj_list

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
#          Probability of fake        #
#######################################


def prepareMetricsDB():
    emotion = []
    subjectivity = []
    affective = []
    polarity = []
    bp = []

    colnames=['Grau', 'Emotion', 'Subjectivity', 'Affective', 'Polarity', 'BP'] 
    df = pd.read_csv("noticias_BD_test.csv", names=colnames, header=None)

    for i in range(len(df)):
        emotion.append((df['Emotion'][i],df['Grau'][i]))
        subjectivity.append((df['Subjectivity'][i],df['Grau'][i]))
        affective.append((df['Affective'][i],df['Grau'][i]))
        polarity.append((df['Polarity'][i],df['Grau'][i]))
        bp.append((df['BP'][i],df['Grau'][i]))
    return emotion, subjectivity, affective, polarity, bp

def getKey(item):
    return item[0]

def doQuartil(lista):
    temp_list = []
    for element in lista:
        temp_list.append(element[0])
    quartil = np.percentile(temp_list, [25, 50, 75])
    return quartil


def getQuartilResultList(quartil, sorted_metric, metric):
    result_list = []
    if (metric <= quartil[0]):
        for element in sorted_metric:
            if(element[0] <= quartil[0]):
                result_list.append(element[1])

    elif (quartil[0] < metric <= quartil[1]):
        for element in sorted_metric:
            if(quartil[0] < element[0] <= quartil[1]):
                result_list.append(element[1])

    elif (quartil[1] < metric <= quartil[2]):
        for element in sorted_metric:
            if(quartil[1] < element[0] <= quartil[2]):
                result_list.append(element[1])

    elif (metric > quartil[2]):
        for element in sorted_metric:
            if(element[0] > quartil[2]):
                result_list.append(element[1])

    return result_list

def getProb(result_list):
    fake_count = 0
    for i in result_list:
        if i == 'Falso ':
            fake_count += 1
    return round(fake_count/len(result_list), 2)

def fakeProbability(metric, metric_total):
    sorted_metric = sorted(metric, key=getKey)
    #print(sorted_metric)
    quartil_metric = doQuartil(sorted_metric)
    #print(quartil_metric)
    metric_result = getQuartilResultList(quartil_metric, sorted_metric, metric_total)
    #print(metric_result)
    metric_prob = getProb(metric_result)
    #print(metric_prob)

    return float('%.1f' % ((metric_prob)*100))

def fakeProbability2(emotion,subj,val_avg,arou_avg,dom_avg,pos_words,neg_words,percep,relat,cogni,personal,bio,social):

    df = pd.read_excel('BD_results_corpus.xlsx')
    model = LogisticRegression()

    # Emotion

    lista = []
    lista.append(emotion)

    X_test = pd.DataFrame(lista, columns=['Emotion'])
    X_train = df[['Emotion']]
    y_train = df.Label

    model.fit(X_train, y_train)

    y_predicted = model.predict_proba(X_test)

    emotion = float('%.0f' % ((y_predicted[0][0])*100))

    # Subj

    lista = []
    lista.append(subj)

    X_test = pd.DataFrame(lista, columns=['Subj'])
    X_train = df[['Subj']]
    y_train = df.Label

    model.fit(X_train, y_train)

    y_predicted = model.predict_proba(X_test)

    subj = float('%.0f' % ((y_predicted[0][0])*100))


    # Affective

    lista = []
    lista.append(val_avg)
    lista.append(arou_avg)
    lista.append(dom_avg)

    X_test = pd.DataFrame([lista], columns=['val_avg','aro_avg','dom_avg'])
    X_train = df[['val_avg','aro_avg','dom_avg']]
    y_train = df.Label

    model.fit(X_train, y_train)

    y_predicted = model.predict_proba(X_test)

    affective = float('%.0f' % ((y_predicted[0][0])*100))

    # Polarity

    lista = []
    lista.append(pos_words)
    lista.append(neg_words)

    X_test = pd.DataFrame([lista], columns=['pos_words','neg_words'])
    X_train = df[['pos_words','neg_words']]
    y_train = df.Label

    model.fit(X_train, y_train)

    y_predicted = model.predict_proba(X_test)

    polarity = float('%.0f' % ((y_predicted[0][0])*100))


    # BP

    lista = []
    lista.append(percep)
    lista.append(relat)
    lista.append(cogni)
    lista.append(personal)
    lista.append(bio)
    lista.append(social)

    X_test = pd.DataFrame([lista], columns=['perceptuality','relativity','cognitivity','personal','biological','social'])
    X_train = df[['perceptuality','relativity','cognitivity','personal','biological','social']]
    y_train = df.Label

    model.fit(X_train, y_train)

    y_predicted = model.predict_proba(X_test)

    bp = float('%.0f' % ((y_predicted[0][0])*100))


    return emotion, subj, affective, polarity, bp
#######################################
#          Auxiliar Functions		  #
#######################################

def get_perceptuality(liwc_tags, words):
    '''sensorial experiences, such as sounds, smells, physical sensations, and visual details over the number of words'''
    # zhou et al: perceptual information
    # liwc categories: [140] perceptual processes, [141] see, [142] hear, [143] feel
    perc_list = []
    n_words = len(words)

    n_perceptual_words = 0
    for word in words:
        if (word in liwc_tags['140']['words'] or 
            word in liwc_tags['141']['words'] or 
            word in liwc_tags['142']['words'] or 
            word in liwc_tags['143']['words']):
            #print(word) 
            n_perceptual_words += 1
            perc_list.append(word)

    return n_perceptual_words, round(n_perceptual_words/n_words, 3)*100, perc_list


def get_relativity(liwc_tags, words):
    ''' number of locations of people or objects or information about when the event happened over the number of words'''
    # zhou et al: space-temporal information
    # liwc: [250] relativity, [251] motion, [252] space, [253] time
    rel_list = []
    n_words = len(words)

    n_relativity_words = 0
    for word in words:
        if (word in liwc_tags['250']['words'] or 
            word in liwc_tags['251']['words'] or 
            word in liwc_tags['252']['words'] or 
            word in liwc_tags['253']['words']):
            #print(word) 
            n_relativity_words += 1
            rel_list.append(word)

    return n_relativity_words, round(n_relativity_words/n_words, 3)*100, rel_list


def get_cognitivity(liwc_tags, words):
    ''' number of cognitive words over the number of words'''
    # liwc categories: [131] cognitive processes, [132] insight, [133] causation, [134] discrepancy, [135] tentative, 
    # [136] certainty, [137] inhibition, [138] inclusive, [139] exclusive
    cog_list = []
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
            cog_list.append(word)

    return n_cognitive_words, round(n_cognitive_words/n_words, 3)*100, cog_list

    
def get_personal_concerns(liwc_tags, words):
    '''personal concerns over the number of words'''
    # liwc categories: [354] work, [355] achievement, [356] leisure, [357] home, 
    # [358] money, [359] religion, [360] death
    pers_list = []
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
            pers_list.append(word)

    return n_personal_concerns_words, round(n_personal_concerns_words/n_words, 3)*100, pers_list


def get_social_processes(liwc_tags, words):
    '''social processes over the number of words'''
    # liwc categories: [121] social, [122] family, [123] friends, [124] humans
    soc_list = []
    n_words = len(words)

    n_social_words = 0
    for word in words:
        if (word in liwc_tags['121']['words'] or 
            word in liwc_tags['122']['words'] or 
            word in liwc_tags['123']['words'] or 
            word in liwc_tags['124']['words']):
            #print(word) 
            n_social_words += 1
            soc_list.append(word)

    return n_social_words, ('%.1f' % ((n_social_words/n_words)*100)), soc_list


def get_biological_processes(liwc_tags, words):
    '''biological processes over the number of words'''
    # liwc categories: [146] bio, [147] body, [148] health, [149] sexual, [150] ingestion
    bio_list = []
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
            bio_list.append(word)
 
    return n_biological_words, ('%.1f' % ((n_biological_words/n_words)*100)), bio_list

def get_positive_words_ratio(sentilex, words):
    '''number of potentially positive words over the number of words'''
    pos_list = []
    n_words = len(words)
    text = ' ' + ' '.join(words) + ' '

    n_pos = 0
    for pos in sentilex['POSITIVO']:
        if ' ' + pos + ' ' in text:
            n_pos += 1
            pos_list.append(pos)
    
    return n_pos, round(n_pos/n_words, 3)*100, pos_list

def get_negative_words_ratio(sentilex, words):
    '''number of potentially negative words over the number of words'''
    neg_list = []
    n_words = len(words)
    text = ' ' + ' '.join(words) + ' '

    n_neg = 0
    for neg in sentilex['NEGATIVO']:
        if ' ' + neg + ' ' in text:
            n_neg += 1
            neg_list.append(neg)

    return n_neg, ('%.1f' % ((n_neg/n_words)*100)), neg_list


def get_positive_contrast(sentilex, words):
    '''number of sequences where a positive word (unigram) is followed by a negative word'''
    pos_cons_list = []
    n_pos_contrast = 0
    for i in range(len(words)-1):
        if words[i] in sentilex['POSITIVO'] and words[i+1] in sentilex['NEGATIVO']:
            #print(words[i], words[i+1])
            n_pos_contrast += 1
            pos_cons_list.append(words[i])
            pos_cons_list.append(words[i+1])

    return n_pos_contrast, pos_cons_list


def get_negative_contrast(sentilex, words):
    '''number of sequences where a negative word (unigram) is followed by a positive word'''
    neg_cons_list = []
    n_neg_contrast = 0
    for i in range(len(words)-1):
        if words[i] in sentilex['NEGATIVO'] and words[i+1] in sentilex['POSITIVO']:
            #print(words[i], words[i+1])
            n_neg_contrast += 1
            neg_cons_list.append(words[i])
            neg_cons_list.append(words[i+1])

    return n_neg_contrast, neg_cons_list

def replace_original_words(emotion_list, words, original_words):
    #print(words)
    #print(words)
    #print(emotion_list)
    print(original_words)
    sp = spacy.load('pt_core_news_sm')
    for i in range(len(words)):
        words[i] = sp(words[i])
        words[i] = words[i].text.lower()
    print("wordssssssssssssssssssssssssssssssssssssssssssssss")

    #print(words)
    print("original wordssssssssssssssssssssssssssssssssssssssssssssss")

    print(original_words)
    for emo in emotion_list:
        for i in range (len(emotion_list[emo])):
            for j in range(len(words)):
                if(emotion_list[emo][i] == words[j]):
                    #print("entrei")
                    #print(words[j])
                    #print(emotion_list[emo][i])
                    emotion_list[emo][i] = original_words[j]
                    #print(original_words[j])
    print("emotion listttttttttttttttttttttttttttttttttt")
    #print(emotion_list)
