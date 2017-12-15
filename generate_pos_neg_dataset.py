import sys
from random import shuffle
import pdb

off = open("output.tsv", "w")

# read in matched positive examples 
with open("matched_positive_multi_all.tsv", "r") as iff:
	lines = iff.readlines()
	
qapairs = {}
for line in lines[1:]:
	asin, questiontype, questiontext, answertext, helpful = line.strip().split("\t")
	if asin not in qapairs:
		qapairs[asin] = {}
	if questiontext not in qapairs[asin]:
		qapairs[asin][questiontext] = []
	qapairs[asin][questiontext] += [[asin, questiontype, questiontext, answertext, helpful]] 

	

#lookup question answer-pair for that ASIN from all qa pairs, confirm asked question is different.  take answer as negative example.
for line in lines[1:]: #ignore header
	foundneg = False
	asin, questiontype, questiontext, answertext, helpful = line.strip().split("\t")

	#write positive example
	pex = "\t".join([asin, questiontype, questiontext, answertext, "1"])
	print(pex, file=off)

	#write negative example
	#find negative example with all same except answertext and "0" label.  use asin to find other question with matching asin.  use its answer as negative example.
	#for otherline in lines[1:]:
	#	casin, cquestiontype, cquestiontext, canswertext, chelpful = otherline.strip().split("\t")
	#get randomized list of all qapairs with asin and questiontext
	candidates = qapairs[asin].values()
	flat_list = [item for sublist in candidates for item in sublist]
	shuffle(flat_list)
	#pdb.set_trace()
	for cand in flat_list:
		casin, cquestiontype, cquestiontext, canswertext, chelpful = cand
		if casin == asin and questiontext != cquestiontext:
			nex = "\t".join([asin, questiontype, questiontext, canswertext, "0"])
			print(nex, file=off)
			foundneg = True
			break
	#assert foundneg == True
	if foundneg == False:
		print("could not find neg example for: {}".format(" ".join([asin, questiontext, answertext])))

		

