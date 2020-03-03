#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import re
import time
import csv
import spacy
#import concurrent.futures
from unicodedata import normalize
from string import punctuation

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from spacy.lang.pt import Portuguese
#import emoji


# Based on https://github.com/rdenadai/sentiment-analysis-2018-president-election/blob/master/src/ai/utils.py



def load_valence_emotions_from_oplexicon(filename):
    """NEUTRAL | POSITIVE | NEGATIVE."""
    spacy_conv = {
        'adj': 'ADJ',
        'n': 'NOUN',
        'vb': 'VERB',
        'det': 'DET',
        'emot': 'EMOT',
        'htag': 'HTAG'
    }

    data = {
        'POSITIVO': [],
        'NEGATIVO': [],
        'NEUTRO': [],
    }
    with codecs.open(filename, 'r', 'UTF-8') as hf:
        lines = hf.readlines()
        for line in lines:
            info = line.lower().split(',')
            #if len(info[0].split()) <= 1:
            info[0] = info[0].replace('=', ' ')
            info[1] = [spacy_conv.get(tag) for tag in info[1].split()]
            word, tags, sent = info[:3]
            if 'HTAG' not in tags and 'EMOT' not in tags:
                #word = tokenizer(word.lower().strip())
                word = word.lower().strip()
                sent = int(sent)
                if sent == 1:
                    data['POSITIVO'] += [word]
                elif sent == -1:
                    data['NEGATIVO'] += [word]
                else:
                    data['NEUTRO'] += [word]
    data['POSITIVO'] = sorted(list(set(data['POSITIVO'])))
    data['NEGATIVO'] = sorted(list(set(data['NEGATIVO'])))
    data['NEUTRO'] = sorted(list(set(data['NEUTRO'])))
    return data


def load_valence_emotions_from_sentilex(filename):
    """NEUTRAL | POSITIVE | NEGATIVE."""
    data = {
        'POSITIVO': [],
        'NEGATIVO': [],
        'NEUTRO': [],
    }
    with codecs.open(filename, 'r', 'UTF-8') as hf:
        lines = hf.readlines()
        for line in lines:
            info = line.lower().split('.')
            words = [word.strip() for word in info[0].split(',')]
            for word in words:
                #word = tokenizer(word.lower().strip())
                word = word.lower().strip()
                #if len(word) > 2:
                cdata = info[1].split(';')
                if len(cdata) > 0:
                    sent0 = [int(k.replace('pol:n0=', '')) if 'pol:n0=' in k else None for k in cdata]
                    sent1 = [int(k.replace('pol:n1=', '')) if 'pol:n1=' in k else None for k in cdata]
                    sent0 = list(filter(None.__ne__, sent0))
                    sent1 = list(filter(None.__ne__, sent1))
                    #if (len(sent0) >= 1 and len(sent1) <= 0) or (sent0 == sent1) or (sent1 == [0]):

                    if (len(sent0) >= 1 and len(sent1) <= 0):
                        sent = sent0[0]
                        if sent == 1:
                            data['POSITIVO'] += [word]
                        elif sent == -1:
                            data['NEGATIVO'] += [word]
                        else:
                            data['NEUTRO'] += [word]
                    #elif sent0 == [0]:
                    elif (len(sent0) <= 0 and len(sent1) >= 1):
                        #print(word, sent0, sent1)
                        #print(word)
                        sent = sent1[0]
                        if sent == 1:
                            data['POSITIVO'] += [word]
                        elif sent == -1:
                            data['NEGATIVO'] += [word]
                        else:
                            data['NEUTRO'] += [word]
                    else:
                        #print(word, sent0, sent1)
                        pass
                        
    data['POSITIVO'] = sorted(list(set(data['POSITIVO'])))
    data['NEGATIVO'] = sorted(list(set(data['NEGATIVO'])))
    data['NEUTRO'] = sorted(list(set(data['NEUTRO'])))
    return data


