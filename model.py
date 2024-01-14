import pandas as pd
import numpy as np

import sklearn
from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import correlation

from sklearn.decomposition import TruncatedSVD
import warnings

from scipy.sparse import csr_matrix

books = pd.read_csv('Dataset/BX-Books.csv', sep=';', encoding="latin-1", on_bad_lines='skip')

books.columns = ['ISBN', 'bookTitle', 'bookAuthor', 'yearOfPublication', 'publisher', 'imageUrlS', 'imageUrlM', 'imageUrlL']
users = pd.read_csv('Dataset/BX-Users.csv', sep=';', on_bad_lines='skip', encoding="latin-1")
users.columns = ['userID', 'Location', 'Age']
ratings = pd.read_csv('Dataset/BX-Book-Ratings.csv', sep=';', on_bad_lines='skip', encoding="latin-1")
ratings.columns = ['userID', 'ISBN', 'bookRating']



combine_book_rating = pd.merge(ratings, books, on = 'ISBN')
columns = ['bookAuthor','yearOfPublication', 'publisher', 'imageUrlS', 'imageUrlM', 'imageUrlL']

combine_book_rating = combine_book_rating.drop(columns, axis = 1)
combine_book_rating.head()

combine_book_rating = combine_book_rating.dropna(axis = 0, subset = ['bookTitle'])

book_ratingcount = (combine_book_rating.
                    groupby(by = ['bookTitle',])['bookRating'].
                    count().
                    reset_index().
                    rename(columns = {'bookRating':'TotalRatingCount'})
                    [['bookTitle','TotalRatingCount']])

rating_with_totalratingcount = combine_book_rating.merge(book_ratingcount, left_on = 'bookTitle', right_on = 'bookTitle', how = 'inner' )

pd.set_option('display.float_format', lambda x: '%.3f' % x)


popularity_threshold = 50
rating_popular_book = rating_with_totalratingcount.query('TotalRatingCount >= @popularity_threshold')

combined = rating_popular_book.merge(users, left_on = 'userID', right_on = 'userID', how = 'left')

us_uk_user_rating = combined[combined['Location'].str.contains("usa|united kingdom")]
us_uk_user_rating = us_uk_user_rating.drop('Age', axis = 1)
us_uk_user_rating.head()

if not us_uk_user_rating[us_uk_user_rating.duplicated(['userID', 'bookTitle'])].empty:
    initial_rows = us_uk_user_rating.shape[0]
    us_uk_user_rating = us_uk_user_rating.drop_duplicates(['userID', 'bookTitle'])
    current_rows = us_uk_user_rating.shape[0]

us_uk_user_rating_pivot = us_uk_user_rating.pivot(index = 'bookTitle',columns = 'userID', values = 'bookRating').fillna(0)
us_uk_user_rating_matrix = csr_matrix(us_uk_user_rating_pivot.values)

model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
model_knn.fit(us_uk_user_rating_matrix)
query_index = np.random.choice(us_uk_user_rating_pivot.shape[0])
distances, indices = model_knn.kneighbors(us_uk_user_rating_pivot.iloc[query_index, :].values.reshape(1, -1), n_neighbors = 6)

# for i in range(0, len(distances.flatten())):
#     if i == 0:
#         print('Recommendations for {0}:\n'.format(us_uk_user_rating_pivot.index[query_index]))
#     else:
#         print('{0}: {1}, with distance of {2}:'.format(i, us_uk_user_rating_pivot.index[indices.flatten()[i]], distances.flatten()[i]))

us_uk_user_rating_pivot2 = us_uk_user_rating.pivot(index = 'userID', columns = 'bookTitle', values = 'bookRating').fillna(0)


X = us_uk_user_rating_pivot2.values.T

SVD = TruncatedSVD(n_components=12, random_state=17)
matrix = SVD.fit_transform(X)
matrix.shape


warnings.filterwarnings("ignore",category =RuntimeWarning)
corr = np.corrcoef(matrix)
corr.shape

us_uk_book_title = us_uk_user_rating_pivot2.columns
us_uk_book_list = list(us_uk_book_title)




def bookRecommendation(selected_book_title):

    coffey_hands = us_uk_book_list.index(selected_book_title)
    corr_coffey_hands  = corr[coffey_hands]
    final=list(us_uk_book_title[(corr_coffey_hands<1.0) & (corr_coffey_hands>0.9)])



    return final 


def methodTwo(abcdef):
    coffey_hands = us_uk_book_list.index(abcdef)
    distances, indices = model_knn.kneighbors(us_uk_user_rating_pivot.iloc[coffey_hands, :].values.reshape(1, -1), n_neighbors = 9)
    c=[]
    for i in range(1, len(distances.flatten())):
        c.append(us_uk_user_rating_pivot.index[indices.flatten()[i]])
    return c


def imgUrlList(final_list):
    
    bt_data=books['bookTitle']
    bi_data = books['imageUrlL']

    bt_list=bt_data.values.tolist()
    bi_list=bi_data.values.tolist()
    gg=[]
    for i in range(len(final_list)):
        gg.append(bi_list[bt_list.index(final_list[i])])
    return gg

book_title =us_uk_user_rating_pivot2.columns

book_title_list=list(book_title)

# print(book_title_list)