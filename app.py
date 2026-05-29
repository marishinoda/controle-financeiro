import flet as ft
from datetime import datetime
import pytz
import asyncio
import json

from ui.tela_home import tela_home
from ui.tela_entradas import tela_entradas
from ui.tela_gastos import tela_gastos
from ui.tela_planejamento import tela_planejamento
from ui.tela_anotacoes import tela_anotacoes
from ui.tela_login import tela_login

from data.supabase_client import supabase


async def main(page: ft.Page):

    import importlib.metadata

    print("FLET VERSION:", importlib.metadata.version("flet"))
    print("HAS shared_preferences:", hasattr(page, "shared_preferences"))
    print("HAS client_storage:", hasattr(page, "client_storage"))


    # Configuração básica
    page.title = "Controle Financeiro"
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
    agora = datetime.now(pytz.timezone("America/Manaus"))

    mes_atual = {
        "ano": agora.year,
        "mes": agora.month,
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

        if destino == "login":
            conteudo.controls.append(
                tela_login(page, navegar)
            )

        elif destino == "home":
            conteudo.controls.append(
                tela_home(page, navegar, mes_atual)
            )

        elif destino == "entradas":
            conteudo.controls.append(
                tela_entradas(page, navegar, mes_atual)
            )

        elif destino == "gastos":
            conteudo.controls.append(
                tela_gastos(page, navegar, mes_atual)
            )

        elif destino == "planejamento":
            conteudo.controls.append(
                tela_planejamento(page, navegar, mes_atual)
            )

        elif destino == "anotacoes":
            conteudo.controls.append(
                tela_anotacoes(page, navegar, mes_atual)
            )

        page.update()

    page.scroll = ft.ScrollMode.AUTO
    page.add(conteudo)

    # Pequena espera para garantir shared_preferences pronto
    await asyncio.sleep(0.1)

    # =========================
    # RESTAURA SESSÃO
    # =========================

    try:
        sessao_json = await page.shared_preferences.get("auth_session")

        if isinstance(sessao_json, str):
            sessao_salva = json.loads(sessao_json)
        else:
            sessao_salva = sessao_json

    except Exception as erro:
        print("ERRO AO LER SESSÃO:", erro)
        sessao_salva = None

    print("SESSÃO LIDA:", sessao_salva)

    if sessao_salva:
        try:
            resposta = supabase.auth.set_session(
                sessao_salva["access_token"],
                sessao_salva["refresh_token"]
            )

            print("SESSÃO RESTAURADA:", resposta.session)

            # SALVA TOKENS NOVOS
            if resposta.session:
                await page.shared_preferences.set(
                    "auth_session",
                    json.dumps({
                        "access_token": resposta.session.access_token,
                        "refresh_token": resposta.session.refresh_token,
                    })
                )

            navegar("home")

        except Exception as erro:
            print("ERRO AO RESTAURAR SESSÃO:", repr(erro))

            await page.shared_preferences.remove("auth_session")

            navegar("login")

    else:
        navegar("login")


# Execução do app
ft.app(target=main)