from services.api import do_get

WEATHER_API_KEY = '8b6becad3b9bf08e8e3341e8b0aa42f2'

async def fetch_weather(city: str, retries: int, api_key: str) -> dict | str:
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    try:
        data = await do_get(url, retries)
    except Exception:
        data = f"Sorry, we can't get weather data for {city}"
    return data

def normalize_weather(city: str, data: dict):
    return '\n'.join([
        f'City: {city}',
        f'Temp: {data['main']['temp']}°C',
        f'Feels like: {data['main']['feels_like']}°C',
        f'Humidity: {data['main']['humidity']}%'
    ])