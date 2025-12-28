from project.config.llm_client import instanciar_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def gerar_meta_prompt(problema: str) -> str:
      llm = instanciar_llm(modelo="gemini-2.5-flash-lite", agent_name="meta_prompt_gerador", temperature=0.2, extra_metadata={"test": False, "step": "gerar_meta_prompt"})  

      prompt = ChatPromptTemplate.from_template("""
            <role>
            Você é um Meta-Estrategista. Sua função é analisar um problema e criar 
            instruções de investigação para um analista júnior.
            </role>
                                            
            <examples>
                  <example>
                        <problem>Devo abrir um SaaS de correção de redações com IA?</problem>
                        <category>Digital / Software as a Service</category>
                        <directives>
                        - Avalie o custo por token (GPT-4o/Gemini) versus o ticket médio que um estudante está disposto a pagar.
                        - Verifique a precisão atual das LLMs nos critérios específicos do ENEM (Competências 1 a 5).
                        - Investigue a existência de APIs abertas do INEP ou repositórios de redações nota 1000 para treinamento/ajuste.
                        </directives>
                  </example>
                  <example>
                        <problem>Vale a pena investir em uma franquia de cafeteria no centro de SP?</problem>
                        <category>Negócio Físico / Alimentação</category>
                        <directives>
                        - Estime o fluxo de pedestres (footfall) no horário comercial na região pretendida.
                        - Pesquise o custo médio de aluguel comercial por m² e tempo de carência para reforma.
                        - Analise o faturamento médio de unidades da mesma franquia em regiões de densidade demográfica similar.
                        </directives>
                  </example>
            </examples>
                                                
            <task>
            Analise o problema abaixo e retorne 3 a 4 diretrizes estratégicas que 
            devem guiar a pesquisa de viabilidade. 
            Diferencie se o projeto é digital, físico, pessoal ou financeiro.
            </task>

            <problem>
            {problema}
            </problem>

            <instructions_format>
            - Retorne apenas as diretrizes, sem introduções.
            - Use tópicos claros.
            - Foque no que é "fazer ou quebrar" (make or break) para este caso específico.
            </instructions_format>
      """)

      chain = prompt | llm | StrOutputParser()

      return chain.invoke({"problema": problema}) 

def refinar_query(query: str) -> str:
      frase = query.strip().lower()
      llm = instanciar_llm(modelo="gemini-2.5-flash-lite", agent_name="meta_prompt_gerador", extra_metadata={"test": False, "step": "query_refinement"})

      prompt = ChatPromptTemplate.from_template("""
            <role>Você é um Especialista em Engenharia de Prompt e Refinamento de Consultas.</role>
            
            <task>
            Sua tarefa é pegar a pergunta bruta de um usuário e transformá-la em uma consulta 
            clara, objetiva e profissional para um motor de tomada de decisão.
            </task>
                                                
            <examples>
                  <example>
                        <input>quero fzr saas enem vale?</input>
                        <output>Vale a pena desenvolver um Software as a Service (SaaS) focado na correção automática de redações do ENEM utilizando inteligência artificial?</output>
                  </example>
                  <example>
                        <input>abrir cafeteria no centro de sp compensa hj em dia?</input>
                        <output>Qual é a viabilidade econômica atual para a abertura de uma cafeteria na região central de São Paulo, considerando custos fixos e concorrência local?</output>
                  </example>
                  <example>
                        <input>comprar um tesla ou carro a gas?</input>
                        <output>Análise comparativa de viabilidade financeira e operacional entre a aquisição de um veículo elétrico Tesla e um veículo movido a combustão interna.</output>
                  </example>
            </examples>                                    

            <instructions>
            - Mantenha a intenção original do usuário.
            - Corrija erros gramaticais e termos técnicos se necessário.
            - Se a pergunta for muito curta, expanda-a para que fique autoexplicativa.
            - Retorne APENAS a consulta refinada.
            </instructions>

            <input_bruto>
            {query_bruta}
            </input_bruto>
      """)

      chain_refinamento = prompt | llm | StrOutputParser()

      return chain_refinamento.invoke({"query_bruta": frase})

