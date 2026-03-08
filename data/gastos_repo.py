from data.supabase_client import supabase


def buscar_gastos():
    response = (
        supabase
        .table("gastos")
        .select("*")
        .order("data")
        .execute()
    )

    return response.data or []

def adicionar_gasto(descricao, valor, data):

    response = (
        supabase
        .table("gastos")
        .insert({
            "descricao": descricao,
            "valor": valor,
            "data": data
        })
        .execute()
    )

    return response.data

def adicionar_entrada(descricao, valor, data):

    response = (
        supabase
        .table("entradas")
        .insert({
            "descricao": descricao,
            "valor": valor,
            "data": data
        })
        .execute()
    )

    return response.data