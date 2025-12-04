# Respostas - Questões Backend

## 1. Qual a diferença entre uma API REST e uma API SOAP?

**REST** é um estilo arquitetural que usa HTTP de forma simples, trabalha com recursos e retorna dados geralmente em JSON. É stateless, leve e mais fácil de consumir.

**SOAP** é um protocolo rígido baseado em XML, com especificação formal, suporta ACID transactions e segurança WS-Security. É mais pesado mas oferece mais garantias empresariais.

Em resumo: REST é flexível e moderno; SOAP é formal e verboso.

---

## 2. O que significa status code 200, 201, 400, 401, 403 e 500 em uma API?

- **200 OK**: Requisição bem-sucedida.
- **201 Created**: Recurso criado com sucesso.
- **400 Bad Request**: Erro de validação nos dados enviados pelo cliente.
- **401 Unauthorized**: Autenticação necessária ou credenciais inválidas.
- **403 Forbidden**: Autenticado mas sem permissão para acessar o recurso.
- **500 Internal Server Error**: Erro não tratado no servidor.

---

## 3. O que é o princípio de responsabilidade única (SRP) e por que é importante?

SRP (Single Responsibility Principle) diz que uma classe/módulo deve ter apenas um motivo para mudar, ou seja, uma única responsabilidade.

**Exemplo**: Uma classe `UserRepository` deve apenas lidar com persistência de dados, não validação de regras de negócio.

**Importância**: Facilita manutenção, testes, reutilização e reduz acoplamento. Código fica mais coeso e menos propenso a bugs.

---

## 4. Como você estruturaria um projeto backend simples (pacotes, camadas, responsabilidades)?

Estrutura típica em Python (arquitetura em camadas):

```
projeto/
├── src/
│   ├── models/          # Entidades/modelos de domínio
│   ├── repositories/    # Acesso a dados (DB, cache)
│   ├── services/        # Regras de negócio
│   ├── controllers/     # Endpoints da API (rotas)
│   └── utils/           # Funções auxiliares
├── tests/
├── requirements.txt
└── app.py
```

**Fluxo**: Controller → Service → Repository → Database

Cada camada tem responsabilidade clara: controllers recebem requests, services processam lógica, repositories persistem dados.

---

## 5. Explique a diferença entre variáveis imutáveis e mutáveis.

**Imutáveis**: Não podem ser alterados após criação. Em Python: `int`, `float`, `str`, `tuple`, `frozenset`.
```python
x = "hello"
x[0] = "H"
```

**Mutáveis**: Podem ser modificados. Em Python: `list`, `dict`, `set`.
```python
lista = [1, 2, 3]
lista[0] = 10
```

**Impacto**: Imutáveis são thread-safe e podem ser keys de dicionários. Mutáveis podem causar side effects se passados por referência.

---

## 6. Em Java, o que é uma Interface? Em Python, o que seria um decorator?

**Interface (Java)**: Contrato que define métodos que classes devem implementar, sem implementação concreta. Garante polimorfismo.

**Decorator (Python)**: Função que modifica comportamento de outra função/método sem alterar seu código. Usa `@` syntax.

```python
def log_execution(func):
    def wrapper(*args, **kwargs):
        print(f"Executando {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_execution
def processar_pedido(id):
    return f"Pedido {id} processado"
```

**Casos de uso**: Logging, validação, cache, autenticação, medição de tempo.

---

## 7. O que é um try/catch (Java) ou try/except (Python) e quando usar?

É uma estrutura para tratamento de exceções. Permite capturar erros e tomar ações apropriadas sem quebrar a aplicação.

```python
try:
    resultado = 10 / 0
except ZeroDivisionError as e:
    print(f"Erro: {e}")
    resultado = None
finally:
    print("Sempre executa")
```

**Quando usar**:
- Operações que podem falhar (IO, rede, DB)
- Validações de entrada do usuário
- Conversões de tipos
- **Não usar** para controle de fluxo normal

**Boa prática**: Capturar exceções específicas, não usar `except Exception` genericamente.

---

## 8. Qual a importância de testes unitários e o que eles devem validar?

**Importância**:
- Garantem que código funciona conforme esperado
- Facilitam refatoração
- Servem como documentação viva
- Reduzem bugs em produção

**O que validar**:
- **Casos normais**: Entradas válidas retornam saídas corretas
- **Casos extremos**: Valores limites (vazios, nulos, máximos)
- **Casos de erro**: Validações e exceções esperadas
- **Regras de negócio**: Lógica específica do domínio

```python
def test_calcular_desconto():
    assert calcular_desconto(100, 0.1) == 90
    assert calcular_desconto(0, 0.1) == 0
    with pytest.raises(ValueError):
        calcular_desconto(100, -0.1)
```

Testes devem ser rápidos, isolados e determinísticos.
