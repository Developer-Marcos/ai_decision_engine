from project.utils.chains_auxiliares import refinar_query
from project.config.config import load_env
from project.core.grafo import criar_grafo

def main():
      load_env()

      pergunta_usuario = "Vale a pena fazer um saas pro enem?"
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
      print(f"Total de pesquisas coletadas: {len(resultado_final['conteudo_pesquisado'])}")

      for i, item in enumerate(resultado_final['conteudo_pesquisado'], 1):
            print(f" Fonte {i}: {item.get('query')}")
      
      
if __name__ == "__main__":
      main()