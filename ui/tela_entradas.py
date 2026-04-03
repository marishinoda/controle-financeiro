import flet as ft
from datetime import datetime

from data.gastos_repo import (
    adicionar_entrada,
    excluir_entrada,
    buscar_entradas,
    converter_real_para_float,
)

from ui.layout_base import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    ACCENT,
)


def formatar_digito(valor_str):
    numeros = "".join(filter(str.isdigit, valor_str))

    if numeros == "":
        return "R$ 0,00"

    valor = int(numeros) / 100

    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


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


def tela_entradas(page: ft.Page, navegar, mes_atual):
    entradas = [
        item for item in buscar_entradas()
        if datetime.strptime(item["data"], "%Y-%m-%d").month == mes_atual["mes"]
           and datetime.strptime(item["data"], "%Y-%m-%d").year == mes_atual["ano"]
    ]

    hoje = datetime.now()
    data_valor = f"{hoje.day:02}/{mes_atual['mes']:02}/{mes_atual['ano']}"

    descricao = ft.TextField(
        label="Descrição",
        hint_text="Ex: Salário, Pix, Venda",
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
        value=data_valor,
        filled=True,
        bgcolor="#ffffff",
        border_radius=25,
        text_style=ft.TextStyle(color=TEXT_PRIMARY),
        label_style=ft.TextStyle(color=TEXT_SECONDARY),
        on_change=lambda e: atualizar_data(e),
    )

    def atualizar_valor(e):
        e.control.value = formatar_digito(e.control.value)
        e.control.update()

    def salvar_entrada(e):
        descricao_valor = descricao.value
        valor_valor = converter_real_para_float(valor.value)
        data_valor_formatada = datetime.strptime(
            data.value, "%d/%m/%Y"
        ).strftime("%Y-%m-%d")

        adicionar_entrada(
            descricao_valor,
            valor_valor,
            data_valor_formatada
        )

        descricao.value = ""
        valor.value = ""
        navegar("entradas")

    return ft.Column(
        controls=[
            ft.Text(
                "Entradas 💰",
                size=26,
                weight=ft.FontWeight.BOLD,
                color=TEXT_PRIMARY,
            ),

            ft.Container(height=20),

            descricao,
            valor,
            data,

            ft.Container(height=20),

            ft.Container(
                width=240,
                height=50,
                bgcolor=ACCENT,
                border_radius=25,
                content=ft.Row(
                    controls=[
                        ft.Text(
                            "Salvar entrada",
                            color="white",
                            weight=ft.FontWeight.BOLD,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                on_click=salvar_entrada,
            ),

            *[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(
                                    item["descricao"],
                                    color=TEXT_PRIMARY,
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                ),

                                ft.Text(
                                    formatar_digito(str(int(item["valor"] * 100))),
                                    color="#0f9d7a",
                                    size=18,
                                    weight=ft.FontWeight.W_500,
                                ),

                                ft.Text(
                                    datetime.strptime(item["data"], "%Y-%m-%d").strftime("%d/%m/%Y"),
                                    color=TEXT_SECONDARY,
                                    size=14,
                                )
                            ],
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color="#e9a0aa",
                            on_click=lambda e, item=item: excluir(item, page, navegar),
                        ),
                    ]
                )
                for item in entradas
            ],

            ft.Container(height=10),

            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.TextButton(
                        content=ft.Text(
                            "← Voltar",
                            color=TEXT_SECONDARY,
                            size=18,
                            weight=ft.FontWeight.W_500,
                        ),
                        on_click=lambda e: navegar("home"),
                    ),
                ],
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

def excluir(item, page, navegar):
    excluir_entrada(item["id"])
    navegar("entradas")