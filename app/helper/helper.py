import numpy as np
import re
import pythainlp

stopwords = pythainlp.corpus.common.thai_stopwords()

def deEmojify(text):
	regrex_pattern = re.compile(pattern = "["
		u"\U0001F600-\U0001F64F"  # emoticons
		u"\U0001F300-\U0001F5FF"  # symbols & pictographs
		u"\U0001F680-\U0001F6FF"  # transport & map symbols
		u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
		"]+", flags = re.UNICODE)
	return regrex_pattern.sub(r'',text)

def check_phone_number(line):
	x=re.search("([0-9]+-+)+[0-9]+|[0-9]{10}|[0-9]{9}|([0-9]+\s+)+[0-9]+",line)
	if x:
		return False
	else:
		return True

def check_other_contact(line):
	x=re.search("Line|line|LINE|ติดต่อ|สาขา|\d{1,3}(?:[,]\d{3})*(?:[,]\d{2})",line)
	if x:
		return False
	else:
		return True

def clear_link(line):
	return re.sub(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))|\S*@\S*\s?"," ",line)


def remove_ht(line):
	line=re.sub("#\S*","",line)
	line=re.sub("\n","",line)
	line=re.sub("\r","",line)
	return line

def regroup_text(text):
	text=clear_link(text)
	text=remove_ht(text)
	words=pythainlp.tokenize.word_tokenize(text,keep_whitespace=True)
	keep_full=[]
	keep=[]
	tmp_full=""
	tmp=[]
	for word in words:
		tmp_full=tmp_full+word
		if word not in stopwords:
			tmp.append(word)
		if len(tmp_full)>120:
			keep_full.append(tmp_full)
			keep.append(" ".join(tmp))
			tmp_full=""
			tmp=[]
	return keep_full,keep

def cleanse_text(fulls,lines):
	keep_full=[]
	keep=[]
	for idx in range(len(fulls)):
		line=fulls[idx]
		tel=check_phone_number(line)
		other=check_other_contact(line)
		if tel and other:
			if len(line)!=0:
				keep_full.append(line)
				keep.append(lines[idx])
	return keep_full,keep













