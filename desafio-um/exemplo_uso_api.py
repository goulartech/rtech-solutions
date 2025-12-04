"""
Script de exemplo de uso da API de Solicitações
Demonstra todas as operações disponíveis na API
"""

import requests
from datetime import date, timedelta
import json

# URL base da API (ajuste conforme necessário)
BASE_URL = "http://localhost:8000/api/v1/solicitacoes/"


def imprimir_resposta(titulo, response):
    """Função auxiliar para imprimir respostas formatadas"""
    print(f"\n{'='*60}")
    print(f"{titulo}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Resposta: {response.text}")


def exemplo_criar_solicitacao_ferias():
    """Exemplo: Criar solicitação de férias"""
    data_inicio = str(date.today() + timedelta(days=30))
    data_fim = str(date.today() + timedelta(days=44))
    
    payload = {
        "tipo": "ferias",
        "titulo": "Férias de Verão 2025",
        "descricao": "Férias programadas para janeiro de 2025",
        "solicitante": "João Silva",
        "data_inicio": data_inicio,
        "data_fim": data_fim
    }
    
    response = requests.post(BASE_URL, json=payload)
    imprimir_resposta("1. CRIAR SOLICITAÇÃO DE FÉRIAS", response)
    return response.json().get('id') if response.status_code == 201 else None


def exemplo_criar_solicitacao_reembolso():
    """Exemplo: Criar solicitação de reembolso"""
    payload = {
        "tipo": "reembolso",
        "titulo": "Reembolso de Transporte - Projeto X",
        "descricao": "Despesas com transporte durante o desenvolvimento do Projeto X",
        "solicitante": "Maria Santos",
        "valor": "350.00"
    }
    
    response = requests.post(BASE_URL, json=payload)
    imprimir_resposta("2. CRIAR SOLICITAÇÃO DE REEMBOLSO", response)
    return response.json().get('id') if response.status_code == 201 else None


def exemplo_criar_solicitacao_treinamento():
    """Exemplo: Criar solicitação de treinamento"""
    data_inicio = str(date.today() + timedelta(days=60))
    data_fim = str(date.today() + timedelta(days=62))
    
    payload = {
        "tipo": "treinamento",
        "titulo": "Treinamento em Django REST Framework",
        "descricao": "Curso avançado de Django REST Framework",
        "solicitante": "Carlos Souza",
        "valor": "1500.00",
        "data_inicio": data_inicio,
        "data_fim": data_fim
    }
    
    response = requests.post(BASE_URL, json=payload)
    imprimir_resposta("3. CRIAR SOLICITAÇÃO DE TREINAMENTO", response)
    return response.json().get('id') if response.status_code == 201 else None


def exemplo_listar_solicitacoes():
    """Exemplo: Listar todas as solicitações"""
    response = requests.get(BASE_URL)
    imprimir_resposta("4. LISTAR TODAS AS SOLICITAÇÕES", response)


def exemplo_buscar_solicitacao(solicitacao_id):
    """Exemplo: Buscar detalhes de uma solicitação específica"""
    if not solicitacao_id:
        print("\nPular busca de solicitação específica (ID não disponível)")
        return
    
    response = requests.get(f"{BASE_URL}{solicitacao_id}/")
    imprimir_resposta(f"5. BUSCAR DETALHES DA SOLICITAÇÃO #{solicitacao_id}", response)


def exemplo_atualizar_solicitacao(solicitacao_id):
    """Exemplo: Atualizar uma solicitação"""
    if not solicitacao_id:
        print("\nPular atualização (ID não disponível)")
        return
    
    payload = {
        "titulo": "Férias de Verão 2025 - ATUALIZADO",
        "observacoes": "Data atualizada conforme calendário da empresa"
    }
    
    response = requests.patch(f"{BASE_URL}{solicitacao_id}/", json=payload)
    imprimir_resposta(f"6. ATUALIZAR SOLICITAÇÃO #{solicitacao_id}", response)


def exemplo_aprovar_solicitacao(solicitacao_id):
    """Exemplo: Aprovar uma solicitação"""
    if not solicitacao_id:
        print("\nPular aprovação (ID não disponível)")
        return
    
    payload = {
        "observacoes": "Aprovado pela gerência de RH"
    }
    
    response = requests.post(f"{BASE_URL}{solicitacao_id}/aprovar/", json=payload)
    imprimir_resposta(f"7. APROVAR SOLICITAÇÃO #{solicitacao_id}", response)


