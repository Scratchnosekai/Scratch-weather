import requests
import scratchattach as scratch3
import time
import os

weather_dict = {
    "thunderstorm": 1,
    "drizzle": 2,
    "rain": 3,
    "snow": 4,
    "clear": 5,
    "clouds": 6,
    "mist": 7,
    "smoke": 8,
    "haze": 9,
    "dust": 16,  
    "fog": 11,
    "sand": 12,
    "ash": 13,
    "squall": 14,
    "tornado": 15
}

city_list = ["nikko", "utsunomiya", "nasu", "takasaki", "minakami", "mito", "hitachi", "tsukuba", "chiba,jp", "narita,jp", "kisarazu", "saitama", "kumagaya", "hanno","hakone","hiratsuka","sumida","shibuya","shinagawa","suginami","koganei","okutama"]
city_dict = {f"{i+1001}": city for i, city in enumerate(city_list)}
api_key = os.getenv("API_KEY")
password = os.getenv("PASSWORD")
city_coords = {
    "yokohama": (35.448, 139.643),
    "kawasaki": (35.521, 139.717)
}

def send_weather(weather):
    if weather in weather_dict:
        return weather_dict[weather]
    else:
        return -1 

session = scratch3.login("Scratchnosekai_2",password)
conn = session.connect_cloud("871346881")

def update_weather(city):
    if city in city_coords:
        lat, lon = city_coords[city]
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    else:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['main'].lower()
        humidity = data['main']['humidity']
        temperature = data['main']['temp']
        weather_code = send_weather(weather)
        print(f"Weather for {city}: {weather} (code: {weather_code}), Humidity: {humidity}%, Temperature: {temperature}°C") 
        return weather_code, humidity, temperature
    else:
        print(f"Failed to get weather for {city}, status code: {response.status_code}")  
        return 0, 0, 0  

def handle_request():
    while True:
        for i in range(1, 10):
            request_var = f"From_Host_{i}"
            request = scratch3.get_var("871346881", request_var)
            print(f"Checking {request_var}: {request}")  
            if request is not None and request != 0:
                city_id = str(request)
                print(f"Request received from {request_var}: {city_id}")  
                if city_id in city_dict:
                    city = city_dict[city_id]
                    print(f"City found: {city}")  
                    weather_code, humidity, temperature = update_weather(city)
                    combined_data = f"{city_id}{weather_code:02d}{humidity:02d}{int(temperature*10):04d}"
                    print(f"Weather code for {city}: {weather_code}, Humidity: {humidity}%, Temperature: {temperature}°C, Combined data: {combined_data}")  # デバッグ用
                    conn.set_var("To_Host", combined_data)
                    print(f"Updated To_Host with combined data: {combined_data}") 
                    conn.set_var(request_var, 0)
                else:
                    conn.set_var("To_Host", f"{city_id}0000000") 
                    print(f"Unknown city ID: {city_id}")  
        time.sleep(1)  

handle_request()
