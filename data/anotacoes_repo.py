from data.supabase_client import supabase


def buscar_anotacao(ano, mes):
    response = (
        supabase
        .table("anotacoes")
        .select("*")
        .eq("ano", ano)
        .eq("mes", mes)
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
        })
        .execute()
    )