def complement_sentilex(sentilex, oplexicon):
    ''' adds oplexicon terms to sentilex '''

    oplexicon_terms = set(oplexicon['POSITIVO'] + oplexicon['NEUTRO'] + oplexicon['NEGATIVO'])
    sentilex_terms = set(sentilex['POSITIVO'] + sentilex['NEUTRO'] + sentilex['NEGATIVO'])
    missing_terms = list(oplexicon_terms - sentilex_terms)

    for term in missing_terms:
        if term in oplexicon['POSITIVO']:
            sentilex['POSITIVO'] += [term]
        elif term in oplexicon['NEUTRO']:
            sentilex['NEUTRO'] += [term]
        elif term in oplexicon['NEGATIVO']:
            sentilex['NEGATIVO'] += [term]
    return sentilex


def load_liwc(filepath):
    '''
    An Evaluation of the Brazilian Portuguese LIWC Dictionary for Sentiment Analysis.
    Balage Filho, P.P.; Aluísio, S.M.; Pardo, T.A.S.
    http://143.107.183.175:21380/portlex/index.php/pt/projetos/liwc
    '''
    load_tags = True

    liwc_tags = dict()

    with open(filepath, 'r', encoding='iso-8859-1') as f:

        next(f)
        for line in f:
            line = line.strip()

            #print(line.strip())
            if '%' in line:
                load_tags = False
            elif load_tags:
                tag = line.split()
                liwc_tags[tag[0]] = {
                    'class': tag[1],
                    'words': []
                }
                
            elif not load_tags:
                line = line.split()
                #print(line)
                for tag in line[1:]:
                    liwc_tags[tag]['words'] += [line[0]]
                
    #print(liwc_tags)
    return liwc_tags


