from rich.console import Console
from rich.theme import Theme
from rich.prompt import Prompt
from rich.panel import Panel
import os

def limpar_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

custom_theme = Theme({
    "titulo": "bold cyan underline",
    "subtitulo": "bold magenta",
    "score": "bold white on cyan",
    "veredito_success": "bold green",
    "veredito_warning": "bold yellow",
    "danger": "bold red",
    "texto": "white"
})

console = Console(theme=custom_theme)

def input_pergunta():
    limpar_console()
    console.print(Panel.fit(
        "[bold cyan]AI DECISION ENGINE[/bold cyan]\n[white]Seu consultor estratégico inteligente[/white]"
    ))

    pergunta = Prompt.ask("\n[bold magenta]Qual ideia você deseja sabe se vale a pena?[/bold magenta]")
    return pergunta

def exibir_relatorio(data, pergunta_original):
    limpar_console()
    
    objeto_pydantic = data["relatorio_final"]
    relatorio = objeto_pydantic.model_dump()

    console.print("\n[titulo]RELATÓRIO DE VIABILIDADE ESTRATÉGICA[/titulo]")
    console.print(f"Pergunta Analisada: [italic white]{pergunta_original}[/italic white]")
    console.print(f"Status do Sistema: [bold green]Processamento Concluído[/bold green]")
    console.print("-" * 65)

    score = relatorio["percentual_score"]
    veredito = relatorio["veredito_final"]
    estilo_veredito = "veredito_warning" if "Cautela" in veredito else "veredito_success"
    
    console.print(f"\n[bold]PONTUAÇÃO FINAL:[/bold] [{estilo_veredito}]{score}%[/{estilo_veredito}]")
    console.print(f"[bold]VEREDITO:[/bold] [{estilo_veredito}]{veredito}[/{estilo_veredito}]")

    console.print("\n[subtitulo]● RESUMO EXECUTIVO[/subtitulo]")
    console.print(f"[texto]{relatorio['sumario_executivo']}[/texto]")

    console.print("\n[subtitulo]● ANÁLISE DOS PILARES (NOTAS)[/subtitulo]")
    for nota_pilar in relatorio["detalhamento_notas"]:
        console.print(f"  [cyan]•[/cyan] {nota_pilar}")

    console.print("\n[subtitulo]● INSIGHTS DE MERCADO[/subtitulo]")
    console.print(f"[texto]{relatorio['analise_mercado']}[/texto]")

    console.print("\n[subtitulo]● PROJEÇÃO E VIABILIDADE FINANCEIRA[/subtitulo]")
    console.print(f"[texto]{relatorio['viabilidade_financeira']}[/texto]")

    console.print("\n[danger]▲ MATRIZ DE RISCOS E PONTOS DE ATENÇÃO[/danger]")
    for risco in relatorio["matriz_riscos"]:
        console.print(f"  [danger]•[/danger] {risco}")

    console.print("\n[subtitulo]➜ CONCLUSÃO E RECOMENDAÇÕES[/subtitulo]")
    
    conclusoes = relatorio.get("conclusao_e_proximos_passos", [])
    
    if isinstance(conclusoes, list):
        for passo in conclusoes:
            console.print(f"  [cyan]•[/cyan] {passo}")
    else:
        console.print(f"[texto]{conclusoes}[/texto]")

    console.print("\n" + "=" * 65)


dados_simulados = {
    "relatorio_final": {
  "veredito_final": "Cautela (55.0%): A viabilidade de uma loja de café e chocolate em área de praia é mitigada pela forte sazonalidade do turismo e alta concorrência, apesar do potencial de demanda em alta temporada. Necessita de planejamento detalhado e capital para suportar flutuações.",
  "percentual_score": 55,
  "detalhamento_notas": [
    "Mercado (Nota 7): A demanda turística de sol e praia é alta, especialmente em alta temporada, indicando um público-alvo considerável.",
    "Operacional/Técnica (Nota 6): A operação é de baixa complexidade, mas exige flexibilidade para gerenciar estoque, pessoal e logística devido à sazonalidade. O ambiente e a experiência do cliente são cruciais.",
    "Financeira (Nota 5): Há potencial de consumo alto em regiões turísticas, mas a sazonalidade impacta a receita. Faltam dados específicos sobre custos e projeções de fluxo de caixa para análise robusta.",
    "Concorrência (Nota 4): O mercado de cafeterias em regiões de praia é saturado, com muitos concorrentes já estabelecidos e com diferenciais, exigindo uma proposta de valor única."
  ],
  "sumario_executivo": "A análise de viabilidade para uma loja de café e chocolate em área de praia revela potencial de demanda durante a alta temporada turística, mas enfrenta desafios significativos devido à sazonalidade acentuada e à alta concorrência. A falta de dados financeiros específicos impede uma avaliação completa da rentabilidade. Recomenda-se cautela, planejamento detalhado de estratégias para baixas temporadas e um estudo financeiro aprofundado para mitigar os riscos.",
  "analise_mercado": "A demanda por turismo de sol e praia no Brasil é alta, com grande fluxo de visitantes, especialmente no final do ano, criando um público-alvo considerável para café e chocolate em alta temporada. No entanto, o mercado de cafeterias em regiões de praia, como Ubatuba (com 28 estabelecimentos), já é saturado e competitivo, com diferenciais como vista para a praia e delivery. A sazonalidade turística implica flutuações significativas na demanda.",
  "viabilidade_financeira": "O turismo em regiões de praia gera alta arrecadação, indicando potencial de consumo. Contudo, a sazonalidade impacta diretamente as projeções de receita e o fluxo de caixa. Há uma lacuna de dados sobre custos de implantação, margens de lucro esperadas, e projeções financeiras anuais detalhadas para este tipo de negócio e localização, impossibilitando uma análise de ROI precisa.",
  "matriz_riscos": [
    "Sazonalidade acentuada da demanda turística e flutuações no fluxo de clientes.",
    "Ausência de dados específicos sobre consumo de café/chocolate por turistas e demografia local.",
    "Gestão de estoque e suprimentos frescos em logística potencialmente desafiadora em região turística.",
    "Contratação e treinamento de equipe para lidar com a sazonalidade, garantindo qualidade e evitando custos excessivos.",
    "Necessidade de investimento inicial em design para criar ambiente diferenciado e agradável.",
    "Alto impacto da sazonalidade no fluxo de caixa e na rentabilidade do negócio ao longo do ano.",
    "Falta de dados sobre investimento inicial, custos operacionais e preços de venda para o tipo de produto e localização.",
    "Ausência de projeções de vendas e lucros que considerem diferentes perfis de clientes e períodos do ano.",
    "Alta saturação do mercado de cafeterias em algumas regiões de praia, com muitos concorrentes diretos.",
    "Concorrentes existentes já oferecem serviços e diferenciais, como localização privilegiada e delivery.",
    "A necessidade de desenvolver uma proposta de valor muito clara e única para se destacar em um ambiente competitivo."
  ],
  "conclusao_e_proximos_passos": [
    "Desenvolver estratégias robustas para as baixas temporadas, como diferenciação de produtos, serviços para moradores locais ou ajuste da operação.",
    "Realizar um estudo financeiro aprofundado com projeções realistas de custos e receitas para todo o ciclo anual.",
    "Conduzir uma análise aprofundada da concorrência local para identificar uma proposta de valor única e sustentável.",
    "Assegurar capital suficiente para suportar a sazonalidade e eventuais períodos de menor faturamento.",
    "Avaliar a demografia local não-turística e seu potencial de consumo de café e chocolate."
  ]
}
}

if __name__ == "__main__":
    exibir_relatorio(dados_simulados)