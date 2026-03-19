from weda.scraping import get_weather_predictions

if __name__ == "__main__":
    city = "Milano"
    year = 2025
    month = 1

    for city in [city]:
        for month in [month]:
            df = get_weather_predictions(city, year, month)
            df.to_csv(f"./weather.{city}.{year}.{month}.data.csv", index=False)

