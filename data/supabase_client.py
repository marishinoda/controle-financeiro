import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise Exception("Variáveis do Supabase não encontradas no .env")

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


def buscar_gastos():
    response = (
        supabase
        .table("gastos")
        .select("*")
        .order("data")
        .execute()
    )
    return response.data

from datetime import date


def buscar_gastos_por_mes(ano, mes):
    data_inicio = date(ano, mes, 1)

    if mes == 12:
        data_fim = date(ano + 1, 1, 1)
    else:
        data_fim = date(ano, mes + 1, 1)

    response = (
        supabase
        .table("gastos")
        .select("*")
        .gte("data", data_inicio)
        .lt("data", data_fim)
        .order("data")
        .execute()
    )

    return response.data

def buscar_gastos_fixos():
    response = supabase.table("gastos").select("*").eq("fixo", True).execute()
    return response.data

def buscar_entradas():
    response = (
        supabase
        .table("entradas")
        .select("*")
        .order("data")
        .execute()
    )
    return response.data

def adicionar_gasto(descricao, valor, categoria, status, data):
    response = (
        supabase
        .table("gastos")
        .insert({
            "descricao": descricao,
            "valor": valor,
            "categoria": categoria,
            "status": status,
            "data": data
        })
        .execute()
    )
    return response.data

def excluir_gasto(id_gasto):
    supabase.table("gastos").delete().eq("id", id_gasto).execute()
