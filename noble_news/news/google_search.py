import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

def check_similarity(X,Y):
    # tokenization 
    X_list = word_tokenize(X)  
    Y_list = word_tokenize(Y) 
    
    # sw contains the list of stopwords 
    sw = stopwords.words('english')  
    l1 =[];l2 =[] 
    
    # remove stop words from the string 
    X_set = {w for w in X_list if not w in sw}  
    Y_set = {w for w in Y_list if not w in sw} 
    
    # form a set containing keywords of both strings  
    rvector = X_set.union(Y_set)  
    for w in rvector: 
        if w in X_set: l1.append(1) # create a vector 
        else: l1.append(0) 
        if w in Y_set: l2.append(1) 
        else: l2.append(0) 
    c = 0
    
    # cosine formula  
    for i in range(len(rvector)): 
            c+= l1[i]*l2[i] 
    cosine = c / float((sum(l1)*sum(l2))**0.5) 
    if(cosine>0.75):
        return 1
    else:
        return 0

def score_generator():
	score=0.0
	score = true_points - (false_points * 3)
	if(false_points >= 3):
		score -= false_points * false_points
	if(true_points <= 5):
		score /= 4
	elif(true_points <= 8):
		score /= 3
	elif(true_points <= 10):
		score /= 2
	elif(true_points <= 13):
		score /= 1.5

	if(true_points == 0 and false_points == 0):
		score=-1
		return score

	score = score / (true_points + false_points)

	if(score < 0):
		score = 0
	elif(score >= 1):
		score = 0.9

	print("Truth probability = " + str("{:.3f}".format(score)))
	return "{:.3f}".format(score)

def check_if_legit(domain_name):

	global true_points
	global false_points

	if domain_name in legit_sites:
		true_points += 1

	if domain_name in illegit_sites:
		false_points += 1

def get_the_domain_name(complete_link):

	broken_url = urlparse(complete_link)
	domain_name = '{uri.scheme}://{uri.netloc}/'.format(uri=broken_url)

	if(domain_name[:5] == 'https'):
		domain_name = domain_name.replace('https://www.', '')
		domain_name = domain_name.replace('https://', '')

		if(domain_name[-1] == '/'):
			domain_name = domain_name[:-1]
   
		if(domain_name!="webcache.googleusercontent.com" and domain_name!="policies.google.com" and domain_name!="support.google.com"):
			check_if_legit(domain_name)
			domains_list.append(domain_name)
			return

	if(domain_name[:4] == 'http'):
		domain_name = domain_name.replace('http://www.', '')
		domain_name = domain_name.replace('https://', '')

		if(domain_name[-1] == '/'):
			domain_name = domain_name[:-1]
		if(domain_name!="webcache.googleusercontent.com" and domain_name!="policies.google.com" and domain_name!="support.google.com"):
			check_if_legit(domain_name)
			domains_list.append(domain_name)

def google_search_it(query):
	global true_points
	global false_points
	url = 'https://www.google.com/search?q=' + query
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
	html = requests.get(url, headers=headers)
	soup = BeautifulSoup(html.text, 'html.parser')
	results = soup.find('div', id='result-stats')

	if(results.text == ""):
		print("wtf?")
	else:
		print(results.text)

	stories = ''

	for links_a in soup.find_all('a'):
		
		if links_a.find('span'):
			t=(links_a.find('span').text)
			#print(t)
			if(t and (check_similarity(t,query)==1)):
				true_points += 1
			if(t and query in t):
				true_points += 1
		if links_a.has_attr('href'):

			complete_title = ''.join(links_a.findAll(text=True))

			complete_link = links_a['href']

			if links_a['href'][:4] != 'http':
				complete_link = links_a['href'][7:]


			
			get_the_domain_name(complete_link)

def start_predict(query):

	global true_points, false_points
	global legit_sites, illegit_sites
	true_points = 0
	false_points = 0

	with open("true_dataset.txt") as true_data:
	    legit_sites = true_data.readlines()
	legit_sites = [x.strip() for x in legit_sites]

	with open("fake_dataset.txt") as fake_data:
	    illegit_sites = fake_data.readlines()
	illegit_sites = [x.strip() for x in illegit_sites]

	fake_words = ['fake', 'hoax', 'lie', 'lies', 'lies','worst','false', 'illegitimate', 'rumour', 'counterfeit', 'forged', 'fictitious', 'fabricated', 'fraud']

	query_list = query.split()
	sumx=0.0
	for i in query_list:
		if i in fake_words:
			sumx += 7

	google_search_it(query)
	#print(sumx)
	score=score_generator()
	score=float(score)+sumx
	return str(score)




domains_list = []

true_points = 0
false_points = 0

legit_sites = []
illegit_sites = []

start_predict("Biden lost the election")
