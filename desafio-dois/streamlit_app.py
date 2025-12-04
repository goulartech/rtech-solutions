"""
Interface Web com Streamlit para gerenciamento de solicitações
"""
import streamlit as st
import requests
from datetime import datetime
from typing import Optional

# Configuração da página
st.set_page_config(
    page_title="Gerenciamento de Solicitações",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL da API
API_URL = "http://localhost:8000"

# Mapeamento de labels em português
STATUS_LABELS = {
    "pendente": "⏳ Pendente",
    "em_andamento": "🔄 Em Andamento",
    "concluida": "✅ Concluída",
    "cancelada": "❌ Cancelada"
}

TIPO_LABELS = {
    "manutencao": "🔧 Manutenção",
    "suporte": "🆘 Suporte",
    "desenvolvimento": "💻 Desenvolvimento",
    "consulta": "❓ Consulta",
    "outros": "📌 Outros"
}

# Cores para status
STATUS_COLORS = {
    "pendente": "#FFA500",
    "em_andamento": "#1E90FF",
    "concluida": "#32CD32",
    "cancelada": "#DC143C"
}


def verificar_api():
    """Verifica se a API está online"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def criar_solicitacao(tipo: str, descricao: str, status: str):
    """Cria uma nova solicitação via API"""
    try:
        data = {
            "tipo": tipo,
            "descricao": descricao,
            "status": status
        }
        response = requests.post(f"{API_URL}/solicitacoes", json=data)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)


def listar_solicitacoes(status_filter: Optional[str] = None):
    """Lista todas as solicitações"""
    try:
        params = {"status": status_filter} if status_filter else {}
        response = requests.get(f"{API_URL}/solicitacoes", params=params)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)


def atualizar_solicitacao(solicitacao_id: int, tipo: str, descricao: str, status: str):
    """Atualiza uma solicitação existente"""
    try:
        data = {}
        if tipo:
            data["tipo"] = tipo
        if descricao:
            data["descricao"] = descricao
        if status:
            data["status"] = status
        
        response = requests.put(f"{API_URL}/solicitacoes/{solicitacao_id}", json=data)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)


def atualizar_status(solicitacao_id: int, novo_status: str):
    """Atualiza apenas o status de uma solicitação"""
    try:
        response = requests.patch(
            f"{API_URL}/solicitacoes/{solicitacao_id}/status",
            params={"novo_status": novo_status}
        )
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)


def deletar_solicitacao(solicitacao_id: int):
    """Deleta uma solicitação"""
    try:
        response = requests.delete(f"{API_URL}/solicitacoes/{solicitacao_id}")
        response.raise_for_status()
        return True, None
    except requests.exceptions.RequestException as e:
        return False, str(e)


def obter_estatisticas():
    """Obtém estatísticas das solicitações"""
    try:
        response = requests.get(f"{API_URL}/solicitacoes/estatisticas/geral")
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)


def formatar_data(data_str: str) -> str:
    """Formata data ISO para formato brasileiro"""
    try:
        dt = datetime.fromisoformat(data_str.replace('Z', '+00:00'))
        return dt.strftime("%d/%m/%Y %H:%M")
    except:
        return data_str


def main():
    """Função principal da aplicação Streamlit"""
    
    # Título principal
    st.title("📋 Sistema de Gerenciamento de Solicitações")
    
    # Verifica se a API está online
    if not verificar_api():
        st.error("⚠️ API não está respondendo! Certifique-se de que está rodando em http://localhost:8000")
        st.info("Execute: `uvicorn app:app --reload` para iniciar a API")
        return
    
    # Sidebar para navegação
    st.sidebar.title("Menu")
    opcao = st.sidebar.radio(
        "Escolha uma opção:",
        ["📊 Dashboard", "➕ Nova Solicitação", "📋 Listar Solicitações", "✏️ Atualizar", "🗑️ Excluir"]
    )
    
    # Dashboard
    if opcao == "📊 Dashboard":
        st.header("Dashboard - Estatísticas")
        
        stats, error = obter_estatisticas()
        if error:
            st.error(f"Erro ao carregar estatísticas: {error}")
        else:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total de Solicitações", stats.get("total", 0))
            
            with col2:
                if stats.get("por_status"):
                    st.metric("Pendentes", stats["por_status"].get("pendente", 0))
            
            with col3:
                if stats.get("por_status"):
                    st.metric("Concluídas", stats["por_status"].get("concluida", 0))
            
            # Gráficos de estatísticas
            if stats.get("por_status"):
                st.subheader("Solicitações por Status")
                col1, col2 = st.columns(2)
                
                with col1:
                    for status_key, count in stats["por_status"].items():
                        label = STATUS_LABELS.get(status_key, status_key)
                        st.write(f"{label}: **{count}**")
                
                with col2:
                    if stats.get("por_tipo"):
                        st.subheader("Por Tipo")
                        for tipo_key, count in stats["por_tipo"].items():
                            label = TIPO_LABELS.get(tipo_key, tipo_key)
                            st.write(f"{label}: **{count}**")
    
    # Nova Solicitação
    elif opcao == "➕ Nova Solicitação":
        st.header("Criar Nova Solicitação")
        
        with st.form("form_criar"):
            tipo = st.selectbox(
                "Tipo da Solicitação",
                options=list(TIPO_LABELS.keys()),
                format_func=lambda x: TIPO_LABELS[x]
            )
            
            descricao = st.text_area(
                "Descrição",
                placeholder="Descreva a solicitação com detalhes (mínimo 10 caracteres)...",
                height=150
            )
            
            status = st.selectbox(
                "Status Inicial",
                options=list(STATUS_LABELS.keys()),
                format_func=lambda x: STATUS_LABELS[x],
                index=0
            )
            
            submitted = st.form_submit_button("✅ Criar Solicitação")
            
            if submitted:
                if len(descricao.strip()) < 10:
                    st.error("A descrição deve ter no mínimo 10 caracteres!")
                else:
                    solicitacao, error = criar_solicitacao(tipo, descricao, status)
                    if error:
                        st.error(f"Erro ao criar solicitação: {error}")
                    else:
                        st.success(f"✅ Solicitação #{solicitacao['id']} criada com sucesso!")
                        st.json(solicitacao)
    
    # Listar Solicitações
    elif opcao == "📋 Listar Solicitações":
        st.header("Lista de Solicitações")
        
        # Filtro por status
        col1, col2 = st.columns([3, 1])
        with col1:
            filtro_status = st.selectbox(
                "Filtrar por Status",
                options=["Todos"] + list(STATUS_LABELS.keys()),
                format_func=lambda x: "Todas" if x == "Todos" else STATUS_LABELS[x]
            )
        
        with col2:
            if st.button("🔄 Atualizar"):
                st.rerun()
        
        # Busca solicitações
        status_filter = None if filtro_status == "Todos" else filtro_status
        solicitacoes, error = listar_solicitacoes(status_filter)
        
        if error:
            st.error(f"Erro ao listar solicitações: {error}")
        elif not solicitacoes:
            st.info("Nenhuma solicitação encontrada.")
        else:
            st.write(f"**Total:** {len(solicitacoes)} solicitação(ões)")
            
            for sol in solicitacoes:
                with st.expander(f"#{sol['id']} - {TIPO_LABELS[sol['tipo']]} - {STATUS_LABELS[sol['status']]}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**ID:** {sol['id']}")
                        st.write(f"**Tipo:** {TIPO_LABELS[sol['tipo']]}")
                        st.write(f"**Status:** {STATUS_LABELS[sol['status']]}")
                    
                    with col2:
                        st.write(f"**Criado em:** {formatar_data(sol['data_criacao'])}")
                        st.write(f"**Atualizado em:** {formatar_data(sol['data_atualizacao'])}")
                    
                    st.write(f"**Descrição:** {sol['descricao']}")
    
    # Atualizar Solicitação
    elif opcao == "✏️ Atualizar":
        st.header("Atualizar Solicitação")
        
        solicitacao_id = st.number_input("ID da Solicitação", min_value=1, step=1)
        
        if st.button("🔍 Buscar"):
            solicitacoes, _ = listar_solicitacoes()
            if solicitacoes:
                sol_encontrada = next((s for s in solicitacoes if s['id'] == solicitacao_id), None)
                if sol_encontrada:
                    st.session_state['solicitacao_atual'] = sol_encontrada
                else:
                    st.error("Solicitação não encontrada!")
        
        if 'solicitacao_atual' in st.session_state:
            sol = st.session_state['solicitacao_atual']
            
            st.info(f"Solicitação #{sol['id']} encontrada!")
            
            with st.form("form_atualizar"):
                tipo = st.selectbox(
                    "Tipo",
                    options=list(TIPO_LABELS.keys()),
                    format_func=lambda x: TIPO_LABELS[x],
                    index=list(TIPO_LABELS.keys()).index(sol['tipo'])
                )
                
                descricao = st.text_area(
                    "Descrição",
                    value=sol['descricao'],
                    height=150
                )
                
                status = st.selectbox(
                    "Status",
                    options=list(STATUS_LABELS.keys()),
                    format_func=lambda x: STATUS_LABELS[x],
                    index=list(STATUS_LABELS.keys()).index(sol['status'])
                )
                
                submitted = st.form_submit_button("💾 Atualizar")
                
                if submitted:
                    if len(descricao.strip()) < 10:
                        st.error("A descrição deve ter no mínimo 10 caracteres!")
                    else:
                        resultado, error = atualizar_solicitacao(
                            sol['id'], tipo, descricao, status
                        )
                        if error:
                            st.error(f"Erro ao atualizar: {error}")
                        else:
                            st.success("✅ Solicitação atualizada com sucesso!")
                            st.session_state['solicitacao_atual'] = resultado
                            st.rerun()
    
    # Excluir Solicitação
    elif opcao == "🗑️ Excluir":
        st.header("Excluir Solicitação")
        
        solicitacao_id = st.number_input("ID da Solicitação", min_value=1, step=1)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Buscar"):
                solicitacoes, _ = listar_solicitacoes()
                if solicitacoes:
                    sol_encontrada = next((s for s in solicitacoes if s['id'] == solicitacao_id), None)
                    if sol_encontrada:
                        st.session_state['solicitacao_deletar'] = sol_encontrada
                    else:
                        st.error("Solicitação não encontrada!")
        
        if 'solicitacao_deletar' in st.session_state:
            sol = st.session_state['solicitacao_deletar']
            
            st.warning("⚠️ Atenção! Esta ação não pode ser desfeita.")
            
            st.write(f"**ID:** {sol['id']}")
            st.write(f"**Tipo:** {TIPO_LABELS[sol['tipo']]}")
            st.write(f"**Descrição:** {sol['descricao']}")
            st.write(f"**Status:** {STATUS_LABELS[sol['status']]}")
            
            with col2:
                if st.button("🗑️ Confirmar Exclusão", type="primary"):
                    success, error = deletar_solicitacao(sol['id'])
                    if error:
                        st.error(f"Erro ao excluir: {error}")
                    else:
                        st.success("✅ Solicitação excluída com sucesso!")
                        del st.session_state['solicitacao_deletar']
                        st.rerun()
    
    # Rodapé
    st.sidebar.markdown("---")
    st.sidebar.info(
        "💡 **Dica:** Mantenha a API rodando em http://localhost:8000 "
        "para utilizar esta interface."
    )


if __name__ == "__main__":
    main()
