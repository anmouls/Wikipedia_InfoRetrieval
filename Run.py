import nltk #package used to extract tokens from the documents
import os,io,glob #used to load all the text documents in the corpus and read them
from nltk.corpus import stopwords #used to import the list of stopwords to be excluded from the dictionary
import math	#perform log operations
from PorterStem import PorterStemmer #stem the tokens to reduce them to a base form
import operator #used to sort the list of documents in decreasing order of ranking

stop_words = stopwords.words('English') #stores all the stopwords in English language
text="" #stores the text read from each document
tokens1=[] #tokens1,2,3,4,5 store the tokens at each step of normalization
tokens2=[]
tokens3=[]
tokens4=[]
tokens5=[]
N=1 #document id
length=0; #used for length normalization for each document
dictionary={} #stores terms and their posting lists
corpus = {}	  #stores document id and titles
idf={}		  #stores 
ps = PorterStemmer() #instance of PorterStemmer class to call the stemming function later
os.chdir("C:\Users\Anmol\Desktop\Corpus") #enter directory location here
for file in glob.glob("*.txt"): #for all text documents in the corpus directory
	corpus.setdefault(N,file)	#add doc id and name to corpus
	f = io.open(file,'rU',encoding='utf-8') #open the doc in read mode 
	text=f.read() 				#read the doc contents and save in text
	tokens = nltk.word_tokenize(text)		#nltk generates tokens from text and then we perform multiple steps for normalization
	tokens1 = [w for w in tokens if w.isalpha() ]	#remove punctuations
	tokens2 = [w.lower() for w in tokens1] 	#convert to lower case
	tokens3 = [w for w in tokens2 if w not in stop_words]	#exclude stopwords
	for w in tokens3:
		tokens4.append(PorterStemmer.stem(ps,w,0,len(w)-1))	#stem the remaining tokens using Porter Stemmer Algorithm
	term_freq = nltk.FreqDist(tokens4)	#store the term frequency of each term in the doc
	tokens5 = set(tokens4)		#remove repeated terms
	for w in tokens5:
		length = length + (1+math.log(term_freq[w],10))*(1+math.log(term_freq[w],10))  #sum up normalized term frequencies for length normalization
	length=math.sqrt(length)	
	for w in tokens5:
		tup = (N,(1+math.log(term_freq[w],10))/float(length))	#for each term, make a posting list containing tuples 
		if dictionary.has_key(w):								#of doc id and normalized term frequency
			dictionary[w].append(tup)
		else:
			dictionary.setdefault(w,[])
			dictionary[w]=[tup]
	text=""		#reset all variables for next doc in the corpus
	length=0
	tokens1=[]
	tokens2=[]
	tokens3=[]
	tokens4=[]
	tokens5=[]
	N=N+1
N=N-1		#now N has the total number of documents in the corpus
for w in dictionary.iterkeys():	#for all terms in the dictionary
	idf[w]=math.log(float(N)/len(dictionary[w]),10) 	#calculate and save the idf
#this completes indexing, now we move on to handling search queries
def search(query): #function to search for a query
	length=0	#performing same steps at the front end (query level) that were done at the back end (document level)
	tokens1=[]
	tokens2=[]
	tokens3=[]
	tokens4=[]
	tokens5=[]
	q_dict={}		#stores the tf-idf for each term in the query
	score_dict={}	#stores the score of each document with respect to each term in the query
	tokens = nltk.word_tokenize(query)
	tokens1 = [w for w in tokens if w.isalpha() ]
	tokens2 = [w.lower() for w in tokens1] 
	tokens3 = [w for w in tokens2 if w not in stop_words]
	for w in tokens3:
		tokens4.append(PorterStemmer.stem(ps,w,0,len(w)-1))
	term_freq = nltk.FreqDist(tokens4)
	tokens5 = set(tokens4)
	for w in tokens5:
		length = length + (1+math.log(term_freq[w],10))*(1+math.log(term_freq[w],10))
	length=math.sqrt(length)
	if(len(tokens5)==1):	#for one word queries do not consider idf, rank documents based on term frequencies
		for w in tokens5: #sort the posting list in descending order
			sorted_list = sorted(dictionary[w],key=operator.itemgetter(1),reverse=True)
	else:	#if query is more than one word
		for w in tokens5:	
			tup = (1+math.log(term_freq[w],10)*idf[w])/length #normalized tf-idf score for each term
			q_dict.setdefault(w,tup)
		for w in tokens5:	#for each term in the query
			for d in dictionary[w]:	#for each document in the posting list of each term
				if score_dict.has_key(d[0]):	
					score_dict[d[0]]=score_dict[d[0]]+(q_dict[w]*(d[1])) #calculate cosine score
				else:
					score_dict.setdefault(d[0],q_dict[w]*(d[1]))	#calculate cosine score
		sorted_list = sorted(score_dict.items(), key=operator.itemgetter(1),reverse=True) #sort the documents in decreasing order of cosine scores
	for x in sorted_list[0:19]:
		print corpus.get(x[0])	#print the titles of first 20 results

for i in range(1,100):	#takes 100 input search queries
	q = raw_input("Enter query: ")
	search(q)