#!/usr/bin/env python3
"""
Script para testar o endpoint /predict da API
"""
import requests
import json
from pathlib import Path

# Configurações
API_URL = "http://localhost:8080"
API_KEY =  "test-api-key"

# Exemplo de payload baseado no schema
example_payload = {
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

def test_predict():
    """Testa o endpoint /predict"""
    print("=" * 80)
    print("TESTE DO ENDPOINT /predict")
    print("=" * 80)
    
    # 1. Verificar se a API está rodando
    print("\n1. Verificando se a API está a rodar...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✓ API está a rodar")
            print(f"   Status: {health_data.get('status')}")
            print(f"   Modelo carregado: {health_data.get('model_loaded')}")
            if not health_data.get('model_loaded'):
                print("AVISO: Modelo não está carregado!")
                return
        else:
            print(f"API retornou status {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print(f"  Não foi possível conectar à API em {API_URL}")
        print(f"   Certifique-se de que a API está rodando:")
        print(f"   uvicorn app.main:app --host 0.0.0.0 --port 8080")
        return
    except Exception as e:
        print(f"Erro ao verificar API: {e}")
        return
    
    # 2. Testar /predict sem API key (deve falhar)
    print("\n2. Testando /predict sem API key (deve retornar 422 ou 403)...")
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=example_payload,
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        if response.status_code in [422, 403]:
            print("   ✓ Rejeição correcta (sem API key)")
        else:
            print(f"Resposta inesperada: {response.text[:200]}")
    except Exception as e:
        print(f"Erro: {e}")
    
    # 3. Testar /predict com API key (deve funcionar)
    print("\n3. Testando /predict com API key...")
    try:
        headers = {
            "X-API-KEY": API_KEY,
            "Content-Type": "application/json"
        }
        response = requests.post(
            f"{API_URL}/predict",
            json=example_payload,
            headers=headers,
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n   ✓ PREDIÇÃO REALIZADA COM SUCESSO!")
            print(f"\n   Resultado:")
            print(f"   - Classe predita: {result.get('prediction')} ({result.get('prediction_label')})")
            print(f"   - Confiança: {result.get('confidence')}%")
            print(f"   - Versão do modelo: {result.get('model_version')}")
            print(f"\n   Probabilidades por classe:")
            for class_name, prob in result.get('all_probabilities', {}).items():
                print(f"     {class_name}: {prob:.4f} ({prob*100:.2f}%)")
            print(f"\n   Probabilidades brutas: {result.get('probabilities')}")
        elif response.status_code == 503:
            print(" Modelo não está carregado (503 Service Unavailable)")
        elif response.status_code == 403:
            print("API key inválida (403 Forbidden)")
            print(f"   Verifique se API_KEY no .env corresponde à usada aqui")
        else:
            print(f"Erro: {response.status_code}")
            print(f"   Resposta: {response.text[:500]}")
    except Exception as e:
        print(f"Erro ao fazer requisição: {e}")
    
    # 4. Testar com payload mínimo (deve funcionar se todas as features forem fornecidas)
    print("\n4. Testando com diferentes valores...")
    test_cases = [
        {
            "name": "Hotel muito sustentável",
            "payload": {**example_payload, "sustainability_index": 90.0, "carbon_footprint_score": 85.0}
        },
        {
            "name": "Hotel pouco sustentável",
            "payload": {**example_payload, "sustainability_index": 20.0, "carbon_footprint_score": 15.0}
        }
    ]
    
    for test_case in test_cases:
        try:
            headers = {"X-API-KEY": API_KEY, "Content-Type": "application/json"}
            response = requests.post(
                f"{API_URL}/predict",
                json=test_case["payload"],
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n   {test_case['name']}:")
                print(f"     → {result.get('prediction_label')} (confiança: {result.get('confidence')}%)")
            else:
                print(f"\n   {test_case['name']}: Erro {response.status_code}")
        except Exception as e:
            print(f"\n   {test_case['name']}: Erro - {e}")
    
    print("\n" + "=" * 80)
    print("TESTE CONCLUÍDO")
    print("=" * 80)

if __name__ == "__main__":
    # Tentar carregar API_KEY do .env se existir
    env_file = Path(".env")
    if env_file.exists():
        try:
            with open(env_file) as f:
                for line in f:
                    if line.startswith("API_KEY="):
                        API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
                        break
        except Exception:
            pass
    
    test_predict()

