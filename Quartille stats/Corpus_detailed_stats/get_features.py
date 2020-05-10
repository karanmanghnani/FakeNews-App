#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pickle
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import os, sys
import datetime
import subprocess
#import hunspell
import spacy
import statistics 
import get_lexicons as lex
import xlsxwriter


STEMMER = nltk.stem.SnowballStemmer('portuguese')
sp = spacy.load('pt_core_news_sm')

def tokenize_sentences(document):
    sent_tokens = sent_tokenize(document)
    #print(sent_tokens)

    sentences = []
    for token in sent_tokens:
        sentences += token.split('\n')

    return sentences 


def spacy_statistics(sentences):
    spacy_stats = []
    '''
    for i in range(len(sentences)):
        spacy_stats += sp(sentences[i])
        for word in sp(sentences[i]):
            print(word.text, word.pos_, word.dep_, word.lemma_ )
    print(spacy_stats)'''
    return spacy_stats



def lemmatize_words(sentences):
    lemmas = []

    for i in range(len(sentences)):
        for word in sp(sentences[i]):
            if word.pos_ != 'PUNCT':
                lemmas += [word.lemma_.lower()]
    return lemmas


def tokenize_words(sentences):
    tokens = []

    for i in range(len(sentences)):
        for word in sp(sentences[i]):
            #print(word.text, word.pos_, word.dep_, )
            if word.pos_ != 'PUNCT':
                tokens += [word.text.lower()]
    return tokens


def process_tags(postags_clean, tags):

    #tags sanity check
    for token in postags_clean:
        if len(token) not in [2,3]:
            #problem with tags length
            print('ATTENTION: ERROR!!!!')
            print(token)
            sys.exit(0)

    for token in postags_clean:
        tag = token[-1]

        if tag.startswith('A'):
            #print(token[0], 'adjective')
            tags['adjective'] += [token]
        elif tag.startswith('C'):
            #print(token[0], 'conjunction')
            tags['conjunction'] += [token]
        elif tag.startswith('D'):
            #print(token[0], 'determiner')
            tags['determiner'] += [token]            
        elif tag.startswith('N'):
            #print(token[0], 'noun')
            tags['noun'] += [token]
        elif tag.startswith('P'):
            #print(token[0], 'pronoun')
            tags['pronoun'] += [token]
        elif tag.startswith('R'):
            #print(token[0], 'adverb')
            tags['adverb'] += [token]
        elif tag.startswith('S'):
            #print(token[0], 'adposition')
            tags['adposition'] += [token]
        elif tag.startswith('V'):
            #print(token[0], 'verb')
            tags['verb'] += [token]
        elif tag.startswith('Z'):
            #print(token[0], 'number')
            tags['number'] += [token]
        elif tag.startswith('W'):
            #print(token[0], 'date')
            tags['date'] += [token]
        elif tag.startswith('I'):
            #print(token[0], 'interjection')
            tags['interjection'] += [token]
        elif tag.startswith('F'):
            #print(token[0], 'punctuation')
            tags['punctuation'] += [token]
        #elif tag.startswith(''):

    #print(tags)
    return tags


def citiustagger_sent(sent, tagger_path, sent_path, doc_citiustags):

    #add period to the sentence to delimit the end.
    sent += '.'

    #write sentence to file.
    file = open(sent_path,'w', encoding='utf-8') 
    file.write(sent) 
    file.close()

    #print(sent)

    #call citius tools
    result = subprocess.run('cd {}; sh nec.sh pt {}'.format(tagger_path, sent_path), shell=True, stdout=subprocess.PIPE)
    postags = result.stdout.decode("utf-8").strip().split('\n')
    #print(postags)
    postags_clean = []

    for token in postags:
        if token:
            postags_clean += [token.split()]
    
    #remove period added before
    last_token = postags_clean[-1][0]
    if last_token == '.':
        postags_clean.pop(-1)

    #print(postags_clean)
    doc_citiustags = process_tags(postags_clean, doc_citiustags)


def citiustagger_doc(doc, tagger_path, sent_path):

    doc_citiustags = {
        'adjective': [],
        'conjunction': [],
        'determiner': [],
        'noun': [],
        'pronoun': [],
        'adverb': [],
        'adposition': [],
        'verb': [],
        'number': [],
        'date': [],
        'interjection': [],
        'punctuation': []
    }

    for sent in doc:
        citiustagger_sent(sent, tagger_path, sent_path, doc_citiustags)

    return doc_citiustags