def exemplo_rejeitar_solicitacao(solicitacao_id):
    """Exemplo: Rejeitar uma solicitação"""
    if not solicitacao_id:
        print("\nPular rejeição (ID não disponível)")
        return
    
    payload = {
        "observacoes": "Período não disponível no calendário"
    }
    
    response = requests.post(f"{BASE_URL}{solicitacao_id}/rejeitar/", json=payload)
    imprimir_resposta(f"8. REJEITAR SOLICITAÇÃO #{solicitacao_id}", response)


def exemplo_cancelar_solicitacao(solicitacao_id):
    """Exemplo: Cancelar uma solicitação"""
    if not solicitacao_id:
        print("\nPular cancelamento (ID não disponível)")
        return
    
    payload = {
        "observacoes": "Cancelado a pedido do solicitante"
    }
    
    response = requests.post(f"{BASE_URL}{solicitacao_id}/cancelar/", json=payload)
    imprimir_resposta(f"9. CANCELAR SOLICITAÇÃO #{solicitacao_id}", response)


def exemplo_filtrar_por_tipo():
    """Exemplo: Filtrar solicitações por tipo"""
    response = requests.get(f"{BASE_URL}?tipo=reembolso")
    imprimir_resposta("10. FILTRAR SOLICITAÇÕES POR TIPO (REEMBOLSO)", response)


def exemplo_filtrar_por_status():
    """Exemplo: Filtrar solicitações por status"""
    response = requests.get(f"{BASE_URL}?status=pendente")
    imprimir_resposta("11. FILTRAR SOLICITAÇÕES POR STATUS (PENDENTE)", response)


def exemplo_buscar_por_solicitante():
    """Exemplo: Buscar solicitações por nome do solicitante"""
    response = requests.get(f"{BASE_URL}?search=Maria")
    imprimir_resposta("12. BUSCAR SOLICITAÇÕES POR SOLICITANTE (Maria)", response)


def exemplo_estatisticas():
    """Exemplo: Obter estatísticas das solicitações"""
    response = requests.get(f"{BASE_URL}estatisticas/")
    imprimir_resposta("13. OBTER ESTATÍSTICAS DAS SOLICITAÇÕES", response)


def exemplo_excluir_solicitacao(solicitacao_id):
    """Exemplo: Excluir uma solicitação"""
    if not solicitacao_id:
        print("\nPular exclusão (ID não disponível)")
        return
    
    response = requests.delete(f"{BASE_URL}{solicitacao_id}/")
    imprimir_resposta(f"14. EXCLUIR SOLICITAÇÃO #{solicitacao_id}", response)


def main():
    """Função principal que executa todos os exemplos"""
    print("\n" + "="*60)
    print("  API DE SOLICITAÇÕES INTERNAS - EXEMPLOS DE USO")
    print("="*60)
    print(f"\nBase URL: {BASE_URL}")
    print("\nCertifique-se de que o servidor está rodando!")
    print("Execute: python manage.py runserver")
    
    input("\nPressione Enter para começar...")
    
    # Criar solicitações de exemplo
    id_ferias = exemplo_criar_solicitacao_ferias()
    id_reembolso = exemplo_criar_solicitacao_reembolso()
    id_treinamento = exemplo_criar_solicitacao_treinamento()
    
    # Listar solicitações
    exemplo_listar_solicitacoes()
    
    # Buscar solicitação específica
    exemplo_buscar_solicitacao(id_ferias)
    
    # Atualizar solicitação
    exemplo_atualizar_solicitacao(id_ferias)
    
    # Aprovar solicitação
    exemplo_aprovar_solicitacao(id_treinamento)
    
    # Rejeitar solicitação
    exemplo_rejeitar_solicitacao(id_reembolso)
    
    # Cancelar solicitação
    exemplo_cancelar_solicitacao(id_ferias)
    
    # Filtros
    exemplo_filtrar_por_tipo()
    exemplo_filtrar_por_status()
    exemplo_buscar_por_solicitante()
    
    # Estatísticas
    exemplo_estatisticas()
    
    # Excluir solicitação (comentado para não excluir dados de exemplo)
    # exemplo_excluir_solicitacao(id_ferias)
    
    print("\n" + "="*60)
    print("  EXEMPLOS CONCLUÍDOS!")
    print("="*60)
    print("\nAcesse a documentação Swagger em: http://localhost:8000/api/docs/")
    print("Acesse o Django Admin em: http://localhost:8000/admin/")
    print("\n")


if __name__ == "__main__":
    main()
