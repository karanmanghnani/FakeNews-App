import xlrd 
import pandas as pd 
import matplotlib.pyplot as plt 

stats = pd.read_excel('BD_results_detailed.xlsx',0) 

stats_true, stats_false = stats[:15], stats[15:]






stats_emotions= [stats_true.alegria, stats_false.alegria, stats_true.desgosto, stats_false.desgosto, stats_true.medo, stats_false.medo, stats_true.raiva, stats_false.raiva, stats_true.surpresa, stats_false.surpresa, stats_true.tristeza, stats_false.tristeza]
stats_subj= [stats_true.strongsubj, stats_false.strongsubj, stats_true.weaksubj, stats_false.weaksubj]
stats_affective_valence = [stats_true.valence_avg, stats_false.valence_avg, stats_true.valence_std, stats_false.valence_std, stats_true.valence_max, stats_false.valence_max, stats_true.valence_min, stats_false.valence_min, stats_true.valence_dif, stats_false.valence_dif]
stats_affective_arousal = [ stats_true.arousal_avg, stats_false.arousal_avg, stats_true.arousal_std, stats_false.arousal_std, stats_true.arousal_max, stats_false.arousal_max, stats_true.arousal_min, stats_false.arousal_min, stats_true.arousal_dif, stats_false.arousal_dif]
stats_affective_dominance = [stats_true.dominance_avg, stats_false.dominance_avg, stats_true.dominance_std, stats_false.dominance_std, stats_true.dominance_max, stats_false.dominance_max, stats_true.dominance_min, stats_false.dominance_min, stats_true.dominance_dif, stats_false.dominance_dif]
stats_polarity = [stats_true.pos_words, stats_false.pos_words, stats_true.neg_words, stats_false.neg_words]
stats_polarity_contrast = [stats_true.pos_contrast, stats_false.pos_contrast, stats_true.neg_contrast, stats_false.neg_contrast]
stats_bp = [stats_true.perceptuality, stats_false.perceptuality, stats_true.relativity, stats_false.relativity, stats_true.cognitivity, stats_false.cognitivity, stats_true.personal, stats_false.personal, stats_true.biological, stats_false.biological, stats_true.social, stats_false.social]
stats_grammatical = [stats_true.informality, stats_false.informality, stats_true.verbs_ratio, stats_false.verbs_ratio, stats_true.adjs_ratio, stats_false.adjs_ratio, stats_true.nouns_ratio, stats_false.nouns_ratio, stats_true.content_diversity, stats_false.content_diversity,	stats_true.redundancy, stats_false.redundancy, stats_true.pausality, stats_false.pausality,	stats_true.expressivity, stats_false.expressivity,	stats_true.non_immediacy, stats_false.non_immediacy, stats_true.modifiers_ratio, stats_false.modifiers_ratio]


######EMOTION######

fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)
box = ax.boxplot(stats_emotions, patch_artist=True)

colors = ['green', 'red','green', 'red','green', 'red','green', 'red','green', 'red','green', 'red']
for patch, color in zip(box['boxes'], colors):
	patch.set_facecolor(color)

plt.xticks([1.5, 3.5, 5.5, 7.5, 9.5, 11.5], ['Happiness','Disgust','Fear','Anger','Surprise','Sadness'])
ax.set_title('Emotion')

fig.savefig('emotion-stats.png', bbox_inches='tight')

######Subjectivity######

fig = plt.figure(2, figsize=(9, 6))
ax = fig.add_subplot(111)
box = ax.boxplot(stats_subj, patch_artist=True)

colors = ['green', 'red','green', 'red']
for patch, color in zip(box['boxes'], colors):
	patch.set_facecolor(color)

plt.xticks([1.5, 3.5], ['Strong subjectivity','Weak subjectivity'])
ax.set_title('Subjectivity')

fig.savefig('subjectivity-stats.png', bbox_inches='tight')

######Affective######

fig = plt.figure(3, figsize=(9, 6))
ax = fig.add_subplot(111)
box = ax.boxplot(stats_affective_valence, patch_artist=True)

colors = ['green', 'red']*5
for patch, color in zip(box['boxes'], colors):
	patch.set_facecolor(color)

