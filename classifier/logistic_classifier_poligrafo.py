import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import precision_recall_fscore_support, accuracy_score, confusion_matrix
from sklearn.metrics import f1_score, precision_score,recall_score


#y_predicted = model.predict_proba(X_test)
#model._classes
def evaluate(y_true,y_pred,metric):
    f1 = f1_score(y_true, y_pred, average=None)
    prec = precision_score(y_true, y_pred, average=None)
    rec = recall_score(y_true, y_pred, average=None)
    acc = accuracy_score(y_true, y_pred)

    print(metric)
    print('Precision: {:0.2f} {:0.2f}'.format(prec[0],prec[1]))
    print('Recall: {:0.2f} {:0.2f}'.format(rec[0], rec[1]))
    print('F1: {:0.2f} {:0.2f}'.format(f1[0],f1[1]))
    print('Accuracy: {:0.2f}'.format(acc))
    print('\n\n')


def predict(df, model, metrics, name):
	X_train, X_test, y_train, y_test = train_test_split(df[metrics],df.Label,train_size=0.8, random_state=0)

	model.fit(X_train, y_train)
	y_predicted = model.predict(X_test)

	evaluate(y_test,y_predicted, name)


#y_predicted = model.predict_proba(X_test)
#model._classes

df = pd.read_excel('BD_results_poligrafo.xlsx')


model = LogisticRegression(max_iter=2000)
#model = LinearSVC(random_state=0, tol=1e-5,max_iter=2000)

#Emotion
predict(df,model,['alegria','desgosto','medo','raiva','surpresa','tristeza'],'Emotion')

#Subjectivity
predict(df, model, ['strongsubj','weaksubj'], 'Subjectivity')

# Affective
predict(df, model, ['valence_avg','arousal_avg','dominance_avg','valence_std','arousal_std','dominance_std','valence_max','arousal_max','dominance_max','valence_min','arousal_min','dominance_min','valence_dif','arousal_dif','dominance_dif'], 'Affectivity')

# Polarity
predict(df, model,['pos_words','neg_words','positive_contrast','negative_contrast'],'Polarity' )

# BP
predict(df,model,['perceptuality','relativity','cognitivity','personal','biological','social'],'BP' )

# All
predict(df, model, ['alegria','positive_contrast','negative_contrast','desgosto','medo','raiva','surpresa','tristeza', 'strongsubj','weaksubj', 'valence_avg','arousal_avg','dominance_avg','valence_std','arousal_std','dominance_std','valence_max','arousal_max','dominance_max','valence_min','arousal_min','dominance_min','valence_dif','arousal_dif','dominance_dif', 'pos_words','neg_words', 'perceptuality','relativity','cognitivity','personal','biological','social'], 'All')

"""#All - Emotion
predict(df, model, ['positive_contrast','negative_contrast','strongsubj','weaksubj', 'valence_avg','arousal_avg','dominance_avg','valence_std','arousal_std','dominance_std','valence_max','arousal_max','dominance_max','valence_min','arousal_min','dominance_min','valence_dif','arousal_dif','dominance_dif', 'pos_words','neg_words', 'perceptuality','relativity','cognitivity','personal','biological','social'], 'All - Emotion')

#All - Subjectivity
predict(df, model, ['positive_contrast','negative_contrast','alegria','desgosto','medo','raiva','surpresa','tristeza', 'valence_avg','arousal_avg','dominance_avg','valence_std','arousal_std','dominance_std','valence_max','arousal_max','dominance_max','valence_min','arousal_min','dominance_min','valence_dif','arousal_dif','dominance_dif', 'pos_words','neg_words', 'perceptuality','relativity','cognitivity','personal','biological','social'], 'All - Subjectivity')

# All - Affective
predict(df, model, ['positive_contrast','negative_contrast','alegria','desgosto','medo','raiva','surpresa','tristeza', 'strongsubj','weaksubj', 'pos_words','neg_words', 'perceptuality','relativity','cognitivity','personal','biological','social'], 'All - Affectivity')

# All - Polarity
predict(df, model, ['alegria','desgosto','medo','raiva','surpresa','tristeza', 'strongsubj','weaksubj', 'valence_avg','arousal_avg','dominance_avg','valence_std','arousal_std','dominance_std','valence_max','arousal_max','dominance_max','valence_min','arousal_min','dominance_min','valence_dif','arousal_dif','dominance_dif', 'perceptuality','relativity','cognitivity','personal','biological','social'], 'All - Polarity')

# All - BP
predict(df, model, ['positive_contrast','negative_contrast','alegria','desgosto','medo','raiva','surpresa','tristeza', 'strongsubj','weaksubj', 'valence_avg','arousal_avg','dominance_avg','valence_std','arousal_std','dominance_std','valence_max','arousal_max','dominance_max','valence_min','arousal_min','dominance_min','valence_dif','arousal_dif','dominance_dif', 'pos_words','neg_words'], 'All - BP')

# All - Affectivity, polarity
predict(df, model, ['alegria','desgosto','medo','raiva','surpresa','tristeza', 'strongsubj','weaksubj', 'perceptuality','relativity','cognitivity','personal','biological','social'], 'All - Affectivity, polarity')

# Affectivity + polarity
predict(df, model, [ 'valence_avg','arousal_avg','dominance_avg','valence_std','arousal_std','dominance_std','valence_max','arousal_max','dominance_max','valence_min','arousal_min','dominance_min','valence_dif','arousal_dif','dominance_dif', 'pos_words','neg_words','positive_contrast','negative_contrast'], 'All + Affectivity, polarity')
"""