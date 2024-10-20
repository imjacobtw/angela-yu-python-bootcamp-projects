from bs4 import BeautifulSoup
import requests

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

movie_elements = soup.select("main .title")
movie_titles = reversed([element.getText() for element in movie_elements])

with open("movies.txt", "w") as file:
    for movie in movie_titles:
        file.write(f"{movie}\n")