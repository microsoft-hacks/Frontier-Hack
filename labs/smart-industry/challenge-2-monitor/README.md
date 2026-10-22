# Challenge 2: Monitorar no Foundry

Tempo: ~20 minutos

## Objetivos
- ✅ Gerar e inspecionar traces no Foundry e no Application Insights sem código

## Contexto
O monitoramento responde **está executando?** Ele expõe spans, chamadas de ferramenta, latência, tokens, erros e custo, mas não prova que a resposta está correta.

## Primeiros passos

1. Abra o `.env` copiado e confirme que ele contém `PROJECT_CONNECTION_STRING`, `APPLICATIONINSIGHTS_CONNECTION_STRING`, `AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true` e `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true`.
2. No Foundry, abra **Observability** → **Tracing**. Se um banner de conexão aparecer, selecione **Connect Application Insights**, escolha a instância no grupo de recursos do laboratório e salve esta conexão única.
3. Abra o `electric-plant-1-classifier-agent` no playground e execute:

   ```text
   Chame get_asset_condition para XFR-401 e classifique-o. Retorne apenas a tabela exigida.
   ```

   Esperado: uma linha 🔴 crítico e uma chamada `get_asset_condition` visível.

4. Volte a **Observability** → **Tracing**, abra a conversa mais recente e inspecione o span raiz, o span do modelo, a chamada de ferramenta OpenAPI, a solicitação/resposta, o conteúdo completo das mensagens, os tokens, a latência e o status.
5. Abra o painel **Monitor** do agente e leia execuções de agentes, uso de tokens e custo estimado.
6. No portal do Azure, abra Application Insights → **Transaction search**, escolha a transação completa recente e revise o painel de agentes com execuções, erros, chamadas de ferramenta, modelos e consumo de tokens.

## Critérios de sucesso
- [ ] Pelo menos um trace aparece no Foundry e no Application Insights
- [ ] A solicitação e a resposta do OpenAPI estão visíveis
- [ ] Você consegue explicar onde investigar erros, latência e comportamento inesperado de ferramentas

Próximo: [Challenge 3 - Evaluation](../challenge-3-evaluate/README.md)