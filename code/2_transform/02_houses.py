import pandas as pd 
import os 

input_path = 'output/houses'
files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith('.csv')]

df = pd.concat([pd.read_csv(file) for file in files], ignore_index = True)

# Asegurarse de que siempre se obtengan dos columnas, incluso si no hay coincidencias
split_price = df['price'].str.split('€/mes', expand=True)

# Si no se encuentra el separador, asignamos NaN a la columna 'garage'
split_price[1] = split_price[1].fillna('')

# Asignar las columnas resultantes
df['price'] = split_price[0].str.replace('.', '', regex=False).astype(float)
df['garage'] = split_price[1].apply(lambda x: True if 'incluido' in x else False)

df['habitaciones'] = df['characteristics'].str.extract(r'(\d+) hab\.').fillna(0).astype(int)
df['size'] = df['characteristics'].str.extract(r'(\d+) m²').fillna(0).astype(float)
df['planta'] = df['characteristics'].str.extract(r'Planta (\d+)ª').fillna(0).astype(int)

df['ascensor'] = df['characteristics'].apply(lambda x: True if 'con ascensor' in str(x) else False)
df['exterior'] = df['characteristics'].apply(lambda x: True if 'exterior' in str(x) else False)

df['photos'] = df['num_photos'].str.extract(r'(?<=/)(\d+)').fillna(0).astype(int)
df['alquiler_temporal'] = df['extra_characteristics'].apply(lambda x: True if 'temporada' in str(x) else False)
df['agency'] = df['inmobiliaria'].notna()

city_mapping = {
    'a-coruna': 'A Coruña',
    'alicante-alacant': 'Alicante',
    'barcelona': 'Barcelona',
    'bilbao': 'Bilbao',
    'donostia-san-sebastian': 'San sebastián',
    'madrid': 'Madrid',
    'malaga': 'Málaga',
    'palma-de-mallorca': 'Palma de Mallorca',
    'pamplonairuna': 'Pamplona',
    'sevilla': 'Sevilla',
    'valencia': 'Valencia',
    'vitoria-gasteiz': 'Vitoria',
    'zaragoza': 'Zaragoza'
}
df['city'] = df['city'].replace(city_mapping)

# Select the relevant columns and remove duplicates
df = df[[
    'date', 
    'price', 
    'garage', 
    'habitaciones', 
    'size', 
    'planta', 
    'ascensor', 
    'exterior', 
    'photos', 
    'alquiler_temporal', 
    'agency', 
    'inmobiliaria', 
    'barrio', 
    'id', 
    'city']].drop_duplicates()


date_suffix = df['date'].astype(str).str.replace('-', '').unique()[0]
df.to_parquet(f'output/houses/houses_{date_suffix}.parquet', index=False)

for file in files:
    os.remove(file)