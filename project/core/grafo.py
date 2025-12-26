from langgraph.graph import StateGraph, END
from project.agents.planejador import node_planejador
from project.agents.pesquisador import node_pesquisador
from project.agents.gerador import node_gerador
from project.agents.critico import node_critico
from project.core.estado import AgentState
import base64

def router_de_pesquisa(state: AgentState):
      if len(state.get("conteudo_pesquisado", [])) > 0 and state.get("numero_iteracao", 0) < 3:
            return "pesquisador"
      
      return "gerador"

def router_pos_critica(state: AgentState):
      if state.get("numero_iteracao", 0) >= 5:
            return "refinador"
      
      return state.get("proximo_passo", "refinador")

def node_refinador_placeholder(state: AgentState):
    print("[Refinador] Polindo o relatório final...")
    return {"relatorio_final": state['relatorio_final'] + "\n\nRelatório revisado e aprovado pelo Crítico."}

def criar_grafo():
      grafo_esqueleto = StateGraph(AgentState)

      grafo_esqueleto.add_node("planejador", node_planejador)
      grafo_esqueleto.add_node("pesquisador", node_pesquisador)
      grafo_esqueleto.add_node("gerador", node_gerador)
      grafo_esqueleto.add_node("critico", node_critico)
      grafo_esqueleto.add_node("refinador", node_refinador_placeholder)

      grafo_esqueleto.set_entry_point("planejador")

      grafo_esqueleto.add_edge("planejador", "pesquisador")
      grafo_esqueleto.add_edge("gerador", "critico")
      grafo_esqueleto.add_edge("refinador", END)

      grafo_esqueleto.add_conditional_edges(
            "pesquisador",
            router_de_pesquisa,
            {
                  "pesquisador": "pesquisador",
                  "gerador": "gerador"
            }
      )

      grafo_esqueleto.add_conditional_edges(
            "critico",
            router_pos_critica,
            {
                  "planejador": "planejador",
                  "pesquisador": "pesquisador",
                  "refinador": "refinador"
            }
      )

      grafo_completo = grafo_esqueleto.compile()

      return grafo_completo

if __name__ == "__main__":
    app = criar_grafo()

    print("\n--- Estrutura do Grafo Compilada com Sucesso ---")
    mermaid_grafo = app.get_graph().draw_mermaid()
    conteudo = base64.b64encode(mermaid_grafo.encode('utf-8')).decode('utf-8')
    print(f"https://mermaid.ink/img/{conteudo}")