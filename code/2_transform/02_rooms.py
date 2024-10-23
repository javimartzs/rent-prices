import pandas as pd 
import os 

input_path = 'output/rooms'
files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith('.csv')]

df = pd.concat([pd.read_csv(file) for file in files], ignore_index=True)

# Procesar el DataFrame
df['price'] = df['price'].str.split('€/mes', expand=True)[0]
df['price'] = df['price'].str.replace(r'\.', '', regex=True).astype(float)

# Extraer el número de habitaciones
df['habitaciones'] = df['characteristics'].str.extract(r'(\d+) hab\.')
df['habitaciones'] = df['habitaciones'].fillna(0).astype(int)

# Eliminar menciones de fumar/no fumar de 'characteristics'
df['characteristics'] = df['characteristics'].str.replace('No se puede fumar', '', regex=False)
df['characteristics'] = df['characteristics'].str.replace('Se puede fumar', '', regex=False)

# Seleccionar las columnas relevantes
df = df[['date', 'price', 'barrio', 'city', 'id']]
city_mapping = {
    'barcelona': 'Barcelona',
    'madrid': 'Madrid',
    'malaga': 'Málaga',
    'sevilla': 'Sevilla',
    'valencia': 'Valencia',
    'zaragoza': 'Zaragoza'
}
df['city'] = df['city'].replace(city_mapping)


date_suffix = df['date'].astype(str).str.replace('-', '').unique()[0]
df.to_parquet(f'output/rooms/rooms_{date_suffix}.parquet', index=False)

for file in files:
    os.remove(file)