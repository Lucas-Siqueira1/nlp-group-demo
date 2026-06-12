import os
from tavily import TavilyClient

tavily_client = TavilyClient()

def search_tool(query: str) -> str:
    """
    Busca informações na internet sobre saúde, doenças, condições médicas,
    medicamentos, sintomas e faixas de referência clínicas. Use quando precisar
    de informações atualizadas ou específicas para responder ao usuário.

    Args:
        query: Termo ou pergunta a ser pesquisada. Seja específico para obter
               melhores resultados. Exemplo: 'faixa normal de pressão arterial adulto'.

    Returns:
        Resultados da busca em formato de texto com as informações encontradas.
    """
    try:
        resposta = tavily_client.search(query=query, max_results=3)
    except Exception as e:
        return f"Erro ao realizar a busca na internet: {str(e)}"

    return str(resposta)
