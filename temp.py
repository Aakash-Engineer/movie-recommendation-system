import requests

url = "https://api.themoviedb.org/3/movie/63?api_key=f5f0e091654432696b191938d11e63df"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNWYwZTA5MTY1NDQzMjY5NmIxOTE5MzhkMTFlNjNkZiIsIm5iZiI6MTcyNjY5ODEwOS4yNDczNTcsInN1YiI6IjY2ZWI0ZmE5NWMwNTE5YTIzNGQzYWRhYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.EzOK_WjEgmeL1GSbSUwH_9DLb8xvl-I_Ezp42LJyFw4"
}

response = requests.get(url, headers=headers)

print(response.text)