
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

def predict(filename):
    df = pd.read_csv('C:\\Users\\verma\\Desktop\\noble_news\\train.csv')

    y = df.Label
    X = df.Body

    #train_test separation
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.2)

    #Applying tfidf to the data set
    tfidf_vect = TfidfVectorizer(stop_words = 'english')
    tfidf_train = tfidf_vect.fit_transform(X_train.apply(lambda x: np.str_(x)))
    tfidf_test = tfidf_vect.transform(X_test.apply(lambda x: np.str_(x)))
    tfidf_df = pd.DataFrame(tfidf_train.A, columns=tfidf_vect.get_feature_names())

    #Applying Naive Bayes
    clf = MultinomialNB() 
    clf.fit(tfidf_train, y_train)                       # Fit Naive Bayes classifier according to X, y
    pred = clf.predict(tfidf_test)                     # Perform classification on an array of test vectors X.
    score = metrics.accuracy_score(y_test, pred)
    print("accuracy:   %0.3f" % score)
    a=pd.read_csv(filename)
    X_test=a['text']
    tfidf_test = tfidf_vect.transform(X_test.apply(lambda x: np.str_(x)))
    pred=clf.predict(tfidf_test)
    probs=clf.predict_proba(tfidf_test)
    probs=(probs+1.0)/2.0
    print(probs[0][0]*100)
    return(probs[0][0]*100)
    
predict('C:\\Users\\verma\\Desktop\\noble_news\\data.csv')