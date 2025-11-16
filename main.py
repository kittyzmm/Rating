import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

URL = "https://www.kinopoisk.ru/lists/movies/top-250/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_top_5_movies():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)
        
        if response.status_code != 200:
            print(f"Ошибка загрузки страницы")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        film_cards = soup.select('.styles_listItem__1PliW')
        
        movies_data = []

        for i, card in enumerate(film_cards[:5], 1):
            try:
                title = card.select_one('.base-movie-link__name').get_text(strip=True)
                year = card.select_one('.desktop-list-main-info_secondaryText').get_text(strip=True)
                rating = card.select_one('.rating__value').get_text(strip=True)
                
                genre_elem = card.select_one('.desktop-list-main-info_genre')
                genre = genre_elem.get_text(strip=True) if genre_elem else "Не указан"
                
                movies_data.append({
                    '№': i,
                    'Название': title,
                    'Год': year,
                    'Рейтинг': rating,
                    'Жанр': genre
                })
                
                time.sleep(1)
                
            except Exception as e:
                print(f"Ошибка при обработке фильма {i}: {e}")

        df = pd.DataFrame(movies_data)
        return df

    except requests.exceptions.RequestException as e:
        print(f"Ошибка сетевого запроса: {e}")
        return None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None
