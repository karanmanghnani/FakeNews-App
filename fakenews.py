from flask import Flask, render_template, url_for, request, make_response
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


			emotion_ratio, emotion_n_words, total_emotion, emotion_list = metrics.get_emotions(words, emotion_words)
			totalsubj, subj_feats, subj_list, ratio_of_each_subj = metrics.get_subjective_ratio(words, subjective_words)
			vad_features, vad_list, total_vad = metrics.get_vad_features(lemmas, anew_extended)
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
			n_tweets = len(tweets)

			finalProb = metrics.finalProb(total_emotion, totalsubj, vad_features['total_vad'], polarity['total_pol'], bp_stats['total_bp'],source)

			return render_template('result.html', title='Misinformation Detector',posts=posts, article_text=article_text, article_title=article_title, emotion_ratio=emotion_ratio, total_emotion=total_emotion, emotion_n_words=emotion_n_words, totalsubj=totalsubj, subj_feats=subj_feats, ratio_of_each_subj=ratio_of_each_subj, vad_features=vad_features, total_vad=total_vad, polarity=polarity, bp_stats=bp_stats, source=source, url=url,absolute_url=absolute_url, tweets=tweets, n_tweets=n_tweets, finalProb=finalProb)
		
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

			return render_template('result.html', title='Misinformation Detector',posts=posts, article_text=article_text, article_title=article_title, emotion_ratio=emotion_ratio, total_emotion=total_emotion, totalsubj=totalsubj, subj_feats=subj_feats, vad_features=vad_features, polarity=polarity, bp_stats=bp_stats, source=source, url=url,absolute_url=absolute_url)
		
	else:
		return render_template('HomePage.html', title='Misinformation Detector')


@app.route("/result",methods = ['POST', 'GET'])
def result():
    return render_template('result.html', posts=posts)

@app.route("/evaluation_labels",methods = ['POST', 'GET'])
def evaluation_labels():

	evaluation = request.cookies.get('evaluation')
	if(evaluation == None):
		key = 1
	else:
		key = len(evaluation.split()) + 1

	result = firebase.get('/fakenews-app-d59dc/noticias/', '')

	articles = {}
	title_date = {}
	source_verification = {}
	metrics = {}
	temp_list = []


	for i in result.values():
		if(i['id_noticia'] == str(key)):
			articles[key] = i['noticia']
			title_date[key] = [i['titulo'], i['data']]
			source_verification[key] = [i['source'], i['verified']]



	if request.method == 'POST': 

		evaluation = request.cookies.get('evaluation')
		if(evaluation == None):
			key = 1
		else:
			key = len(evaluation.split()) + 1
		value = 6 - key
		
		data =  {  'article': key, 'Q1': request.form['1_'+str(key)], 'Q2': request.form['2_'+str(key)], 'Q3': request.form['3_'+str(key)], 'Q4': request.form['4_'+str(key)], 'Q5': request.form['5_'+str(key)], 'Q6': request.form['6_'+str(key)], 'Q7': request.form['7_'+str(key)], 'Q8': request.form['8_'+str(key)]}

		# 0 = both 1 = with indicator
		result = firebase.get('/fakenews-app-d59dc/evaluation_needed/noticias', 'noticia_' + str(key))

		if(result == '0'):
			firebase.post('/fakenews-app-d59dc/with_labels/',data)
			firebase.put('/fakenews-app-d59dc/evaluation_needed/noticias','noticia_' + str(key),'1')
		else:
			firebase.post('/fakenews-app-d59dc/with_labels_only/',data)
			firebase.put('/fakenews-app-d59dc/evaluation_needed/noticias','noticia_' + str(key),'0')

		resp = make_response(render_template('evaluation_message.html', posts=posts, articles=articles, title_date=title_date, source_verification=source_verification,value=value))
		
		value = ''
		for i in range(1,key+1):
			value += ' '.join(str(i)) + ' '
		#print(value)

		key = value
		resp.set_cookie('evaluation', str(key))

		return resp
		
	else:
		return render_template('evaluation_labels.html', posts=posts, articles=articles, metrics=metrics, title_date=title_date, source_verification=source_verification)

