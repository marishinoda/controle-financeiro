from textwrap import wrap
import flet as ft
from datetime import datetime
import pytz
import calendar

from data.gastos_repo import atualizar_pago, adicionar_gasto, atualizar_gasto
from data.gastos_repo import (
    atualizar_pago,
    adicionar_gasto,
    atualizar_gasto,
    excluir_gasto_total,
)
from data.supabase_client import (
    buscar_entradas,
    buscar_gastos_por_mes,
    excluir_gasto,
    buscar_gastos_fixos,
)

from ui.layout_base import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    CARD_BG,
    CARD_RADIUS,
    CARD_PADDING,
    CARD_TITLE_SIZE,
    CARD_SUBTITLE_SIZE,
    VALUE_SIZE,
    SUMMARY_LABEL_SIZE,
    SUMMARY_VALUE_SIZE,
)

# ---------- FUNÇÕES AUXILIARES ----------
def mes_formatado(mes_atual):
    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    return f"{meses[mes_atual['mes'] - 1]} {mes_atual['ano']}"


def valor_para_float(valor_str):
    return float(
        valor_str.replace("R$", "")
        .replace(".", "")
        .replace(",", ".")
        .strip()
    )

def hoje_manaus():
    return datetime.now(
        pytz.timezone("America/Manaus")
    )


def calcular_resumo_real(gastos, entradas):
    total_gastos = sum(float(g["valor"]) for g in gastos) if gastos else 0
    total_entradas = sum(float(e["valor"]) for e in entradas) if entradas else 0
    saldo = total_entradas - total_gastos
    return total_entradas, total_gastos, saldo


def formatar_real(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def marcar_pago_click(item, page, navegar, mes_atual):
    novo_valor = not item.get("pago", False)

    atualizado = atualizar_pago(
        item["id"],
        novo_valor,
        item["data"],
    )

    if not atualizado:
        adicionar_gasto(
            item["descricao"],
            item["valor"],
            item["data"],
            item.get("fixo", False),
            novo_valor,
        )

    page.snack_bar = ft.SnackBar(
        ft.Text("Atualizado"),
        open=True
    )

    navegar("planejamento")


def excluir(item, page, navegar):
    if item.get("fixo"):
        excluir_gasto_total(item["descricao"], item["valor"])
    else:
        excluir_gasto(item["id"])

    page.snack_bar = ft.SnackBar(
        ft.Text("Conta excluída"),
        open=True
    )

    navegar("planejamento")


def editar_gasto(item, page, navegar):
    descricao = ft.TextField(
        label="Descrição",
        value=item["descricao"],
        border_radius=20,
    )

    valor = ft.TextField(
        label="Valor",
        value=str(item["valor"]).replace(".", ","),
        border_radius=20,
    )

    def salvar_edicao(e):
        novo_valor = valor_para_float(valor.value)

        atualizar_gasto(
            item["id"],
            descricao.value,
            novo_valor,
            item["data"],
        )

        page.pop_dialog()

        page.snack_bar = ft.SnackBar(
            ft.Text("Edição salva"),
            open=True
        )

        navegar("planejamento")

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Editar gasto"),
        content=ft.Column(
            tight=True,
            controls=[descricao, valor],
        ),
        actions=[
            ft.TextButton(
                "Cancelar",
                on_click=lambda e: page.pop_dialog()
            ),
            ft.ElevatedButton(
                "Salvar",
                on_click=salvar_edicao
            ),
        ],
    )

    page.show_dialog(dialog)

def fechar_modal(e):
    e.page.dialog.open = False
    e.page.update()



