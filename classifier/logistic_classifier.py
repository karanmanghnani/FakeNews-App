import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import precision_recall_fscore_support, accuracy_score, confusion_matrix


colnames=['Grau', 'Emotion', 'Subjectivity', 'Affective', 'Polarity', 'BP'] 
df = pd.read_csv("noticias_BD_test.csv", names=colnames, header=None)

#print(df.columns)

model = LogisticRegression()
#model = LinearSVC(random_state=0, tol=1e-5)

# Emotion

X_train, X_test, y_train, y_test = train_test_split(df[['Emotion']],df.Grau,train_size=0.8)

model.fit(X_train, y_train)
y_predicted = model.predict(X_test)
acc = accuracy_score(y_test, y_predicted)
print("Emotion: " + str(acc))

confusion_matrix_1 = confusion_matrix(y_test, y_predicted)
print(confusion_matrix_1)



# Emotion + Subjectivity

X_train, X_test, y_train, y_test = train_test_split(df[['Emotion','Subjectivity']],df.Grau,train_size=0.8)

model.fit(X_train, y_train)
y_predicted = model.predict(X_test)
acc = accuracy_score(y_test, y_predicted)
print("Emotion + Subjectivity: " + str(acc))


confusion_matrix_2 = confusion_matrix(y_test, y_predicted)
print(confusion_matrix_2)



# Emotion + Subjectivity + Affective

X_train, X_test, y_train, y_test = train_test_split(df[['Emotion','Subjectivity','Affective']],df.Grau,train_size=0.8)

model.fit(X_train, y_train)
y_predicted = model.predict(X_test)
acc = accuracy_score(y_test, y_predicted)
print("Emotion + Subjectivity + Affective: " + str(acc))

confusion_matrix_3 = confusion_matrix(y_test, y_predicted)
print(confusion_matrix_3)



# Emotion + Subjectivity + Affective + Polarity

X_train, X_test, y_train, y_test = train_test_split(df[['Emotion','Subjectivity','Affective','Polarity']],df.Grau,train_size=0.8)

model.fit(X_train, y_train)
y_predicted = model.predict(X_test)
acc = accuracy_score(y_test, y_predicted)
print("Emotion + Subjectivity + Affective + Polarity: " + str(acc))


confusion_matrix_4 = confusion_matrix(y_test, y_predicted)
print(confusion_matrix_4)



# Emotion + Subjectivity + Affective + Polarity + BP

X_train, X_test, y_train, y_test = train_test_split(df[['Emotion','Subjectivity','Affective','Polarity','BP']],df.Grau,train_size=0.8)

model.fit(X_train, y_train)
y_predicted = model.predict(X_test)
acc = accuracy_score(y_test, y_predicted)
print("All metrics: " + str(acc))

confusion_matrix_5 = confusion_matrix(y_test, y_predicted)
print(confusion_matrix_5)