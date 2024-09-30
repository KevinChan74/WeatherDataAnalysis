import requests
import schedule
import time
from datetime import datetime
import sqlite3

# Define a database and table

def create_table():
    conn = sqlite3.connect("weather_database.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weathers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT NOT NULL,
        date DATE NOT NULL,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        day INTEGER NOT NULL,
        hour INTEGER NOT NULL,
        minute INTEGER NOT NULL,
        second INTEGER NOT NULL,
        microsecond INTEGER NOT NULL,
        temperature NUMERIC(4,2),
        humidity INTEGER NOT NULL,
        weather TEXT NOT NULL
    )
    '''
    )
    conn.commit()
    conn.close()

# API_KEY = Your API key
city_list = ["Tokyo, JP","Sydney, AU",
            "Paris, FR","Berlin, DE","Moscow, RU",
            "Beijing, CN","Singapore, SG","Seoul, KR","Bangkok, TH","Toronto, CA","Shanghai, CN","Chicago, US"]

# Fetch data into database with finetuned column

def fetch_weather_data():
    create_table()
    for city in city_list:
        API_URL = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(API_URL) # get all cities' weather records in the city_list
        if response.status_code == 200:
            data = response.json()
            timestamp = datetime.now()
            date_string = timestamp.strftime('%Y-%m-%d')
            raw_weather_data = {
                'city' : data['name'],
                'date' : date_string,
                'year': timestamp.year,
                'month': timestamp.month,
                'day': timestamp.day,
                'hour': timestamp.hour,
                'minute': timestamp.minute,
                'second': timestamp.second,
                'microsecond': timestamp.microsecond,
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'weather': data['weather'][0]['description'],
            }

            print("-----------------------",raw_weather_data)

            # Insert data into database
            conn = sqlite3.connect('weather_database.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO weathers 
            (city, date, year, month, day, hour, minute, second, microsecond, temperature, humidity, weather) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (data['name'], date_string, timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second, timestamp.microsecond, data['main']['temp'], data['main']['humidity'], data['weather'][0]['description']))
            conn.commit()
            conn.close()
        else:
            print(f"Failed to fetch data for {city}") 

# Define scheduler to fetch data

def run_scheduler():
    # Set it as 1 for thread later
    interval = 1

    schedule.every(interval).minutes.do(fetch_weather_data)
    
    print(f"Scheduler started. Fetching weather data every {interval} minute(s).")
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()
