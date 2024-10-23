library(tidyverse)
library(arrow)


rent <- read_parquet('output/rent/rent_20241022.parquet') |> 
    filter(city %in% c("Madrid", "Barcelona")) |> 
    mutate(tipo =  'Vivienda') |> 
    select(id, price, tipo, city, barrio)

rooms <- read_parquet('output/rooms/rooms_20241021.parquet') |> 
    filter(city %in% c("Madrid", "Barcelona")) |> 
    mutate(tipo = 'Habitacional') |> 
    select(id, price, tipo, city, barrio)

df <- full_join(rooms, rent)
rm(rent, rooms)

p <- df |> 
    group_by(barrio, tipo) |> 
    summarise(
        n = n(), 
        city = first(city)) |> 
    pivot_wider(names_from = tipo, values_from = n) |> 
    ungroup() |> 
    mutate(ratio = Habitacional / Vivienda)
write.csv(p, '/Volumes/javimartzs/ratio_rooms_houses.csv')



p <- df |> 
    group_by(city, tipo) |> 
    summarise(
        n = n()) |> 
    pivot_wider(names_from = tipo, values_from = n) |> 
    ungroup() |> 
    mutate(ratio = Habitacional / Vivienda)
write.csv(p, '/Volumes/javimartzs/ratio_rooms_houses.csv')





# TABLAS DEL BONO DE ALQUILER 

df <- read_parquet('output/rent/rent_20241022.parquet')
p <- df |> 
    mutate(
        bono1 = ifelse(price < 600, 1, 0), 
        bono2 = ifelse(price < 900, 1, 0)) |> 
    group_by(barrio) |> 
    summarise(
        city = first(city),
        mean = mean(bono1)*100, 
        mean2 = mean(bono2)*100) |> 
    filter(city %in% c('Madrid', 'Barcelona')) |> 
    arrange(-mean) |> 
    mutate(barrio = case_when(
        barrio == 'arganzuela' ~ 'Arganzuela',
        barrio == 'barajas' ~ 'Barajas', 
        barrio == 'barrio-de-salamanca' ~ 'Barrio de Salamanca',
        barrio == 'carabanchel' ~ 'Carabanchel',
        barrio == 'centro' ~ 'Centro',
        barrio == 'chamartin' ~ 'Chamartín',
        barrio == 'chamberi' ~ 'Chamberí',
        barrio == 'ciudad-lineal' ~ 'Ciudad Lineal',
        barrio == 'ciutat-vella' ~ 'Ciutat Vella',
        barrio == 'fuencarral' ~ 'Fuencarral',
        barrio == 'gracia' ~ 'Gracia',
        barrio == 'eixample' ~ 'Eixample',
        barrio == 'horta-guinardo' ~ 'Horta Guinardó',
        barrio == 'hortaleza' ~ 'Hortaleza',
        barrio == 'latina' ~ 'Latina',
        barrio == 'les-corts' ~ 'Les Corts',
        barrio == 'moncloa' ~ 'Moncloa',
        barrio == 'moratalaz' ~ 'Moratalaz',
        barrio == 'nou-barris' ~ 'Nou Barri',
        barrio == 'puente-de-vallecas' ~ 'Puente de Vallecas',
        barrio == 'retiro' ~ 'Retiro',
        barrio == 'san-blas' ~ 'San Blas',
        barrio == 'sant-andreu' ~ 'Sant Andreu',
        barrio == 'sant-marti' ~ 'Sant Martí',
        barrio == 'sants-montjuic' ~ 'Sants Montjuïc',
        barrio == 'sarria-sant-gervasi' ~ 'Sarrià Sant Gervasi',
        barrio == 'usera' ~ 'Usera',
        barrio == 'vicalvaro' ~ 'Vicálvaro',
        barrio == 'villa-de-vallecas' ~ 'Villa de Vallecas',
        barrio == 'villaverde' ~ 'Villaverde',
    ))

write_csv(p, '/Volumes/javimartzs/rent_bonus_by_barrio.csv')
