# Respostas - Questões Frontend

## 1. O que é o DOM e como ele funciona?

O DOM é a representação em árvore do HTML que o navegador cria, cada tag vira um objeto que eu posso manipular com JavaScript usando métodos como `getElementById` ou `querySelector`. É a ponte entre o HTML e o JS.

## 2. Explique a diferença entre == e === no JavaScript.

O `==` compara valores convertendo tipos automaticamente, tipo `"1" == 1` é `true`. Já o `===` compara valor e tipo, então `"1" === 1` é `false`.

## 3. O que é o conceito de estado (state) em aplicações front-end?

Estado são os dados que a aplicação precisa lembrar e que podem mudar. Quando o estado muda, a interface atualiza. Normalmente, uso `useState` pra gerenciar isso, e o componente re-renderiza automaticamente.

## 4. Explique como funciona o CSS Box Model.

É como o navegador calcula o espaço de um elemento: conteúdo, padding, border e margin. Por padrão, `width` só conta o conteúdo.

## 5. O que são promessas (Promises) no JavaScript e como funcionam?

Promises representam operações assíncronas. Têm três estados: pending, fulfilled ou rejected. Uso principalmente pra chamadas de API com `.then()` e `.catch()`, mas hoje prefiro `async/await` que deixa o código mais limpo.

## 6. Explique a diferença entre componentes funcionais e de classe.

Componentes de classe usavam `this.state` e métodos de ciclo de vida. Funcionais são funções que retornam JSX. Hoje só uso funcionais, são mais simples e diretos.

## 7. O que é um Hook? Cite pelo menos 3 e explique seus usos.

Hooks são funções que permitem usar recursos do React em componentes funcionais:

- **useState**: gerencia estado local
- **useEffect**: executa efeitos colaterais como chamadas de API
- **useContext**: acessa valores de contexto sem prop drilling

Também uso `useRef`, `useMemo` e `useCallback` quando preciso.

## 8. Por que a chave (key) é importante em listas no React?

A key ajuda o React a identificar qual item mudou, foi adicionado ou removido. Uso um ID único como key, nunca o índice do array. Sem isso, o React pode perder estado ou renderizar errado.

## 9. O que é lifting state up?

É mover o estado pra um componente pai quando vários filhos precisam compartilhar o mesmo dado, mantenho uma única fonte de verdade, se ficar muito aninhado, uso Context ou gerenciador de estado.

## 10. Explique como funciona o useEffect e dê exemplos de dependências.

O `useEffect` executa após a renderização. O array de dependências controla quando ele roda:

```javascript
useEffect(() => {
  fetchData();
}, []);

useEffect(() => {
  fetchUserData(userId);
}, [userId]);

useEffect(() => {
  const sub = subscribe();
  return () => sub.unsubscribe();
}, []);
```

Se uso uma variável no efeito, ela deve estar nas dependências, mas devemos tomar cuidado para não gerar loops.
