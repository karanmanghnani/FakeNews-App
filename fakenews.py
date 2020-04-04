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
		if('url' in request.values ):
			url = request.form['url']
			article_text = parse(url)

			#emotion_count,emotion_ratio,total_emotion = metrics.get_emotions(article_text)
			total_emotion=5
			emotion_ratio = {'Happiness' : 10, 'Disgust' : 20, 'Fear' : 30, 'Anger':40, 'Surprise':50, 'Sadness':60} 
			emotion_count = {'Happiness' : 0, 'Disgust' : 0, 'Fear' : 0, 'Anger':0, 'Surprise':0, 'Sadness':0}
			
			#totalsubj, subj_feats = metrics.get_subjective_ratio(article_text)
			totalsubj = 20
			subj_feats = {'strongsubj':10, 'weaksubj':20}

			vad_features = {
			'total_vad': 0,
			'valence_avg': 0,
			'valence_std': 0,
			'valence_max': 0,
			'valence_min': 0,
			'valence_dif': 0,
			'arousal_avg': 0,
			'arousal_std': 0,
			'arousal_max': 0,
			'arousal_min': 0,
			'arousal_dif': 0,
			'dominance_avg': 0,
			'dominance_std': 0,
			'dominance_max': 0,
			'dominance_min': 0,
			'dominance_dif': 0,
			}
            #vad_features = metrics.get_vad_features(article_text)

            #polarity = metrics.sentiment_polarity(article_text)
			polarity = {}
			polarity['positive_ratio'] = 10
			polarity['negative_ratio'] = 10
			polarity['positive_contrast'] = 20
			polarity['negative_contrast'] = 20
			polarity['total_pol'] = 5

			#bp_stats = metrics.behavioral_physiological(article_text)
			bp_stats = {}
			bp_stats['perceptuality'] = 5
			bp_stats['relativity'] = 3
			bp_stats['cognitivity'] = 5
			bp_stats['personal_concerns'] = 6
			bp_stats['biological_processes'] = 4
			bp_stats['social_processes'] = 7
			bp_stats['total_bp'] = 80

			source, url = metrics.source(url)
			print(source)
			return render_template('result.html', title='FakeNews',posts=posts, article_text=article_text, emotion_count=emotion_count, emotion_ratio=emotion_ratio, total_emotion=total_emotion, totalsubj=totalsubj, subj_feats=subj_feats, vad_features=vad_features, polarity=polarity, bp_stats=bp_stats, source=source, url=url)
		else:
			article_text = request.form['ArticleText']
			emotion_count,emotion_ratio,total_emotion = metrics.get_emotions(article_text)
			totalsubj, subj_feats = metrics.get_subjective_ratio(article_text)
			"""vad_features = {
			'total_vad': 0,
			'valence_avg': 0,
			'valence_std': 0,
			'valence_max': 0,
			'valence_min': 0,
			'valence_dif': 0,
			'arousal_avg': 0,
			'arousal_std': 0,
			'arousal_max': 0,
			'arousal_min': 0,
			'arousal_dif': 0,
			'dominance_avg': 0,
			'dominance_std': 0,
			'dominance_max': 0,
			'dominance_min': 0,
			'dominance_dif': 0,
			}"""
			vad_features = metrics.get_vad_features(article_text)
			polarity = metrics.sentiment_polarity(article_text)
			bp_stats = metrics.behavioral_physiological(article_text)
			return render_template('result.html', title='FakeNews',posts=posts, article_text=article_text, emotion_count=emotion_count, emotion_ratio=emotion_ratio, total_emotion=total_emotion, totalsubj=totalsubj, subj_feats=subj_feats, vad_features=vad_features, polarity=polarity, bp_stats=bp_stats)

	else:
		return render_template('HomePage.html', title='FakeNews')


@app.route("/result",methods = ['POST', 'GET'])
def result():
    return render_template('result.html', posts=posts)


if __name__ == '__main__':
    app.run(debug=True)