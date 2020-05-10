import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import precision_recall_fscore_support, accuracy_score, confusion_matrix


#y_predicted = model.predict_proba(X_test)
#model._classes

df = pd.read_excel('BD_results.xlsx')

#print(df)
#print(df.Label)
model = LogisticRegression()
#model = LinearSVC(random_state=0, tol=1e-5)

# Emotion

#X_train, X_test, y_train, y_test = train_test_split(df[['Emotion']],df.Label,train_size=0.8)

num = [5.2]
X_test = pd.DataFrame(num,  columns=['Emotion'])

X_train = df[['Emotion']]
y_train = df.Label

model.fit(X_train, y_train)


print(model.classes_)
y_predicted = model.predict_proba(X_test)
print(y_predicted[0][0])


"""acc = accuracy_score(y_test, y_predicted)
print("Emotion: " + str(acc))

confusion_matrix_1 = confusion_matrix(y_test, y_predicted)
print(confusion_matrix_1)
"""




#Subjectivity

X_train, X_test, y_train, y_test = train_test_split(df[['Subj']],df.Label,train_size=0.8)

model.fit(X_train, y_train)
y_predicted = model.predict(X_test)
acc = accuracy_score(y_test, y_predicted)
print("Subjectivity: " + str(acc))


confusion_matrix_2 = confusion_matrix(y_test, y_predicted)
print(confusion_matrix_2)



# Affective

X_train, X_test, y_train, y_test = train_test_split(df[['val_avg','aro_avg','dom_avg']],df.Label,train_size=0.8)

model.fit(X_train, y_train)
y_predicted = model.predict(X_test)
acc = accuracy_score(y_test, y_predicted)
print("Affective: " + str(acc))

confusion_matrix_3 = confusion_matrix(y_test, y_predicted)
print(confusion_matrix_3)


# Polarity

X_train, X_test, y_train, y_test = train_test_split(df[['pos_words','neg_words']],df.Label,train_size=0.8)

model.fit(X_train, y_train)
y_predicted = model.predict(X_test)
acc = accuracy_score(y_test, y_predicted)
print("Polarity: " + str(acc))


confusion_matrix_4 = confusion_matrix(y_test, y_predicted)
print(confusion_matrix_4)


# BP

X_train, X_test, y_train, y_test = train_test_split(df[['perceptuality','relativity','cognitivity','personal','biological','social']],df.Label,train_size=0.8)

model.fit(X_train, y_train)
y_predicted = model.predict(X_test)
acc = accuracy_score(y_test, y_predicted)
print("BP: " + str(acc))

confusion_matrix_5 = confusion_matrix(y_test, y_predicted)
print(confusion_matrix_5)