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
		#try:

		#metrics.prepare_lexicons()

		liwc_tags, sentilex, anew_extended, emotion_words, subjective_words = metrics.load_lexicons()

		if('url' in request.values ):
			url = request.form['url']
			#print(url)
			#print(type(url))

			saved_articles = firebase.get('/fakenews-app-d59dc/saved_articles/', '')
			for article in saved_articles.values():
				if (article['url'] == url):
					if("tweets" not in article.keys()):
						article['tweets'] = []
					return render_template('result.html', title='FactMe',posts=posts, article_text=article['article_text'], article_title=article['article_title'], emotion_ratio=article['emotion_ratio'], total_emotion=article['total_emotion'], emotion_n_words=article['emotion_n_words'], totalsubj=article['totalsubj'], subj_feats=article['subj_feats'], ratio_of_each_subj=article['ratio_of_each_subj'], vad_features=article['vad_features'], total_vad=article['total_vad'], polarity=article['polarity'], bp_stats=article['bp_stats'], source=article['source'], url=article['url'],absolute_url=article['absolute_url'], tweets=article['tweets'], n_tweets=article['n_tweets'], finalProb=article['finalProb'], gram_stats=article['grammar'])

			article_text, article_title = parse(url)
			sentences = metrics.tokenize_sentences(article_text)
			lemmas, original_lemmas = metrics.lemmatize_words(sentences)
			words, original_words = metrics.tokenize_words(sentences)


			gram_stats = metrics.get_grammatical(sentences, words)
			emotion_ratio, emotion_n_words, total_emotion, emotion_list = metrics.get_emotions(words, emotion_words)
			totalsubj, subj_feats, subj_list, ratio_of_each_subj = metrics.get_subjective_ratio(words, subjective_words)
			vad_features, vad_list, total_vad = metrics.get_vad_features(lemmas, anew_extended)
			polarity = metrics.sentiment_polarity(words, sentilex)
			bp_stats = metrics.behavioral_physiological(words, liwc_tags)
			"""
			para mostrar as palavras nas metricas nao funciona funcao replace

			keys = ['pos_list', 'neg_list', 'pos_cons_list', 'neg_cons_list']
			polarity_list = {x:polarity[x] for x in keys}

			keys = ['perc_list', 'rel_list', 'cog_list', 'pers_list', 'soc_list', 'bio_list']
			bp_list = {x:bp_stats[x] for x in keys}

			splitted_words =  nltk.word_tokenize(article_text)

			#emotion_list = metrics.replace_original_words(emotion_list, article_text.split())
			subj_list = metrics.replace_original_words(subj_list, splitted_words, splitted_words)"""

			#finalProb = metrics.finalProb2(emotion_ratio, ratio_of_each_subj, vad_features, polarity, bp_stats)


			total_emotion, totalsubj, vad_features['total_vad'], polarity['total_pol'], bp_stats['total_bp'], gram_stats['total'] = metrics.fakeProbability2(emotion_ratio, ratio_of_each_subj, vad_features, polarity, bp_stats, gram_stats)

			source, absolute_url = metrics.source(url)

			tweets = metrics.createTweetsDB(article_title)
			#print(tweets)
			#metrics.runMetricsOnTweets()
			n_tweets = len(tweets)

			finalProb = metrics.finalProb(total_emotion, totalsubj, vad_features['total_vad'], polarity['total_pol'], bp_stats['total_bp'], gram_stats['total'],source)


			url_data1 = {
				"url":url,
				"article_text":article_text,
				"article_title":article_title,
				"emotion_ratio":emotion_ratio,
				"emotion_n_words":emotion_n_words,
				"total_emotion":total_emotion,
				"totalsubj":totalsubj,
				"subj_feats":subj_feats,
				"ratio_of_each_subj":ratio_of_each_subj,
				"vad_features":vad_features,
				"total_vad":total_vad,
				"polarity":polarity,
				"bp_stats":bp_stats,
				"source":source,
				"absolute_url":absolute_url,
				"tweets":tweets,
				"n_tweets":n_tweets,
				"finalProb":finalProb,
				"grammar":gram_stats
			}

			firebase.post('/fakenews-app-d59dc/saved_articles/',url_data1)

			return render_template('result.html', title='FactMe',posts=posts, article_text=article_text, article_title=article_title, emotion_ratio=emotion_ratio, total_emotion=total_emotion, emotion_n_words=emotion_n_words, totalsubj=totalsubj, subj_feats=subj_feats, ratio_of_each_subj=ratio_of_each_subj, vad_features=vad_features, total_vad=total_vad, polarity=polarity, bp_stats=bp_stats, source=source, url=url,absolute_url=absolute_url, tweets=tweets, n_tweets=n_tweets, finalProb=finalProb,gram_stats=gram_stats)

		else:
			article_title = request.form['ArticleTitle']
			article_text = request.form['ArticleText']

			sentences = metrics.tokenize_sentences(article_text)
			lemmas, original_lemmas = metrics.lemmatize_words(sentences)
			words, original_words = metrics.tokenize_words(sentences)

			gram_stats = metrics.get_grammatical(sentences, words)
			emotion_ratio, emotion_n_words, total_emotion, emotion_list = metrics.get_emotions(words, emotion_words)
			totalsubj, subj_feats, subj_list, ratio_of_each_subj = metrics.get_subjective_ratio(words, subjective_words)
			vad_features, vad_list, total_vad = metrics.get_vad_features(lemmas, anew_extended)
			polarity = metrics.sentiment_polarity(words, sentilex)
			bp_stats = metrics.behavioral_physiological(words, liwc_tags)

			total_emotion, totalsubj, vad_features['total_vad'], polarity['total_pol'], bp_stats['total_bp'], gram_stats['total'] = metrics.fakeProbability2(emotion_ratio, ratio_of_each_subj, vad_features, polarity, bp_stats, gram_stats)

			source = False
			absolute_url = "No url"
			url = "No url"
			if(article_title == ""):
				tweets = []
				n_tweets = 0
			else:
				tweets = metrics.createTweetsDB(article_title)
				n_tweets = len(tweets)

			finalProb = metrics.finalProb(total_emotion, totalsubj, vad_features['total_vad'], polarity['total_pol'], bp_stats['total_bp'], gram_stats['total'],source)


			return render_template('result.html', title='FactMe',posts=posts, article_text=article_text, article_title=article_title, emotion_ratio=emotion_ratio, total_emotion=total_emotion, emotion_n_words=emotion_n_words, totalsubj=totalsubj, subj_feats=subj_feats, ratio_of_each_subj=ratio_of_each_subj, vad_features=vad_features, total_vad=total_vad, polarity=polarity, bp_stats=bp_stats, source=source, url=url,absolute_url=absolute_url, tweets=tweets, n_tweets=n_tweets, finalProb=finalProb,gram_stats=gram_stats)
		#except Exception as e:
			#return render_template('error.html')
	else:
		return render_template('HomePage.html', title='FactMe')


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
			count = firebase.get('/fakenews-app-d59dc', 'answer_count')
			firebase.put('/fakenews-app-d59dc','answer_count', str(int(count) + 1) )
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

			total_emotion, totalsubj, vad_features['total_vad'], polarity['total_pol'], bp_stats['total_bp'] = metrics.fakeProbability2(emotion_ratio, ratio_of_each_subj, vad_features, polarity, bp_stats)

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

