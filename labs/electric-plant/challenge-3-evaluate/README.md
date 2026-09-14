# Challenge 3: Avaliar a qualidade das respostas

Tempo: ~30 minutos

## Objetivos
- ✅ Executar uma avaliação de qualidade com 10 casos e identificar uma melhoria concreta

## Contexto
O monitoramento pode mostrar uma resposta rápida e sem erros que ainda assim está errada. Por exemplo, recomendar monitoramento de rotina para o XFR-401 em 300 ms pareceria operacionalmente saudável, mas deixaria de perceber uma falha combinada sensível à segurança. A avaliação mede a corretude em relação aos resultados esperados — aqui, os casos esperam que o advisor aja e **cite a fonte da base de conhecimento** para cada recomendação (`eval_portal.jsonl` usa `query`/`ground_truth`).

## Primeiros passos

1. No Foundry, abra o projeto e depois **Build** → **Evaluations** → **Create**.
2. Selecione **Agent** como alvo e escolha `maintenance-efficiency-advisor-agent`.
3. Escolha **Individual turns** e **Existing dataset**.
4. Nomeie o dataset `electric-plant-10-cases` primeiro e depois envie `challenge-3-evaluate/eval_portal.jsonl`. O envio permanece desabilitado até o dataset ter um nome.
5. Mantenha o mapeamento padrão de `input` para entrada e `expected` para o resultado esperado, a menos que o assistente solicite um mapeamento explícito.
6. Mantenha apenas os avaliadores de qualidade relevantes, como groundedness, relevance, coherence e similarity. Desmarque tool-call accuracy: a busca do advisor é resolvida pelo serviço e as funções locais não são executadas nesse caminho de avaliação, então esse avaliador adiciona latência e pontuações ruins enganosas.
7. Envie e aguarde até as 10 linhas terminarem.
8. Registre as pontuações agregadas produzidas pela sua execução. Ordene as linhas pela menor pontuação, leia input, resultado esperado, saída e a justificativa do avaliador e, em seguida, anote uma melhoria específica de instrução. Não presuma uma pontuação-alvo.

## Critérios de sucesso
- [ ] Todas as 10 linhas terminam
- [ ] As pontuações agregadas e por linha são legíveis
- [ ] Você identifica uma melhoria concreta na linha com a menor pontuação

Próximo: [Challenge 4 - Workflow](../challenge-4-workflow/README.md)