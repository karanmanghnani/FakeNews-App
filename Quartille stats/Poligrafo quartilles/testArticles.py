import xlrd 
import unidecode
import get_metrics as metrics
import xlsxwriter

workbook = xlsxwriter.Workbook('BD_results.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write(0, 0,"Label")
worksheet.write(0, 1,"Emotion")
worksheet.write(0, 2,"Subj")
worksheet.write(0, 3,"val_avg")
worksheet.write(0, 4,"aro_avg")
worksheet.write(0, 5,"dom_avg")
worksheet.write(0, 6,"pos_words")
worksheet.write(0, 7,"neg_words")
worksheet.write(0, 8,"perceptuality")
worksheet.write(0, 9,"relativity")
worksheet.write(0, 10,"cognitivity")
worksheet.write(0, 11,"personal")
worksheet.write(0, 12,"biological")
worksheet.write(0, 13,"social")

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
	worksheet.write(row, col, total_emotion)
	col+=1

	totalsubj, subj_feats = metrics.get_subjective_ratio(words, subjective_words)
	worksheet.write(row, col, totalsubj)
	col+=1

	vad_features = metrics.get_vad_features(lemmas, anew_extended)
	worksheet.write(row, col, vad_features['valence_avg'])
	col+=1

	worksheet.write(row, col, vad_features['arousal_avg'])
	col+=1

	worksheet.write(row, col, vad_features['dominance_avg'])
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