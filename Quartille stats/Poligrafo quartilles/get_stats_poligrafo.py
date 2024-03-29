import xlrd 
import pandas as pd 
import matplotlib.pyplot as plt 

stats = pd.read_excel('BD_results.xlsx',0) 

stats_true, stats_false = stats[:15], stats[15:]


stats_emotions= [stats_true.Emotion, stats_false.Emotion]
stats_subj= [stats_true.Subj, stats_false.Subj]
stats_affective = [stats_true.val_avg, stats_false.val_avg, stats_true.aro_avg, stats_false.aro_avg, stats_true.dom_avg, stats_false.dom_avg]
stats_polarity = [stats_true.pos_words, stats_false.pos_words, stats_true.neg_words, stats_false.neg_words ]
stats_polarity_contrast = [stats_true.positive_contrast, stats_false.positive_contrast, stats_true.negative_contrast, stats_false.negative_contrast]
stats_bp = [stats_true.perceptuality, stats_false.perceptuality, stats_true.relativity, stats_false.relativity, stats_true.cognitivity, stats_false.cognitivity, stats_true.personal, stats_false.personal, stats_true.biological, stats_false.biological, stats_true.social, stats_false.social]


######EMOTION######

fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)
box = ax.boxplot(stats_emotions, patch_artist=True)

colors = ['green', 'red']
for patch, color in zip(box['boxes'], colors):
	patch.set_facecolor(color)

ax.set_xticklabels(['True', 'False'])
ax.set_title('Emotion')

fig.savefig('emotion-stats.png', bbox_inches='tight')

######Subjectivity######

fig = plt.figure(2, figsize=(9, 6))
ax = fig.add_subplot(111)
box = ax.boxplot(stats_subj, patch_artist=True)

colors = ['green', 'red']
for patch, color in zip(box['boxes'], colors):
	patch.set_facecolor(color)

ax.set_xticklabels(['True', 'False'])
ax.set_title('Subjectivity')

fig.savefig('subjectivity-stats.png', bbox_inches='tight')

######Affective######

fig = plt.figure(3, figsize=(9, 6))
ax = fig.add_subplot(111)
box = ax.boxplot(stats_affective, patch_artist=True)

colors = ['green', 'red','green', 'red','green', 'red']
for patch, color in zip(box['boxes'], colors):
	patch.set_facecolor(color)

ax.set_xticklabels(['True', 'False','True', 'False','True', 'False'])
ax.set_title('Affective')

fig.savefig('affective-stats.png', bbox_inches='tight')

######Polarity######

fig = plt.figure(4, figsize=(9, 6))
ax = fig.add_subplot(111)
box = ax.boxplot(stats_polarity, patch_artist=True)

colors = ['green', 'red','green', 'red']
for patch, color in zip(box['boxes'], colors):
	patch.set_facecolor(color)

ax.set_xticklabels(['True', 'False','True', 'False'])
ax.set_title('Polarity (Positive & Negative words)')

fig.savefig('poligrafo-polarity-stats.png', bbox_inches='tight')

######Polarity contrast ######

fig = plt.figure(5, figsize=(9, 6))
ax = fig.add_subplot(111)
box = ax.boxplot(stats_polarity_contrast, patch_artist=True)

colors = ['green', 'red','green', 'red']
for patch, color in zip(box['boxes'], colors):
	patch.set_facecolor(color)

ax.set_xticklabels(['True', 'False','True', 'False'])
ax.set_title('Polarity (Positive & Negative contrast)')

fig.savefig('poligrafo-polarity-contrast-stats.png', bbox_inches='tight')



######BP######

fig = plt.figure(6, figsize=(9, 6))
ax = fig.add_subplot(111)
box = ax.boxplot(stats_bp, patch_artist=True)

colors = ['green', 'red', 'green', 'red', 'green', 'red', 'green', 'red', 'green', 'red', 'green', 'red']
for patch, color in zip(box['boxes'], colors):
	patch.set_facecolor(color)

ax.set_xticklabels(['True', 'False','True', 'False','True', 'False', 'True', 'False','True', 'False','True', 'False'])
ax.set_title('BP')

fig.savefig('bp-stats.png', bbox_inches='tight')