@app.route("/about",methods = ['POST', 'GET'])
def about():
    return render_template('about.html', posts=posts)

@app.route("/evaluation_interface",methods = ['POST', 'GET'])
def evaluation_interface():
    return render_template('evaluation_interface.html', posts=posts)

@app.route("/how_it_works",methods = ['POST', 'GET'])
def how_it_works():
    return render_template('how_it_works.html', posts=posts)

@app.route("/fact_checks",methods = ['POST', 'GET'])
def fact_checks():
	if request.method == 'POST':
		saved_articles = firebase.get('/fakenews-app-d59dc/saved_articles/', '')
		
		url = request.form['url']
		#print(url)

		for article in saved_articles.values():
			if (article['url'] == url):
				if("tweets" not in article.keys()):
					article['tweets'] = []
				return render_template('result.html', title='FactMe',posts=posts, article_text=article['article_text'], article_title=article['article_title'], emotion_ratio=article['emotion_ratio'], total_emotion=article['total_emotion'], emotion_n_words=article['emotion_n_words'], totalsubj=article['totalsubj'], subj_feats=article['subj_feats'], ratio_of_each_subj=article['ratio_of_each_subj'], vad_features=article['vad_features'], total_vad=article['total_vad'], polarity=article['polarity'], bp_stats=article['bp_stats'], source=article['source'], url=article['url'],absolute_url=article['absolute_url'], tweets=article['tweets'], n_tweets=article['n_tweets'], finalProb=article['finalProb'])


		return render_template('fact_checks.html', posts=posts, saved_articles=saved_articles, url=url)

	else:
		saved_articles = firebase.get('/fakenews-app-d59dc/saved_articles/', '')
		for article in saved_articles.values():
			if("tweets" not in article.keys()):
				article['tweets'] = []
				url = article['url']
				#print(url)

		return render_template('fact_checks.html', posts=posts, saved_articles=saved_articles, url=url)

@app.errorhandler(404)
def page_not_found(e):
	return("ERROR 404: This page does not exist in FactMe.")

if __name__ == '__main__':
    app.run(debug=True)

