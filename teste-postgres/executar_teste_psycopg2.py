#!/usr/bin/env python3
"""
Script para executar todos os arquivos SQL do teste PostgreSQL
usando psycopg2 (conexão direta com o banco).

Instalação: pip install psycopg2-binary
"""

import psycopg2
import sys
from datetime import datetime
from pathlib import Path


def executar_sql(arquivo, conn):
    """Executa um arquivo SQL e retorna sucesso/falha"""
    print(f"\n▶ Executando: {arquivo.name}")
    
    start = datetime.now()
    
    try:
        # Lê o conteúdo do arquivo
        sql_content = arquivo.read_text(encoding='utf-8')
        
        # Cria cursor
        cursor = conn.cursor()
        
        # Executa o SQL
        cursor.execute(sql_content)
        
        # Commit
        conn.commit()
        
        # Pega resultados se houver
        try:
            resultados = cursor.fetchall()
            if resultados:
                for row in resultados:
                    print(row)
        except psycopg2.ProgrammingError:
            # Não há resultados (DDL/DML)
            pass
        
        cursor.close()
        
        duracao = (datetime.now() - start).total_seconds()
        print(f"✓ Sucesso ({duracao:.2f}s)")
        return True
        
    except psycopg2.Error as e:
        conn.rollback()
        duracao = (datetime.now() - start).total_seconds()
        print(f"✗ Erro ({duracao:.2f}s)")
        print(f"  {e}")
        return False
    except Exception as e:
        conn.rollback()
        duracao = (datetime.now() - start).total_seconds()
        print(f"✗ Erro inesperado ({duracao:.2f}s)")
        print(f"  {e}")
        return False


def main():
    """Função principal"""
    print("=" * 80)
    print("  EXECUTOR DE TESTES POSTGRESQL (psycopg2)")
    print("=" * 80)
    
    # Configurações de conexão
    db_config = {
        'dbname': 'prova_banco_dados',
        'user': 'postgres',
        'password': 'postgres',  # Adicione se necessário
        'host': 'localhost',
        'port': 5432
    }
    
    print(f"\nConectando ao banco: {db_config['dbname']}@{db_config['host']}")
    
    # Conecta ao banco
    try:
        conn = psycopg2.connect(**db_config)
        conn.autocommit = False  # Controle manual de transação
        print("✓ Conectado com sucesso\n")
    except psycopg2.Error as e:
        print(f"✗ Erro ao conectar: {e}")
        print("\nDica: Certifique-se que:")
        print("  1. PostgreSQL está rodando")
        print("  2. Banco 'prova_banco_dados' existe")
        print("  3. Credenciais estão corretas")
        print("  4. psycopg2 está instalado: pip install psycopg2-binary")
        sys.exit(1)
    
    # Obtém arquivos SQL (01 a 08)
    base_dir = Path(__file__).parent
    arquivos_sql = []
    for i in range(1, 9):
        arquivos = list(base_dir.glob(f"{i:02d}_*.sql"))
        if arquivos:
            arquivos_sql.extend(sorted(arquivos))
    
    if not arquivos_sql:
        print("✗ Nenhum arquivo SQL encontrado!")
        conn.close()
        sys.exit(1)
    
    print(f"Encontrados {len(arquivos_sql)} arquivos SQL\n")
    
    # Cria arquivo de log
    log_file = base_dir / f"log_execucao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    # Executa cada arquivo
    resultados = []
    for arquivo in arquivos_sql:
        sucesso = executar_sql(arquivo, conn)
        resultados.append((arquivo.name, sucesso))
        
        # Salva no log
        with open(log_file, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            status = "SUCESSO" if sucesso else "ERRO"
            f.write(f"[{timestamp}] {arquivo.name}: {status}\n")
        
        if not sucesso:
            continuar = input("\nErro detectado. Continuar? (s/N): ").strip().lower()
            if continuar != 's':
                print("\n⚠ Execução interrompida")
                break
    
    # Fecha conexão
    conn.close()
    print("\n✓ Conexão fechada")
    
    # Resumo
    print("\n" + "=" * 80)
    print("  RESUMO DA EXECUÇÃO")
    print("=" * 80)
    
    total = len(resultados)
    sucessos = sum(1 for _, sucesso in resultados if sucesso)
    
    print(f"\nTotal: {total} | Sucesso: {sucessos} | Erro: {total - sucessos}")
    print(f"\nLog salvo em: {log_file}")
    
    if sucessos == total:
        print("\n✅ Todos os testes executados com sucesso!")
        sys.exit(0)
    else:
        print("\n⚠ Execução finalizada com erros")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Interrompido pelo usuário")
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ Erro: {e}")
        sys.exit(1)
