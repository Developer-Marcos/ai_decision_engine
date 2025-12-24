from project.agents.planejador import node_planejador
from project.utils.chains_auxiliares import refinar_query
from project.config.config import load_env

def main():
      load_env()

      query_refinada = refinar_query(query="Vale a pena fazer um saas pro enem?")
      state_simulado = {
            "problema": query_refinada
      }
      print(state_simulado)

      #resultado = node_planejador(state=state_simulado)
      #print(resultado)
      
      

if __name__ == "__main__":
      main()