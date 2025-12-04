"""
Script de exemplo para testar a API
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def print_response(title, response):
    """Exibe resposta formatada"""
    print(f"\n{'='*60}")
    print(f"📌 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    if response.status_code != 204:
        print(f"Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")


def main():
    """Demonstração de uso da API"""
    
    print("🚀 Testando API de Gerenciamento de Solicitações")
    
    # 1. Health Check
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    
    # 2. Criar primeira solicitação
    response = requests.post(f"{BASE_URL}/solicitacoes", json={
        "tipo": "suporte",
        "descricao": "Problema crítico no módulo de autenticação do sistema principal",
        "status": "pendente"
    })
    print_response("Criar Solicitação #1", response)
    sol1_id = response.json()["id"]
    
    # 3. Criar segunda solicitação
    response = requests.post(f"{BASE_URL}/solicitacoes", json={
        "tipo": "desenvolvimento",
        "descricao": "Implementar novo dashboard com gráficos interativos para análise de dados",
        "status": "pendente"
    })
    print_response("Criar Solicitação #2", response)
    sol2_id = response.json()["id"]
    
    # 4. Criar terceira solicitação
    response = requests.post(f"{BASE_URL}/solicitacoes", json={
        "tipo": "manutencao",
        "descricao": "Manutenção preventiva do servidor de banco de dados PostgreSQL",
        "status": "em_andamento"
    })
    print_response("Criar Solicitação #3", response)
    
    # 5. Listar todas as solicitações
    response = requests.get(f"{BASE_URL}/solicitacoes")
    print_response("Listar Todas as Solicitações", response)
    
    # 6. Buscar solicitação específica por ID
    response = requests.get(f"{BASE_URL}/solicitacoes/{sol1_id}")
    print_response(f"Buscar Solicitação #{sol1_id}", response)
    
    # 7. Atualizar status da primeira solicitação
    response = requests.patch(
        f"{BASE_URL}/solicitacoes/{sol1_id}/status",
        params={"novo_status": "em_andamento"}
    )
    print_response(f"Atualizar Status da Solicitação #{sol1_id}", response)
    
    # 8. Atualizar completamente a segunda solicitação
    response = requests.put(f"{BASE_URL}/solicitacoes/{sol2_id}", json={
        "tipo": "desenvolvimento",
        "descricao": "Implementar novo dashboard com gráficos interativos e relatórios exportáveis",
        "status": "concluida"
    })
    print_response(f"Atualizar Completamente Solicitação #{sol2_id}", response)
    
    # 9. Filtrar por status
    response = requests.get(f"{BASE_URL}/solicitacoes", params={"status": "em_andamento"})
    print_response("Filtrar Solicitações - Status: Em Andamento", response)
    
    # 10. Obter estatísticas
    response = requests.get(f"{BASE_URL}/solicitacoes/estatisticas/geral")
    print_response("Estatísticas Gerais", response)
    
    # 11. Excluir uma solicitação
    response = requests.delete(f"{BASE_URL}/solicitacoes/{sol1_id}")
    print_response(f"Excluir Solicitação #{sol1_id}", response)
    
    # 12. Verificar que foi excluída
    response = requests.get(f"{BASE_URL}/solicitacoes/{sol1_id}")
    print_response(f"Tentar Buscar Solicitação Excluída #{sol1_id}", response)
    
    # 13. Listar novamente para ver estado final
    response = requests.get(f"{BASE_URL}/solicitacoes")
    print_response("Estado Final - Todas as Solicitações", response)
    
    print(f"\n{'='*60}")
    print("✅ Demonstração concluída com sucesso!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Erro: Não foi possível conectar à API!")
        print("Certifique-se de que a API está rodando:")
        print("   uvicorn app:app --reload\n")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}\n")
