# Challenge 3: Avaliar a qualidade das respostas

Tempo: ~30 minutos

## Objetivos
- ✅ Completar uma avaliação de 10 linhas no portal e encontrar uma melhoria de qualidade

## Contexto
O monitoramento pode mostrar uma resposta rápida e sem erros que está errada. Uma recomendação de monitoramento de rotina para o XFR-401 poderia ter baixa latência e zero erros HTTP enquanto deixa de perceber sua falha combinada sensível à segurança. A avaliação compara a qualidade da resposta com expectativas fundamentadas.

## Primeiros passos

1. No Foundry, abra o projeto e depois **Build** → **Evaluations** → **Create**.
2. Selecione **Agent** e escolha `maintenance-efficiency-advisor-agent`.
3. Escolha **Individual turns** e **Existing dataset**.
4. Nomeie o dataset `electric-plant-portal-10-cases` antes de enviar `labs/electric-plant-portal/challenge-3-evaluate/eval_portal.jsonl`; o envio permanece desabilitado até existir um nome.
5. Mantenha o mapeamento dos campos `input` e `expected`, a menos que o assistente peça para defini-lo.
6. Mantenha apenas os avaliadores de qualidade necessários para o laboratório, como groundedness, relevance, coherence e similarity. Desmarque tool-call accuracy porque este advisor não tem ferramenta; marcá-lo adiciona latência e produz uma pontuação ruim irrelevante.
7. Envie e aguarde as 10 linhas terminarem.
8. Registre as pontuações agregadas da sua execução. Ordene os resultados por linha pela menor pontuação, inspecione a justificativa dos avaliadores e registre uma melhoria concreta de instrução. Não há pontuação esperada predefinida.

## Critérios de sucesso
- [ ] Todas as 10 linhas terminam
- [ ] As pontuações agregadas e por linha são legíveis
- [ ] Você identifica uma melhoria concreta em um caso com pontuação baixa

Próximo: [Challenge 4 - Workflow](../challenge-4-workflow/README.md)