def get_content_diversity(doc_citiustags):
    ''' total number of different content words (nouns, verbs, adjectives, adverbs) over the total number of content words '''
    content_words = []
    keys = ['adjective', 'adverb', 'noun', 'verb']
    
    for k in keys:
        for w in doc_citiustags[k]:
            #print(w)
            if len(w) == 3:
                content_words += [w[1]]
            elif len(w) == 2:
                content_words += [w[0]]
    #print(set(content_words))
    return round(len(set(content_words))/len(content_words), 4)


def get_redundancy(n_sentences, doc_citiustags):
    ''' total number of function words (prepositions, pronouns, conjunctions, determiner) over the total number of sentences '''

    function_words = doc_citiustags['adposition'] + doc_citiustags['pronoun'] + doc_citiustags['conjunction'] + doc_citiustags['determiner']

    return  round(len(function_words)/n_sentences, 4)


def get_pausality(n_sentences, doc_citiustags):
    ''' the number of punctuation signals over the number of sentences '''

    n_punct = len(doc_citiustags['punctuation'])

    return round(n_punct/n_sentences, 4)


def get_emotiveness(doc_citiustags):
    ''' the sum of the number of adjectives and adverbs over the sum of nouns and verbs '''

    n_adjs = len(doc_citiustags['adjective'])
    n_advs = len(doc_citiustags['adverb'])
    n_nouns = len(doc_citiustags['noun'])
    n_verbs =  len(doc_citiustags['verb'])

    return round((n_adjs+n_advs)/(n_nouns+n_verbs), 4)


def get_non_immediacy(doc_citiustags, words):
    ''' the (normalized) number of 1st and 2nd pronouns '''

    n_words = len(words)
    pronouns = doc_citiustags['pronoun']

    n_12p = 0
    for pronoun in pronouns:
        tag = pronoun[-1]
        #person = tag[2]
        if tag[2] in ['1', '2']:
            n_12p += 1 

    #normalized by the number of sentences 
    return round(n_12p/n_words, 4)


def get_verbs_ratio(doc_citiustags, words):
    '''number of verbs over the number of words'''

    n_words = len(words)
    n_verbs = len(doc_citiustags['verb'])

    return round(n_verbs/n_words, 4)


def get_nouns_ratio(doc_citiustags, words):
    '''number of nouns over the number of words'''

    n_words = len(words)
    n_nouns = len(doc_citiustags['noun'])

    return round(n_nouns/n_words, 4)


def get_adjectives_ratio(doc_citiustags, words):
    '''number of adjectives over the number of words'''

    n_words = len(words)
    n_adjs = len(doc_citiustags['adjective'])

    return round(n_adjs/n_words, 4)


def get_modifiers_ratio(doc_citiustags, words):
    '''number of modifiers (adjectives and adverbs) over the number of words'''
    
    n_words = len(words)
    n_adjs = len(doc_citiustags['adjective'])
    n_advs = len(doc_citiustags['adverb'])

    return round((n_adjs+n_advs)/n_words, 4)


def get_typographical_error_ratio(words):
    ''' total number of misspelled words over total number of words '''
    #https://datascience.blog.wzb.eu/2016/07/13/autocorrecting-misspelled-words-in-python-using-hunspell/
    #https://natura.di.uminho.pt/download/sources/Dictionaries/hunspell/

    n_words = len(words)

    misspelled = 0
    spellchecker = hunspell.HunSpell('/usr/share/hunspell/pt_PT.dic',
                                     '/usr/share/hunspell/pt_PT.aff')
    
    for word in words:
        if not spellchecker.spell(word.lower()):
            misspelled += 1
            #print(word)

    return round(misspelled/n_words, 4)


def get_negation_words_ratio(liwc_tags, words):
    '''number of negation words over the number of words'''
    # liwc categories: [19] negation

    n_words = len(words)

    n_negation_words = 0
    for word in words:
        if (word in liwc_tags['19']['words']):
            #print(word) 
            n_negation_words += 1

    return round(n_negation_words/n_words, 4)


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

    return round(n_perceptual_words/n_words, 4)


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

    return round(n_relativity_words/n_words, 4)


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

    return round(n_cognitive_words/n_words, 4)

    
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

    return round(n_personal_concerns_words/n_words, 4)


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

    return round(n_social_words/n_words, 4)


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

    return round(n_biological_words/n_words, 4)




