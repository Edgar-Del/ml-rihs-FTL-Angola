# Como Testar o Endpoint `/predict`

Este guia mostra diferentes formas de testar o endpoint `/predict` da API.

## Pré-requisitos

1. **API rodando**: Certifique-se de que a API está em execução
   ```bash
   source venv/bin/activate
   uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
   ```

2. **API_KEY configurada**: Verifique seu `.env` ou variáveis de ambiente
   ```bash
   # No .env
   API_KEY=test-api-key
   ```

## Método 1: Usando o Script Python (Recomendado)

Execute o script de teste automatizado:

```bash
python3 test_predict_endpoint.py
```

Este script:
- Verifica se a API está rodando
- Testa sem API key (deve falhar)
- Testa com API key (deve funcionar)
- Mostra resultados detalhados

## Método 2: Usando cURL

### Teste básico com API key:

```bash
curl -X POST "http://localhost:8080/predict" \
  -H "X-API-KEY: test-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "price_per_night_usd": 150.0,
    "rating": 4.5,
    "avaliação_clientes": 4.2,
    "distância_do_centro_km": 5.0,
    "energia_renovável": 75.0,
    "gestão_resíduos_índice": 80.0,
    "consumo_água_por_hóspede": 200.0,
    "carbon_footprint_score": 60.0,
    "reciclagem_score": 70.0,
    "energia_limpa_score": 75.0,
    "water_usage_index": 30.0,
    "sustainability_index": 65.0,
    "eco_impact_index": 68.0,
    "eco_value_ratio": 0.43,
    "sentimento_score": 0.5,
    "eco_keyword_count": 3,
    "região_encoded": 2,
    "possui_selo_sustentável_encoded": 1,
    "sentimento_sustentabilidade_encoded": 1,
    "price_sust_ratio": 0.43,
    "eco_value_score": 43.0,
    "total_sust_score": 65.0,
    "price_category": 2,
    "water_consumption_ratio": 0.30
  }'
```

### Teste sem API key (deve retornar erro):

```bash
curl -X POST "http://localhost:8080/predict" \
  -H "Content-Type: application/json" \
  -d '{"price_per_night_usd": 150.0, "rating": 4.5}'
```

## Método 3: Usando Swagger UI (Interface Web)

1. Abra o navegador em: `http://localhost:8080/docs`

2. Expanda o endpoint `POST /predict`

3. Clique em "Try it out"

4. Cole o JSON de exemplo abaixo no campo "Request body"

5. Clique em "Execute"

6. Veja a resposta na seção "Responses"

### Exemplo de JSON para Swagger:

```json
{
  "price_per_night_usd": 150.0,
  "rating": 4.5,
  "avaliação_clientes": 4.2,
  "distância_do_centro_km": 5.0,
  "energia_renovável": 75.0,
  "gestão_resíduos_índice": 80.0,
  "consumo_água_por_hóspede": 200.0,
  "carbon_footprint_score": 60.0,
  "reciclagem_score": 70.0,
  "energia_limpa_score": 75.0,
  "water_usage_index": 30.0,
  "sustainability_index": 65.0,
  "eco_impact_index": 68.0,
  "eco_value_ratio": 0.43,
  "sentimento_score": 0.5,
  "eco_keyword_count": 3,
  "região_encoded": 2,
  "possui_selo_sustentável_encoded": 1,
  "sentimento_sustentabilidade_encoded": 1,
  "price_sust_ratio": 0.43,
  "eco_value_score": 43.0,
  "total_sust_score": 65.0,
  "price_category": 2,
  "water_consumption_ratio": 0.30
}
```

**Nota**: No Swagger UI, você precisa adicionar o header `X-API-KEY` manualmente:
- Clique em "Authorize" no topo da página
- Adicione: `X-API-KEY: test-api-key`

## Método 4: Usando Python requests

