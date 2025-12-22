from project.config.llm_client import instanciar_llm

def testar_agente():
      llm = instanciar_llm(agent_name="Testador", extra_metadata={"test": True, "step": "teste_inicial"})

      resposta = llm.invoke("Liste 3 riscos técnicos de construir um sistema de IA em produção.")
      print("\n--- Resposta ---")
      print(resposta.content)

if __name__ == "__main__":
      testar_agente()