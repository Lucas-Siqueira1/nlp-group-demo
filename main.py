import asyncio
import os
import warnings

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from langfuse import get_client
from openinference.instrumentation.google_adk import GoogleADKInstrumentor

from agents.root_agent import root_agent

load_dotenv()

langfuse = get_client()

try:
    if langfuse.auth_check():
        print("Langfuse client is authenticated and ready!")
    else:
        print("Authentication failed. Please check your credentials and host.")
except Exception as e:
    print(f"Langfuse auth check skipped: {e}")

if os.getenv("ENABLE_ADK_TRACING") == "1":
    GoogleADKInstrumentor().instrument()

async def run(user_input: str, session_id: str = "demo-session"):
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="nlp-demo",
        user_id="demo-user",
        session_id=session_id,
    )

    runner = Runner(
        agent=root_agent,
        app_name="nlp-demo",
        session_service=session_service,
    )

    message = Content(parts=[Part(text=user_input)])

    async for event in runner.run_async(
        user_id="demo-user",
        session_id=session_id,
        new_message=message,
    ):
        if event.is_final_response():
            print(f"\nResposta: {event.content.parts[0].text}")

    try:
        langfuse.flush()
    except Exception as e:
        print(f"Langfuse flush skipped: {e}")

if __name__ == "__main__":
    user_input = input("Você: ")
    asyncio.run(run(user_input))
