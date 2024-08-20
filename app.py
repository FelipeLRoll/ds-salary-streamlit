import pandas as pd
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn import linear_model

df = pd.read_csv(r'E:\\ROLL\DataScience\\Projetos\\ds-salary-streamlit\\dataset\\updated_ds_jobs_2021.csv')

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
  df = pd.read_csv(uploaded_file)
  st.write(df)

skills = ["python", "spark", "aws", "excel", "sql", "sas", "keras", "pytorch", "scikit", "tensor", "hadoop", "tableau", "bi", "flink", "mongo", "google_an"]
manter = skills + ["avg_salary_month"]
df = df[manter]

scaler = MinMaxScaler()

df_normalizado =  pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)

var_preditoras = df_normalizado.drop("avg_salary_month", axis = 1)

var_target = df_normalizado[["avg_salary_month"]]

X_train, X_test, y_train, y_test = train_test_split(var_preditoras, var_target, test_size=0.3, random_state=10)

linear_regression = linear_model.LinearRegression()
linear_regression.fit(X_train, y_train)

resultados = linear_regression.predict(X_test)

#testando o MAE
mae_score = mean_absolute_error(y_test, resultados)
print("Mean Absolute Error: " , mae_score)

#testando o MSE
mse_score = mean_squared_error(y_test, resultados)
print("Mean Squared Error: " , mse_score)


#dicionario
features = {}

# Dicionario para mudar o nome de cada Sill
skill_names = {
    "python": "Python",
    "spark": "Apache Spark",
    "aws": "AWS",
    "excel": "Microsoft Excel",
    "sql": "SQL",
    "sas": "SAS",
    "keras": "Keras",
    "pytorch": "PyTorch",
    "scikit": "Scikit-learn",
    "tensor": "TensorFlow",
    "hadoop": "Hadoop",
    "tableau": "Tableau",
    "bi": "Business Intelligence",
    "flink": "Apache Flink",
    "mongo": "MongoDB",
    "google_an": "Google Analytics"
}


st.header("Prevendo o salário de um Cientista de Dados de acordo com as skills que ele possui")
st.divider()

#loop para criar as selectboxes
for skill in skills:
    display_name = skill_names.get(skill, skill)
    features[skill] = 1 if st.selectbox(f"Tem Conhecimento de {display_name}?", ("Não", "Sim"), index=1) == "Sim" else 0
        
#convertendo o dicionario em dataframe    
features_df = pd.DataFrame([features])    

salario_previsto = linear_regression.predict(features_df)[0][0]

salario_previsto_ajustado = scaler.inverse_transform([[0]*len(var_preditoras.columns) + [salario_previsto]])[0][-1]

st.metric(label="Salário Previsto", value=f"$ {salario_previsto_ajustado:,.2f}")
