# %%
import glob
import pandas as pd
import matplotlib.pyplot as plt 
import json 
import random
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

# %%
#Read the txt into a list and then into a dataframe
def read_txt(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        #Delete the /usercomments part of the url and leave the rest
        lines = [re.sub('/usercomments\n', '', line) for line in lines]
    return lines

path = 'data/reviews_url.txt'

urls = read_txt(path)

urls_df = pd.DataFrame(urls, columns=['url'])

print (urls_df.head(10))

# %%
#Read all files from a folder and save them in a dataframe
path = 'data/reviews/'
all_files = glob.glob(path + "/*.txt")

reviews = []

for filename in all_files:
    with open(filename, 'r') as f:
        data = f.read()
        reviews.append(data)

#Clean non alphanumeric characters in each review from the reviews list
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

reviews = [clean_text(review) for review in reviews]

#Create a dataframe with the reviews
reviews_df = pd.DataFrame(reviews, columns=['review'])

print(reviews_df.head(10))

# %%
#Join the dataframe with the urls and the reviews
data = pd.concat([urls_df, reviews_df], axis=1)

#Save the data to a csv file
data.to_csv('data/data.csv', index=False)

#Create a smaller file with only 30% of the data
data_smaller = data.sample(frac=0.1, random_state=42)

#Save the smaller file to a csv file
data_smaller.to_csv('data/data_smaller.csv', index=False)

print(data.head(10))

# %%
#Check that every url has a review
print(data.isnull().sum())

# %%
#iloc is used to select rows and columns by number, in the order that they appear in the data frame
x = data.iloc[0]
x

# %%
x['review']

# %%
#This would be necessary in case the contents of a column contained more than a single string
#So we could join the strings into a single one

#j = json.loads(x['review'])
#j
#' '.join(''.join(jj['name'].split()) for jj in j)

# %%
#This too would be necessary in case the contents of a column contained more than a single string

# convert the relevant data for each movie into a single string
# to be ingested by TfidfVectorizer
def urls_and_reviews_to_string(row):
  urls = json.loads(row['url'])
  urls = ' '.join(''.join(j['name'].split()) for j in urls)

  reviews = json.loads(row['review'])
  reviews = ' '.join(''.join(j['name'].split()) for j in reviews)
  return "%s %s" % (urls, reviews)

# %%
#create a tf-idf vectorizer object
#max_features: build a vocabulary that only consider the top max_features ordered by term frequency across the corpus
tfidf = TfidfVectorizer(max_features=2000, stop_words='english')

# %%
#Create a data matrix from the reviews
X = tfidf.fit_transform(data['review'])

# %%
X

# %%
query = X[2345]
query

# %%
#Print the query vector
query.toarray()

# %%
#compute similarity between query and every vector in X
scores = cosine_similarity(query, X)
scores

# %%
# currently the array is 1 x N, make it just a 1-D array
scores = scores.flatten()

# %%
plt.plot(scores)

# %%
(-scores).argsort()

# %%
plt.plot(scores[(-scores).argsort()])

# %%
#Get the top 10 most similar reviews
top_10 = (-scores).argsort()[:10]
# The - sign is used to sort in descending order

# %%
#convert indices to urls
data.iloc[top_10]['url']

# %%
#convert indices to reviews
data.iloc[top_10]['review']

# %%
#Save indices, urls and reviews to a csv file 
with open("top_10.csv", 'w') as f:
    data.iloc[top_10].to_csv(f)

# %%
#Create a function to do the same as above
def recommend(index):
    #Get the vector in the dataframe for an index
    query = X[index]
    #Compute pairwise similarity between the query vector and all the vectors in the dataframe
    scores = cosine_similarity(query, X)
    #Currently the array is 1 x N, make it just a 1-D array
    scores = scores.flatten()
    #Plot the scores
    plt.plot(scores)
    #Plot the scores in descending order
    plt.plot(scores[(-scores).argsort()])
    #Get the top 6 most similar reviews
    top_6 = (-scores).argsort()[1:7]
    #Convert indices to urls
    print(data.iloc[top_6]['url'])
    #Convert indices to reviews
    print(data.iloc[top_6]['review'])
    #Save indices, urls and reviews to a csv file
    with open("top_6_{}.csv".format(index), 'w') as f:
        data.iloc[top_6].to_csv(f,)

# %%
print("Recommendations for index 4435:\n")
print(recommend(4435))

# %%



