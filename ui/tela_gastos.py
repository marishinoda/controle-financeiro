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
        bgcolor="#ffffff",
        border_radius=25,
        text_style=ft.TextStyle(color=TEXT_PRIMARY),
        label_style=ft.TextStyle(color=TEXT_SECONDARY),
    )

    valor = ft.TextField(
        label="Valor",
        hint_text="R$ 0,00",
        filled=True,
        bgcolor="#ffffff",
        border_radius=25,
        text_style=ft.TextStyle(color=TEXT_PRIMARY),
        label_style=ft.TextStyle(color=TEXT_SECONDARY),
        on_change=lambda e: atualizar_valor(e),
    )


    data = ft.TextField(
        label="Data",
        value=datetime.now().strftime("%d/%m/%Y"),
        filled=True,
        bgcolor="#ffffff",
        border_radius=25,
        text_style=ft.TextStyle(color=TEXT_PRIMARY),
        label_style=ft.TextStyle(color=TEXT_SECONDARY),
        on_change=lambda e: atualizar_data(e),
    )

    fixo_valor = False

    def toggle_fixo(e):
        nonlocal fixo_valor
        fixo_valor = not fixo_valor

        container = e.control
        row = container.content
        texto = row.controls[0]
        icone = row.controls[1]

        if fixo_valor:
            container.bgcolor = "#e75480"

            texto.color = "white"
            icone.color = "white"
        else:
            container.bgcolor = "#ffffff"
            texto.color = TEXT_PRIMARY
            icone.color = "#cccccc"

        container.update()

    fixo = ft.Container(
        on_click=toggle_fixo,
        bgcolor="#f1f1f1",
        border_radius=25,
        padding=15,
        width=220,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(
                    "Gasto fixo",
                    color=TEXT_PRIMARY,
                    size=14,
                    weight=ft.FontWeight.W_500,
                ),
                ft.Icon(ft.Icons.CHECK_CIRCLE, color="#cccccc")
            ],
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
                            color="white",
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
        spacing=20,
    )