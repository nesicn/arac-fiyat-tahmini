import streamlit as st
import pandas as pd
import pickle

# Sayfa Konfigürasyonu
st.set_page_config(page_title="Araç Fiyat Tahmini", page_icon="🚗", layout="wide")

# Modeli Yükleme
@st.cache_resource
def load_model():
    with open("car_pipe.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# Başlıklar
st.title("🚗 İkinci El Araç Fiyat Tahmin Sistemi")
st.write("Lütfen tahmin yapmak istediğiniz aracın özelliklerini seçin.")

# Seçenek Listeleri
makes = ['Buick', 'Cadillac', 'Chevrolet', 'Pontiac', 'SAAB', 'Saturn']
types = ['Convertible', 'Coupe', 'Hatchback', 'Sedan', 'Wagon']
models = ['9-2X AWD', '9_3', '9_3 HO', '9_5', '9_5 HO', 'AVEO', 'Bonneville', 'CST-V', 'CTS', 'Century', 'Classic', 'Cobalt', 'Corvette', 'Deville', 'G6', 'GTO', 'Grand Am', 'Grand Prix', 'Impala', 'Ion', 'L Series', 'Lacrosse', 'Lesabre', 'Malibu', 'Monte Carlo', 'Park Avenue', 'STS-V6', 'STS-V8', 'Sunfire', 'Vibe', 'XLR-V8']
trims = ['AWD Sportwagon 4D', 'Aero Conv 2D', 'Aero Sedan 4D', 'Aero Wagon 4D', 'Arc Conv 2D', 'Arc Sedan 4D', 'Arc Wagon 4D', 'CX Sedan 4D', 'CXL Sedan 4D', 'CXS Sedan 4D', 'Conv 2D', 'Coupe 2D', 'Custom Sedan 4D', 'DHS Sedan 4D', 'DTS Sedan 4D', 'GT Coupe 2D', 'GT Sedan 4D', 'GT Sportwagon', 'GTP Sedan 4D', 'GXP Sedan 4D', 'Hardtop Conv 2D', 'L300 Sedan 4D', 'LS Coupe 2D', 'LS Hatchback 4D', 'LS MAXX Hback 4D', 'LS Sedan 4D', 'LS Sport Coupe 2D', 'LS Sport Sedan 4D', 'LT Coupe 2D', 'LT Hatchback 4D', 'LT MAXX Hback 4D', 'LT Sedan 4D', 'Limited Sedan 4D', 'Linear Conv 2D', 'Linear Sedan 4D', 'Linear Wagon 4D', 'MAXX Hback 4D', 'Quad Coupe 2D', 'SE Sedan 4D', 'SLE Sedan 4D', 'SS Coupe 2D', 'SS Sedan 4D', 'SVM Hatchback 4D', 'SVM Sedan 4D', 'Special Ed Ultra 4D', 'Sportwagon 4D']

# Arayüz Kolonları
col1, col2, col3 = st.columns(3)

with col1:
    make = st.selectbox("Marka", makes, index=2)
    model_name = st.selectbox("Model", models, index=11)
    trim = st.selectbox("Donanım / Paket", trims, index=25)
    car_type = st.selectbox("Kasa Tipi", types, index=3)

with col2:
    mileage = st.number_input("Kilometre", min_value=0, value=20000, step=1000)
    cylinder = st.selectbox("Silindir Sayısı", [4, 6, 8], index=0)
    liter = st.number_input("Motor Hacmi (Örn: 2.2)", min_value=0.0, value=2.2, step=0.1)
    doors = st.selectbox("Kapı Sayısı", [2, 4], index=1)

with col3:
    cruise = st.checkbox("Hız Sabitleyici (Cruise Control)", value=False)
    sound = st.checkbox("Gelişmiş Ses Sistemi", value=False)
    leather = st.checkbox("Deri Koltuk", value=False)

st.markdown("---")

# Tahmin Butonu
if st.button("Tahmin Et 💰", type="primary", use_container_width=True):
    input_data = pd.DataFrame([{
        'Mileage': mileage,
        'Make': make,
        'Model': model_name,
        'Trim': trim,
        'Type': car_type,
        'Cylinder': cylinder,
        'Liter': liter,
        'Doors': doors,
        'Cruise': int(cruise),
        'Sound': int(sound),
        'Leather': int(leather)
    }])
    
    prediction = model.predict(input_data)[0]
    st.success(f"### Tahmini Satış Fiyatı: **${prediction:,.2f}**")