def get_positive_words_ratio(sentilex, words):
    '''number of potentially positive words over the number of words'''

    n_words = len(words)
    text = ' ' + ' '.join(words) + ' '

    n_pos = 0
    for pos in sentilex['POSITIVO']:
        if ' ' + pos + ' ' in text:
            n_pos += 1
    
    return round(n_pos/n_words, 4)


def get_negative_words_ratio(sentilex, words):
    '''number of potentially negative words over the number of words'''

    n_words = len(words)
    text = ' ' + ' '.join(words) + ' '

    n_neg = 0
    for neg in sentilex['NEGATIVO']:
        if ' ' + neg + ' ' in text:
            n_neg += 1

    return round(n_neg/n_words, 4)


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


def get_vad_features(anew, lemmas):
    V, A, D = [], [], []
    total = 0

    for lemma in lemmas:

        if lemma in anew.keys():
            #print(lemma, ' lemma found')
            #print(lemma)
            V += [anew[lemma]['V']]
            A += [anew[lemma]['A']]
            D += [anew[lemma]['D']]
            total += 1
        #else:
        #    print(lemma, ' lemma not found')
    vad_features = {
        'valence_avg': round(statistics.mean(V) , 4),
        'valence_std': round(statistics.stdev(V), 4),
        'valence_max': round(max(V), 4),
        'valence_min': round(min(V), 4),
        'valence_dif': round(max(V) - min(V), 4),
        'arousal_avg': round(statistics.mean(A), 4),
        'arousal_std': round(statistics.stdev(A), 4),
        'arousal_max': round(max(A), 4),
        'arousal_min': round(min(A), 4),
        'arousal_dif': round(max(A) - min(A), 4),
        'dominance_avg': round(statistics.mean(D), 4),
        'dominance_std': round(statistics.stdev(D), 4),
        'dominance_max': round(max(D), 4),
        'dominance_min': round(min(D), 4),
        'dominance_dif': round(max(D) - min(D), 4),
        'total': total,
    }

    #print(V,A,D)
    #print(vad_features)
    return  vad_features


def get_six_emotions_features(emotion_words, words):

    six_emotions = list(emotion_words.keys())
    emotion_feats = {k:0 for k in six_emotions}
    n_emotions = 0

    for word in words:
        stem = STEMMER.stem(word)
        for emo in six_emotions:
            if stem in emotion_words[emo]:
                #print(word, stem, emo)
                emotion_feats[emo] += 1
                n_emotions +=1

    if n_emotions:
        emotion_feats.update({k:round(emotion_feats[k]/n_emotions, 4) for k in six_emotions})
    print(emotion_feats)
    print(n_emotions)

    return emotion_feats, n_emotions




def get_subjective_ratio(subjective_words, words):

    #six_emotions = list(emotion_words.keys())
    subj_feats = {'strongsubj':0, 'weaksubj':0}
    n_words = len(words)
    total = 0

    for word in words:
        stem = STEMMER.stem(word)
        if stem in subjective_words['strongsubj']:
            subj_feats['strongsubj'] += 1
            total += 1
            #print('strongsubj', word, stem)
        elif stem in subjective_words['weaksubj']:
            subj_feats['weaksubj'] += 1
            total += 1
            #print('weaksubj', word, stem)

    subj_feats.update({k:round(v/n_words, 4) for k,v in subj_feats.items()})
    
    #print(subj_feats)
    return subj_feats, total



def load_fakebr_corpus(fakebr_corpus_path):
    corpus = {'fake': {}, 'true': {}}
    classes = ['fake', 'true']
    for cls in classes:
        encodings = dict()
        with open('{}{}/{}_encoding.txt'.format(fakebr_corpus_path,cls,cls), 'r') as fe:
            lines = fe.readlines()
            for line in lines:
                line = line.split()
                encodings[line[0].replace(':', '')] = line[2].replace('charset=', '')
        #print(encodings)

        for file in os.listdir('{}{}'.format(fakebr_corpus_path,cls)):
            filename = '{}{}/{}'.format(fakebr_corpus_path, cls, os.fsdecode(file))

            if file == '{}_encoding.txt'.format(cls):
                continue
            elif encodings[file] == 'utf-8':
                with open(filename, 'r', encoding='utf-8') as f:
                    doc = f.readlines()
                    doc = ' '.join(doc)
                    #doc = doc.replace(u'\xa0', u' ')
            elif encodings[file] == 'iso-8859-1':
                with open(filename, 'r', encoding='iso-8859-1') as f:
                
                    doc = f.readlines()
                    doc = ' '.join(doc)
                    
            else:       
                print(cls, file, encodings[file])
                #sys.exit(0)

            id_doc = int(file.replace('.txt',''))
            corpus[cls].update({id_doc:doc.replace('\ufeff', '')})  

    return corpus



