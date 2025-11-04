import os
import streamlit as st
import requests

API_URL = os.getenv("API_URL", "http://api:8000/predict")

st.set_page_config(page_title="Churn predictor", layout="centered")

st.title("Previsão de Churn — Demo")
st.write("Preencha os campos do cliente e clique em Prever. O app envia os dados para a API e mostra a probabilidade de churn.")

with st.form("client_form"):
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"], index=0)
        senior = st.selectbox("SeniorCitizen", [0, 1], index=0)
        partner = st.selectbox("Partner", ["Yes", "No"], index=1)
        dependents = st.selectbox("Dependents", ["Yes", "No"], index=1)
        tenure = st.number_input("Tenure (months)", min_value=0, max_value=200, value=12)
        phone = st.selectbox("PhoneService", ["Yes", "No"], index=0)
    with col2:
        multiple_lines = st.selectbox("MultipleLines", ["Yes", "No", "No phone service"], index=1)
        internet = st.selectbox("InternetService", ["DSL", "Fiber optic", "No"], index=0)
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"], index=0)
        paperless = st.selectbox("PaperlessBilling", ["Yes", "No"], index=0)
        payment = st.selectbox("PaymentMethod", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"], index=0)
        monthly = st.number_input("MonthlyCharges", min_value=0.0, step=1.0, value=70.0)

    submitted = st.form_submit_button("Prever")

if submitted:
    payload = {
        "gender": gender,
        "SeniorCitizen": int(senior),
        "Partner": partner,
        "Dependents": dependents,
        "tenure": int(tenure),
        "PhoneService": phone,
        "MultipleLines": multiple_lines,
        "InternetService": internet,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": float(monthly),
        # Optional fields commonly present in dataset
        "TotalCharges": None
    }

    try:
        # the API expects a body like {"data": { ... }}
        res = requests.post(API_URL, json={"data": payload}, timeout=10)
        res.raise_for_status()
        data = res.json()
        st.subheader("Resultado")
        st.write(f"Probabilidade de churn: {data.get('probability'):.3f}")
        st.write(f"Predição (0 = não, 1 = sim): {data.get('prediction')}" )
        st.json(data)
    except Exception as e:
        st.error(f"Falha ao chamar a API: {e}")

st.markdown("---")
st.markdown("Se preferir, edite o arquivo `streamlit_app.py` para incluir mais campos ou ajustar o endpoint da API.")
