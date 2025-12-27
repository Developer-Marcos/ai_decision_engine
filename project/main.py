import warnings
warnings.filterwarnings("ignore", message="Field name .* shadows an attribute in parent \"BaseTool\"")
warnings.filterwarnings("ignore", category=UserWarning, module="langchain_tavily")


from project.utils.chains_auxiliares import refinar_query
from project.config.config import load_env
from project.core.grafo import criar_grafo


def main():
      load_env()

      pergunta_usuario = "Vale a pena criar um SaaS de agendamento e gestao para petshops pequenos com automacao de whatssap no brasil?"
      query_refinada = refinar_query(query=pergunta_usuario)

      state_inicial = {
            "problema": query_refinada,
            "conteudo_pesquisado": [],
            "numero_iteracao": 0
      }

      print(f"\n[Main] Query Refinada: {query_refinada}")
      print("-" * 30)

      fluxo = criar_grafo()

      print("[Main] Iniciando execução do Grafo...")
      resultado_final = fluxo.invoke(state_inicial)

      print("-" * 30)
      print(f"[Main] Execução Finalizada!")
      
      
if __name__ == "__main__":
      main()