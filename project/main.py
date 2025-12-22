from project.tests.teste_agente import testar_agente
from project.config.config import load_env

def main():
      load_env()
      testar_agente()

if __name__ == "__main__":
      main()