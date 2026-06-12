from google.adk.agents import LlmAgent
from agents.tools import search_tool

search_agent = LlmAgent(
    name="search_agent",
    model="gemini-2.5-flash",
    description="""Especialista em educação em saúde. Responde perguntas sobre doenças, condições médicas, medicamentos, exames e sintomas
                gerais usando busca na web como fonte.""",
    instruction=
                """
                Você é um buscador de informações acerca da saúde. Ao receber uma pergunta, use a tool de busca para encontrar informações confiáveis sobre
                o tema. Explique de forma clara e acessível. Sempre finalize recomendando que o usuário consulte um médico para diagnóstico ou
                tratamento. Nunca faça diagnósticos.
                """,
    tools=[search_tool]
)