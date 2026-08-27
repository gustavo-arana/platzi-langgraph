from langchain_core.tools import tool
import requests

@tool("get_products", description="Obtiene la lista de productos disponibles en la tienda.")
def get_products():
    #Connect with API to get the products
    """Obtiene la lista de productos disponibles en la tienda."""
    response = requests.get("https://api.escuelajs.co/api/v1/products")
    products = response.json()
    return "".join([f"{product['title']}: ${product['price']} \n" for product in products])


@tool("get_weather", description="Get a Weather frof a City")
def get_weather(city: str):
    response    = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1")
    data        = response.json()
    latitude    = data['results'][0]['latitude']
    longitude   = data['results'][0]['longitude']

    response    = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true")
    data        = response.json()

    return f"The weather on the city {city.title()} is {data['current_weather']['temperature']}"


tools = [get_products, get_weather]