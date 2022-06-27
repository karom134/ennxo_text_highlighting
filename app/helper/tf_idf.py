import os
import pandas as pd
import numpy as np

storage=pd.read_csv(os.getcwd()+"/app/storage/sample_word_char.csv")

def sum_dict(dic):
	return np.sum([dic[key] for key in dic.keys() if key!=""])

def build_global_dict(storage):
	global_dict={}
	for row in storage.itertuples():
		document_dict={}
		document_id=row.generated_id
		text=row.tokenized_desc
		lines=text.split("\n")
		for line in lines:
			words=line.split(" ")
			for word in words:
				document_dict[word]=document_dict.get(word,0)+1
		global_dict[document_id]=document_dict
	return global_dict

global_dict=build_global_dict(storage)

def tf(word,word_count,document_dict):
	if word!="":
		return document_dict[word]/word_count
	else:
		return 0

idf_dict={}
def idf(word,documents_dict=global_dict):
	if word in idf_dict:
		return idf_dict[word]
	else:
		total=len(documents_dict)
		count=0
		for key in documents_dict.keys():
			document_dict=documents_dict[key]
			if word in document_dict:
				count+=1
		idf_dict[word]=np.log(total/(count+1))
	return idf_dict[word]