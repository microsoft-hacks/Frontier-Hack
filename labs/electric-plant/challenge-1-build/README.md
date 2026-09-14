# Challenge 1: Construir agentes baseados em ferramentas

Tempo: ~35 minutos

## Objetivos
- ✅ Criar o classificador com exatamente uma ferramenta de função anexada e o advisor com o Azure AI Search tool (RAG) para fundamentar cada recomendação

## Contexto
Um agente combina um modelo, instruções e ferramentas opcionais. Uma **função** executa código local; **Azure AI Search** recupera conteúdo corporativo indexado para ancorar respostas na base de conhecimento (RAG). O modelo decide se deve chamar uma ferramenta apenas pelo **nome e descrição** dela, portanto uma descrição vaga é o motivo mais comum para uma ferramenta ser ignorada.

O classificador obtém evidências e nunca recomenda ações. O advisor consulta a base de conhecimento, cita a fonte de cada procedimento e nunca inventa leituras ou técnicas.

> **Pré-requisitos deste desafio**: o índice `electric-plant-maintenance` e a conexão `search-hack-shared` devem existir no projeto. Os organizadores provisionam tudo em `scripts/deploy-search-electric-plant.ps1` antes do workshop (cria o Azure AI Search compartilhado e faz o upload da base). Se a conexão não existir, consulte o facilitador.

## Primeiros passos

1. Abra `agents.py`. Ele define `get_asset_condition(asset_id)` e um `FunctionTool` com o mesmo nome, anexa essa ferramenta ao `electric-plant-1-classifier-agent` e cria o `maintenance-efficiency-advisor-agent` com o Azure AI Search tool sobre o índice `electric-plant-maintenance`.
2. Pela raiz do repositório, execute:

   ```powershell
   Set-Location labs/electric-plant
   python challenge-1-build/agents.py
   ```

   A saída esperada nomeia as duas versões criadas dos agentes, informa que o classificador tem `get_asset_condition` e o advisor tem o Azure AI Search tool sobre `electric-plant-maintenance`, e imprime uma classificação de XFR-401 contendo 🔴 crítico com evidências de vibração e temperatura do enrolamento.

3. No Foundry, abra **Build** → **Agents**. Confirme que os dois nomes exatos existem:

   ```text
   electric-plant-1-classifier-agent
   maintenance-efficiency-advisor-agent
   ```

4. Teste a classificação inline no playground do classificador:

   ```text
   Classifique este ativo usando as leituras fornecidas: MOTOR-201, vibração 2,4 mm/s RMS (0-4,0), temperatura do enrolamento 68 C (20-85), carga de corrente 72 % (25-90), eficiência operacional 94 por cento (90-100).
   ```

   Esperado: uma linha de tabela marcada como ✅ normal, quatro leituras dentro da faixa e nenhuma recomendação.

5. Force a ferramenta de dados:

   ```text
   Chame get_asset_condition para MOTOR-201, GEN-301, XFR-401, DRIVE-101 e VFD-501. Classifique cada resultado usando os limites de cada ativo.
   ```

   Esperado: 2 ✅ normal, 2 ⚠️ aviso e 1 🔴 crítico. Expanda cada evento `get_asset_condition` nos detalhes da execução e inspecione a solicitação `asset_id` e a resposta JSON.

6. Teste o advisor com contexto comprovado:

   ```text
   Achado do classificador: XFR-401 está crítico porque a vibração 7,6 excede 4,5 mm/s RMS e a temperatura do enrolamento 112 excede 90 C. Dê urgência, ação e escalonamento.
   ```

   Esperado: desligamento controlado imediato e escalonamento de segurança/manutenção, com citação da base de conhecimento para cada ação, sem novas leituras.

## Critérios de sucesso
- [ ] Os dois nomes exatos dos agentes existem
- [ ] O classificador chama sua única ferramenta e retorna apenas uma tabela de classificação
- [ ] A distribuição do resultado é 2 normal, 2 aviso, 1 crítico
- [ ] O advisor cita a base de conhecimento (RAG) e nunca inventa procedimentos ou leituras

Próximo: [Challenge 2 - Monitor](../challenge-2-monitor/README.md)