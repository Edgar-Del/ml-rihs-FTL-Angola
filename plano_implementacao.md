# PLANO DE IMPLEMENTAÇÃO DO BACKEND

O backend do sistema **Recomendador Inteligente de Hospedagem Sustentável** será responsável por gerir o núcleo lógico e analítico do projecto, integrando a camada de dados, os modelos de machine learning e a interface de comunicação com o frontend e sistemas externos. O seu objectivo é disponibilizar uma API inteligente, escalável e segura, capaz de:

- Processar dados de alojamentos sustentáveis
- Executar inferências com modelos preditivos e de recomendação
- Analisar feedbacks e sentimentos sobre sustentabilidade
- Fornecer recomendações personalizadas via endpoints RESTful
- Monitorar métricas de desempenho, sustentabilidade e uso

## STACK TECNOLÓGICO PRINCIPAL

| CAMADA | TECNOLOGIA | FINALIDADE |
|--------|------------|------------|
| Linguagem principal | Python 3.10+ | Base do desenvolvimento e integração dos módulos |
| Framework Web | FastAPI | Criação da API REST e documentação automática |
| Banco de dados | PostgreSQL + PostGIS | Armazenamento tabular e geoespacial |
| Data Lake | AWS S3 (ou GCP Storage) | Armazenamento bruto e versionamento de datasets |
| Machine Learning | Scikit-learn, XGBoost, MLflow | Treino, rastreamento e versionamento de modelos |
| NLP | HuggingFace Transformers (BERT / DistilBERT) | Análise de sentimentos e feedbacks ecológicos |
| ETL / Orquestração | Apache Airflow | Pipelines automáticos de colecta e actualização de dados |
| Infraestrutura | Docker + Kubernetes | Containerização e orquestração |
| Monitoramento | Prometheus + Grafana | Observabilidade e métricas em produção |

## ESTRUTURA GERAL DO PROJECTO

```
backend/
├── app/
│   ├── main.py                # Ponto de entrada FastAPI
│   ├── config/                # Configurações e variáveis de ambiente
│   │   ├── settings.py
│   │   ├── database.py
│   │   └── s3_client.py
│   ├── api/                   # Rotas e endpoints
│   │   ├── predict.py         # Recomendação e inferência
│   │   ├── feedback.py        # Coleta de feedback dos usuários
│   │   ├── update_data.py     # Atualização de dados e retraining
│   │   └── healthcheck.py     # Status e monitoramento
│   ├── models/                # SQLAlchemy e Pydantic Models
│   ├── ml/                    # Módulos de ML (treino, inferência, NLP)
│   ├── services/              # Lógica de negócios
│   ├── utils/                 # Funções auxiliares e logs
│   └── tests/                 # Testes unitários e integração
│
├── airflow/                   # DAGs de coleta e pré-processamento
│   ├── collect_data.py
│   ├── preprocess_data.py
│   └── update_model.py
│
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
└── README.md
```

## ENDPOINTS PRINCIPAIS DA API

| ENDPOINT | MÉTODO | DESCRIÇÃO | RETORNO |
|----------|--------|-----------|---------|
| `/predict` | POST | Retorna recomendações de hospedagem com base em preferências e localização | Lista de alojamentos sustentáveis recomendados |
| `/update-data` | POST | Actualiza dados de plataformas turísticas (TripAdvisor, Booking, etc.) | Confirmação de actualização e logs |
| `/feedback` | POST | Registra opiniões e avaliações dos usuários | Feedback armazenado e usado para retreinar modelo |
| `/metrics` | GET | Exibe métricas de desempenho e sustentabilidade | KPIs e métricas de monitoramento |

## PLANO FASEADO DE IMPLEMENTAÇÃO

| FASE | PERÍODO | ACTIVIDADES PRINCIPAIS | ENTREGÁVEIS |
|------|---------|------------------------|-------------|
| **Fase 1 – Configuração Inicial** | Semana 1 | Configurar ambiente FastAPI, PostgreSQL, Docker e GitHub | Estrutura inicial funcional do backend |
| **Fase 2 – Integração de Dados** | Semana 2–3 | Criar DAGs no Airflow, conectar APIs e realizar colecta de dados | Pipeline ETL operacional |
| **Fase 3 – Treino e Validação de Modelos** | Semana 4–5 | Pré-processar, treinar e avaliar modelos ML e NLP | Modelos versionados no MLflow |
| **Fase 4 – Desenvolvimento da API** | Semana 6–7 | Implementar endpoints principais e lógica de recomendação | API REST funcional e documentada |
| **Fase 5 – Testes e Integração** | Semana 8 | Integração com frontend (Next.js) e testes unitários | API integrada ao painel interativo |
| **Fase 6 – Deploy e Monitoramento** | Semana 9–10 | Containerização, deploy cloud e monitoramento (Grafana/Prometheus) | Sistema implantado e monitorado |

## CRITÉRIOS TÉCNICOS DE SUCESSO

| MÉTRICA | VALOR ESPERADO | INDICADOR |
|---------|----------------|-----------|
| Tempo de resposta da API | < 2 segundos | Teste de carga e benchmark |
| Precisão do modelo ML | ≥ 80% | Métricas: F1-score e ROC-AUC |
| Disponibilidade do sistema | ≥ 99.5% | Monitoramento em produção |
| Segurança | Autenticação JWT + HTTPS | Conformidade LPDP / GDPR |
| Escalabilidade | Docker + Kubernetes activos | Teste de stress e replicação |

## CONSIDERAÇÕES ÉTICAS E SUSTENTÁVEIS

- Colecta apenas de dados públicos e anonimizados
- Armazenamento e processamento conformes ao GDPR e LPDP Angola
- Eficiência energética digital, priorizando cloud com políticas verdes (AWS Clean Energy Regions)
- IA explicável e transparente (XAI) para reforçar a confiança do utilizador
- Apoio directo aos ODS:
  - **ODS 8**: Promove inovação e empregos verdes no turismo
  - **ODS 12**: Incentiva consumo responsável e escolhas conscientes
  - **ODS 13**: Reduz a pegada de carbono através da valorização de hospedagens sustentáveis

## EM RESUMO...

O backend do **Recomendador Inteligente de Hospedagem Sustentável** representa o núcleo tecnológico da solução, garantindo desempenho, segurança e integração fluida entre os módulos de IA e o ecossistema digital do turismo sustentável.

A sua arquitectura modular e escalável permitirá futuras expansões tais como:
- Novos algoritmos de recomendação híbrida
- Integração com certificações ambientais
- Interoperabilidade com sistemas turísticos nacionais e regionais

---

**Projecto Final - Bootcamp FTL UNDP Angola 2025**  
**Grupo 1**: Arsénio Eurico Muassangue, Edgar Delfino Tchissingui, Francisco Adão Vika Manuel, Raquel de Jesus