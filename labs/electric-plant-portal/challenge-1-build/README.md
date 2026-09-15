# Challenge 1: Construir agentes no portal

Tempo: ~35 minutos

## Objetivos
- ✅ Criar duas definições exatas de agentes e anexar uma ferramenta de dados OpenAPI ao classificador

## Contexto
Um agente combina um modelo, instruções e ferramentas opcionais. Uma **função** executa código de aplicação; **OpenAPI** chama uma API HTTP descrita; **Azure AI Search** recupera conteúdo corporativo indexado; **Code Interpreter** calcula e analisa arquivos; **File Search** recupera de arquivos enviados. O modelo decide chamar uma ferramenta apenas pelo **nome e descrição** dela, portanto descrições vagas são o motivo mais comum de uma ferramenta ser ignorada.

O facilitador deve fornecer uma URL de API industrial implantada. O `openapi.json` contém `https://YOUR-API-HOST.example.com`, que é um placeholder, não um deployment real. Confirme se a URL fornecida responde antes de anexá-la.

## Primeiros passos

1. Substitua o placeholder `servers[0].url` em `labs/electric-plant-portal/challenge-1-build/openapi.json` pela URL base HTTPS confirmada pelo facilitador. Verifique-a no navegador abrindo `<url-confirmada>/assets/XFR-401/condition`; o JSON contendo XFR-401 deve aparecer. Se não aparecer, pare e peça ao facilitador para confirmar o endpoint. Os participantes não implantam nem escrevem código de API.
2. No Foundry, abra o projeto e depois **Build** → **Agents** → **+ New agent**. Selecione o modelo implantado no Challenge 0 e use este nome exato:

   ```text
   electric-plant-1-classifier-agent
   ```

3. Cole estas instruções completas:

   ```text
   ## Propósito
   -  Você é um assistente de IA para a Smart Electric, referência global em motores, geradores, transformadores e controles elétricos com oferta integrada para eletrificação, automação e digitalização, que ajuda o usuário a classificar as condições dos ativos.

   ## Contexto
   Tente carregar os dados por meio das ferramentas ou use os limites padrão =
   - vibração: 0-4,0 mm/s RMS
   - temperatura do enrolamento: 20-85 °C
   - carga de corrente: 25-90 %
   - eficiência operacional: 90-100 %.

   ## Formato de Saída
   - SOMENTE a tabela de resumo da classificação
   - linhas = para cada ativo.
   - colunas = para cada métrica
   - use 🔴 para crítico, ⚠️ para alto, e ✅ para baixo.
   - adicione uma coluna de prioridade com base na classificação das métricas

   ## Escopo
   - Antes de responder, verifique se a solicitação está relacionada a este Propósito.
   - Se estiver no escopo: continue a conversa.
   - Se estiver fora do escopo: não responda ao conteúdo da solicitação. Apenas explique o seu propósito

   ## Guardrails
   - Não crie dados de clientes.
   - Não recomende nada
   - Se faltarem dados-chave, faça perguntas de acompanhamento precisas.
   ```

4. Salve. Selecione **Tools** → **+ Add** → **OpenAPI**. Escolha **Upload file**, selecione `labs/electric-plant-portal/challenge-1-build/openapi.json`, use autenticação **Anonymous** e confirme que a operação importada é exatamente `get_asset_condition`. Salve a ferramenta.
5. Crie outro agente com o mesmo modelo implantado e o nome exato:

   ```text
   maintenance-efficiency-advisor-agent
   ```

6. Cole estas instruções e salve. Não anexe ferramenta.

   ```text
   ## Propósito
   Transformar os achados estruturados de um classificador em ações de manutenção, urgência e orientações de escalonamento para a Smart Electric.

   ## Formato de Saída
   Para cada ativo, retorne Status, Urgência, Evidências recebidas, Ação recomendada e Escalonamento. Use exatamente: 🔴 crítico, ⚠️ aviso, ✅ normal.

   ## Escopo
   Use apenas os achados do classificador fornecidos na solicitação. Para falhas combinadas de vibração e temperatura do enrolamento, exija desligamento controlado, isolamento conforme o procedimento do local e escalonamento imediato de segurança/manutenção. Para avisos, recomende inspeção ou manutenção planejada. Para ativos normais, continue o monitoramento.

   ## Guardrails
   Não invente, altere ou reclassifique leituras ou limites. Não afirme que um desligamento ocorreu. Preserve a incerteza e direcione o pessoal aos procedimentos de segurança aprovados no local.
   ```

7. Teste o classificador:

   ```text
   Chame get_asset_condition para MOTOR-201, GEN-301, XFR-401, DRIVE-101 e VFD-501. Classifique cada resultado usando os limites de cada ativo.
   ```

   Esperado: exatamente 2 ✅ normal, 2 ⚠️ aviso e 1 🔴 crítico; as evidências do XFR-401 incluem vibração 7,6 acima de 4,5 e temperatura 112 acima de 90. Expanda os detalhes das chamadas de ferramenta para inspecionar cada solicitação e resposta.

8. Teste o advisor:

   ```text
   Achado do classificador: XFR-401 está crítico porque a vibração 7,6 excede 4,5 mm/s RMS e a temperatura do enrolamento 112 excede 90 C. Dê urgência, ação e escalonamento.
   ```

   Esperado: desligamento controlado conforme o procedimento do local e escalonamento imediato de segurança/manutenção, sem leituras inventadas.

Se o classificador pedir leituras em vez de chamar a ferramenta, a descrição da ferramenta está vaga demais, o placeholder não foi substituído ou o endpoint está inacessível.

## Critérios de sucesso
- [ ] Os dois nomes exatos dos agentes existem
- [ ] O classificador chama apenas `get_asset_condition` e retorna apenas uma tabela
- [ ] A distribuição é 2 normal, 2 aviso, 1 crítico
- [ ] O advisor não tem ferramenta e não inventa leituras

Próximo: [Challenge 2 - Monitor](../challenge-2-monitor/README.md)