plt.xticks([1.5, 3.5, 5.5, 7.5, 9.5], ['Average','Standard deviation','Maximum','Minimum','Maximum - Minimum'])
ax.set_title('Affective-Valence')

fig.savefig('affective-valence-stats.png', bbox_inches='tight')



fig = plt.figure(4, figsize=(9, 6))
ax = fig.add_subplot(111)
box = ax.boxplot(stats_affective_arousal, patch_artist=True)

colors = ['green', 'red']*5
for patch, color in zip(box['boxes'], colors):
	patch.set_facecolor(color)

plt.xticks([1.5, 3.5, 5.5, 7.5, 9.5], ['Average','Standard deviation','Maximum','Minimum','Maximum - Minimum'])
ax.set_title('Affective-Arousal')

fig.savefig('affective-arousal-stats.png', bbox_inches='tight')


fig = plt.figure(5, figsize=(9, 6))
ax = fig.add_subplot(111)
box = ax.boxplot(stats_affective_dominance, patch_artist=True)

colors = ['green', 'red']*5
for patch, color in zip(box['boxes'], colors):
	patch.set_facecolor(color)

plt.xticks([1.5, 3.5, 5.5, 7.5, 9.5], ['Average','Standard deviation','Maximum','Minimum','Maximum - Minimum'])
ax.set_title('Affective-Domincance')

fig.savefig('affective-dominance-stats.png', bbox_inches='tight')

######Polarity######

fig = plt.figure(6, figsize=(9, 6))
ax = fig.add_subplot(111)
box = ax.boxplot(stats_polarity, patch_artist=True)

colors = ['green', 'red','green', 'red']
for patch, color in zip(box['boxes'], colors):
	patch.set_facecolor(color)

plt.xticks([1.5, 3.5], ['Positive words','Negative words'])
ax.set_title('Polarity (Positive & Negative words)')

fig.savefig('polarity-stats.png', bbox_inches='tight')

fig = plt.figure(7, figsize=(9, 6))
ax = fig.add_subplot(111)
box = ax.boxplot(stats_polarity_contrast, patch_artist=True)

colors = ['green', 'red','green', 'red']
for patch, color in zip(box['boxes'], colors):
	patch.set_facecolor(color)

plt.xticks([1.5, 3.5], ['Positive contrast','Negative contrast'])
ax.set_title('Polarity (Positive & Negative contrast)')

fig.savefig('polarity-contrast-stats.png', bbox_inches='tight')


######BP######

fig = plt.figure(8, figsize=(9, 6))
ax = fig.add_subplot(111)
box = ax.boxplot(stats_bp, patch_artist=True)

colors = ['green', 'red', 'green', 'red', 'green', 'red', 'green', 'red', 'green', 'red', 'green', 'red']
for patch, color in zip(box['boxes'], colors):
	patch.set_facecolor(color)

plt.xticks([1.5, 3.5, 5.5, 7.5, 9.5, 11.5], ['Perceptuality', 'Relativity', 'Cognitivity', 'Personal', 'Biological', 'Social'])
ax.set_title('BP')

fig.savefig('bp-stats.png', bbox_inches='tight')

######Grammatical######

fig = plt.figure(9, figsize=(15, 10))
ax = fig.add_subplot(111)
box = ax.boxplot(stats_grammatical, patch_artist=True)

colors = ['green', 'red', 'green', 'red', 'green', 'red', 'green', 'red', 'green', 'red', 'green', 'red', 'green', 'red', 'green', 'red', 'green', 'red', 'green', 'red']
for patch, color in zip(box['boxes'], colors):
	patch.set_facecolor(color)

plt.xticks([1.5, 3.5, 5.5, 7.5, 9.5, 11.5, 13.5, 15.5, 17.5, 19.5], ['Informality', 'Verbs ratio', 'Adjectives ratio', 'Nouns ratio', 'Diversity', 'Redundancy', 'Pausality', 'Expressivity', 'Non immediacy', 'Modifiers ratio'])
ax.set_title('Grammatical')

fig.savefig('grammatical-stats.png', bbox_inches='tight')