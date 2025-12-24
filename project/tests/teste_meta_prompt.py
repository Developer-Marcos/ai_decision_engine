from project.utils.chains_auxiliares import gerar_meta_prompt

def testar_meta_prompt(entrada):
      print(gerar_meta_prompt(problema=entrada))

if __name__ == "__main__":
      testar_meta_prompt()