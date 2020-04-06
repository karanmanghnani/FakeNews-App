
# Program extracting first column 
import xlrd 
import unidecode
import /home/karan/Desktop/FakeNews-App/get_metrics as metrics

news = {}
loc = ("Noticías_BD.xlsx") 
  
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
sheet.cell_value(0, 0) 
liwc_tags, sentilex, anew_extended, emotion_words, subjective_words = metrics.load_lexicons()
  
""" news = 1:['noticia', vericidade]"""
for i in range(1,31):
	news[i] = [sheet.cell_value(i, 1),sheet.cell_value(i, 3)]
	#print(sheet.cell_value(i, 3))

#print(news[1][0])
for i in range(1,31):
	sentences = metrics.tokenize_sentences(news[i][0])
	lemmas = metrics.lemmatize_words(sentences)
	words = metrics.tokenize_words(sentences)

	emotion_count,emotion_ratio,total_emotion  = metrics.get_emotions(news[i][0])
	news[i].append("total emotion:" + str(total_emotion))

	totalsubj, subj_feats = metrics.get_subjective_ratio(words, subjective_words)
	news[i].append("total subj: " + str(totalsubj))

	vad_features = metrics.get_vad_features(lemmas, anew_extended)
	news[i].append("total vad: " + str(vad_features['total_vad']))

	polarity = metrics.sentiment_polarity(words, sentilex)
	news[i].append("total polarity:" + str(polarity['total_pol']))

	bp_stats = metrics.behavioral_physiological(words, liwc_tags)
	news[i].append("total BP:" + str( bp_stats['total_bp']))

print(news)