def prepare_lexicons(base_dir):

    liwc_pt_path = '{}lexicons/LIWC2007_Portugues_win.dic.txt'.format(base_dir)
    oplexicon_path = '{}lexicons/oplexico_v3.0.txt'.format(base_dir)
    sentilex_path = '{}lexicons/SentiLex-flex-PT02.txt'.format(base_dir)
    filename_anew = '{}lexicons/anew-pt.csv'.format(base_dir)
    filename_anew_extended = '{}lexicons/BRM-emot-submit-pt.csv'.format(base_dir)
    filename_emotions = '{}lexicons/emotions'.format(base_dir)
    filename_subjectivity = '{}lexicons/subjectivity-clues-pt.csv'.format(base_dir)

    liwc_tags = lex.load_liwc(liwc_pt_path)
    with open('{}proc_lexicons/liwc.pkl'.format(base_dir), 'wb') as f:
        pickle.dump(liwc_tags,f)
    print('Done LIWC.')

    oplexicon = lex.load_valence_emotions_from_oplexicon(oplexicon_path)
    sentilex = lex.load_valence_emotions_from_sentilex(sentilex_path)
    sentilex = lex.complement_sentilex(sentilex,oplexicon)
    with open('{}proc_lexicons/sentilex.pkl'.format(base_dir), 'wb') as f:
        pickle.dump(sentilex,f)
    print('Done Sentilex.')
    
    anew = lex.load_anew_pt(filename_anew)
    anew_extended = lex.load_anew_extended_pt(filename_anew_extended)
    anew_extended.update(anew)
    with open('{}proc_lexicons/anew.pkl'.format(base_dir), 'wb') as f:
        pickle.dump(anew_extended,f)
    print('Done ANEW.')

    emotion_words = lex.load_six_emotions(filename_emotions)
    with open('{}proc_lexicons/emotion_words.pkl'.format(base_dir), 'wb') as f:
        pickle.dump(emotion_words,f)
    print('Done Emotion words.')

    subjective_words = lex.load_subjectivity_lexicon(filename_subjectivity)
    with open('{}proc_lexicons/subjective_words.pkl'.format(base_dir), 'wb') as f:
        pickle.dump(subjective_words,f)
    print('Done Subjective words.')


def load_lexicons(base_dir):
    with open('{}proc_lexicons/liwc.pkl'.format(base_dir), 'rb') as f:
        liwc_tags = pickle.load(f)
    print('Done LIWC.')

    with open('{}proc_lexicons/sentilex.pkl'.format(base_dir), 'rb') as f:
        sentilex = pickle.load(f)
    print('Done Sentilex.')
    
    with open('{}proc_lexicons/anew.pkl'.format(base_dir), 'rb') as f:
        anew_extended = pickle.load(f)
    print('Done ANEW.')

    with open('{}proc_lexicons/emotion_words.pkl'.format(base_dir), 'rb') as f:
        emotion_words = pickle.load(f)
    print('Done Emotion words.')

    with open('{}proc_lexicons/subjective_words.pkl'.format(base_dir), 'rb') as f:
        subjective_words = pickle.load(f)
    print('Done Subjective words.')

    return liwc_tags, sentilex, anew_extended, emotion_words, subjective_words



