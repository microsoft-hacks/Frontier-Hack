# Challenge 2: Monitorar a execução dos agentes

Tempo: ~20 minutos

## Objetivos
- ✅ Produzir e inspecionar um trace completo no Foundry e no Application Insights

## Contexto
O monitoramento responde **está executando?** por meio de spans, latência, tokens, erros e custo. Ele não responde se uma classificação ou recomendação está correta; o Challenge 3 trata disso.

## Primeiros passos

1. Confirme que o `.env` inclui `PROJECT_CONNECTION_STRING`, `APPLICATIONINSIGHTS_CONNECTION_STRING`, `AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true` e `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true`:

   ```powershell
   Get-Content .env | Select-String 'PROJECT_CONNECTION_STRING|APPLICATIONINSIGHTS_CONNECTION_STRING|AZURE_EXPERIMENTAL|OTEL_INSTRUMENTATION'
   ```

2. No Foundry, abra **Observability** → **Tracing**. Se um banner de conexão aparecer, selecione **Connect Application Insights**, escolha a instância no grupo de recursos do laboratório e salve uma vez.
3. Execute o script de rastreamento. Ele habilita a instrumentação antes de criar o `AIProjectClient`, verifica se o Challenge 1 criou o `electric-plant-1-classifier-agent`, chama `get_asset_condition` para XFR-401 e exclui a conversa temporária.

   ```powershell
   Set-Location labs/electric-plant
   python challenge-2-monitor/monitor.py
   ```

   Resultado esperado no terminal: uma classificação crítica para XFR-401 com evidências de vibração e temperatura do enrolamento.

4. No **Tracing** do Foundry, abra a conversa mais recente. Expanda os spans e inspecione o conteúdo completo das mensagens, o span do modelo, as contagens de tokens, a latência e o status. Para spans de chamadas de ferramenta, inspecione os argumentos e a saída.
5. Abra o `electric-plant-1-classifier-agent`, selecione o painel **Monitor** e localize execuções de agentes, uso de tokens e custo estimado.
6. No portal do Azure, abra Application Insights → **Transaction search**, selecione a transação completa recente e revise o painel de agentes com execuções, erros, chamadas de ferramenta, modelos e consumo de tokens.

## Critérios de sucesso
- [ ] Pelo menos um trace está visível no Foundry e no Application Insights
- [ ] Você consegue identificar spans, tokens, latência, mensagens e detalhes de chamadas de ferramenta
- [ ] Você consegue explicar onde investigar uma execução com falha ou lenta

Próximo: [Challenge 3 - Evaluation](../challenge-3-evaluate/README.md)