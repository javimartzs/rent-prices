import undetected_chromedriver as uc # type: ignore
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import random
import pickle
import os


class Browser:
    def __init__(self):
        self.browser = None

    def init_browser(self):
        url = 'https://www.idealista.com'
        self.browser = uc.Chrome(version_main=129)
        self.browser.get(url)
        self.browser.implicitly_wait(14)

        # Accept cookies if present
        try:
            time.sleep(random.uniform(2, 4))
            self.browser.find_element('xpath', '//*[@id="didomi-notice-agree-button"]').click()
        except Exception as e:
            print(f"Error al aceptar las cookies: {e}")

        # Save cookies to a file 
        cookies = self.browser.get_cookies()
        with open('cookies.pkl', 'wb') as file:
            pickle.dump(cookies, file)
        
        # Load cookies from the file 
        with open('cookies.pkl', 'rb') as file:
            cookies = pickle.load(file)

        for cookie in cookies:
            self.browser.add_cookie(cookie)
        
        if os.path.exists('cookies.pkl'):
            os.remove('cookies.pkl')
        else:
            print("No se encontró el archivo cookies.pkl")
    
    def random_scroll(self):
        scroll_height = random.randint(100, 300)
        self.browser.execute_script(f"window.scrollBy(0, {scroll_height});")
        time.sleep(random.uniform(1, 3))

    def random_sleep(self, min_time=2, max_time=4):
        """Genera una pausa aleatoria para evitar detección como bot."""
        time.sleep(random.uniform(min_time, max_time))

    def get_browser(self):
        return self.browser
    
    def quit(self):
        self.browser.quit()
        
class BarrioLoader:
    
    def __init__(self, cities):
        self.cities = cities

    def import_barrios(self):
        barrios = {}
        for city in self.cities:
            try:
                with open(f'input/barrios/barrios_{city}.txt', 'r') as file:
                    barrios[city] = file.read().splitlines()
            except FileNotFoundError:
                print(f"No se encontró el archivo barrios_{city}.txt")
        return barrios

class Scraper:
    def __init__(self, browser, barrios, home_url, home):
        self.browser = browser
        self.barrios = barrios
        self.home_url = home_url
        self.home = home

    def scrape(self):
        # Iteramos sobre las ciudades y los barrios de cada ciudad
        for city, barrios_list in self.barrios.items():
            data = []
            for barrio in barrios_list:

                # Navegamos a la URL inicial del barrio 
                self.browser.get_browser().get(f"{self.home_url}/{city}/{barrio}/")

                # Loop para navegar por todas las páginas del barrio
                while True:
                    self.browser.random_scroll()
                    self.browser.random_sleep()

                    # Extraemos el contenido HTML
                    html = self.browser.get_browser().page_source
                    soup = bs(html, 'html.parser')

                    # Encuentra los articulos de la página
                    items = soup.find_all('article', class_='item')

                    for item in items:
                        div = item.find('div', class_='item-info-container')
                        photos = item.find('picture', class_='item-multimedia')

                        # Extraer los datos
                        _id = div.find('a', href=lambda href: href and 'inmueble' in href)
                        _id = _id['href'] if _id else ''
                        
                        title = div.find('a', href=lambda href: href and 'inmueble' in href)
                        title = title.get_text(strip=True) if title else ''

                        price = div.find('div', class_='price-row')
                        price = price.get_text(strip=True) if price else ''

                        characteristics = div.find('div', class_='item-detail-char')
                        characteristics = characteristics.get_text(strip=True) if characteristics else ''

                        extra_char_div = div.find('div', class_='listing-tags-container')
                        extra_char = extra_char_div.get_text(strip=True) if extra_char_div else ''

                        inmobiliaria = div.find('picture', class_='logo-branding')
                        inmobiliaria = inmobiliaria.find('a', href=True)['href'] if inmobiliaria else ''

                        num_photos = photos.find('div', class_='item-multimedia-pictures')
                        num_photos = num_photos.get_text(strip=True) if num_photos else ''

                        page_url = self.browser.get_browser().current_url
                        page_suffix = os.path.basename(page_url).replace('.htm', '')

                        # Almacenamos los datos en una lista
                        data.append({
                            'date': time.strftime('%Y-%m-%d'),
                            'title': title,
                            'price': price,
                            'characteristics': characteristics,
                            'num_photos': num_photos,
                            'extra_characteristics': extra_char,
                            'inmobiliaria': inmobiliaria,
                            'barrio': barrio,
                            'city': city,
                            'id': _id,
                            'page_suffix': page_suffix
                        })

                    # Convertimos la lista a un DF y lo guardamos en un CSV para cada ciudad
                    df = pd.DataFrame(data)
                    date_suffix = time.strftime('%Y%m%d')
                    df.to_csv(f'output/{self.home}/{city}_{date_suffix}.csv', index=False)

                    # Comprobamos si hay una siguiente página
                    current_page = self.browser.get_browser().current_url
                    try:
                        self.browser.random_sleep()
                        next_page_button = self.browser.get_browser().find_element('class name', 'icon-arrow-right-after')
                        next_page_button.click()
                        self.browser.random_sleep()
                        
                        # Si la URL no cambia, significa que estamos en la última página
                        new_page = self.browser.get_browser().current_url
                        if new_page == current_page:
                            print(f"La pagina web no ha cambiado")
                            continue

                    except Exception as e:
                        print(f"No hay más páginas para el barrio {barrio} en la ciudad {city}")
                        break  

class BuyScraper:
    def __init__(self, browser, barrios):
        self.browser = browser
        self.barrios = barrios

    def scrape(self):

        for city, barrios_list in self.barrios.items():
            data = []
            filters = ['con-estudios,de-un-dormitorio,de-dos-dormitorios/','con-de-tres-dormitorios,de-cuatro-cinco-habitaciones-o-mas']

            for barrio in barrios_list:
                for filter in filters:
                    pass