# ---------- COMPONENTE ITEM ----------
def linha_planejamento(item, page, navegar, mes_atual):
    data_formatada = datetime.strptime(item["data"], "%Y-%m-%d").strftime("%d")

    return ft.Container(
        bgcolor="#ffffff",
        border_radius=20,
        padding=15,
        margin=ft.margin.only(bottom=15),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[

                ft.Row(
                    spacing=10,
                    expand=True,
                    controls=[

                        ft.Text(
                            data_formatada,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_PRIMARY,
                        ),

                        ft.Container(
                            width=40,
                            height=40,
                            border_radius=20,
                            bgcolor="#d1fae5" if item.get("pago") else "#fce7f3",
                            on_click=lambda e: marcar_pago_click(item, page, navegar, mes_atual),
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(
                                        "✓" if item.get("pago") else "",
                                        size=18,
                                        color="#059669",
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ],
                            ),
                        ),

                        ft.Column(
                            expand=True,
                            spacing=2,
                            controls=[
                                ft.Text(
                                    item["descricao"],
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                    size=16,
                                    weight=ft.FontWeight.W_600,
                                    color=TEXT_PRIMARY,
                                ),
                                ft.Row(
                                    spacing=6,
                                    controls=[
                                        ft.Text(
                                            formatar_real(item["valor"]),
                                            size=18,
                                            color="#059669" if item.get("pago") else TEXT_SECONDARY,
                                        ),
                                        ft.Container(
                                            content=ft.Text(
                                                "Fixo",
                                                size=10,
                                                color="#065f46",
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            bgcolor="#d1fae5",
                                            padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                            border_radius=10,
                                            visible=item.get("fixo", False),
                                        ),
                                    ],
                                ),
                            ],
                        ),

                        ft.PopupMenuButton(
                            icon=ft.Icons.MORE_VERT,
                            icon_color="#999999",
                            items=[
                                ft.PopupMenuItem(
                                    content=ft.Text("Editar"),
                                    on_click=lambda e, item=item: editar_gasto(item, page, navegar),
                                ),
                                ft.PopupMenuItem(
                                    content=ft.Text("Excluir"),
                                    on_click=lambda e, item=item: excluir(item, page, navegar),
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )



# ---------- TELA PRINCIPAL ----------
def tela_planejamento(page: ft.Page, navegar, mes_atual):
    ano = mes_atual["ano"]
    mes = mes_atual["mes"]

    itens = buscar_gastos_por_mes(ano, mes)

    fixos = buscar_gastos_fixos()

    fixos_unicos = {}
    for f in fixos:
        chave = (f["descricao"], float(f["valor"]))
        if chave not in fixos_unicos:
            fixos_unicos[chave] = f

    fixos = list(fixos_unicos.values())

    for fixo in fixos:
        dia_original = int(fixo["data"].split("-")[2])
        ultimo_dia = calendar.monthrange(ano, mes)[1]
        dia_final = min(dia_original, ultimo_dia)

        nova_data = f"{ano}-{mes:02}-{dia_final:02}"

        ja_existe = any(
            item["descricao"] == fixo["descricao"]
            and float(item["valor"]) == float(fixo["valor"])
            and item["data"] == nova_data
            for item in itens
        )

    if not ja_existe:
        novo = adicionar_gasto(
            fixo["descricao"],
            fixo["valor"],
            nova_data,
            True,
            False,
        )
        if novo:
            itens.extend(novo)


    itens.sort(key=lambda x: x["data"])

    hoje = hoje_manaus().strftime("%Y-%m-%d")

    alertas = [
        item for item in itens
        if item.get("fixo") and not item.get("pago") and item.get("data", "").startswith(hoje)
    ]

    entradas = [
        e for e in buscar_entradas()
        if e["data"].startswith(f"{ano}-{mes:02}")
    ]

    total_entradas, total_gastos, saldo = calcular_resumo_real(itens, entradas)

    return ft.Container(
        bgcolor="#f5e6ea",
        padding=20,
        expand=True,
        content=ft.Column(
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
            controls=[

                *(
                    [
                        ft.Container(
                            bgcolor="#fff3cd",
                            border_radius=12,
                            padding=10,
                            content=ft.Text(
                                f"⚠️ Vence hoje: {len(alertas)} conta(s)",
                                color="#856404",
                            ),
                        )
                    ] if alertas else []
                ),

                ft.Text(
                    f"Planejamento • {mes_formatado(mes_atual)}",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_PRIMARY,
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=min(page.width * 0.84, 340),
                            margin=ft.margin.only(left=-8),
                            bgcolor="white",
                            border_radius=35,
                            padding=ft.padding.symmetric(horizontal=18, vertical=10),
                            content=ft.Column(
                                spacing=4,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                        controls=[
                                            ft.Column(
                                                spacing=2,
                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                controls=[
                                                    ft.Text("Entradas 💰", size=13, color="#6b7280"),
                                                    ft.Text(
                                                        formatar_real(total_entradas),
                                                        size=18,
                                                        weight=ft.FontWeight.BOLD,
                                                        color="#63d8b4",
                                                    ),
                                                ],
                                            ),
                                            ft.Column(
                                                spacing=2,
                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                controls=[
                                                    ft.Text("Gastos 📉", size=13, color="#6b7280"),
                                                    ft.Text(
                                                        formatar_real(total_gastos),
                                                        size=18,
                                                        weight=ft.FontWeight.BOLD,
                                                        color="#f4a3ad",
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    ft.Divider(height=1, color="#dddddd"),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Column(
                                                spacing=1,
                                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                controls=[
                                                    ft.Text("Saldo 💵", size=13, color="#6b7280"),
                                                    ft.Text(
                                                        formatar_real(saldo),
                                                        size=17,
                                                        weight=ft.FontWeight.BOLD,
                                                        color="#63d8b4" if saldo >= 0 else "#e76f7a",
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),


                *[
                    linha_planejamento(item, page, navegar, mes_atual)
                    for item in itens
                ],
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.TextButton(
                            content=ft.Text(
                                "← Voltar",
                                color=TEXT_SECONDARY,
                                size=16,
                                weight=ft.FontWeight.BOLD,
                            ),
                            on_click=lambda e: navegar("home"),
                        ),
                    ],
                ),
            ]
        )
    )

