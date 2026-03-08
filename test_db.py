from data.supabase_client import supabase
from datetime import date

# teste de insert em entradas
response = supabase.table("entradas").insert({
    "descricao": "Teste inicial",
    "valor": 100.0,
    "data": date.today().isoformat()
}).execute()

print("Resposta do Supabase:")
print(response)
