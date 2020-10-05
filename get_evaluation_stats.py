from firebase import firebase


def q1_stats(q1, result):
	if(result == '1'):
		q1['Completely Unrepresentative'] += 1
	elif(result == '2'):
		q1['Somewhat Unrepresentative'] += 1
	elif(result == '3'):
		q1['Somewhat Representative'] += 1
	elif(result == '4'):
		q1['Completely Representative'] += 1

def q2_stats(q2, result):
	if(result == '1'):
		q2['It representative'] += 1
	elif(result == '2'):
		q2['Title is on a different topic than the body'] += 1
	elif(result == '3'):
		q2['Title carries only little information about the body'] += 1
	elif(result == '4'):
		q2['Title takes a different point of view than the body'] += 1
	elif(result == '5'):
		q2['Title overstates/understates claims or conclusions'] += 1

def q3_stats(q3, result):
	if(result == '1'):
		q3['1'] += 1
	elif(result == '2'):
		q3['2'] += 1
	elif(result == '3'):
		q3['3'] += 1
	elif(result == '4'):
		q3['4'] += 1
	elif(result == '5'):
		q3['5'] += 1

def q4_stats(q4, result):
	q4.append(result)

def q5_stats(q5, result):
	if(result == '1'):
		q5['1'] += 1
	elif(result == '2'):
		q5['2'] += 1
	elif(result == '3'):
		q5['3'] += 1
	elif(result == '4'):
		q5['4'] += 1
	elif(result == '5'):
		q5['5'] += 1

def q6_stats(q6, result):
	if(result == 'true'):
		q6['true'] += 1
	elif(result == 'dubious'):
		q6['dubious'] += 1
	elif(result == 'false'):
		q6['false'] += 1

def q7_stats(q7, result):
	if(result == '1'):
		q7['Big impact'] += 1
	elif(result == '2'):
		q7['Small impact'] += 1
	elif(result == '3'):
		q7['No impact'] += 1

def q8_stats(q8, result):
	if(result == 'Emotion'):
		q8['Emotion'] += 1
	elif(result == 'Subjectivity'):
		q8['Subjectivity'] += 1
	elif(result == 'Affectivity'):
		q8['Affectivity'] += 1
	elif(result == 'Polarity'):
		q8['Polarity'] += 1
	elif(result == 'BP'):
		q8['BP'] += 1
	elif(result == 'Source'):
		q8['Source'] += 1
	elif(result == 'None'):
		q8['None'] += 1

def get_article_stats(article, result, firebase, bool):
	q1 = { 'Completely Unrepresentative': 0, 'Somewhat Unrepresentative': 0, 'Somewhat Representative': 0,'Completely Representative': 0}

	q2 = { 'It representative': 0, 'Title is on a different topic than the body': 0, 'Title carries only little information about the body': 0, 'Title takes a different point of view than the body': 0, 'Title overstates/understates claims or conclusions': 0}

	q3 = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}

	q4 = []

	q5 = { '1': 0, '2': 0, '3': 0, '4': 0, '5': 0 }

	q6 = { 'true': 0, 'dubious': 0, 'false': 0}

	q7 = { 'Big impact': 0,  'Small impact': 0, 'No impact': 0 }

	q8 = { 'Emotion': 0, 'Subjectivity': 0, 'Affectivity': 0, 'Polarity': 0, 'BP': 0,'Source': 0,'None': 0 }

	for key in result.keys():
		if (result[key]['article'] == article):
			q1_stats(q1, result[key]['Q1'])
			q2_stats(q2, result[key]['Q2'])
			q3_stats(q3, result[key]['Q3'])
			q4_stats(q4, result[key]['Q4'])
			q5_stats(q5, result[key]['Q5'])
			q6_stats(q6, result[key]['Q6'])
			if(bool == True):
				q7_stats(q7, result[key]['Q7'])
				q8_stats(q8, result[key]['Q8'])

	print("Answers for article " + str(article))
	print('1. Does the title represent the content of the article?')
	print(q1)
	print('\n')
	print('2. If you selected unrepresentative, why do you think the title does not represent the content of the article?')
	print(q2)
	print('\n')
	print('3. Is the title clickbaity (form of false advertisement to attract attention and to make users read the news)? <br> Rank on a scale of 1 (Not clickbaity) to 5 (Very clickbaity)')
	print(q3)
	print('\n')
	print('4. If you think the headline is clickbaity, what makes you think it is?')
	print(q4)
	print('\n')
	print('5. Is the article subjective (it is expressed an opinion)? <br> Rank on a scale of 1 (Not subjective) to 5 (Very subjective)')
	print(q5)
	print('\n')
	print('6. How do you classify this news?')
	print(q6)
	print('\n')
	print('7. Did the indicators made an impact in your assessment of the credibility of the article?')
	print(q7)
	print('\n')
	print('8. If it made an impact in your assessment, which indicator made the biggest impact?')
	print(q8)
	print('\n')



firebase = firebase.FirebaseApplication('https://fakenews-app-d59dc.firebaseio.com/', None)




##############################
#       With indicators      #
##############################
print("With Indicators")

result = firebase.get('/fakenews-app-d59dc/with_labels', '')


get_article_stats(1, result, firebase, True)
get_article_stats(2, result, firebase, True)
get_article_stats(3, result, firebase, True)
get_article_stats(4, result, firebase, True)
get_article_stats(5, result, firebase, True)
get_article_stats(6, result, firebase, True)

##############################
#     Without indicators     #
##############################
print("Without Indicators")

result = firebase.get('/fakenews-app-d59dc/without_labels', '')


get_article_stats(1, result, firebase, False)
get_article_stats(2, result, firebase, False)
get_article_stats(3, result, firebase, False)
get_article_stats(4, result, firebase, False)
get_article_stats(5, result, firebase, False)
get_article_stats(6, result, firebase, False)



##############################
#     With indicators only   #
##############################
print("With Indicators only")

result = firebase.get('/fakenews-app-d59dc/with_labels_only', '')


get_article_stats(1, result, firebase, True)
get_article_stats(2, result, firebase, True)
get_article_stats(3, result, firebase, True)
get_article_stats(4, result, firebase, True)
get_article_stats(5, result, firebase, True)
get_article_stats(6, result, firebase, True)