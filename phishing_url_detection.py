import numpy as np
import pandas as pd

#from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression as lr
from sklearn.model_selection import train_test_split


data = pd.read_csv("urldata.csv")
y = data["label"]
urls = data["url"]
vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(urls)

X_train, X_test, y_train, y_test = train_test_split(X, y,test_size = 0.3)

clf = lr()
clf.fit(X_train, y_train)

print(clf.predict(X_test))
print(clf.score(X_test, y_test)*100)

X_input = []
url = input("Enter a Url:")
X_input.append(url)

X_input = vectorizer.transform(X_input)

print(clf.predict(X_input))
