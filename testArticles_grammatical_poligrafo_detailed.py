import xlrd 
import unidecode
import get_metrics as metrics
import xlsxwriter

workbook = xlsxwriter.Workbook('BD_results_poligrafo_grammatical.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write(0, 0,"n_sents")
worksheet.write(0, 1,"informality")
worksheet.write(0, 2,"verbs_ratio")
worksheet.write(0, 3,"adjs_ratio")
worksheet.write(0, 4,"nouns_ratio")
worksheet.write(0, 5,"content_diversity")
worksheet.write(0, 6,"redundancy")

worksheet.write(0, 7,"pausality")
worksheet.write(0, 8,"expressivity")

worksheet.write(0, 9,"non_immediacy")
worksheet.write(0, 10,"'modifiers_ratio")


row=1
col=0

loc = ("Noticías_BD.xlsx") 
  
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
sheet.cell_value(0, 0) 
  
for i in range(1,sheet.nrows):
	worksheet.write(row, col, sheet.cell_value(i, 3))
	row+=1

row=1
col=1



for i in range(1,sheet.nrows):
	sentences = metrics.tokenize_sentences(sheet.cell_value(i, 1))
	lemmas = metrics.lemmatize_words(sentences)
	words = metrics.tokenize_words(sentences)
	words = words[0]

	doc_citiustags = metrics.citiustagger_doc(sentences)
	#print(doc_citiustags)

	gram_stats = {}

	gram_stats['n_sents'] = len(sentences)
	gram_stats['informality'] = metrics.get_typographical_error_ratio(words)

	gram_stats['verbs_ratio'] = metrics.get_verbs_ratio(doc_citiustags, words)
	gram_stats['adjs_ratio'] = metrics.get_adjectives_ratio(doc_citiustags, words)
	gram_stats['nouns_ratio'] = metrics.metrics.get_nouns_ratio(doc_citiustags, words)
	gram_stats['content_diversity'] = metrics.get_content_diversity(doc_citiustags)
	gram_stats['redundancy'] = metrics.get_redundancy(gram_stats['n_sents'], doc_citiustags)
	gram_stats['pausality'] = metrics.get_pausality(gram_stats['n_sents'], doc_citiustags)
	gram_stats['expressivity'] = metrics.get_emotiveness(doc_citiustags)
	gram_stats['non_immediacy'] = metrics.get_non_immediacy(doc_citiustags, words)
	gram_stats['modifiers_ratio'] = metrics.get_modifiers_ratio(doc_citiustags, words)
	print(gram_stats)

	worksheet.write(row, col, gram_stats['n_sents'])
	col+=1
	worksheet.write(row, col, gram_stats['informality'])
	col+=1
	worksheet.write(row, col, gram_stats['verbs_ratio'])
	col+=1
	worksheet.write(row, col, gram_stats['adjs_ratio'])
	col+=1
	worksheet.write(row, col, gram_stats['nouns_ratio'])
	col+=1
	worksheet.write(row, col, gram_stats['content_diversity'])
	col+=1
	worksheet.write(row, col, gram_stats['redundancy'])
	col+=1
	worksheet.write(row, col, gram_stats['pausality'])
	col+=1
	worksheet.write(row, col, gram_stats['expressivity'])
	col+=1
	worksheet.write(row, col, gram_stats['non_immediacy'])
	col+=1
	worksheet.write(row, col, gram_stats['modifiers_ratio'])

	col=1
	row+=1

workbook.close()