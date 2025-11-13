#!/usr/bin/env python3
"""
Script para treinar o modelo de classificação de sustentabilidade
baseado no notebook rihs.ipynb e usando dataset_ready_for_ml.csv
"""
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report
try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except (ImportError, Exception) as e:
    XGBOOST_AVAILABLE = False
    print(f"⚠️  XGBoost não disponível ({type(e).__name__}), usando apenas RandomForest")
import warnings
warnings.filterwarnings('ignore')

# Configurações
RANDOM_STATE = 42
MODEL_OUTPUT_DIR = Path("models/latest")
MODEL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("TREINAMENTO DO MODELO DE CLASSIFICAÇÃO DE SUSTENTABILIDADE")
print("=" * 80)

# 1. Carregar dataset
print("\n1. Carregando dataset...")
df = pd.read_csv("dataset_ready_for_ml.csv")
print(f"   Dataset carregado: {len(df)} linhas, {len(df.columns)} colunas")

# 2. Preparar features e target
print("\n2. Preparando features e target...")

# Features canônicas (mesmas usadas na API)
CANONICAL_FEATURES = [
    "price_per_night_usd",
    "rating",
    "avaliacao_clientes",
    "distancia_do_centro_km",
    "energia_renovavel",
    "gestao_residuos_indice",
    "consumo_agua_por_hospede",
    "carbon_footprint_score",
    "reciclagem_score",
    "energia_limpa_score",
    "water_usage_index",
    "sustainability_index",
    "eco_impact_index",
    "eco_value_ratio",
    "sentimento_score",
    "eco_keyword_count",
    "regiao_encoded",
    "possui_selo_sustentavel_encoded",
    "sentimento_sustentabilidade_encoded",
    "price_sust_ratio",
    "eco_value_score",
    "total_sust_score",
    "price_category",
    "water_consumption_ratio",
]

# Normalizar nomes de colunas (remover acentos)
column_mapping = {
    'avaliação_clientes': 'avaliacao_clientes',
    'distância_do_centro_km': 'distancia_do_centro_km',
    'energia_renovável_%': 'energia_renovavel',
    'gestão_resíduos_índice': 'gestao_residuos_indice',
    'consumo_água_por_hóspede': 'consumo_agua_por_hospede',
    'região_encoded': 'regiao_encoded',
    'possui_selo_sustentável_encoded': 'possui_selo_sustentavel_encoded',
    'sentimento_sustentabilidade_encoded': 'sentimento_sustentabilidade_encoded',
}

# Renomear colunas se necessário
for old_name, new_name in column_mapping.items():
    if old_name in df.columns:
        df[new_name] = df[old_name]

# Verificar se todas as features existem e criar as faltantes
missing_features = [f for f in CANONICAL_FEATURES if f not in df.columns]
if missing_features:
    print(f"   ⚠️  Features faltando: {missing_features}")
    # Tentar criar features faltantes se possível
    if 'price_sust_ratio' not in df.columns and 'price_per_night_usd' in df.columns and 'sustainability_index' in df.columns:
        df['price_sust_ratio'] = df['sustainability_index'] / (df['price_per_night_usd'] + 1)
        print("      ✓ Criado: price_sust_ratio")
    if 'eco_value_score' not in df.columns and 'eco_value_ratio' in df.columns:
        df['eco_value_score'] = df['eco_value_ratio'] * 100
        print("      ✓ Criado: eco_value_score")
    if 'total_sust_score' not in df.columns and 'sustainability_index' in df.columns:
        df['total_sust_score'] = df['sustainability_index']
        print("      ✓ Criado: total_sust_score")
    if 'price_category' not in df.columns and 'price_per_night_usd' in df.columns:
        df['price_category'] = pd.cut(df['price_per_night_usd'], bins=5, labels=[0, 1, 2, 3, 4]).astype(int)
        print("      ✓ Criado: price_category")
    if 'water_consumption_ratio' not in df.columns and 'water_usage_index' in df.columns:
        df['water_consumption_ratio'] = df['water_usage_index'] / 100
        print("      ✓ Criado: water_consumption_ratio")

# Selecionar apenas features que existem
available_features = [f for f in CANONICAL_FEATURES if f in df.columns]
print(f"   Features disponíveis: {len(available_features)}/{len(CANONICAL_FEATURES)}")

