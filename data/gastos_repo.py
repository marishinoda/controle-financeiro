from data.supabase_client import supabase

def converter_real_para_float(valor_str):

    return float(
        valor_str
        .replace("R$", "")
        .replace(".", "")
        .replace(",", ".")
        .strip()
    )

def buscar_gastos():
    response = (
        supabase
        .table("gastos")
        .select("*")
        .order("data")
        .execute()
    )

    return response.data or []

def adicionar_gasto(descricao, valor, data, fixo, pago=False):

    response = (
        supabase
        .table("gastos")
        .insert({
            "descricao": descricao,
            "valor": valor,
            "data": data,
            "fixo": fixo,
            "pago": pago,
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

def atualizar_pago(gasto_id, pago, data):

    response = (
        supabase
        .table("gastos")
        .update({"pago": pago})
        .eq("id", gasto_id)
        .eq("data", data)
        .execute()
    )

    return response.data

def excluir_entrada(entrada_id):

    response = (
        supabase
        .table("entradas")
        .delete()
        .eq("id", entrada_id)
        .execute()
    )

    return response.data

def buscar_entradas():

    response = (
        supabase
        .table("entradas")
        .select("*")
        .order("data")
        .execute()
    )

    return response.data or []

def atualizar_gasto(id, descricao, valor, data):
    from data.supabase_client import supabase

    supabase.table("gastos").update({
        "descricao": descricao,
        "valor": valor,
        "data": data
    }).eq("id", id).execute()

def buscar_gastos_fixos():
    return supabase.table("gastos").select("*").eq("fixo", True).execute().data