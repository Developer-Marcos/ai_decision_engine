from project.utils.interface import exibir_relatorio
from project.config.config import load_env
from project.core.grafo import criar_grafo
from project.utils.interface import exibir_relatorio, console, limpar_console, input_pergunta
from rich.panel import Panel
import time

def main():
      load_env()

      pergunta_usuario = input_pergunta()
      state_inicial = {
            "problema": pergunta_usuario,
            "conteudo_pesquisado": [],
            "numero_iteracao": 0
      }

      fluxo = criar_grafo()
      with console.status("[bold yellow]Iniciando motores analíticos...[/bold yellow]", spinner="dots"):
            time.sleep(1)
            limpar_console()
            
            console.log("[cyan]Processando dados... Isso pode demorar um pouco.[/cyan]")
            resultado_final = fluxo.invoke(state_inicial)

      if resultado_final.get("aprovado") is False:
            limpar_console()
            console.print(Panel("[bold red]Análise Abortada:[/bold red] A pergunta viola as diretrizes de segurança.", border_style="red"))
      else:
            exibir_relatorio(data=resultado_final, pergunta_original=pergunta_usuario)
      
      
if __name__ == "__main__":
      main()