import xlrd 
import pandas as pd 
import matplotlib.pyplot as plt 

stats = pd.read_excel('BD_results_corpus_detailed.xlsx',0) 

stats_true, stats_false = stats[:998], stats[998:]






stats_emotions= [stats_true.alegria, stats_false.alegria, stats_true.desgosto, stats_false.desgosto, stats_true.medo, stats_false.medo, stats_true.raiva, stats_false.raiva, stats_true.surpresa, stats_false.surpresa, stats_true.tristeza, stats_false.tristeza]
stats_subj= [stats_true.strongsubj, stats_false.strongsubj, stats_true.weaksubj, stats_false.weaksubj]
stats_affective_valence = [stats_true.valence_avg, stats_false.valence_avg, stats_true.valence_std, stats_false.valence_std, stats_true.valence_max, stats_false.valence_max, stats_true.valence_min, stats_false.valence_min, stats_true.valence_dif, stats_false.valence_dif]
stats_affective_arousal = [ stats_true.arousal_avg, stats_false.arousal_avg, stats_true.arousal_std, stats_false.arousal_std, stats_true.arousal_max, stats_false.arousal_max, stats_true.arousal_min, stats_false.arousal_min, stats_true.arousal_dif, stats_false.arousal_dif]
stats_affective_dominance = [stats_true.dominance_avg, stats_false.dominance_avg, stats_true.dominance_std, stats_false.dominance_std, stats_true.dominance_max, stats_false.dominance_max, stats_true.dominance_min, stats_false.dominance_min, stats_true.dominance_dif, stats_false.dominance_dif]
stats_polarity = [stats_true.pos_words, stats_false.pos_words, stats_true.neg_words, stats_false.neg_words]
stats_bp = [stats_true.perceptuality, stats_false.perceptuality, stats_true.relativity, stats_false.relativity, stats_true.cognitivity, stats_false.cognitivity, stats_true.personal, stats_false.personal, stats_true.biological, stats_false.biological, stats_true.social, stats_false.social]


######EMOTION######

fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)
box = ax.boxplot(stats_emotions, patch_artist=True)

colors = ['green', 'red','green', 'red','green', 'red','green', 'red','green', 'red','green', 'red']
for patch, color in zip(box['boxes'], colors):
	patch.set_facecolor(color)

ax.set_xticklabels(['True', 'False','True', 'False','True', 'False','True', 'False','True', 'False','True', 'False'])
ax.set_title('Emotion')

fig.savefig('emotion-stats.png', bbox_inches='tight')

######Subjectivity######

fig = plt.figure(2, figsize=(9, 6))
ax = fig.add_subplot(111)
box = ax.boxplot(stats_subj, patch_artist=True)

colors = ['green', 'red','green', 'red']
for patch, color in zip(box['boxes'], colors):
	patch.set_facecolor(color)

ax.set_xticklabels(['True', 'False','True', 'False'])
ax.set_title('Subjectivity')

fig.savefig('subjectivity-stats.png', bbox_inches='tight')

######Affective######

fig = plt.figure(3, figsize=(9, 6))
ax = fig.add_subplot(111)
box = ax.boxplot(stats_affective_valence, patch_artist=True)

colors = ['green', 'red']*5
for patch, color in zip(box['boxes'], colors):
	patch.set_facecolor(color)

ax.set_xticklabels(['True', 'False']*5)
ax.set_title('Affective-Valence')

fig.savefig('affective-valence-stats.png', bbox_inches='tight')



fig = plt.figure(4, figsize=(9, 6))
ax = fig.add_subplot(111)
box = ax.boxplot(stats_affective_arousal, patch_artist=True)

colors = ['green', 'red']*5
for patch, color in zip(box['boxes'], colors):
	patch.set_facecolor(color)

ax.set_xticklabels(['True', 'False']*5)
ax.set_title('Affective-Arousal')

fig.savefig('affective-arousal-stats.png', bbox_inches='tight')


fig = plt.figure(5, figsize=(9, 6))
ax = fig.add_subplot(111)
box = ax.boxplot(stats_affective_dominance, patch_artist=True)

colors = ['green', 'red']*5
for patch, color in zip(box['boxes'], colors):
	patch.set_facecolor(color)

ax.set_xticklabels(['True', 'False']*5)
ax.set_title('Affective-Domincance')

fig.savefig('affective-dominance-stats.png', bbox_inches='tight')

######Polarity######

fig = plt.figure(6, figsize=(9, 6))
ax = fig.add_subplot(111)
box = ax.boxplot(stats_polarity, patch_artist=True)

colors = ['green', 'red','green', 'red']
for patch, color in zip(box['boxes'], colors):
	patch.set_facecolor(color)

ax.set_xticklabels(['True', 'False','True', 'False'])
ax.set_title('Polarity')

fig.savefig('polarity-stats.png', bbox_inches='tight')


######BP######

fig = plt.figure(7, figsize=(9, 6))
ax = fig.add_subplot(111)
box = ax.boxplot(stats_bp, patch_artist=True)

colors = ['green', 'red', 'green', 'red', 'green', 'red', 'green', 'red', 'green', 'red', 'green', 'red']
for patch, color in zip(box['boxes'], colors):
	patch.set_facecolor(color)

ax.set_xticklabels(['True', 'False','True', 'False','True', 'False', 'True', 'False','True', 'False','True', 'False'])
ax.set_title('BP')

fig.savefig('bp-stats.png', bbox_inches='tight')