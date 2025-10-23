# Recomendador Inteligente de Hospedagem Sustentável

## Visão Geral

Plataforma digital baseada em **Inteligência Artificial e Machine Learning** que identifica, classifica e recomenda hospedagens sustentáveis em Angola, promovendo práticas ecológicas, consumo responsável e turismo consciente.

Este projecto alinha-se aos Objectivos de Desenvolvimento Sustentável (ODS):
- **ODS 8**: Trabalho Decente e Crescimento Económico
- **ODS 12**: Consumo e Produção Responsáveis
- **ODS 13**: Acção Climática

---

## Problema e Oportunidade

Alojamentos sustentáveis em Angola — pousadas, lodges e quintas ecológicas com práticas responsáveis — permanecem **invisíveis** nas plataformas digitais internacionais. Viajantes conscientes não conseguem identificar facilmente opções verdes, enquanto empreendedores comprometidos com a sustentabilidade têm pouca visibilidade e reconhecimento.

O RECOMENDADOR resolve essa lacuna ao integrar sustentabilidade, inovação e desenvolvimento local num único ecossistema digital.

---

## Principais Funcionalidades

- **Classificação Inteligente**: Algoritmos de ML analisam indicadores ambientais, sociais e económicos
- **EcoScore**: Atribui pontuação de 0 a 100 para cada alojamento baseada em sustentabilidade
- **Recomendações Personalizadas**: Combina preferências do viajante com atributos de sustentabilidade
- **Análise de Sentimentos (NLP)**: Extrai insights sobre práticas verdes de comentários online
- **Visualização Interativa**: Mapas ecológicos e dashboards educativos
- **Transparência**: Explicações claras sobre por que cada alojamento é recomendado

---

## Stack Tecnológico

### Backend & Machine Learning
- **Python** com Pandas, NumPy, Scikit-learn, XGBoost
- **NLP**: BERT, DistilBERT (HuggingFace Transformers)
- **FastAPI**: Serviço de inferência REST
- **MLflow**: Tracking de experimentos e model registry
- **Apache Airflow**: Orquestração de pipelines ETL

### Armazenamento & Dados
- **PostgreSQL + PostGIS**: Dados tabulares e geoespaciais
- **AWS S3 / MongoDB**: Data Lake para dados não estruturados
- **DVC**: Versionamento de datasets

### Frontend & Visualização
- **Next.js + React**: Interface responsiva
- **TailwindCSS**: Estilização
- **Mapbox GL JS**: Visualização geoespacial
- **Chart.js / Recharts**: Gráficos interativos

### Infraestrutura
- **Docker**: Contêinerização
- **Kubernetes (EKS/GKE)**: Orquestração em produção
- **Prometheus + Grafana**: Monitoramento
- **GitHub Actions**: CI/CD

---

## Arquitetura

```
┌─────────────────┐
│   Colecta de    │
│     Dados       │
│ (APIs, Scraping)│
└────────┬────────┘
         │
         ↓
┌─────────────────────────────┐
│   Armazenamento & ETL       │
│ (PostgreSQL, S3, Airflow)   │
└────────┬────────────────────┘
         │
         ↓
┌─────────────────────────────┐
│  Pré-processamento &        │
│  Feature Engineering        │
└────────┬────────────────────┘
         │
         ↓
┌─────────────────────────────┐
│  Machine Learning Models    │
│ (RF, XGBoost, LR + NLP)    │
└────────┬────────────────────┘
         │
         ↓
┌─────────────────────────────┐
│  API FastAPI                │
│  (/predict, /feedback)      │
└────────┬────────────────────┘
         │
         ↓
┌─────────────────────────────┐
│  Frontend (Next.js)         │
│  Dashboards & Mapa          │
└─────────────────────────────┘
```

---

## Fontes de Dados

### Primárias
- **TripAdvisor**: Avaliações textuais e ratings
- **Booking.com**: Dados estruturados de localização e comodidades
- **EcoBnb**: Base de alojamentos sustentáveis
- **GreenHotelWorld / Green Key**: Dados de certificações verdes

### Secundárias
- **Kaggle**: Datasets de hotelaria e turismo
- **UNWTO**: Indicadores macro de turismo
- **OpenStreetMap**: Dados geoespaciais
- **ERA5 / Climate Data Store**: Variáveis climáticas

---

## Variáveis Principais

| Variável | Descrição | Fonte |
|----------|-----------|-------|
| Pegada de Carbono (kg CO₂/noite) | Estimativa de emissões por hóspede | EcoBnb, cálculos próprios |
| % Energia Renovável | Percentagem de energia limpa utilizada | Booking, EcoBnb |
| Política de Reciclagem | Sim/Não/Parcial | TripAdvisor, GreenHotelWorld |
| Sentimento Ambiental | Score NLP de comentários | NLP analysis |
| Localização | Coordenadas e proximidade a parques | OSM |
| Preço Médio/Noite | Valor normalizado | Booking |
| **EcoScore** | Índice composto final (0-100) | Ponderação múltipla |

---

## Modelos de Machine Learning

### Abordagem Supervisionada
- **Random Forest**: Baseline robusto e interpretável
- **XGBoost**: Modelo de alta performance em dados tabulares
- **Logistic Regression**: Baseline simples para comparação

### Avaliação
- **Métricas**: Precision@k, Recall@k, NDCG, ROC-AUC, F1-score
- **Validação**: Time-aware split (80/20), k-fold stratificado
- **Tuning**: Optuna (busca bayesiana) + GridSearchCV
- **Explicabilidade**: SHAP, LIME

---

## Impacto Esperado

### Social
- Fomentar consciência ecológica entre turistas
- Valorizar empreendimentos locais sustentáveis
- Criar empregos verdes e decentes

### Económico
- Aumentar procura por hospedagens sustentáveis
- Impulsionar micro e pequenas empresas
- Diversificar economia através do turismo verde

### Ambiental
- Reduzir pegada de carbono do turismo
- Estimular eficiência energética e reciclagem
- Preservar ecossistemas locais

---

## Próximos Passos

1. **Colecta piloto de dados** em províncias-chave (Namibe, Benguela, Huíla)
2. **Validação empírica** com alojamentos e turistas reais
3. **Parcerias** com Ministério da Cultura e Turismo
4. **Desenvolvimento de versão open source** para reutilização em África
5. **Escalabilidade** para outros países da África Austral

---

## Contribuição

Para contribuir, abra uma issue ou pull request. Respeite as boas práticas de desenvolvimento (commits descritivos, testes, documentação).

## Contacto

**Grupo 1 - Bootcamp FTL UNDP Angola 2025**

Membros:
- Arsénio Eurico Muassangue
- Edgar Delfino Tchissingui
- Francisco Adão Vika Manuel
- Raquel de Jesus

---

## Referências

- UNWTO. (2023). Tourism for Development
- UNDP. (2022). Tourism and Sustainable Development Goals
- UNEP. (2021). Making Tourism More Sustainable