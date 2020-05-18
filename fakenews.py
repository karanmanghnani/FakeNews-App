from flask import Flask, render_template, url_for, request
from newspaper import Article
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import spacy
import get_metrics as metrics
import statistics 
import xlrd
from openpyxl import load_workbook

app = Flask(__name__)



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

def parse(website):
    article = Article(website)
    article.download()
    article.parse()
    article_text = article.text
    article_title = article.title
    return article_text, article_title


@app.route("/")
@app.route("/HomePage",methods = ['POST', 'GET'])
def HomePage():
	if request.method == 'POST': 
		#metrics.prepare_lexicons()

		liwc_tags, sentilex, anew_extended, emotion_words, subjective_words = metrics.load_lexicons()

		if('url' in request.values ):
			url = request.form['url']
			print(url)
			print(type(url))
			article_text, article_title = parse(url)
			sentences = metrics.tokenize_sentences(article_text)
			lemmas, original_lemmas = metrics.lemmatize_words(sentences)
			words, original_words = metrics.tokenize_words(sentences)


			emotion_ratio, total_emotion, emotion_list = metrics.get_emotions(words, emotion_words)
			totalsubj, subj_feats, subj_list = metrics.get_subjective_ratio(words, subjective_words)
			vad_features, vad_list = metrics.get_vad_features(lemmas, anew_extended)
			polarity = metrics.sentiment_polarity(words, sentilex)
			bp_stats = metrics.behavioral_physiological(words, liwc_tags)
			"""
			para mostrar as palavras nas metricas nao funciona função replace

			keys = ['pos_list', 'neg_list', 'pos_cons_list', 'neg_cons_list']
			polarity_list = {x:polarity[x] for x in keys}

			keys = ['perc_list', 'rel_list', 'cog_list', 'pers_list', 'soc_list', 'bio_list']
			bp_list = {x:bp_stats[x] for x in keys}

			splitted_words =  nltk.word_tokenize(article_text)

			#emotion_list = metrics.replace_original_words(emotion_list, article_text.split())
			subj_list = metrics.replace_original_words(subj_list, splitted_words, splitted_words)"""
			total_emotion, totalsubj, vad_features['total_vad'], polarity['total_pol'], bp_stats['total_bp'] = metrics.fakeProbability2(total_emotion,totalsubj,vad_features['valence_avg'],vad_features['arousal_avg'],vad_features['dominance_avg'],polarity['positive_ratio'],polarity['negative_ratio'],bp_stats['perceptuality'],bp_stats['relativity'],bp_stats['cognitivity'],bp_stats['personal_concerns'],bp_stats['biological_processes'],bp_stats['social_processes'])

			source, absolute_url = metrics.source(url)

			return render_template('result.html', title='FakeNews',posts=posts, article_text=article_text, article_title=article_title, emotion_ratio=emotion_ratio, total_emotion=total_emotion, totalsubj=totalsubj, subj_feats=subj_feats, vad_features=vad_features, polarity=polarity, bp_stats=bp_stats, source=source, url=url,absolute_url=absolute_url)
		
		else:
			article_title = "No title"
			article_text = request.form['ArticleText']
			sentences = metrics.tokenize_sentences(article_text)
			lemmas, original_lemmas = metrics.lemmatize_words(sentences)
			words, original_words = metrics.tokenize_words(sentences)


			emotion_ratio, total_emotion, emotion_list = metrics.get_emotions(words, emotion_words)
			totalsubj, subj_feats, subj_list = metrics.get_subjective_ratio(words, subjective_words)
			vad_features, vad_list = metrics.get_vad_features(lemmas, anew_extended)
			polarity = metrics.sentiment_polarity(words, sentilex)
			bp_stats = metrics.behavioral_physiological(words, liwc_tags)

			total_emotion, totalsubj, vad_features['total_vad'], polarity['total_pol'], bp_stats['total_bp'] = metrics.fakeProbability2(total_emotion,totalsubj,vad_features['valence_avg'],vad_features['arousal_avg'],vad_features['dominance_avg'],polarity['positive_ratio'],polarity['negative_ratio'],bp_stats['perceptuality'],bp_stats['relativity'],bp_stats['cognitivity'],bp_stats['personal_concerns'],bp_stats['biological_processes'],bp_stats['social_processes'])

			source = False
			absolute_url = "No url"
			url = "No url"

			return render_template('result.html', title='FakeNews',posts=posts, article_text=article_text, article_title=article_title, emotion_ratio=emotion_ratio, total_emotion=total_emotion, totalsubj=totalsubj, subj_feats=subj_feats, vad_features=vad_features, polarity=polarity, bp_stats=bp_stats, source=source, url=url,absolute_url=absolute_url)
		
	else:
		return render_template('HomePage.html', title='FakeNews')


