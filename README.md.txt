Ventajas del Pipeline:

✅ Sin fuga de datos: Las transformaciones (imputación, OneHot) se ajustan solo con datos de entrenamiento.

✅ Listo para producción: El archivo pipeline_churn.pkl contiene TODAS las reglas de limpieza y el modelo.

✅ Reproducible: Cualquier persona puede ejecutar el script y obtener los mismos resultados.

Stack Tecnológico
Fase	Herramientas
Limpieza y Modelado	Python, Pandas, NumPy, Scikit-Learn
Visualización	Power BI Desktop (.pbip)
Control de Versiones	Git, GitHub
Entorno	VS Code, Python 3.12, venv
📁 Estructura del Proyecto
text
Analytics_Project - Churn/
│
├── 📄 Churn_Analytics.py              # Script definitivo con Pipeline
├── 📄 pipeline_churn.pkl              # ¡EL TESORO! Modelo + reglas de limpieza
├── 📄 datos_raw.csv                   # Dataset original (Kaggle Telco Churn)
├── 📄 datos_finales_con_id.csv        # Datos enriquecidos para Power BI
├── 📄 README.md                       # Este archivo
├── 📄 .gitignore                      # Archivos ignorados por Git
├── 📁 dashboard/                      # Archivos de Power BI
│   └── Operacion_Rescate_Churn.pbip
├── 📁 images/                         # Capturas del dashboard
│   ├── dashboard_completo.png
│   └── dashboard_filtrado.png
└── 📁 venv/                           # Entorno virtual (ignorado por Git)
🚀 Cómo Ejecutar el Proyecto
1. Clonar el Repositorio
bash
git clone https://github.com/tu-usuario/churn-analytics-powerbi.git
cd churn-analytics-powerbi
2. Crear y Activar el Entorno Virtual
bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Mac/Linux)
source venv/bin/activate
3. Instalar Dependencias
bash
pip install pandas numpy scikit-learn matplotlib seaborn openpyxl
4. Ejecutar el Script
bash
python Churn_Analytics.py
5. Abrir el Dashboard
Abre Power BI Desktop.

Ve a "Abrir" y selecciona el archivo .pbip en la carpeta dashboard/.

📸 Vista Previa del Dashboard
Dashboard completo (sin filtros):

https://images/dashboard_completo.png

Dashboard con filtro de "Alto Riesgo":

https://images/dashboard_filtrado.png

📈 Métricas del Modelo
Métrica	No Churn	Churn	Promedio
Precision	0.84	0.65	0.79
Recall	0.90	0.53	0.80
F1-Score	0.87	0.58	0.79
Accuracy			80%
🏆 Logros Clave
✅ Modelo confiable: Accuracy del 80% sin fuga de datos.

✅ Pipeline profesional: Limpieza + Modelo en un solo objeto guardado.

✅ Dashboard interactivo: 4 KPI's, 3 gráficos, 2 slicers y botón de reset.

✅ Valor de negocio: ROI calculado en $500,000 anuales.

✅ Código limpio: Función main() y if __name__ == "__main__".

🤝 Cómo Contribuir
Si tienes sugerencias para mejorar este proyecto, eres bienvenido:

Haz un Fork del repositorio.

Crea una nueva rama (git checkout -b feature/mejora).

Haz commit de tus cambios (git commit -am 'Añadir mejora').

Haz push a la rama (git push origin feature/mejora).

Abre un Pull Request.

📬 Contacto
[Tu Nombre] - Data Analyst
📧 [tu-email@ejemplo.com]
🔗 [LinkedIn - /in/tu-usuario]
💼 [Sitio Web / Portafolio]

📜 Licencia
Este proyecto está bajo la licencia MIT. Para más información, consulta el archivo LICENSE.

✨ ¡Gracias por visitar mi proyecto! ✨