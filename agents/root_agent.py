from google.adk.agents import LlmAgent
from agents.analysis_agent import analysis_agent
from agents.search_agent import search_agent

root_agent = LlmAgent(
    name="root_agent",
    model="gemini-2.5-flash",
    description="""Agente de triagem de saúde. Recebe a mensagem do usuário e decide qual agente especialista deve responder: search_agent para
                dúvidas sobre doenças e saúde ou analysis_agent para interpretação de dados e sintomas pessoais.""",
    instruction=
                """
                Você é um triador de um assistente de saúde. Analise a mensagem do usuário e transfira para o agente correto:

                - search_agent: perguntas sobre doenças, condições, medicamentos,
                sintomas em geral;

                - analysis_agent: quando o usuário fornece dados próprios como pressão,
                glicose, peso, frequência cardíaca ou descreve sintomas que está
                sentindo agora;

                Você DEVE sempre transferir. Nunca responda diretamente.
                """,
    sub_agents=[search_agent, analysis_agent]
)