---
id: cbm
title: Manutenção baseada em condição (CBM)
category: metodologia
---

# Manutenção baseada em condição

## Princípio geral
A manutenção baseada em condição (condition-based maintenance, CBM) recomenda intervenções a partir do estado operacional do ativo, e não de um calendário fixo. Três estados são reconhecidos: **normal**, **alerta/aviso** e **crítico**.

## Estados operacionais
- **Normal**: nenhuma métrica viola o limite específico do ativo. Mantenha o monitoramento rotineiro no ciclo definido pelo plano de manutenção.
- **Aviso**: pelo menos uma métrica viola o limite. Programe inspeção ou manutenção no próximo ciclo de produção, sem interromper a operação.
- **Crítico**: falha composta ou violação grave e simultânea em mais de uma métrica. Exija interrupção controlada, isolamento e escalonamento imediato.

## Boas práticas
- Cada recomendação deve indicar urgência, evidência que a justifica e a fonte técnica usada.
- Ordens de manutenção devem ser registradas e priorizadas pela criticidade do ativo (sistema CMMS).
- Metas prioritárias: reduzir paradas não planejadas, otimizar ações de reparo e acelerar a decisão da equipe de operação e manutenção.
- Não invente evidências: toda ação deve derivar de leitura registrada ou de diagnóstico recuperado.