import streamlit as st
from PIL import Image

from app import predict
from chat import ask
from detection import analyze_image

tab1, tab2, tab3 = st.tabs(["📊 Crop Prediction", "🧠 AI Chat", "🖼️ Leaf Analysis"])

# --- Tab 1: Predict Best Crop ---
with tab1:
    st.subheader("🌱 Predict the Best Crop to Grow")
    N = st.number_input("Nitrogen", 0.0)
    P = st.number_input("Phosphorus", 0.0)
    K = st.number_input("Potassium", 0.0)
    temp = st.number_input("Temperature (°C)", 0.0)
    humidity = st.number_input("Humidity (%)", 0.0)
    ph = st.number_input("pH", 0.0)
    rainfall = st.number_input("Rainfall (mm)", 0.0)

    if st.button("Predict Crop"):
        result = predict(N, P, K, temp, humidity, ph, rainfall)
        st.success(f"✅ Recommended Crop: {result}")

# --- Tab 2: Gemini Chat ---
with tab2:
    st.subheader("🧠 Ask Anything")
    question = st.text_input("Enter your question about farming, crops, soil, etc.")
    if st.button("Ask Gemini"):
        reply = ask(question)
        st.markdown(reply)

# --- Tab 3: Leaf Image Analysis ---
with tab3:
    st.subheader("🖼️ Upload a Leaf Image")
    file = st.file_uploader("Upload image", type=["jpg", "png", "jpeg"])
    if file:
        img = Image.open(file)
        st.image(img, caption="Uploaded Leaf", use_column_width=True)
        if st.button("Analyze Image"):
            analysis = analyze_image(img)
            st.markdown(analysis)