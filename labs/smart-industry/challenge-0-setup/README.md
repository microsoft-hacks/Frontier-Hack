# Desafio 0: Crie seu projeto Foundry

Tempo: ~25 minutos

## Objetivos

Ao final deste desafio, você terá:

- ✅ Um recurso e um projeto do Microsoft Foundry criados a partir do portal do Azure
- ✅ Um modelo de chat implantado e testado no playground
- ✅ Application Insights conectado ao seu projeto, pronto para o Desafio 2

![setup](./images/setup.png)

## Pré-requisitos

- Um navegador web moderno
- Uma assinatura do Azure na qual você tenha as funções **Contributor** e **Foundry User**
- O nome da **região** do Azure que o instrutor pediu para você usar (este laboratório utiliza **Sweden Central**)

> [!NOTE]
> Não há nada para instalar. Não clone o repositório, não crie um ambiente virtual nem use um terminal — tudo abaixo acontece no navegador.

---

## Etapa 1 — Criar o recurso Microsoft Foundry

1. Acesse [portal.azure.com](https://portal.azure.com) e faça login.
2. Na caixa de pesquisa superior, digite **Azure AI Foundry** e selecione-o nos resultados de **Services**.
3. Selecione **+ Create** e, em seguida, **Azure AI Foundry**.
4. Preencha a aba **Basics**:

   | Campo | Valor |
   |---|---|
   | **Subscription** | A assinatura designada pelo instrutor |
   | **Resource group** | Selecione **Create new** e nomeie como `rg-hack-dev-<suffix>` |
   | **Region** | **Sweden Central** (ou a região informada pelo instrutor) |
   | **Name** | `foundry-hack-dev-<suffix>` — deve ser globalmente único |
   | **Project name** | `prj-hack-dev-<suffix>` |

5. Deixe as demais abas com os valores padrão. Selecione **Review + create** e depois **Create**.
6. Aguarde a mensagem **Your deployment is complete** e selecione **Go to resource**.

> [!TIP]
> Use nomes curtos, em minúsculas e sem espaços. Se o portal indicar que o nome já está em uso, adicione um número ao final.

Seu grupo de recursos deve ficar parecido com isto:

![Azure Portal Resources](./images/azure-portal-resources.png)

> [!NOTE]
> Os prefixos dos nomes de recursos variam de acordo com o cenário, e os sufixos são únicos para cada implantação. Sua lista não será exatamente igual.

---

## Etapa 2 — Abrir o projeto no portal do Foundry

1. Acesse [ai.azure.com/nextgen](https://ai.azure.com/nextgen) e faça login com a mesma conta.
2. Se você não for direcionado automaticamente ao seu projeto, use o seletor de projetos no canto superior direito e selecione **prj-hack-dev-<suffix>**.

![Foundry Project](./images/foundry-project.png)

Mantenha esta aba aberta — você usará ela durante todo o restante do laboratório.

---

## Etapa 3 — Implantar um modelo

1. Na navegação superior, selecione **Build** e depois **Models** na barra lateral esquerda.

   > [!NOTE]
   > Em algumas versões do portal do Foundry, a aba **Models** é chamada de **Deployments**. Ambas têm a mesma finalidade.

2. Selecione **+ Deploy model** → **Deploy base model**.
![Foundry Model](./images/foundry-model.png)
3. Procure por um modelo de chat — este laboratório foi escrito para o **gpt-5.4**. Se ele não estiver disponível na sua região, escolha o modelo GPT de chat mais recente aprovado pelo instrutor.
![Foundry Model](./images/foundry-model-2.png)
4. Selecione o modelo
5. Clicar **Deploy** >> **Custom Settings**
- **Tokens per Minute Rate Limit** = 100 
- **Deployment Type** = Global Standard
- clicar **Deploy**.

![Foundry Model Deploy](./images/foundry-model-deploy.png)

---

## Etapa 4 — Testar o modelo no playground

1. Selecione sua implantação e depois **Open in playground**.
2. Digite uma mensagem simples, por exemplo:

   ```text
   Você é o assistente de manutenção e operação da Linha A da plataforma Smart Industry. Explique o funcionamento das máquinas (CNC, robôs, esteiras, empilhadeiras, injetoras, prensa e solda), interprete alarmes de temperatura/vibração e recomende ajustes de parâmetros e manutenção. Use somente os valores do contexto em tempo real enviado em cada execução; nunca invente leituras. Responda em português, de forma objetiva, citando o código da máquina.
   ```

3. Envie e confirme que você recebeu uma resposta.

![Foundry Model Playground](./images/foundry-model-playground.png)

Se ocorrer um erro aqui, pare e corrija antes de continuar — todos os desafios seguintes dependem de uma implantação de modelo funcional.

## Critérios de sucesso

- [ ] Seu grupo de recursos no portal do Azure contém um recurso Microsoft Foundry
- [ ] Você consegue abrir **prj-hack-dev-<suffix>** em [ai.azure.com/nextgen](https://ai.azure.com/nextgen)
- [ ] Sua implantação de modelo mostra o status **Succeeded**
- [ ] Você recebeu uma resposta no playground do modelo
- [ ] **Observability → Tracing** mostra um recurso Application Insights conectado, e não o banner de conexão

Próximo: [Desafio 1 — Construir agentes](../challenge-1-build/README.md)
