# Smart Electric (SDK)

Smart Electric é referência global em motores, geradores, transformadores e controles elétricos, com oferta ampla e integrada para eletrificação, automação e digitalização — a empresa busca ser reconhecida globalmente como marca de referência em máquinas elétricas, entregando soluções completas e eficientes e construindo relacionamentos fortes com os clientes. A Smart Electric opera o Complexo Industrial Serrana. Cinco ativos reportam vibração, temperatura do enrolamento, carga de corrente e eficiência operacional. Seu objetivo é construir um classificador baseado em ferramentas e um advisor de manutenção ancorado em uma base de conhecimento técnico (RAG via Azure AI Search), observar e avaliar ambos e, em seguida, orquestrar a passagem de dados entre eles. Cada recomendação do advisor deve citar a fonte recuperada.

| Ativo | Nome | Status | Problema atual |
|---|---|---|---|
| MOTOR-201 | Motor de Linha de Bobinagem de Estator (Média Tensão) | ✅ normal | Nenhum |
| GEN-301 | Bomba de Resfriamento do Turbogerador | ⚠️ aviso | Vibração acima do máximo específico do ativo |
| XFR-401 | Ventilador de Resfriamento do Transformador de Potência (138/13,8 kV) | 🔴 crítico | Falha combinada de vibração e temperatura; desligamento controlado e escalonamento necessários |
| DRIVE-101 | Acionamento do Sistema de Excitação Estática | ✅ normal | Nenhum |
| VFD-501 | Motor de Transportador com Inversor de Frequência | ⚠️ aviso | Eficiência abaixo do mínimo específico do ativo |

As leituras e limites canônicos estão em [`api-data/data/api_data.json`](api-data/data/api_data.json).

| Challenge | Tempo | Resultado |
|---|---:|---|
| [0 - Setup](challenge-0-setup/README.md) | 20 min | Provisionamento e verificação do Foundry |
| [1 - Build](challenge-1-build/README.md) | 35 min | Criação dos dois agentes, anexação de uma ferramenta de função e do Azure AI Search (RAG) |
| [2 - Monitor](challenge-2-monitor/README.md) | 20 min | Inspeção de traces e telemetria operacional |
| [3 - Evaluation](challenge-3-evaluate/README.md) | 30 min | Avaliação de 10 casos de qualidade |
| [4 - Workflow](challenge-4-workflow/README.md) | 25 min | Execução da orquestração classificador → advisor |

Comece pelo [Challenge 0](challenge-0-setup/README.md).
