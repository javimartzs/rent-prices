from base import Browser, BarrioLoader, Scraper
import time 

if __name__ == '__main__':

    with open('input/cities.txt', 'r', encoding='utf-8') as file:
        cities = [line.strip() for line in file]

    success = False

    while not success:
        try:
            # Inicializamos el navegador
            browser_obj = Browser()
            browser_obj.init_browser()

            # Load Barrios 
            loader = BarrioLoader(cities)
            barrios = loader.import_barrios()

            # Start Scraping
            home_url = 'https://www.idealista.com/alquiler-viviendas'
            home = 'rent'
            scraper = Scraper(browser_obj, barrios, home_url, home)
            scraper.scrape()

            success = True
        
        except Exception as e:
            print(f"Error durante la ejecución del script: {e}")
            print(f"Esperando 10 minutos antes de reintentar...")
            time.sleep(600)

    print("Script finalizado correctamente")