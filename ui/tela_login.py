import flet as ft
from data.supabase_client import supabase


def tela_login(page: ft.Page, navegar):
    email = ft.TextField(
        label="Email",
        width=300,
        border_radius=25,
        filled=True,
        bgcolor="white",
        color="#555555",
        label_style=ft.TextStyle(color="#777777"),

    )

    senha = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        width=300,
        border_radius=25,
        bgcolor="white",
        color="#555555",
        label_style=ft.TextStyle(color="#777777"),
    )

    async def entrar(e):
        try:
            resposta = supabase.auth.sign_in_with_password({
                "email": email.value,
                "password": senha.value,
            })

            if resposta.session:
                await page.shared_preferences.set(
                    "auth_session",
                    {
                        "access_token": resposta.session.access_token,
                        "refresh_token": resposta.session.refresh_token,
                    }
                )

                print(
                    "SESSÃO SALVA:",
                    await page.shared_preferences.get("auth_session")
                )

            navegar("home")

        except Exception:
            page.snack_bar = ft.SnackBar(
                ft.Text("Erro ao entrar"),
                open=True,
            )
            page.update()


    def criar_conta(e):
        try:
            supabase.auth.sign_up({
                "email": email.value,
                "password": senha.value,
            })
            page.snack_bar = ft.SnackBar(
                ft.Text("Conta criada 💖"),
                open=True,
            )
            page.update()


        except Exception:
            page.snack_bar = ft.SnackBar(
                ft.Text("Erro ao criar conta"),
                open=True,
            )
            page.update()

    return ft.Container(
        bgcolor="#f5e6ea",
        expand=True,
        alignment=ft.Alignment(0, -0.2),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=24,
            controls=[
                ft.Text(
                    "🔐Controle Financeiro",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color="#555555",
                ),

                ft.Text(
                    "Entre na sua conta 💖",
                    size=16,
                    color="#777777",
                ),

                ft.Container(
                    width=320,
                    content=email,
                ),

                ft.Container(
                    width=320,
                    content=senha,
                ),

                ft.Container(
                    width=220,
                    height=52,
                    bgcolor="#eb5c8c",
                    border_radius=30,
                    alignment=ft.Alignment(0, 0),
                    on_click=entrar,
                    content=ft.Text(
                        "Entrar",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="white",
                    ),
                ),

                ft.Container(
                    width=220,
                    height=48,
                    bgcolor="#dbeafe",
                    border_radius=28,
                    alignment=ft.Alignment(0, 0),
                    on_click=criar_conta,
                    content=ft.Text(
                        "Criar conta",
                        size=18,
                        weight=ft.FontWeight.W_600,
                        color="#60a5fa",
                    ),
                ),
            ],
        ),
    )
