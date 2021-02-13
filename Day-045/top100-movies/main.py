import requests
from bs4 import BeautifulSoup

URL = "https://www.empireonline.com/movies/features/best-movies-2/"

response = requests.get(URL)

website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")

all_movies = soup.find_all(name="h3", class_="title")
print(all_movies)

movies = [movie.getText() for movie in all_movies[::-1]]

with open("movies.txt", mode="w") as file:
    for movie in movies:
        file.write(f"{movie}\n")
