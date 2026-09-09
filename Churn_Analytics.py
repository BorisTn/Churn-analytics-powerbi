# Churn_Analytics.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import pickle
import warnings

warnings.filterwarnings('ignore')

def main():
    print("🚀 INICIANDO OPERACIÓN RESCATE - ANÁLISIS DE CHURN...")
    print("="*60)

    # 1. CARGAR DATOS
    print("\n📂 Cargando datos raw...")
    try:
        df = pd.read_csv('datos_raw.csv')
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo 'datos_raw.csv'.")
        return

    # Limpieza inicial básica
    df.columns = df.columns.str.strip()
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    
    # --- AJUSTE 2: Tratamiento correcto de SeniorCitizen ---
    # Convertimos la variable binaria a texto para que no reciba imputación de media aritmética
    if 'SeniorCitizen' in df.columns:
        df['SeniorCitizen'] = df['SeniorCitizen'].astype(str)
    
    # 2. DEFINIR VARIABLES
    # Asegurar que Churn sea 1/0
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0, 1: 1, 0: 0})
    
    # Separar Target y Features
    X = df.drop(columns=['Churn', 'customerID'])
    y = df['Churn']
    
    # --- AJUSTE 1: Selección Dinámica de Columnas ---
    num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    cat_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()

    print(f"\n📊 Estadísticas del dataset:")
    print(f"✅ Total de registros: {len(df)}")
    print(f"✅ Columnas numéricas detectadas: {len(num_cols)}")
    print(f"✅ Columnas categóricas detectadas: {len(cat_cols)}")
    print(f"✅ % de Churn en datos: {y.mean()*100:.2f}%")

    # 3. SEPARAR DATOS (Train/Test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 4. CREAR EL PIPELINE DE PREPROCESAMIENTO
    print("\n🔄 Configurando Pipeline de transformación...")
    
    # Transformaciones numéricas (media)
    numeric_transformer = SimpleImputer(strategy='mean')
    
    # Transformaciones categóricas (moda + OneHot)
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', drop='if_binary'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, num_cols),
            ('cat', categorical_transformer, cat_cols)
        ])

    # 5. CREAR EL PIPELINE COMPLETO
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=150, max_depth=10, random_state=42, n_jobs=-1))
    ])

    # 6. ENTRENAR EL PIPELINE
    print("🤖 Entrenando Pipeline (Limpieza + Random Forest)...")
    pipeline.fit(X_train, y_train)

    # 7. EVALUAR
    print("\n📈 REPORTE DE CALIDAD:")
    predicciones = pipeline.predict(X_test)
    print(classification_report(y_test, predicciones, target_names=['No Churn (0)', 'Churn (1)']))

    # 8. TOP 3 VARIABLES MÁS IMPORTANTES
    try:
        importancias = pipeline.named_steps['classifier'].feature_importances_
        feature_names = pipeline.named_steps['preprocessor'].get_feature_names_out()
        indices = np.argsort(importancias)[::-1]
        
        print("\n🎯 TOP 3 VARIABLES QUE PREDICEN LA CANCELACIÓN:")
        print("="*50)
        for i in range(3):
            nombre_var = feature_names[indices[i]].split('__')[-1]
            print(f"{i+1}. {nombre_var:25s} - Importancia: {importancias[indices[i]]:.4f} ({importancias[indices[i]]*100:.2f}%)")
    except Exception as e:
        print(f"\n⚠️ No se pudieron calcular las importancias de las variables: {e}")

    # 9. GENERAR PREDICCIONES
    print("\n🎯 Generando predicciones para todos los clientes...")
    probabilidades = pipeline.predict_proba(X)[:, 1]

    df_resultados = pd.DataFrame({
        'customerID': df['customerID'],
        'Probabilidad_Churn': probabilidades,
    })

    df_resultados['Nivel_Riesgo'] = pd.cut(
        df_resultados['Probabilidad_Churn'],
        bins=[0, 0.3, 0.6, 1.0],
        labels=['Bajo Riesgo', 'Medio Riesgo', 'Alto Riesgo'],
        include_lowest=True
    )

    df_final = df.merge(df_resultados, on='customerID', how='left')

    # 10. GUARDAR ARCHIVOS
    print("\n💾 Guardando archivos...")
    
    # --- AJUSTE 3: Guardar y nombrar correctamente el Pipeline ---
    with open('pipeline_churn.pkl', 'wb') as archivo:
        pickle.dump(pipeline, archivo)

    df_final.to_csv('datos_finales_con_id.csv', index=False)

    # 11. RESUMEN FINAL
    print("\n" + "="*60)
    print("✨ ¡PROCESO COMPLETADO CON ÉXITO! ✨")
    print("="*60)
    print("\n📁 Archivos generados:")
    print("   ✅ datos_finales_con_id.csv (Datos originales + predicciones)")
    print("   ✅ pipeline_churn.pkl (EL SISTEMA COMPLETO: Contiene reglas de imputación, OneHot y el RandomForest)")
    print("\n📊 Estadísticas finales:")
    print(f"   🔴 Clientes en ALTO RIESGO: {len(df_final[df_final['Nivel_Riesgo'] == 'Alto Riesgo'])}")
    print(f"   🟡 Clientes en RIESGO MEDIO: {len(df_final[df_final['Nivel_Riesgo'] == 'Medio Riesgo'])}")
    print(f"   🟢 Clientes en BAJO RIESGO: {len(df_final[df_final['Nivel_Riesgo'] == 'Bajo Riesgo'])}")
    print("="*60)

if __name__ == "__main__":
    main()