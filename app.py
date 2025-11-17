import streamlit as st
import requests
import uuid
import json

# -----------------------------
#  Azure Translator Credentials
# -----------------------------
AZURE_TRANSLATOR_KEY = "BME6F8rNa65iMWqTu04hk3Ux3JaUg0cuap7E0KjmekGI08pkSi8nJQQJ99BKAC3pKaRXJ3w3AAAbACOGxrcj"
AZURE_REGION = "eastasia"   # e.g., "eastus"
AZURE_ENDPOINT = "https://api.cognitive.microsofttranslator.com/"


# -----------------------------
#  Translation Function
# -----------------------------
def translate_text(text, target_language):
    path = '/translate?api-version=3.0'
    params = f"&to={target_language}"
    constructed_url = AZURE_ENDPOINT + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_TRANSLATOR_KEY,
        'Ocp-Apim-Subscription-Region': AZURE_REGION,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': text}]
    response = requests.post(constructed_url, headers=headers, json=body)

    try:
        result = response.json()
        return result[0]["translations"][0]["text"]
    except Exception as e:
        return f"Error: {response.text}"


# -----------------------------
#   Streamlit User Interface
# -----------------------------
st.title("🌍 Azure AI Translator")
st.write("Translate text using Microsoft Azure AI Translator API.")

# User Input
input_text = st.text_area("Enter text to translate", height=150)
target_lang = st.selectbox(
    "Select target language",
    ["ur", "hi", "fr", "es", "de", "ar", "zh-Hans", "ru", "ja"]
)

# Translate Button
if st.button("Translate"):
    if input_text.strip():
        with st.spinner("Translating..."):
            translated_text = translate_text(input_text, target_lang)
        st.success("Translation Complete")
        st.text_area("Translated Output", translated_text, height=150)
    else:
        st.warning("Please enter some text!")
