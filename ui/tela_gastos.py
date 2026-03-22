import flet as ft
from datetime import datetime

from data.gastos_repo import adicionar_gasto, converter_real_para_float
from ui.layout_base import (
    CARD_BG,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    ACCENT,
    CARD_RADIUS,
)


def tela_gastos(page: ft.Page, navegar):
    def formatar_data(valor):
        numeros = "".join(filter(str.isdigit, valor))

        if len(numeros) <= 2:
            return numeros
        elif len(numeros) <= 4:
            return f"{numeros[:2]}/{numeros[2:]}"
        else:
            return f"{numeros[:2]}/{numeros[2:4]}/{numeros[4:8]}"

    def atualizar_data(e):
        e.control.value = formatar_data(e.control.value)
        e.control.update()
    # Campos
    descricao = ft.TextField(
        label="Descrição",
        hint_text="Ex: Aluguel, Mercado, Internet",
        filled=True,
        bgcolor=CARD_BG,
        border_radius=CARD_RADIUS,
        text_style=ft.TextStyle(color=TEXT_PRIMARY),
        label_style=ft.TextStyle(color=TEXT_SECONDARY),
    )

    valor = ft.TextField(
        label="Valor",
        hint_text="R$ 0,00",
        filled=True,
        bgcolor=CARD_BG,
        border_radius=CARD_RADIUS,
        text_style=ft.TextStyle(color=TEXT_PRIMARY),
        on_change=lambda e: atualizar_valor(e),
        label_style=ft.TextStyle(color=TEXT_SECONDARY),
    )

    data = ft.TextField(
        label="Data",
        value=datetime.now().strftime("%d/%m/%Y"),
        filled=True,
        bgcolor=CARD_BG,
        border_radius=CARD_RADIUS,
        text_style=ft.TextStyle(color=TEXT_PRIMARY),
        label_style=ft.TextStyle(color=TEXT_SECONDARY),
        on_change=lambda e: atualizar_data(e),
    )

    fixo_valor = False

    def toggle_fixo(e):
        nonlocal fixo_valor
        fixo_valor = not fixo_valor

        container = e.control
        texto = container.content

        container.bgcolor = "#e75480" if fixo_valor else "#ffffff"
        container.border = ft.border.all(0, "#ffffff") if fixo_valor else ft.border.all(1, "#dddddd")

        texto.color = "white" if fixo_valor else TEXT_PRIMARY

        container.update()

    fixo = ft.Container(
        on_click=toggle_fixo,
        bgcolor="#ffffff",
        border=ft.border.all(1, "#dddddd"),
        border_radius=20,
        padding=ft.padding.symmetric(horizontal=16, vertical=8),
        content=ft.Text(
            "Gasto fixo",
            color=TEXT_PRIMARY,
            size=14,
            weight=ft.FontWeight.W_500,
        ),
    )

    # Função salvar

    def formatar_digito(valor_str):
        numeros = "".join(filter(str.isdigit, valor_str))

        if numeros == "":
            return "R$ 0,00"

        valor = int(numeros) / 100

        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def atualizar_valor(e):
        e.control.value = formatar_digito(e.control.value)
        e.control.update()

    def formatar_data(valor):
        numeros = "".join(filter(str.isdigit, valor))

        if len(numeros) <= 2:
            return numeros
        elif len(numeros) <= 4:
            return f"{numeros[:2]}/{numeros[2:]}"
        else:
            return f"{numeros[:2]}/{numeros[2:4]}/{numeros[4:8]}"

    def salvar_gasto(e):
        try:
            descricao_valor = descricao.value
            valor_valor = converter_real_para_float(valor.value)
            data_valor = datetime.strptime(data.value, "%d/%m/%Y").strftime("%Y-%m-%d")



            adicionar_gasto(descricao_valor, valor_valor, data_valor, fixo_valor)

            print("Gasto salvo com sucesso!")

            # limpa campos
            descricao.value = ""
            valor.value = ""
            page.update()

        except Exception as erro:
            print("Erro ao salvar gasto:", erro)

    return ft.Column(
        controls=[
            # Título
            ft.Text(
                "Gastos 💸",
                size=26,
                weight=ft.FontWeight.BOLD,
                color=TEXT_PRIMARY,
            ),

            ft.Container(height=20),

            descricao,
            valor,
            data,
            fixo,

            ft.Container(height=20),

            # Botão salvar
            ft.Container(
                width=240,
                height=50,
                bgcolor=ACCENT,
                border_radius=25,
                content=ft.Row(
                    controls=[
                        ft.Text(
                            "Salvar gasto",
                            color=ft.Colors.BLACK,
                            weight=ft.FontWeight.BOLD,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                on_click=salvar_gasto,
            ),

            ft.Container(height=10),

            # Voltar
            ft.TextButton(
                content=ft.Text("← Voltar", color="#666666"),
                on_click=lambda e: navegar("home"),
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=14,
    )