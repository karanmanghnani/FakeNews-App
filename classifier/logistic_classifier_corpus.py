import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import precision_recall_fscore_support, accuracy_score, confusion_matrix
from sklearn.metrics import f1_score, precision_score,recall_score

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

df = pd.read_excel('BD_results_corpus.xlsx')


model = LogisticRegression(max_iter=1000)
#model = LinearSVC(random_state=0, tol=1e-5,max_iter=2000)

#Emotion
predict(df,model,['Emotion'],'Emotion')

#Subjectivity
predict(df, model, ['Subj'], 'Subjectivity')

# Affective
predict(df, model, ['val_avg','aro_avg','dom_avg'], 'Affectivity')

# Polarity
predict(df, model,['pos_words','neg_words'],'Polarity' )

# BP
predict(df,model,['perceptuality','relativity','cognitivity','personal','biological','social'],'BP' )

# All
predict(df, model, ['Emotion', 'Subj', 'val_avg','aro_avg','dom_avg', 'pos_words','neg_words', 'perceptuality','relativity','cognitivity','personal','biological','social'], 'All')