# Target: classificação_sustentabilidade_encoded
if 'classificação_sustentabilidade_encoded' in df.columns:
    target_col = 'classificação_sustentabilidade_encoded'
elif 'classificacao_sustentabilidade_encoded' in df.columns:
    target_col = 'classificacao_sustentabilidade_encoded'
else:
    # Criar target a partir da classificação textual
    if 'classificação_sustentabilidade' in df.columns:
        class_mapping = {
            'Muito Baixo': 0,
            'Baixo': 1,
            'Médio': 2,
            'Alto': 3,
            'Muito Alto': 4
        }
        df['classificacao_sustentabilidade_encoded'] = df['classificação_sustentabilidade'].map(class_mapping)
        target_col = 'classificacao_sustentabilidade_encoded'
    else:
        raise ValueError("Não foi possível encontrar a coluna target")

# Preparar X e y
X = df[available_features].copy()
y = df[target_col].copy()

# Remover valores nulos
X = X.fillna(X.median())
y = y.fillna(y.mode()[0] if not y.mode().empty else 2)

print(f"   X shape: {X.shape}")
print(f"   y shape: {y.shape}")
print(f"   Classes: {sorted(y.unique())}")

# 3. Split train/test
print("\n3. Dividindo em treino e teste...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
)
print(f"   Treino: {X_train.shape[0]} amostras")
print(f"   Teste: {X_test.shape[0]} amostras")

# 4. Treinar modelos
print("\n4. Treinando modelos...")

models = {
    'RandomForest': RandomForestClassifier(
        n_estimators=200,
        max_depth=7,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=RANDOM_STATE,
        n_jobs=-1
    ),
}

if XGBOOST_AVAILABLE:
    models['XGBoost'] = XGBClassifier(
        random_state=RANDOM_STATE,
        n_jobs=-1,
        eval_metric='mlogloss'
    )

results = {}
for name, model in models.items():
    print(f"   Treinando {name}...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    f1_weighted = f1_score(y_test, y_pred, average='weighted')
    
    results[name] = {
        'model': model,
        'accuracy': accuracy,
        'f1_weighted': f1_weighted,
        'predictions': y_pred
    }
    
    print(f"      Accuracy: {accuracy:.4f}, F1 Weighted: {f1_weighted:.4f}")

# 5. Selecionar melhor modelo
print("\n5. Selecionando melhor modelo...")
best_model_name = max(results.keys(), key=lambda k: results[k]['f1_weighted'])
best_model = results[best_model_name]['model']
print(f"   Melhor modelo: {best_model_name}")
print(f"   Accuracy: {results[best_model_name]['accuracy']:.4f}")
print(f"   F1 Weighted: {results[best_model_name]['f1_weighted']:.4f}")

# 6. Relatório detalhado
print("\n6. Relatório de classificação:")
y_pred_best = results[best_model_name]['predictions']
print(classification_report(y_test, y_pred_best))

# 7. Salvar modelo no formato esperado pela API
print("\n7. Salvando modelo...")

# Criar dicionário com modelo e metadados (formato esperado pela API)
model_info = {
    'model': best_model,
    'features': available_features,
    'feature_importance': dict(zip(available_features, best_model.feature_importances_)) if hasattr(best_model, 'feature_importances_') else {},
    'performance': {
        'accuracy': float(results[best_model_name]['accuracy']),
        'f1_weighted': float(results[best_model_name]['f1_weighted']),
        'model_name': best_model_name,
        'training_date': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    'class_names': ['Muito Baixo', 'Baixo', 'Médio', 'Alto', 'Muito Alto']
}

# Salvar modelo
model_path = MODEL_OUTPUT_DIR / "sustainability_classification_pipeline.pkl"
joblib.dump(model_info, model_path)
print(f"   ✓ Modelo salvo em: {model_path}")

# 8. Salvar também apenas o modelo (fallback)
model_only_path = MODEL_OUTPUT_DIR / "model.pkl"
joblib.dump(best_model, model_only_path)
print(f"   ✓ Modelo (apenas) salvo em: {model_only_path}")

print("\n" + "=" * 80)
print("TREINAMENTO CONCLUÍDO COM SUCESSO!")
print("=" * 80)

