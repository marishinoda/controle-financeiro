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
    entradas = buscar_entradas()

    hoje = datetime.now()
    data_valor = f"{hoje.day:02}/{mes_atual['mes']:02}/{mes_atual['ano']}"

    descricao = ft.TextField(label="Descrição")
    valor = ft.TextField(label="Valor", on_change=lambda e: atualizar_valor(e))
    data = ft.TextField(label="Data", value=data_valor, on_change=lambda e: atualizar_data(e))

    def atualizar_valor(e):
        e.control.value = formatar_digito(e.control.value)
        e.control.update()

    def salvar_entrada(e):
        descricao_valor = descricao.value
        valor_valor = converter_real_para_float(valor.value)
        data_valor_formatada = datetime.strptime(data.value, "%d/%m/%Y").strftime("%Y-%m-%d")

        adicionar_entrada(descricao_valor, valor_valor, data_valor_formatada)

        descricao.value = ""
        valor.value = ""
        page.update()

    return ft.Column(
        controls=[
            ft.Text("Entradas 💰", size=26),

            descricao,
            valor,
            data,

            ft.ElevatedButton("Salvar entrada", on_click=salvar_entrada),

            *[
                ft.Row(
                    controls=[
                        ft.Text(item["descricao"]),
                        ft.Text(item["data"]),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            on_click=lambda e, item=item: excluir(item, page, navegar),
                        ),
                    ]
                )

                for item in entradas
            ],

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
        ]
    )

def excluir(item, page, navegar):
    excluir_entrada(item["id"])
    navegar("entradas")