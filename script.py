import pandas as pd  #Pandas for Data Manipulation
import openai        #Open AI for AI!
import numpy as np
import math
from openai.embeddings_utils import distances_from_embeddings, indices_of_nearest_neighbors_from_distances

# Download CMU books dataset from Kaggle
df = pd.read_csv("C:/Users/hp/Downloads/BooksDataSet.csv")

# Obtain API key from OpenAI
openai.api_key = "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"
 
df.head()
print(df.head())
df['summary'] = df.summary.replace("\n", " ")
dfList = []
for index, row in df.iterrows():
    print(index) #To keep track of which row we are on

    # Create an empty dictionary to store the information for this row
    entry = {}
    # Add the 'wikiId' value from the current row to the dictionary
    entry['book_id'] = row['book_id']
    # Add the 'freeBaseId' value from the current row to the dictionary
    entry['book_name'] = row['book_name']
    entry['genre'] = row['genre']
    # Add the 'summary' value from the current row to the dictionary
    entry['summary'] = row['summary']
    
    # If the length of the 'summary' column is less than 33000...
    if len(row['summary']) <33000:
        # ... set the 'embedding' key in the dictionary to the result of calling the 'openai.Embedding.create' function on the 'summary' value
        entry['embedding'] = openai.Embedding.create(
            input = row['summary'], model="text-embedding-ada-002")['data'][0]['embedding']
        
    # If the length of the 'summary' column is greater than or equal to 33000...
    else:
        # ... split the 'summary' value at the first period (.) after the middle of the string and take the second half as the first substring
        embedding1 = openai.Embedding.create(
            input = row['summary'][row['summary'].find('.', int (len(row['summary'])/2))+1:], model="text-embedding-ada-002")['data'][0]['embedding']
        # ... take the first half of the 'summary' value as the second substring
        embedding2 = openai.Embedding.create(
            input = row['summary'][:row['summary'].find('.', int (len(row['summary'])/2))+1], model="text-embedding-ada-002")['data'][0]['embedding']
        # ... set the 'embedding' key in the dictionary to the mean of the embeddings of the two substrings
        entry['embedding'] = np.mean([embedding1, embedding2], axis=0)
    # Add the dictionary to the list
    dfList.append(entry)

# Convert the list of dictionaries into a new dataframe and store it in the 'df' variable, overwriting the original dataframe
df = pd.DataFrame(dfList)
# Get user query
query = input("Enter your book recommendation query: ")

# Convert query to embedding
query_embedding = openai.Embedding.create(input=query, model="text-embedding-ada-002")['data'][0]['embedding']
# Create a dictionary that maps 'wikiId' values to 'embedding' values
embedding_dict = df.set_index('book_id')[['embedding']].to_dict()['embedding']

# Calculate the distances between the query embedding and the summary embeddings using the cosine distance metric
distances = distances_from_embeddings(query_embedding, list(embedding_dict.values()), distance_metric="cosine")

# Get the indices of the nearest neighbors (i.e., the summaries with the smallest distances)
indices_of_nearest_neighbors = indices_of_nearest_neighbors_from_distances(distances)
# Print the titles of the top 5 recommended books
print("Titles of top 5 recommended books:")
print(df.loc[indices_of_nearest_neighbors[:5]]['title'])
