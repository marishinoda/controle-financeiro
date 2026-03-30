import flet as ft
from datetime import datetime

from ui.tela_home import tela_home
from ui.tela_entradas import tela_entradas
from ui.tela_gastos import tela_gastos
from ui.tela_planejamento import tela_planejamento


def main(page: ft.Page):
    # Configuração básica
    page.title = "Controle Financeiro"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#f5e6ea"
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_resizable = True

    # Container principal
    conteudo = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Estado global do mês
    mes_atual = {
        "ano": datetime.now().year,
        "mes": datetime.now().month,
    }

    def navegar(destino: str, direcao_mes: int = 0):
        # Atualiza mês se clicou nas setas
        if direcao_mes != 0:
            mes_atual["mes"] += direcao_mes

            if mes_atual["mes"] > 12:
                mes_atual["mes"] = 1
                mes_atual["ano"] += 1

            if mes_atual["mes"] < 1:
                mes_atual["mes"] = 12
                mes_atual["ano"] -= 1

        # Limpa a tela
        conteudo.controls.clear()

        # Decide qual tela mostrar
        if destino == "home":
            conteudo.controls.append(
                tela_home(page, navegar, mes_atual)
            )

        elif destino == "entradas":
            conteudo.controls.append(
                tela_entradas(page, navegar, mes_atual)
            )

        elif destino == "gastos":
            conteudo.controls.append(
                tela_gastos(page, navegar)
            )

        elif destino == "planejamento":
            conteudo.controls.append(
                tela_planejamento(page, navegar, mes_atual)
            )

        page.update()

    # Inicializa o app na Home
    navegar("home")

    # Adiciona o container à página
    page.scroll = ft.ScrollMode.AUTO

    page.add(conteudo)


# Execução do app
ft.run(main)
