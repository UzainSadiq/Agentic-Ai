
import ast
import operator as op
import requests
from ddgs import DDGS

from langchain.tools import tool


# =========================================================
# 1. SAFE CALCULATOR TOOL
# =========================================================

_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}


def _safe_calculate(expression):
    def evaluate(node):

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError("Only numbers are allowed.")

        if isinstance(node, ast.BinOp):
            left = evaluate(node.left)
            right = evaluate(node.right)

            operator = _ALLOWED_OPERATORS.get(type(node.op))

            if operator is None:
                raise ValueError("Operator not allowed.")

            return operator(left, right)

        if isinstance(node, ast.UnaryOp):
            operand = evaluate(node.operand)

            operator = _ALLOWED_OPERATORS.get(type(node.op))

            if operator is None:
                raise ValueError("Operator not allowed.")

            return operator(operand)

        raise ValueError("Invalid mathematical expression.")

    tree = ast.parse(expression, mode="eval")

    return evaluate(tree.body)


@tool
def calculator(expression: str) -> str:
    """
    Calculate mathematical expressions.

    Use this tool whenever the user asks for arithmetic,
    mathematical calculations, percentages, powers, division,
    multiplication, addition, subtraction, or similar calculations.

    Args:
        expression: A mathematical expression such as
                    25 * 4 + 10 or (100 / 4) + 20.
    """

    try:
        result = _safe_calculate(expression)

        return f"Calculation result: {result}"

    except Exception as e:
        return f"Calculator error: {str(e)}"


# =========================================================
# 2. WEATHER TOOL
# =========================================================

@tool
def weather(city: str) -> str:
    """
    Get the current weather for a city.

    Use this tool whenever the user asks about current
    temperature, humidity, rain, wind, or weather conditions.

    Args:
        city: Name of the city, for example Lahore or London.
    """

    try:

        # -------------------------------------------------
        # Step 1: Find city coordinates
        # -------------------------------------------------

        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
        }

        geo_response = requests.get(
            geo_url,
            params=geo_params,
            timeout=10
        )

        geo_response.raise_for_status()

        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return f"Could not find the city: {city}"

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        city_name = location.get("name", city)
        country = location.get("country", "")

        # -------------------------------------------------
        # Step 2: Get current weather
        # -------------------------------------------------

        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "apparent_temperature,"
                "precipitation,"
                "weather_code,"
                "wind_speed_10m"
            ),
            "timezone": "auto",
        }

        weather_response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10
        )

        weather_response.raise_for_status()

        data = weather_response.json()

        current = data["current"]

        temperature = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m")
        apparent = current.get("apparent_temperature")
        precipitation = current.get("precipitation")
        wind = current.get("wind_speed_10m")

        weather_code = current.get("weather_code")

        description = weather_code_description(weather_code)

        return (
            f"Weather for {city_name}, {country}:\n"
            f"Temperature: {temperature}°C\n"
            f"Feels like: {apparent}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind speed: {wind} km/h\n"
            f"Precipitation: {precipitation} mm\n"
            f"Condition: {description}"
        )

    except Exception as e:
        return f"Weather tool error: {str(e)}"


def weather_code_description(code):

    codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }

    return codes.get(code, "Unknown weather condition")


# =========================================================
# 3. WEB SEARCH TOOL
# =========================================================

@tool
def web_search(query: str) -> str:
    """
    Search the web for current or external information.

    Use this tool when the user asks to search the internet,
    find recent information, research a topic, find facts,
    websites, articles, or online information.

    Args:
        query: The search query.
    """

    try:

        results = DDGS().text(
            query,
            max_results=5
        )

        if not results:
            return "No web search results were found."

        formatted_results = []

        for i, result in enumerate(results, start=1):

            title = result.get("title", "No title")
            body = result.get("body", "No description")
            url = result.get("href", "")

            formatted_results.append(
                f"{i}. {title}\n"
                f"   {body}\n"
                f"   URL: {url}"
            )

        return "\n\n".join(formatted_results)

    except Exception as e:
        return f"Web search error: {str(e)}"


# =========================================================
# ALL TOOLS
# =========================================================

TOOLS = [
    calculator,
    weather,
    web_search,
]
