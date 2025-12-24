from project.config.llm_client import instanciar_llm
from langchain_core.messages import HumanMessage, ToolMessage
from project.core.estado import AgentState
from langchain_tavily import TavilySearch

def node_pesquisador(state: AgentState):
      ferramenta_de_pesquisa = TavilySearch(max_results=3)
      ferramentas = [ferramenta_de_pesquisa]

      llm = instanciar_llm(modelo="gemini-2.5-flash", agent_name="pesquisador_ativo", temperature=0)
      llm_com_ferramentas = llm.bind_tools(ferramentas)

      prompt_sistema = f"""
            Você é um Pesquisador Especialista. 
            Seu objetivo é cumprir este plano de pesquisa: {state['plano']}
            Utilize as queries sugeridas como ponto de partida: {state['querys_de_pesquisa']}
            
            INSTRUÇÕES:
            1. Use a ferramenta Tavily para buscar dados factuais.
            2. Analise os resultados. Se a informação estiver incompleta para um tópico do plano, faça uma nova busca com termos diferentes.
            3. Só finalize quando tiver dados suficientes para o Gerador avaliar (Demanda, Técnico, Financeiro, Competição).
            4. Se o conteúdo pesquisado já contém o que você precisa, não chame a ferramenta novamente.
      """

      mensagens = [HumanMessage(content=prompt_sistema)]

      if state.get("conteudo_pesquisado"):
            mensagens.append(HumanMessage(content=f"Dados já coletados até agora: {state['conteudo_pesquisado']}"))
      
      resposta = llm_com_ferramentas.invoke(mensagens)

      novos_resultados = list()
      if resposta.tool_calls:
            mensagens.append(resposta)

            for chamada in resposta.tool_calls:
                  resultado_bruto = ferramenta_de_pesquisa.invoke(chamada['args'])
                  
                  tool_message = ToolMessage(
                        tool_call_id=chamada["id"],
                        content=str(resultado_bruto)
                  )
                  mensagens.append(tool_message)

                  novos_resultados.append({
                        "query": chamada['args'].get("query"),
                        "conteudo": resultado_bruto
                  })

            return {"conteudo_pesquisado": novos_resultados, "numero_iteracao": 1}
      
      return {"conteudo_pesquisado": [], "numero_iteracao": 0}
