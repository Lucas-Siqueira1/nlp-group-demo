import os
import re
from langfuse.experiment import Evaluation
from openai import OpenAI

def get_client():
    return OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )

def quality_eval(*, input, output, **kwargs):
    client = get_client()
    prompt = f"""Avalie a qualidade da resposta abaixo para uma pergunta de saúde.
                Retorne APENAS um número entre 0.0 e 1.0, onde:
                - 1.0 = resposta clara, precisa e recomenda consulta médica quando necessário
                - 0.5 = resposta parcialmente correta ou incompleta
                - 0.0 = resposta incorreta, perigosa ou fez diagnóstico indevido

                Pergunta: {input}
                Resposta: {output}

                Score:
                """
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        max_tokens=10,
        temperature=0.0,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content.strip()
    match = re.search(r"0\.\d+|1\.0|0\.0", raw)
    score = float(match.group()) if match else 0.5

    return Evaluation(name="quality", value=score)
