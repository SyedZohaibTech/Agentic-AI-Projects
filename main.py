from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import requests
import os
# Step 1: Laod .env
load_dotenv(
    
)
# Keys
gemini_api_key=os.getenv("GEMINI_API_KEY")
weather_api_key=os.getenv("WEATHER_API_KEY")
# Step 2 Gemini client
external_client=AsyncOpenAI(api_key=gemini_api_key,base_url="https://generativelanguage.googleapis.com/v1beta/openai")
# step 3: Model Config
model=OpenAIChatCompletionsModel(
    openai_client=external_client
    ,model="gemini-2.0-flash"
 )
# Step 4: Run Config
run_config=RunConfig(model=model,tracing_disabled=True
                    )
# Step 5: Weather Agent
agent=Agent(name="Weather Agent",
            instructions="You are a helpful assistant. Format the weather data in a nice human readable "
            )
# Step 6: Function to fetch live weather
def get_weather(city):
    url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    response=requests.get(url)
    data = response.json()
    if data.get("cod") != 200:
        return f"Could not fetch weather for {city}."
    
    desc = data["weather"][0]["description"].title()
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    return f"Weather in {city}: {desc}, Temperature: {temp}°C, Humidity: {humidity}%."

# Step 7: Run Agent with real data
city = "karachi"
live_weather = get_weather(city)

query = f"Format this weather info nicely: {live_weather}"

result = Runner.run_sync(
    agent,
    query,
    run_config=run_config
)

print("Raw Data:", live_weather)
print("Weather Agent Output:", result.final_output)