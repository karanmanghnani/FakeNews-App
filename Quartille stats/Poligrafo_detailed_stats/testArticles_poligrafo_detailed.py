import xlrd 
import unidecode
import get_metrics as metrics
import xlsxwriter

workbook = xlsxwriter.Workbook('BD_results_detailed.xlsx')
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

loc = ("Noticías_BD.xlsx") 
  
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
sheet.cell_value(0, 0) 
liwc_tags, sentilex, anew_extended, emotion_words, subjective_words = metrics.load_lexicons()
  
for i in range(1,sheet.nrows):
	worksheet.write(row, col, sheet.cell_value(i, 3))
	row+=1

row=1
col=1

for i in range(1,sheet.nrows):
	sentences = metrics.tokenize_sentences(sheet.cell_value(i, 1))
	lemmas = metrics.lemmatize_words(sentences)
	words = metrics.tokenize_words(sentences)

	emotion_ratio,total_emotion  = metrics.get_emotions(words, emotion_words)
	worksheet.write(row, col, emotion_ratio['alegria']*100)
	col+=1
	worksheet.write(row, col, emotion_ratio['desgosto']*100)
	col+=1
	worksheet.write(row, col, emotion_ratio['medo']*100)
	col+=1
	worksheet.write(row, col, emotion_ratio['raiva']*100)
	col+=1
	worksheet.write(row, col, emotion_ratio['surpresa']*100)
	col+=1
	worksheet.write(row, col, emotion_ratio['tristeza']*100)
	col+=1

	totalsubj, subj_feats = metrics.get_subjective_ratio(words, subjective_words)
	worksheet.write(row, col, subj_feats['strongsubj'])
	col+=1
	worksheet.write(row, col, subj_feats['weaksubj'])
	col+=1

	vad_features = metrics.get_vad_features(lemmas, anew_extended)
	worksheet.write(row, col, vad_features['valence_avg'])
	col+=1
	worksheet.write(row, col, vad_features['valence_std'])
	col+=1
	worksheet.write(row, col, vad_features['valence_max'])
	col+=1
	worksheet.write(row, col, vad_features['valence_min'])
	col+=1
	worksheet.write(row, col, vad_features['valence_dif'])
	col+=1
	worksheet.write(row, col, vad_features['arousal_avg'])
	col+=1
	worksheet.write(row, col, vad_features['arousal_std'])
	col+=1
	worksheet.write(row, col, vad_features['arousal_max'])
	col+=1
	worksheet.write(row, col, vad_features['arousal_min'])
	col+=1
	worksheet.write(row, col, vad_features['arousal_dif'])
	col+=1
	worksheet.write(row, col, vad_features['dominance_avg'])
	col+=1
	worksheet.write(row, col, vad_features['dominance_std'])
	col+=1
	worksheet.write(row, col, vad_features['dominance_max'])
	col+=1
	worksheet.write(row, col, vad_features['dominance_min'])
	col+=1
	worksheet.write(row, col, vad_features['dominance_dif'])
	col+=1

	polarity = metrics.sentiment_polarity(words, sentilex)
	worksheet.write(row, col, polarity['positive_ratio'])
	col+=1
	worksheet.write(row, col, polarity['negative_ratio'])
	col+=1

	bp_stats = metrics.behavioral_physiological(words, liwc_tags)
	worksheet.write(row, col, bp_stats['perceptuality'])
	col+=1
	worksheet.write(row, col, bp_stats['relativity'])
	col+=1
	worksheet.write(row, col, bp_stats['cognitivity'])
	col+=1
	worksheet.write(row, col, bp_stats['personal_concerns'])
	col+=1
	worksheet.write(row, col, bp_stats['biological_processes'])
	col+=1
	worksheet.write(row, col, bp_stats['social_processes'])

	col=1
	row+=1

workbook.close()