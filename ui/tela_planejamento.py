from textwrap import wrap
import flet as ft
from datetime import datetime
import pytz

hoje = datetime.now(pytz.timezone("America/Manaus")).strftime("%Y-%m-%d")
from data.gastos_repo import atualizar_pago
from data.supabase_client import (
    buscar_entradas,
    buscar_gastos_por_mes,
    excluir_gasto,
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

# ---------- MOCK DE ENTRADAS ----------
ENTRADAS_MOCK = [
    {"descricao": "Salário", "valor": "R$ 2.500,00"},
    {"descricao": "Freela", "valor": "R$ 350,00"},
]

# ---------- MOCK DE GASTOS POR MÊS ----------
DADOS_POR_MES = {
    "2026-01": [
        {"data": "08", "descricao": "Rosiane (comida)", "valor": "R$ 235,00", "pago": True},
        {"data": "10", "descricao": "Rejane (comida)", "valor": "R$ 150,00", "pago": True},
        {"data": "21", "descricao": "Água", "valor": "R$ 156,86", "pago": False},
        {"data": "24", "descricao": "Luz", "valor": "R$ 180,00", "pago": False},
    ],
    "2026-02": [
        {"data": "05", "descricao": "Internet", "valor": "R$ 120,00", "pago": False},
        {"data": "10", "descricao": "Academia", "valor": "R$ 90,00", "pago": True},
        {"data": "18", "descricao": "Cartão", "valor": "R$ 540,00", "pago": False},
    ],
}

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


def calcular_resumo_real(gastos, entradas):
    total_gastos = sum(float(g["valor"]) for g in gastos) if gastos else 0
    total_entradas = sum(float(e["valor"]) for e in entradas) if entradas else 0
    saldo = total_entradas - total_gastos
    return total_entradas, total_gastos, saldo

def resumo_mes(gastos, entradas):
    total_gastos = sum(valor_para_float(i["valor"]) for i in gastos)
    total_entradas = sum(valor_para_float(i["valor"]) for i in entradas)
    saldo = total_entradas - total_gastos
    return total_entradas, total_gastos, saldo

def formatar_real(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def marcar_pago(e):
    item = e.control.data
    novo_valor = e.control.value
    item["pago"] = novo_valor
    atualizar_pago(item["id"], novo_valor)


# ---------- COMPONENTES ----------
def coluna_resumo(titulo, valor):
    if titulo == "Saldo":
        cor = "#6ee7b7" if valor >= 0 else "#fb7185"
    elif titulo == "Entradas":
        cor = "#6ee7b7"
    else:
        cor = "#fb7185"

    return ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text(
                titulo,
                size=SUMMARY_LABEL_SIZE,
                color=TEXT_SECONDARY,
            ),
            ft.Text(
                f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                size=18,
                weight=ft.FontWeight.W_600,
                color=cor,
                max_lines=1,
                overflow=ft.TextOverflow.ELLIPSIS,
            ),
        ],
    )


def card_resumo(total_entradas, total_gastos, saldo):
    return ft.Container(
        bgcolor="#ffffff",
        border_radius=20,
        padding=20,
        margin=ft.margin.only(bottom=10),

        content=ft.Column(
            spacing=6,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    controls=[
                        coluna_resumo("Entradas", total_entradas),
                        coluna_resumo("Gastos", total_gastos),
                    ],
                ),

                ft.Divider(height=1, color="#eeeeee"),

                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            "Saldo",
                            size=12,
                            color=TEXT_SECONDARY,
                        ),
                        ft.Text(
                            formatar_real(saldo),
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color="#6ee7b7" if saldo >= 0 else "#fb7185",
                        ),
                    ],
                ),
            ],
        ),
    )

def linha_planejamento(item, page, navegar):
        from datetime import datetime
        import pytz

        data_formatada = datetime.strptime(item["data"], "%Y-%m-%d").strftime("%d")

        return ft.Container(
            bgcolor="#ffffff",
            border_radius=20,
            padding=15,
            margin=ft.margin.only(bottom=15),

            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,

                controls=[

                    # ESQUERDA (tudo agrupado)
                    ft.Row(
                        spacing=15,
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
                                animate=ft.Animation(300, "easeInOut"),
                                on_click=lambda e: marcar_pago_click(item, page, navegar),
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
                                spacing=2,
                                controls=[

                                    ft.Text(
                                        item["descricao"],
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
                        ],
                    ),

                    # DIREITA (botões juntinhos)
                    ft.Row(
                        spacing=2,
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                icon_color="#666666",
                                tooltip="Editar",
                                on_click=lambda e, item=item: editar_item(e, item, page, navegar)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color="#e57373",
                                icon_size=18,
                                tooltip="Excluir",
                                on_click=lambda e: excluir(item, page, navegar)
                            ),
                        ],
                    ),
                ]
            )
        )


def excluir(item, page, navegar):
    excluir_gasto(item["id"])

    page.snack_bar = ft.SnackBar(
        ft.Text("Conta excluída"),
        open=True
    )

    navegar("planejamento")

def marcar_pago_click(item, page, navegar):
    novo_valor = not item.get("pago", False)

    atualizar_pago(item["id"], novo_valor)

    page.snack_bar = ft.SnackBar(
        ft.Text("Atualizado"),
        open=True
    )

    page.update()

    navegar("planejamento")

# ---------- TELA ----------

def formatar_data(e):
    numeros = "".join(filter(str.isdigit, e.control.value))

    if len(numeros) <= 2:
        e.control.value = numeros
    elif len(numeros) <= 4:
        e.control.value = f"{numeros[:2]}/{numeros[2:]}"
    else:
        e.control.value = f"{numeros[:2]}/{numeros[2:4]}/{numeros[4:8]}"

    e.control.update()


def editar_item(e, item, page, navegar):

    from datetime import datetime

    descricao = ft.TextField(value=item["descricao"])
    valor = ft.TextField(value=f'R$ {item["valor"]:.2f}')

    data_formatada = datetime.strptime(item["data"], "%Y-%m-%d").strftime("%d/%m/%Y")

    data = ft.TextField(
        value=data_formatada,
        on_change=lambda e: formatar_data(e)
    )

    def salvar(e):
        from data.gastos_repo import atualizar_gasto

        descricao_valor = descricao.value
        valor_valor = float(
            valor.value.replace("R$", "").replace(".", "").replace(",", ".")
        )

        data_valor = datetime.strptime(data.value, "%d/%m/%Y").strftime("%Y-%m-%d")

        atualizar_gasto(
            item["id"],
            descricao_valor,
            valor_valor,
            data_valor
        )

        dialog.open = False
        page.update()
        navegar("planejamento")

    def fechar(e):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Editar gasto"),
        content=ft.Column(
            controls=[descricao, valor, data],
            tight=True
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=fechar),
            ft.ElevatedButton("Salvar", on_click=salvar),
        ],
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()


def tela_planejamento(page: ft.Page, navegar, mes_atual):
    ano = mes_atual["ano"]
    mes = mes_atual["mes"]

    itens = buscar_gastos_por_mes(ano, mes)
    hoje = datetime.now(pytz.timezone("America/Manaus")).strftime("%Y-%m-%d")

    alertas = [
        item for item in itens
        if item.get("fixo") and not item.get("pago") and item.get("data", "").startswith(hoje)
    ]
    entradas = buscar_entradas()

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
                                size=14,
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

                card_resumo(total_entradas, total_gastos, saldo),

                *[
                    linha_planejamento(item, page, navegar)
                    for item in itens
                ],

                ft.TextButton(
                    "← Voltar",
                    on_click=lambda e: navegar("home"),
                ),
            ],
        ),
    )