@app.route("/evaluation",methods = ['POST', 'GET'])
def evaluation():

	liwc_tags, sentilex, anew_extended, emotion_words, subjective_words = metrics.load_lexicons()

	evaluation = request.cookies.get('evaluation')
	if(evaluation == None):
		key = 1
	else:
		key = len(evaluation.split()) + 1

	result = firebase.get('/fakenews-app-d59dc/noticias/', '')

	articles = {}
	title_date = {}
	source_verification = {}
	for i in result.values():
		if(i['id_noticia'] == str(key)):
			articles[key] = i['noticia']
			title_date[key] = [i['titulo'], i['data']]
			source_verification[key] = [i['source'], i['verified']]

			article_text = i['noticia']
			article_title = i['titulo']
			sentences = metrics.tokenize_sentences(article_text)
			lemmas, original_lemmas = metrics.lemmatize_words(sentences)
			words, original_words = metrics.tokenize_words(sentences)


			emotion_ratio, emotion_n_words, total_emotion, emotion_list = metrics.get_emotions(words, emotion_words)
			totalsubj, subj_feats, subj_list, ratio_of_each_subj = metrics.get_subjective_ratio(words, subjective_words)
			vad_features, vad_list, total_vad = metrics.get_vad_features(lemmas, anew_extended)
			polarity = metrics.sentiment_polarity(words, sentilex)
			bp_stats = metrics.behavioral_physiological(words, liwc_tags)

			total_emotion, totalsubj, vad_features['total_vad'], polarity['total_pol'], bp_stats['total_bp'] = metrics.fakeProbability2(total_emotion,totalsubj,vad_features['valence_avg'],vad_features['arousal_avg'],vad_features['dominance_avg'],polarity['positive_ratio'],polarity['negative_ratio'],bp_stats['perceptuality'],bp_stats['relativity'],bp_stats['cognitivity'],bp_stats['personal_concerns'],bp_stats['biological_processes'],bp_stats['social_processes'])

			#source, absolute_url = metrics.source(url)
			if(i['verified'] == "True"):
				source = True
			else:
				source = False
			absolute_url = i['url']
			url = "No url"

			tweets = metrics.createTweetsDB(article_title)
			n_tweets = len(tweets)

	if request.method == 'POST': 
		#print(request.form)
		#print(key)

		evaluation = request.cookies.get('evaluation')
		if(evaluation == None):
			key = 1
		else:
			key = len(evaluation.split()) + 1

		data =  {  'article': key, 'Q1': request.form['1_'+str(key)], 'Q2': request.form['2_'+str(key)], 'Q3': request.form['3_'+str(key)], 'Q4': request.form['4_'+str(key)], 'Q5': request.form['5_'+str(key)], 'Q6': request.form['6_'+str(key)]}
		firebase.post('/fakenews-app-d59dc/without_labels/',data)

		return render_template('evaluation_labels.html', posts=posts, articles=articles, title_date=title_date, source_verification=source_verification, article_text=article_text, article_title=article_title, emotion_ratio=emotion_ratio, total_emotion=total_emotion, emotion_n_words=emotion_n_words, totalsubj=totalsubj, subj_feats=subj_feats, ratio_of_each_subj=ratio_of_each_subj, vad_features=vad_features, total_vad=total_vad, polarity=polarity, bp_stats=bp_stats, source=source, url=url,absolute_url=absolute_url, tweets=tweets, n_tweets=n_tweets)
		
	else:

		evaluation = request.cookies.get('evaluation')
		if(evaluation == None):
			key = 1
			result = firebase.get('/fakenews-app-d59dc/evaluation_needed/noticias', 'noticia_'+str(key))
		else:
			key = len(evaluation.split())
			result = firebase.get('/fakenews-app-d59dc/evaluation_needed/noticias', 'noticia_'+str(key+1))

		# 0 = both 1 = with indicator
		if(key == 6):
			if(result == '1'):
				value = True
				return render_template('evaluation_labels.html' ,posts=posts, articles=articles, title_date=title_date, source_verification=source_verification, key=key, value=value)
			else:
				value = False
				return render_template('evaluation.html' ,posts=posts, articles=articles, title_date=title_date, source_verification=source_verification, key=key, value=value)
		else:
			if(result == '1'):
				value = True
				return render_template('evaluation_labels.html' ,posts=posts, articles=articles, title_date=title_date, source_verification=source_verification, key=key, value=value,  article_text=article_text, article_title=article_title, emotion_ratio=emotion_ratio, total_emotion=total_emotion, emotion_n_words=emotion_n_words, totalsubj=totalsubj, subj_feats=subj_feats, ratio_of_each_subj=ratio_of_each_subj, vad_features=vad_features, total_vad=total_vad, polarity=polarity, bp_stats=bp_stats, source=source, url=url,absolute_url=absolute_url, tweets=tweets, n_tweets=n_tweets)
			else:
				value = False
				return render_template('evaluation.html' ,posts=posts, articles=articles, title_date=title_date, source_verification=source_verification, key=key, value=value,  article_text=article_text, article_title=article_title, emotion_ratio=emotion_ratio, total_emotion=total_emotion, emotion_n_words=emotion_n_words, totalsubj=totalsubj, subj_feats=subj_feats, ratio_of_each_subj=ratio_of_each_subj, vad_features=vad_features, total_vad=total_vad, polarity=polarity, bp_stats=bp_stats, source=source, url=url,absolute_url=absolute_url, tweets=tweets, n_tweets=n_tweets)

		

@app.route("/evaluation_message",methods = ['POST', 'GET'])
def evaluation_message():	
	if request.method == 'POST': 
		evaluation = request.cookies.get('evaluation')
		if(len(evaluation.split())==6):
			return render_template('evaluation.html' ,posts=posts, articles=articles, title_date=title_date, source_verification=source_verification, key=key, value=value)
		else:
			return render_template('evaluation.html' ,posts=posts, articles=articles, title_date=title_date, source_verification=source_verification, key=key, value=value,  article_text=article_text, article_title=article_title, emotion_ratio=emotion_ratio, total_emotion=total_emotion, emotion_n_words=emotion_n_words, totalsubj=totalsubj, subj_feats=subj_feats, ratio_of_each_subj=ratio_of_each_subj, vad_features=vad_features, total_vad=total_vad, polarity=polarity, bp_stats=bp_stats, source=source, url=url,absolute_url=absolute_url, tweets=tweets, n_tweets=n_tweets)

	else:
		return render_template('evaluation_message.html' ,posts=posts, articles=articles, title_date=title_date, source_verification=source_verification, key=key, value=value,  article_text=article_text, article_title=article_title, emotion_ratio=emotion_ratio, total_emotion=total_emotion, emotion_n_words=emotion_n_words, totalsubj=totalsubj, subj_feats=subj_feats, ratio_of_each_subj=ratio_of_each_subj, vad_features=vad_features, total_vad=total_vad, polarity=polarity, bp_stats=bp_stats, source=source, url=url,absolute_url=absolute_url, tweets=tweets, n_tweets=n_tweets)

if __name__ == '__main__':
    app.run(debug=True)
