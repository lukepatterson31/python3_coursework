import requests_with_caching


def get_movies_from_tastedive(movie_name):
    param_d = {'q': movie_name, 'type' : 'movies', 'limit' : 5}
    baseurl = "https://tastedive.com/api/similar"
    search = requests_with_caching.get(baseurl, params=param_d)
    return search.json()

def extract_movie_titles(dictionary):    
    return [i['Name'] for i in dictionary['Similar']['Results']]

def get_related_titles(movie_list):
    related = [extract_movie_titles(get_movies_from_tastedive(i)) for i in movie_list]
    lists = []
    for i in related:
        for x in i:
            if x not in lists:
                lists.append(x)
    return lists

def get_movie_data(movie_title):
    param_d = {'t' : movie_title, 'r' : 'json'}
    baseurl = 'http://www.omdbapi.com/'
    search = requests_with_caching.get(baseurl, params=param_d)
    return search.json()

def get_movie_rating(dictionary):
    test = dictionary['Ratings']
    rating = 0
    for i in test:
        if i['Source'] == 'Rotten Tomatoes':
            rating = int(i['Value'][:2])
    return rating

def get_sorted_recommendations(movie_list):
    return sorted(get_related_titles(movie_list), key=lambda x: (get_movie_rating(get_movie_data(x)), x), reverse=True)
        
    
get_sorted_recommendations(['Sherlock Holmes', 'Bridesmaids'])    
