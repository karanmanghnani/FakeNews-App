from flask import Flask, render_template, url_for, request
from newspaper import Article
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import spacy
import get_metrics as metrics
import statistics 
import xlrd
from openpyxl import load_workbook
from firebase import firebase

app = Flask(__name__)

firebase = firebase.FirebaseApplication('https://fakenews-app-d59dc.firebaseio.com/', None)


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
			#print(url)
			#print(type(url))
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

			tweets = metrics.createTweetsDB(article_title)
			#metrics.runMetricsOnTweets()

			return render_template('result.html', title='FakeNews',posts=posts, article_text=article_text, article_title=article_title, emotion_ratio=emotion_ratio, total_emotion=total_emotion, totalsubj=totalsubj, subj_feats=subj_feats, vad_features=vad_features, polarity=polarity, bp_stats=bp_stats, source=source, url=url,absolute_url=absolute_url, tweets=tweets)
		
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
	result = firebase.get('/fakenews-app-d59dc/noticias/', '')

	articles = {}
	title_date = {}
	source_verification = {}
	metrics = {}
	temp_list = []

	for i in result.values():
		for j in range(1,7):
			if(i['id_noticia'] == str(j)):
				articles[j] = i['noticia']
				title_date[j] = [i['titulo'], i['data']]
				source_verification[j] = [i['source'], i['verified']]
				metrics[j] = [i['Emotion'], i['Subjectivity'],i['Affectivity'], i['Polarity'],i['BP']]	


	if request.method == 'POST': 
		for i in range(1,7):
			data =  {  'article': i, 'Q1': request.form['1_'+str(i)], 'Q2': request.form['2_'+str(i)], 'Q3': request.form['3_'+str(i)], 'Q4': request.form['4_'+str(i)], 'Q5': request.form['5_'+str(i)], 'Q6': request.form['6_'+str(i)], 'Q7': request.form['7_'+str(i)], 'Q8': request.form['8_'+str(i)]}
			firebase.post('/fakenews-app-d59dc/with_labels/',data)

		return render_template('evaluation_labels.html' ,posts=posts, articles=articles, metrics=metrics, title_date=title_date, source_verification=source_verification)
		
	else:
		return render_template('evaluation_labels.html', posts=posts, articles=articles, metrics=metrics, title_date=title_date, source_verification=source_verification)

@app.route("/evaluation",methods = ['POST', 'GET'])
def evaluation():
	result = firebase.get('/fakenews-app-d59dc/noticias/', '')

	articles = {}
	title_date = {}
	source_verification = {}

	for i in result.values():
		for j in range(1,7):
			if(i['id_noticia'] == str(j)):
				articles[j] = i['noticia']
				title_date[j] = [i['titulo'], i['data']]
				source_verification[j] = [i['source'], i['verified']]

	if request.method == 'POST': 
		#print(request.form)

		for i in range(1,7):
			data =  {  'article': i, 'Q1': request.form['1_'+str(i)], 'Q2': request.form['2_'+str(i)], 'Q3': request.form['3_'+str(i)], 'Q4': request.form['4_'+str(i)], 'Q5': request.form['5_'+str(i)], 'Q6': request.form['6_'+str(i)]}
			firebase.post('/fakenews-app-d59dc/without_labels/',data)

		return render_template('evaluation.html' ,posts=posts, articles=articles, title_date=title_date, source_verification=source_verification)
		
	else:
		return render_template('evaluation.html', posts=posts, articles=articles, title_date=title_date, source_verification=source_verification)


if __name__ == '__main__':
    app.run(debug=True)