@app.route("/result",methods = ['POST', 'GET'])
def result():
    return render_template('result.html', posts=posts)

@app.route("/evaluation_labels",methods = ['POST', 'GET'])
def evaluation_labels():

	articles = {}
	metrics = {}
	temp_list = []
	loc = ("evaluation_answer_labels.xlsx") 
	wb = xlrd.open_workbook(loc) 
	sheet = wb.sheet_by_index(0) 
	for i in range(1,sheet.nrows):
		articles[i] = sheet.cell_value(i, 1)
		for j in range(2,8):
			print(sheet.cell_value(i, j))
			temp_list.append(sheet.cell_value(i, j))
		metrics[i] = temp_list
		temp_list = []

	if request.method == 'POST': 

		loc = ("evaluation_answer_labels.xlsx") 
		wb = xlrd.open_workbook(loc) 
		sheet = wb.sheet_by_index(0)
		row = 2
		col = sheet.ncols + 1

		wb = load_workbook(filename = "evaluation_answer_labels.xlsx")
		ws = wb.active

		ws.cell(row=row,column=col).value = request.form['1']
		row+=1
		ws.cell(row=row,column=col).value = request.form['2']
		row+=1
		ws.cell(row=row,column=col).value = request.form['3']
		row+=1
		ws.cell(row=row,column=col).value = request.form['4']
		row+=1
		ws.cell(row=row,column=col).value = request.form['5']
		row+=1
		ws.cell(row=row,column=col).value = request.form['6']
		row+=1

		wb.save("evaluation_answer_labels.xlsx")


		return render_template('evaluation_labels.html' ,posts=posts, articles=articles, metrics=metrics)
		
	else:
		return render_template('evaluation_labels.html', posts=posts, articles=articles, metrics=metrics)

@app.route("/evaluation",methods = ['POST', 'GET'])
def evaluation():

	articles = {}
	loc = ("evaluation_answer.xlsx") 
	wb = xlrd.open_workbook(loc) 
	sheet = wb.sheet_by_index(0) 
	for i in range(1,sheet.nrows):
		articles[i] = sheet.cell_value(i, 1)
	print(articles)

	if request.method == 'POST': 

		loc = ("evaluation_answer.xlsx") 
		wb = xlrd.open_workbook(loc) 
		sheet = wb.sheet_by_index(0)
		row = 2
		col = sheet.ncols + 1

		wb = load_workbook(filename = "evaluation_answer.xlsx")
		ws = wb.active

		ws.cell(row=row,column=col).value = request.form['1']
		row+=1
		ws.cell(row=row,column=col).value = request.form['2']
		row+=1
		ws.cell(row=row,column=col).value = request.form['3']
		row+=1
		ws.cell(row=row,column=col).value = request.form['4']
		row+=1
		ws.cell(row=row,column=col).value = request.form['5']
		row+=1
		ws.cell(row=row,column=col).value = request.form['6']
		row+=1

		wb.save("evaluation_answer.xlsx")


		return render_template('evaluation.html' ,posts=posts, articles=articles)
		
	else:
		return render_template('evaluation.html', posts=posts, articles=articles)


if __name__ == '__main__':
    app.run(debug=True)