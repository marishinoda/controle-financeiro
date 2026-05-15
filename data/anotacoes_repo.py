from data.supabase_client import supabase
def get_user_id():
    user = supabase.auth.get_user()

    if user and user.user:
        return user.user.id

    return None


def buscar_anotacao(ano, mes):
    response = (
        supabase
        .table("anotacoes")
        .select("*")
        .eq("ano", ano)
        .eq("mes", mes)
        .eq("user_id", get_user_id())
        .execute()
    )

    return response.data[0] if response.data else None


def salvar_anotacao(ano, mes, texto):
    existente = buscar_anotacao(ano, mes)

    if existente:
        return (
            supabase
            .table("anotacoes")
            .update({"texto": texto})
            .eq("id", existente["id"])
            .execute()
        )

    return (
        supabase
        .table("anotacoes")
        .insert({
            "ano": ano,
            "mes": mes,
            "texto": texto,
            "user_id": get_user_id(),
        })
        .execute()
    )