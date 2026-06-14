import asyncio
import os
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from langfuse import get_client
from openinference.instrumentation.google_adk import GoogleADKInstrumentor
from opentelemetry import trace
from agents.root_agent import root_agent
from observability.evaluators import quality_eval

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

    response_text = ""
    trace_id = None

    async for event in runner.run_async(
        user_id="demo-user",
        session_id=session_id,
        new_message=message,
    ):
        if trace_id is None:
            span_context = trace.get_current_span().get_span_context()
            if span_context.trace_id != 0:
                trace_id = format(span_context.trace_id, "032x")

        if event.is_final_response():
            response_text = event.content.parts[0].text
            print(f"\nResposta: {response_text}")
            
    try:
        evaluation = quality_eval(input=user_input, output=response_text)
        if trace_id:
            langfuse.create_score(
                trace_id=trace_id,
                name=evaluation.name,
                value=evaluation.value,
                comment=evaluation.comment,
            )
            print(f"Score de qualidade: {evaluation.value}")
        else:
            print("Trace ID não encontrado, score não registrado")
    except Exception as e:
        print(f"Quality eval skipped: {e}")

    try:
        langfuse.flush()
    except Exception as e:
        print(f"Langfuse flush skipped: {e}")

    return response_text


if __name__ == "__main__":
    user_input = input("Você: ")
    asyncio.run(run(user_input))