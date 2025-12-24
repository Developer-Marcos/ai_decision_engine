from project.agents.planejador import node_planejador
from project.config.config import load_env

def main():
      load_env()

      state_simulado = {
            "problema": "Vale a pena criar um SaaS de correção de redações para o ENEM?"
      }

      resultado = node_planejador(state=state_simulado)
      print(resultado)
      
      

if __name__ == "__main__":
      main()