from flask import Flask, render_template, url_for, request
from newspaper import Article
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import spacy
import get_metrics as metrics
import statistics 

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
    return article_text


@app.route("/")
@app.route("/HomePage",methods = ['POST', 'GET'])
def HomePage():
	if request.method == 'POST': 
		#metrics.prepare_lexicons()

		liwc_tags, sentilex, anew_extended, emotion_words, subjective_words = metrics.load_lexicons()
		emotionDB, subjectivityDB, affectiveDB, polarityDB, bpDB = metrics.prepareMetricsDB()

		if('url' in request.values ):
			url = request.form['url']
			article_text = parse(url)
			sentences = metrics.tokenize_sentences(article_text)
			lemmas = metrics.lemmatize_words(sentences)
			words = metrics.tokenize_words(sentences)

			emotion_ratio, total_emotion = metrics.get_emotions(words, emotion_words)
			print("emotion")
			print(total_emotion)
			total_emotion = metrics.fakeProbability(emotionDB,total_emotion)
			
			totalsubj, subj_feats = metrics.get_subjective_ratio(words, subjective_words)
			totalsubj = metrics.fakeProbability(subjectivityDB, totalsubj)

			vad_features = metrics.get_vad_features(lemmas, anew_extended)
			vad_features['total_vad'] = metrics.fakeProbability(affectiveDB, vad_features['total_vad'])

			polarity = metrics.sentiment_polarity(words, sentilex)
			polarity['total_pol'] = metrics.fakeProbability(polarityDB, polarity['total_pol'])

			bp_stats = metrics.behavioral_physiological(words, liwc_tags)
			bp_stats['total_bp'] = metrics.fakeProbability(bpDB, bp_stats['total_bp'])

			source, url = metrics.source(url)
			print(source)
			return render_template('result.html', title='FakeNews',posts=posts, article_text=article_text, emotion_ratio=emotion_ratio, total_emotion=total_emotion, totalsubj=totalsubj, subj_feats=subj_feats, vad_features=vad_features, polarity=polarity, bp_stats=bp_stats, source=source, url=url)
		else:
			article_text = request.form['ArticleText']
			emotion_ratio,total_emotion = metrics.get_emotions(words, emotion_words)
			totalsubj, subj_feats = metrics.get_subjective_ratio(article_text)
			vad_features = metrics.get_vad_features(article_text)
			polarity = metrics.sentiment_polarity(article_text)
			bp_stats = metrics.behavioral_physiological(article_text)
			return render_template('result.html', title='FakeNews',posts=posts, article_text=article_text, emotion_ratio=emotion_ratio, total_emotion=total_emotion, totalsubj=totalsubj, subj_feats=subj_feats, vad_features=vad_features, polarity=polarity, bp_stats=bp_stats)

	else:
		return render_template('HomePage.html', title='FakeNews')


@app.route("/result",methods = ['POST', 'GET'])
def result():
    return render_template('result.html', posts=posts)


if __name__ == '__main__':
    app.run(debug=True)