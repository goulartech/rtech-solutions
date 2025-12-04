# Sistema de Auxílio Transporte - Teste PostgreSQL

Sistema de banco de dados PostgreSQL para gerenciar solicitações de auxílio transporte de funcionários, incluindo controle de pagamentos e auditoria.

## Estrutura do Projeto

```
teste-postgres/
├── 01_create_tables.sql           # Criação das tabelas
├── 02_insert_data.sql              # Carga de dados inicial
├── 03_questao_01.sql               # Consulta com JOIN e ORDER BY
├── 04_questao_02.sql               # Consulta com GROUP BY e HAVING
├── 05_questao_03.sql               # Implementação de TRIGGER
├── 06_questao_04.sql               # Stored Procedure
├── 07_questao_05.sql               # Window Functions
├── 08_testes.sql                   # Scripts de validação
├── executar_teste.py               # Script Python (usa psql)
├── executar_teste_psycopg2.py      # Script Python (usa psycopg2)
├── REQUISITOS.md                   # Especificação detalhada
└── CHECKLIST.md                    # Checklist de validação
```

## Execução Automatizada

### Pré-requisitos

- PostgreSQL instalado e em execução (ou Docker)
- Python 3.6 ou superior
- Cliente `psql` disponível no PATH (ou psycopg2: `pip install psycopg2-binary`)

### Subindo PostgreSQL com Docker

Se você não tem PostgreSQL instalado localmente, pode usar Docker:

```bash
# Subir PostgreSQL em container
docker run --name postgres-teste \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=prova_banco_dados \
  -p 5432:5432 \
  -d postgres:15

# Verificar se está rodando
docker ps

# Acessar o PostgreSQL
docker exec -it postgres-teste psql -U postgres -d prova_banco_dados

# Parar o container
docker stop postgres-teste

# Remover o container
docker rm postgres-teste
```

**Dica**: Se o banco já existe e você quer limpar tudo:
```bash
docker stop postgres-teste && docker rm postgres-teste
# Depois suba novamente com o comando docker run acima
```

### Método 1: Script com psql

O script executa todos os arquivos SQL em sequência usando o cliente `psql`:

```bash
chmod +x executar_teste.py
python3 executar_teste.py
```

### Método 2: Script com psycopg2 (Conexão Python Pura)

Usa conexão direta ao banco via biblioteca Python:

```bash
pip install psycopg2-binary
python3 executar_teste_psycopg2.py
```

**Vantagens**: Não precisa do cliente `psql` instalado, melhor tratamento de erros.

### Configuração de Conexão

Por padrão, os scripts usam:
- **Database**: `prova_banco_dados`
- **User**: `postgres`
- **Password**: `` (vazio ou `postgres` se usando Docker)
- **Host**: `localhost`
- **Port**: `5432`

**Nota**: Se usar o Docker conforme comando acima, a senha é `postgres`. Edite o script `executar_teste_psycopg2.py` se necessário.

### Funcionalidades dos Scripts

Executa todos os arquivos SQL na ordem correta (01 a 08)  
Salva log completo em arquivo com timestamp  
Mostra resumo detalhado da execução  
Permite continuar ou parar em caso de erro  
Exibe tempo de execução de cada arquivo  
Captura e exibe outputs e erros

### Saída dos Scripts

Os scripts geram:

1. **Terminal**: Output com status em tempo real
2. **Arquivo de log**: `log_execucao_YYYYMMDD_HHMMSS.txt` com histórico completo

Exemplo de resumo:

```
================================================================================
  RESUMO DA EXECUÇÃO
================================================================================

Total: 8 | Sucesso: 8 | Erro: 0

Log salvo em: log_execucao_20251204_153045.txt

Todos os testes executados com sucesso!
```

## Execução Manual

Se preferir executar manualmente, siga esta ordem:

```bash
# 1. Criar banco de dados
psql -U postgres -c "CREATE DATABASE prova_banco_dados;"

# 2. Conectar ao banco
psql -U postgres -d prova_banco_dados

# 3. Executar cada arquivo na ordem
\i 01_create_tables.sql
\i 02_insert_data.sql
\i 03_questao_01.sql
\i 04_questao_02.sql
\i 05_questao_03.sql
\i 06_questao_04.sql
\i 07_questao_05.sql
\i 08_testes.sql
```

Ou executar de uma vez via terminal:

```bash
for file in 0{1..8}_*.sql; do
    echo "Executando $file..."
    psql -U postgres -d prova_banco_dados -f "$file"
done
```

## Estrutura do Banco de Dados

### Tabelas

1. **funcionarios**: Dados dos colaboradores
2. **solicitacoes**: Pedidos de auxílio transporte
3. **pagamentos**: Registros de pagamentos realizados
4. **log_auditoria**: Histórico de operações do sistema

### Recursos Implementados

- Integridade referencial com Foreign Keys
- Constraints de validação (CHECK, UNIQUE)
- Índices para otimização de consultas
- Trigger para atualização automática de status
- Stored Procedure para cancelamento de solicitações
- Auditoria automática de operações críticas

## Questões Implementadas

### Questão 1: JOIN e ORDER BY (2,0 pontos)
Relatório de solicitações aprovadas dos últimos 6 meses, ordenado por departamento e valor.

### Questão 2: GROUP BY e HAVING (2,0 pontos)
Análise mensal agregada de solicitações com estatísticas por período.

### Questão 3: TRIGGER (2,0 pontos)
Trigger que atualiza status para 'PAGO' automaticamente quando pagamento é inserido.

### Questão 4: STORED PROCEDURE (2,0 pontos)
Procedure `sp_cancelar_solicitacao` para cancelamento seguro de solicitações.

### Questão 5: WINDOW FUNCTIONS (2,0 pontos)
Ranking dos top 3 funcionários por departamento em gastos com auxílio transporte.

## Testes

O arquivo `08_testes.sql` inclui:

- Teste do trigger de pagamento
- Teste da procedure de cancelamento
- Teste de cenários de erro
- Validação de integridade dos dados

## Documentação Adicional

- **REQUISITOS.md**: Especificação completa do sistema

## Troubleshooting

### Erro: "psql: command not found"
Use o script `executar_teste_psycopg2.py` ou instale o cliente PostgreSQL.

### Erro: "connection refused"
Verifique se o PostgreSQL está rodando:
```bash
# Local
sudo systemctl status postgresql

# Docker
docker ps | grep postgres-teste
```

### Erro: "database does not exist"
Se usar Docker, certifique-se de ter criado o banco:
```bash
docker exec -it postgres-teste psql -U postgres -c "CREATE DATABASE prova_banco_dados;"
```
Ou recrie o container com a variável `POSTGRES_DB`.

### Erro de autenticação
No Docker, a senha padrão é `postgres`. Edite o arquivo `executar_teste_psycopg2.py` na linha `'password': ''` para `'password': 'postgres'`.

## Notas

- Todos os scripts são idempotentes quando possível (DROP IF EXISTS, CREATE OR REPLACE)
- Os logs incluem timestamp para rastreabilidade
- O script Python suporta interrupção por CTRL+C
- Recomenda-se revisar o log gerado após cada execução

Modelagem completa  
Carga de dados  
Todas as 5 questões implementadas  
Testes e validações  
Script de execução automatizada  
Documentação completa  
