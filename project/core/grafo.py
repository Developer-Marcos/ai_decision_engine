from langgraph.graph import StateGraph, END
from project.agents.guardrail import node_guardrail
from project.agents.planejador import node_planejador
from project.agents.pesquisador import node_pesquisador
from project.agents.gerador import node_gerador
from project.agents.critico import node_critico
from project.agents.refinador import node_refinador
from project.utils.chains_auxiliares import refinar_query
from project.core.estado import AgentState
import base64

def node_refinar_query(state: AgentState):
      query_original = state.get("problema", "")
      query_refinada = refinar_query(query=query_original)

      return {"problema": query_refinada}

def router_guardrail(state: AgentState):
      if state.get("aprovado") is False:
            return "Rejeitado"
      
      return "Aprovado"

def router_de_pesquisa(state: AgentState):
      if len(state.get("conteudo_pesquisado", [])) > 0 and state.get("iteracao_pesquisa", 0) < 3:
            return "pesquisador"
      
      return "gerador"

def router_pos_critica(state: AgentState):
      if state.get("iteracao_critica", 0) >= 3:
            return "refinador"
      
      destino = state.get("proximo_passo", "refinador").lower().strip()

      if destino in ["planejador", "pesquisador", "refinador"]:
           return destino
      
      return "refinador"

def sub_grafo_processamento():
      sub_esqueleto = StateGraph(AgentState)

      sub_esqueleto.add_node("planejador", node_planejador)
      sub_esqueleto.add_node("pesquisador", node_pesquisador)
      sub_esqueleto.add_node("gerador", node_gerador)
      sub_esqueleto.add_node("critico", node_critico)
      sub_esqueleto.add_node("refinador", node_refinador)

      sub_esqueleto.set_entry_point("planejador")
      sub_esqueleto.add_edge("planejador", "pesquisador")
      sub_esqueleto.add_edge("gerador", "critico")
      sub_esqueleto.add_edge("refinador", END)

      sub_esqueleto.add_conditional_edges(
            "pesquisador",
            router_de_pesquisa,
            {"pesquisador": "pesquisador", "gerador": "gerador"}
      )

      sub_esqueleto.add_conditional_edges(
            "critico",
            router_pos_critica,
            {
                  "planejador": "planejador", 
                  "pesquisador": "pesquisador", 
                  "refinador": "refinador"
            }
      )

      return sub_esqueleto.compile()

def criar_grafo():
      grafo_principal = StateGraph(AgentState)

      processamento = sub_grafo_processamento()

      grafo_principal.add_node("guardrail", node_guardrail)
      grafo_principal.add_node("melhorar_query", node_refinar_query)
      grafo_principal.add_node("processamento", processamento)

      grafo_principal.set_entry_point("guardrail")

      grafo_principal.add_conditional_edges(
            "guardrail",
            router_guardrail,
            {
                  "Rejeitado": END,
                  "Aprovado": "melhorar_query"
            }
      )

      grafo_principal.add_edge("melhorar_query", "processamento")
      grafo_principal.add_edge("processamento", END)

      return grafo_principal.compile()

if __name__ == "__main__":
    app = criar_grafo()

    print("\n--- Estrutura do Grafo Compilada com Sucesso ---")
    mermaid_grafo = app.get_graph(xray=1).draw_mermaid()
    conteudo = base64.b64encode(mermaid_grafo.encode('utf-8')).decode('utf-8')

    print(f"https://mermaid.ink/img/{conteudo}")