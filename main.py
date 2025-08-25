from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
print(gemini_api_key)

# Create AsyncOpenAI client for Gemini
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

# Model (latest syntax uses openai_client, not client)
model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-2.5-flash"
)

# RunConfig
run_config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Agent
agent = Agent(
    name="Simple Agent",
    instructions="You are a helpful assistant."
)

# Run
runner = Runner.run_sync(
    agent,
    " What si the capital in Islamabad",
    run_config=run_config
)

print(runner.final_output)