def main():

    try:
        base_dir = sys.argv[1]
    except Exception as e:
        print('\nATTENTION: You should provide the base directory as a parameter!!\n')
        sys.exit(0)
    


    
    lower_limit = 1
    upper_limit = 1000

    tagger_path = '{}/CitiusTools/'.format(base_dir)
    
    fakebr_corpus_path = '{}Fake.br-Corpus/full_texts/'.format(base_dir)
    sent_path = '{}temp_file_{}_{}.txt'.format(base_dir, lower_limit, upper_limit)

    now = datetime.datetime.now()
    print('{} Loading lexicons'.format(now.strftime("%Y-%m-%d %H:%M:%S")))
    #prepare_lexicons(base_dir)
    liwc_tags, sentilex, anew_extended, emotion_words, subjective_words = load_lexicons(base_dir)

    now = datetime.datetime.now()
    print('{} Loading corpus'.format(now.strftime("%Y-%m-%d %H:%M:%S")))

    corpus_fakebr = load_fakebr_corpus(fakebr_corpus_path)

    workbook = xlsxwriter.Workbook('BD_results_corpus_detailed.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0,"Label")
    worksheet.write(0, 1,"alegria")
    worksheet.write(0, 2,"desgosto")
    worksheet.write(0, 3,"medo")
    worksheet.write(0, 4,"raiva")
    worksheet.write(0, 5,"surpresa")
    worksheet.write(0, 6,"tristeza")

    worksheet.write(0, 7,"strongsubj")
    worksheet.write(0, 8,"weaksubj")

    worksheet.write(0, 9,"valence_avg")
    worksheet.write(0, 10,"valence_std")
    worksheet.write(0, 11,"valence_max")
    worksheet.write(0, 12,"valence_min")
    worksheet.write(0, 13,"valence_dif")

    worksheet.write(0, 14,"arousal_avg")
    worksheet.write(0, 15,"arousal_std")
    worksheet.write(0, 16,"arousal_max")
    worksheet.write(0, 17,"arousal_min")
    worksheet.write(0, 18,"arousal_dif")

    worksheet.write(0, 19,"dominance_avg")
    worksheet.write(0, 20,"dominance_std")
    worksheet.write(0, 21,"dominance_max")
    worksheet.write(0, 22,"dominance_min")
    worksheet.write(0, 23,"dominance_dif")

    worksheet.write(0, 24,"pos_words")
    worksheet.write(0, 25,"neg_words")

    worksheet.write(0, 26,"perceptuality")
    worksheet.write(0, 27,"relativity")
    worksheet.write(0, 28,"cognitivity")
    worksheet.write(0, 29,"personal")
    worksheet.write(0, 30,"biological")
    worksheet.write(0, 31,"social")

    row=1
    col=0

    #sys.exit(0)

    for k,v in corpus_fakebr.items():
        print(k)

        id_docs = sorted(corpus_fakebr[k].keys())

        for id_doc in id_docs:

            if id_doc >= lower_limit and id_doc < upper_limit:
            #if id_doc == 2814:
                doc = corpus_fakebr[k][id_doc]
                print(k,id_doc)

                sentences = tokenize_sentences(doc)
                #print(sentences)
                words = tokenize_words(sentences)
                #print(words)
                lemmas = lemmatize_words(sentences)
                #print(lemmas)
                #doc_citiustags = citiustagger_doc(sentences, tagger_path, sent_path)
                #print(doc_citiustags)

                doc_stats = {}
                
                doc_stats['n_sents'] = len(sentences)
                #doc_stats['informality'] = get_typographical_error_ratio(words)
                
                """doc_stats['verbs_ratio'] = get_verbs_ratio(doc_citiustags, words)
                doc_stats['adjs_ratio'] = get_adjectives_ratio(doc_citiustags, words)
                doc_stats['nouns_ratio'] = get_nouns_ratio(doc_citiustags, words)
                doc_stats['content_diversity'] = get_content_diversity(doc_citiustags)
                doc_stats['redundancy'] = get_redundancy(doc_stats['n_sents'], doc_citiustags)
                doc_stats['pausality'] = get_pausality(doc_stats['n_sents'], doc_citiustags)
                doc_stats['expressivity'] = get_emotiveness(doc_citiustags)
                doc_stats['non_immediacy'] = get_non_immediacy(doc_citiustags, words)
                doc_stats['modifiers_ratio'] = get_modifiers_ratio(doc_citiustags, words)"""
                
                doc_stats['perceptuality'] = get_perceptuality(liwc_tags, words)
                doc_stats['relativity'] = get_relativity(liwc_tags, words)
                doc_stats['cognitivity'] = get_cognitivity(liwc_tags, words)
                doc_stats['personal_concerns'] = get_personal_concerns(liwc_tags, words)
                doc_stats['biological_processes'] = get_biological_processes(liwc_tags, words)
                doc_stats['social_processes'] = get_social_processes(liwc_tags, words)
                doc_stats['negation_words_ratio'] = get_negation_words_ratio(liwc_tags, words)
                
                doc_stats['positive_ratio'] = get_positive_words_ratio(sentilex, words)
                doc_stats['negative_ratio'] = get_negative_words_ratio(sentilex, words)
                doc_stats['positive_contrast'] = get_positive_contrast(sentilex, words)
                doc_stats['negative_contrast'] = get_negative_contrast(sentilex, words)
                #doc_stats = {}
                temp_vad = get_vad_features(anew_extended, lemmas)
                temp_emotions, n_emotions = get_six_emotions_features(emotion_words, words)
                #print(get_subjective_ratio(subjective_words, words))
                temp_subj, n_subj = get_subjective_ratio(subjective_words, words)


                worksheet.write(row, col, k)
                col+=1

                worksheet.write(row, col, temp_emotions['alegria']*100)
                col+=1
                worksheet.write(row, col, temp_emotions['desgosto']*100)
                col+=1
                worksheet.write(row, col, temp_emotions['medo']*100)
                col+=1
                worksheet.write(row, col, temp_emotions['raiva']*100)
                col+=1
                worksheet.write(row, col, temp_emotions['surpresa']*100)
                col+=1
                worksheet.write(row, col, temp_emotions['tristeza']*100)
                col+=1

                worksheet.write(row, col, temp_subj['strongsubj'])
                col+=1
                worksheet.write(row, col, temp_subj['weaksubj'])
                col+=1

                worksheet.write(row, col, temp_vad['valence_avg'])
                col+=1
                worksheet.write(row, col, temp_vad['valence_std'])
                col+=1
                worksheet.write(row, col, temp_vad['valence_max'])
                col+=1
                worksheet.write(row, col, temp_vad['valence_min'])
                col+=1
                worksheet.write(row, col, temp_vad['valence_dif'])
                col+=1
                worksheet.write(row, col, temp_vad['arousal_avg'])
                col+=1
                worksheet.write(row, col, temp_vad['arousal_std'])
                col+=1
                worksheet.write(row, col, temp_vad['arousal_max'])
                col+=1
                worksheet.write(row, col, temp_vad['arousal_min'])
                col+=1
                worksheet.write(row, col, temp_vad['arousal_dif'])
                col+=1
                worksheet.write(row, col, temp_vad['dominance_avg'])
                col+=1
                worksheet.write(row, col, temp_vad['dominance_std'])
                col+=1
                worksheet.write(row, col, temp_vad['dominance_max'])
                col+=1
                worksheet.write(row, col, temp_vad['dominance_min'])
                col+=1
                worksheet.write(row, col, temp_vad['dominance_dif'])
                col+=1
                    
                worksheet.write(row, col, doc_stats['positive_ratio']*100)
                col+=1

                worksheet.write(row, col, doc_stats['negative_ratio']*100)
                col+=1

                worksheet.write(row, col, doc_stats['perceptuality']*100)
                col+=1

                worksheet.write(row, col, doc_stats['relativity']*100)
                col+=1

                worksheet.write(row, col, doc_stats['cognitivity']*100)
                col+=1

                worksheet.write(row, col, doc_stats['personal_concerns']*100)
                col+=1

                worksheet.write(row, col, doc_stats['biological_processes']*100)
                col+=1

                worksheet.write(row, col, doc_stats['social_processes']*100)

                col=0
                row+=1
                #print(doc_stats)

                with open('{}feats/{}/{}.pkl'.format(base_dir, k, id_doc), 'wb') as f:
                    pickle.dump(doc_stats,f)

                #with open('{}feats/{}/{}.pkl'.format(base_dir, k, id_doc), 'rb') as f:
                #    loaded_doc_feats = pickle.load(f)
                #print (doc_stats == loaded_doc_feats)

    workbook.close()
    now = datetime.datetime.now()
    print('{} Done generating features'.format(now.strftime("%Y-%m-%d %H:%M:%S")))

            

    
    #doc_stats['uncertainty'] = ''
    #doc_stats['specificity'] = doc_stats['relativity'] + doc_stats['perceptuality']
    



if __name__== "__main__":
    main()


def get_pos_tag(text):
    ''' the (normalized) number of occurrences of each part of speech tag (NLPNet tagger) '''
    pass


def get_uncertainty():
    ''' the (normalized) number of modal verbs and occurrences of passive voice '''
    return

#http://www.cs.columbia.edu/~julia/papers/dict_of_affect/DictionaryofAffect
#16.  Affect: conscious subjective aspect of a emotion apart from bodily changes
#17.  Pleasantness: positive or negative feelings associated with the emotional state.
#18.  Activation: the dynamics of emotional state.
#19.  Imagery: words that provide a clear mental picture.
# emotion


