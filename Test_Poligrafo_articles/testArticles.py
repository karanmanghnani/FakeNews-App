
# Program extracting first column 
import xlrd 
import unidecode
import /home/karan/Desktop/FakeNews-App/get_metrics as metrics

news = {}
loc = ("Noticías_BD.xlsx") 
  
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
sheet.cell_value(0, 0) 
  
""" news = 1:['noticia', vericidade]"""
for i in range(1,31):
	news[i] = [sheet.cell_value(i, 1),sheet.cell_value(i, 3)]
	#print(sheet.cell_value(i, 3))

#print(news[1][0])
for i in range(1,31):
	emotion_count,emotion_ratio,total_emotion  = metrics.get_emotions(news[i][0])
	news[i].append("total emotion:" + str(total_emotion))
	totalsubj, subj_feats = metrics.get_subjective_ratio(news[i][0])
	news[i].append("total subj: " + str(totalsubj))
	vad_features = metrics.get_vad_features(news[i][0])
	news[i].append("total vad: " + str(vad_features['total_vad']))
	polarity = metrics.sentiment_polarity(news[i][0])
	news[i].append("total polarity:" + str(polarity['total_pol']))
	bp_stats = metrics.behavioral_physiological(news[i][0])
	news[i].append("total BP:" + str( bp_stats['total_bp']))

print(news)