def load_anew_pt(filepath):
    '''
    The adaptation of the affective norms for English words (ANEW) for European Portuguese.
    Ana Paula Soares, Montserrat Comesana, Ana P Pinheiro, Alberto Simões, and Carla Sofia Frade.
    https://link.springer.com/article/10.3758/s13428-011-0131-7
    '''
    nlp = spacy.load('pt_core_news_sm')

    anew = dict()
    with open(filepath, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            vad = {
            'V': float(row[3].replace(',','.')), 
            'A':float(row[5].replace(',','.')), 
            'D':float(row[7].replace(',','.'))
            }
            anew[row[2]] = vad

    #print(anew)
    return anew


def load_anew_extended_pt(filepath):
    ''' loads the extended and translated anew.
    for each PT term in anew, extracts the lemma and the vad values.

    Norms of valence, arousal, and dominance for 13,915 English lemmas
    Amy Beth Warriner, Victor Kuperman, Marc Brysbaert
    https://link.springer.com/article/10.3758%2Fs13428-012-0314-x#SupplementaryMaterial
    '''

    nlp = spacy.load('pt_core_news_sm')

    anew = dict()
    with open(filepath, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            text = nlp(row[2])
            #token.text, token.lemma_

            if len(text) > 1:
                token = row[2]
            else:
                #print(token[0].text, token[0].lemma_)
                token = text[0].lemma_                
            
            vad = {'V': float(row[3]), 'A':float(row[6]), 'D':float(row[9])}
            anew[token] = vad
            #print(token, type(token))
    
    #print(anew)
    return anew
            


def load_six_emotions(filepath):
    """Ekman, Friesen, and Ellsworth : anger, disgust, fear, joy, sadness, surprise."""
    emotion_words = {
        'alegria': _load_emotion_file_content('alegria', filepath),
        'desgosto': _load_emotion_file_content('desgosto', filepath),
        'medo': _load_emotion_file_content('medo', filepath),
        'raiva': _load_emotion_file_content('raiva', filepath),
        'surpresa': _load_emotion_file_content('surpresa', filepath),
        'tristeza': _load_emotion_file_content('tristeza', filepath),
    }
    return emotion_words



def load_subjectivity_lexicon(filepath):
    '''
    Recognizing Contextual Polarity in Phrase-Level Sentiment Analysis.
    Theresa Wilson, Janyce Wiebe, and Paul Hoffmann (2005). 
    http://mpqa.cs.pitt.edu/lexicons/subj_lexicon/
    '''

    #subjectivity: strongsubj or weaksubj   
    #polarity: positive, negative, both, neutral
 
    lex = {'strongsubj':[], 'weaksubj':[]}

    with open(filepath, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)

        for row in csv_reader:
            stem = STEMMER.stem(row[3])
            #lex[stem] = {'strongsubj':0, 'weaksubj':0}
            if row[0] == 'strongsubj':
                lex['strongsubj'] += [stem]
            elif row[0] == 'weaksubj':
                lex['weaksubj'] += [stem]

    all_words = list(set(lex['strongsubj'] + lex['weaksubj']))

    for w in all_words:
        if lex['weaksubj'].count(w) > lex['strongsubj'].count(w):
            lex['strongsubj'] = list(filter((w).__ne__, lex['strongsubj']))
        elif lex['weaksubj'].count(w) < lex['strongsubj'].count(w):
            lex['weaksubj'] = list(filter((w).__ne__, lex['weaksubj']))
        else:
            lex['strongsubj'] = list(filter((w).__ne__, lex['strongsubj']))
            lex['weaksubj'] = list(filter((w).__ne__, lex['weaksubj']))

    return lex



def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')


def is_number(s):
    try:
        complex(s) # for int, long, float and complex
    except ValueError:
        return False
    return True


def _get_stopwords():
    stpwords = stopwords.words('portuguese')
    rms = ['um', 'não', 'mais', 'muito']
    for rm in rms:
        del stpwords[stpwords.index(rm)]
    return stpwords, punctuation


def generate_corpus(documents=None, debug=False):
    assert len(documents) > 0
    if debug: print('Iniciando processamento...')
    tokenized_docs = documents
    #with concurrent.futures.ProcessPoolExecutor() as procs:
    #    if debug: print('Executando processo de remoção das stopwords...')
    #    tokenized_frases = procs.map(tokenizer, tokenized_docs, chunksize=25)
    if debug: print('Finalizado...')
    return list(tokenized_frases)


def tokenizer(phrase, clean=False):
    if not clean:
        phrase = clean_up(phrase, False)
    clean_frase = []
    clfa = clean_frase.append
    for palavra in phrase:
        palavra = ''.join([word.lemma_ for word in NLP(palavra)])
        clfa(STEMMER.stem(palavra))
    return ' '.join(clean_frase)


def clean_up(phrase, join=True):
    STOPWORDS, PUNCT = _get_stopwords()
    # Transforma as hashtags em palavras
    try:
        for group in re.findall(r'#\S+\b', phrase, re.DOTALL):
            g2 = re.sub(r'([A-Z])', r' \1', group, flags=re.MULTILINE)
            phrase = re.sub(r'{}\b'.format(group), g2, phrase, flags=re.MULTILINE)
    except Exception:
        pass
    # lowercase para fazer outros pre-processamentos
    phrase = phrase.lower()
    #phrase = emoji.get_emoji_regexp().sub(r'', phrase)
    for stw in STOPWORDS:
        phrase = re.sub(r'\b{}\b'.format(stw), '', phrase, flags=re.MULTILINE)
    for punct in PUNCT:
        phrase = phrase.replace(punct, ' ')
    for o, r in RM:
        phrase = re.sub(o, r, phrase, flags=re.MULTILINE)

    # Limpeza extra
    phrase = word_tokenize(phrase)
    clean_frase = []
    clfa = clean_frase.append
    for palavra in phrase:
        if not is_number(palavra) and len(palavra) > 2:
            clfa(palavra)
    return ' '.join(clean_frase) if join else clean_frase



def _load_emotion_file_content(emotion, path):
    with open('{}/{}'.format(path,emotion), 'r') as h:
        words = h.readlines()
        for i, word in enumerate(words):
            word = word.replace('\n', '').lower().strip()
            words[i] = tokenizer(word)
            # words[i] = [w.lemma_ for w in NLP(word, disable=['parser'])][0]
    return sorted(list(set(words)))








def load_3_emotions(filepath):
    """Ekman, Friesen, and Ellsworth : anger, disgust, fear, joy, sadness, surprise."""
    emotion_words = {
        'POSITIVO': _load_emotion_file_content('positivo', filepath),
        'NEGATIVO': _load_emotion_file_content('negativo', filepath),
        'NEUTRO': _load_emotion_file_content('neutro', filepath),
    }
    return emotion_words



def load_valence_emotions(filename_oplexicon, filename_sentilex):
    data = {
        'POSITIVO': [],
        'NEGATIVO': [],
        'NEUTRO': [],
    }

    oplexicon = load_valence_emotions_from_oplexicon(filename_oplexicon)
    sentilex = load_valence_emotions_from_sentilex(filename_sentilex)

    data['POSITIVO'] = oplexicon['POSITIVO'] + sentilex['POSITIVO']
    data['NEGATIVO'] = oplexicon['NEGATIVO'] + sentilex['NEGATIVO']
    data['NEUTRO'] = oplexicon['NEUTRO'] + sentilex['NEUTRO']
    data['POSITIVO'] = sorted(list(set(data['POSITIVO'])))
    data['NEGATIVO'] = sorted(list(set(data['NEGATIVO'])))
    data['NEUTRO'] = sorted(list(set(data['NEUTRO'])))
    return data



# GLOBALS
NLP = Portuguese()
# STEMMER = nltk.stem.RSLPStemmer()
STEMMER = nltk.stem.SnowballStemmer('portuguese')
STOPWORDS, PUNCT = _get_stopwords()
RM = [
    (r'(http[s]*?:\/\/)+.*[\r\n]*', r''), (r'@', r''),
    (r'\n+', r' . '), (r'"', r' '), (r'\'', r' '),
    (r'#', r''), (r'(RT)', r''), (r'[…]', ' . '), (r'[0-9]*', r''),
    (r'“', r''), (r'”', ''), (r'([aeiouqwtyupdfghjklçzxcvbnm|!@$%&\.\[\]\(\)+-_=<>,;:])\1+', r'\1'),
    (r'(\bñ\n)', 'não'), (r'(nã)', 'não'), (r'\s+', r' '), (r'(nãoo)', 'não'),
]





def main():
    print('Hello')
    filename_oplexicon = '/home/revy/Work/lexicons/oplexico_v3.0.txt'
    filename_sentilex = '/home/revy/Work/lexicons/SentiLex-flex-PT02.txt'
    #filename_anew = '/home/revy/Work/lexicons/anew-pt.csv'
    filename_anew_extended = '/home/revy/Work/lexicons/BRM-emot-submit-pt.csv'
    filename_anew = '/home/revy/Work/lexicons/anew-pt.csv'
    filename_emotions = '/home/revy/Work/lexicons/emotions'
    filename_subjectivity = '/home/revy/Work/lexicons/subjectivity-clues-pt.csv'
    
    #oplexicon = load_valence_emotions_from_oplexicon(filename_oplexicon)
    #sentilex = load_valence_emotions_from_sentilex(filename_sentilex)
    #print(len(sentilex['POSITIVO']), len(sentilex['NEUTRO']), len(sentilex['NEGATIVO']))
    #sentilex = complement_sentilex(sentilex,oplexicon)
    #print(len(sentilex['POSITIVO']), len(sentilex['NEUTRO']), len(sentilex['NEGATIVO']))

    #anew = load_anew_pt(filename_anew)
    anew_extended = load_anew_extended_pt(filename_anew_extended)
    #anew_extended.update(anew)

    #emotion_words = load_six_emotions(filename_emotions)
    #print(emotion_words)

    #subj = load_subjectivity_lexicon(filename_subjectivity)
    #print(len(subj['weaksubj']))
    #print(len(subj['strongsubj']))

    #for w in subj['weaksubj']:
    #    if w in subj['strongsubj']:
    #        print(w)
    #for w in subj['strongsubj']:
    #    if w in subj['weaksubj']:
    #        print(w)

    #print(subj)



if __name__== "__main__":
    main()
