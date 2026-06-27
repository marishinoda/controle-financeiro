import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

_client = None


def get_supabase():
    global _client

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")

    if not url or not key:
        raise RuntimeError("Variáveis do Supabase não encontradas")

    if _client is None:
        _client = create_client(url, key)

    return _client


class LazySupabase:
    def __getattr__(self, name):
        return getattr(get_supabase(), name)


supabase = LazySupabase()


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
