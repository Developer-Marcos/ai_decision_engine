import os
from dotenv import load_dotenv

def load_env():
    load_dotenv()

    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError("GOOGLE_API_KEY não encontrada no ambiente")

    if os.getenv("LANGSMITH_API_KEY"):
        print(f"LangSmith ativado no projeto: {os.getenv('LANGCHAIN_PROJECT')}")
    else:
        print("LangSmith NÃO configurado, iniciando sem ele.")

