from fastapi import APIRouter
from pydantic import BaseModel
from ..helper.helper import regroup_text,cleanse_text
from ..helper.tf_idf import tf,idf
import numpy as np


router = APIRouter(
	prefix="/highlight",
	tags=["highlight"],
	responses={404:{"description":"Not found"}}
	)

class Product(BaseModel):
	desc: str

def build_document_dict(tokenized_lines):
	tracker={}
	for line in tokenized_lines:
		words=line.split(" ")
		for word in words:
			tracker[word]=tracker.get(word,0)+1
	return tracker

def sum_dict(dic):
	return np.sum([dic[key] for key in dic.keys() if key!=""])


@router.put("/")
async def makeHighlight(product: Product):
	desc=product.desc
	full,filtered=regroup_text(desc)
	full,filtered=cleanse_text(full,filtered)

	doc_dict=build_document_dict(filtered)
	count=sum_dict(doc_dict)

	line_score=[]
	decay_factor=0
	decay_rate=1.1
	for line in filtered:
		score=0
		words=line.split(" ")
		for word in words:
			tf_score=tf(word,count,doc_dict)
			idf_score=idf(word)
			score+=tf_score*idf_score
		line_score.append(score/len(words)*(1/decay_rate**decay_factor))
		decay_factor+=1
	line_score=np.array(line_score)
	max_score_line=np.argmax(line_score)
	return {"result":full[max_score_line]}