```python
import requests

url = "http://localhost:8080/predict"
headers = {
    "X-API-KEY": "test-api-key",
    "Content-Type": "application/json"
}

payload = {
    "price_per_night_usd": 150.0,
    "rating": 4.5,
    "avaliação_clientes": 4.2,
    "distância_do_centro_km": 5.0,
    "energia_renovável": 75.0,
    "gestão_resíduos_índice": 80.0,
    "consumo_água_por_hóspede": 200.0,
    "carbon_footprint_score": 60.0,
    "reciclagem_score": 70.0,
    "energia_limpa_score": 75.0,
    "water_usage_index": 30.0,
    "sustainability_index": 65.0,
    "eco_impact_index": 68.0,
    "eco_value_ratio": 0.43,
    "sentimento_score": 0.5,
    "eco_keyword_count": 3,
    "região_encoded": 2,
    "possui_selo_sustentável_encoded": 1,
    "sentimento_sustentabilidade_encoded": 1,
    "price_sust_ratio": 0.43,
    "eco_value_score": 43.0,
    "total_sust_score": 65.0,
    "price_category": 2,
    "water_consumption_ratio": 0.30
}

response = requests.post(url, json=payload, headers=headers)
print(response.status_code)
print(response.json())
```

## Resposta Esperada

### Sucesso (200 OK):

```json
{
  "prediction": 3,
  "probabilities": [0.05, 0.10, 0.15, 0.60, 0.10],
  "prediction_label": "Alto",
  "confidence": 60.0,
  "all_probabilities": {
    "Muito Baixo": 0.05,
    "Baixo": 0.10,
    "Médio": 0.15,
    "Alto": 0.60,
    "Muito Alto": 0.10
  },
  "model_version": "unknown"
}
```

### Erros Comuns:

- **422 Unprocessable Entity**: Payload inválido ou campos faltando
- **403 Forbidden**: API key inválida ou ausente
- **503 Service Unavailable**: Modelo não carregado
- **500 Internal Server Error**: Erro interno do servidor

## Campos Obrigatórios

Todos os 24 campos são obrigatórios:

1. `price_per_night_usd` (float)
2. `rating` (float)
3. `avaliação_clientes` (float)
4. `distância_do_centro_km` (float)
5. `energia_renovável` (float)
6. `gestão_resíduos_índice` (float)
7. `consumo_água_por_hóspede` (float)
8. `carbon_footprint_score` (float)
9. `reciclagem_score` (float)
10. `energia_limpa_score` (float)
11. `water_usage_index` (float)
12. `sustainability_index` (float)
13. `eco_impact_index` (float)
14. `eco_value_ratio` (float)
15. `sentimento_score` (float)
16. `eco_keyword_count` (int)
17. `região_encoded` (int)
18. `possui_selo_sustentável_encoded` (int)
19. `sentimento_sustentabilidade_encoded` (int)
20. `price_sust_ratio` (float)
21. `eco_value_score` (float)
22. `total_sust_score` (float)
23. `price_category` (int)
24. `water_consumption_ratio` (float)

## Dicas

1. **Verificar health primeiro**: Sempre verifique `/health` antes de testar `/predict`
2. **Usar Swagger para explorar**: A interface Swagger é ótima para entender o schema
3. **Testar casos extremos**: Teste com valores muito altos/baixos de sustentabilidade
4. **Verificar logs**: Os logs da API mostram detalhes sobre cada predição

## Troubleshooting

### "Modelo não está carregado"
- Verifique os logs da API ao iniciar
- Confirme que `models/latest/sustainability_classification_pipeline.pkl` existe
- Execute `train_model.py` se necessário

### "API key inválida"
- Verifique o `.env` e confirme que `API_KEY` está configurado
- Use o mesmo valor no header `X-API-KEY`

### "422 Unprocessable Entity"
- Verifique se todos os 24 campos estão presentes
- Confirme que os tipos estão corretos (float vs int)
- Use o Swagger UI para validar o schema

