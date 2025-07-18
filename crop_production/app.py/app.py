import streamlit as st
import pandas as pd
import pickle

# Load model and feature columns
with open("regression_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("model_features.pkl", "rb") as f:
    feature_names = pickle.load(f)

st.title("🌾 Crop Production Predictor")
st.write("Enter details below to predict total crop production (in tons).")

# Collect user inputs
year = st.number_input("Year", min_value=1960, max_value=2050, value=2023)

area = st.selectbox("Select Region (Area)", [
    'Africa', 'Asia', 'Europe', 'North America', 'South America',
    'Oceania', 'India', 'China', 'United States', 'Brazil'
])

item = st.selectbox("Select Crop (Item)", [
    'Wheat', 'Maize', 'Rice, paddy', 'Barley', 'Sorghum', 'Soybeans', 'Cassava'
])

area_harvested = st.number_input("Area Harvested (hectares)", min_value=0.0, value=10000.0)
yield_value = st.number_input("Yield (hg/ha)", min_value=0.0, value=35000.0)

# Build input row
input_dict = {
    'year': year,
    'Area harvested': area_harvested,
    'Yield': yield_value,
}

# Add one-hot columns
for col in feature_names:
    if col.startswith("area_"):
        input_dict[col] = 1 if col == f"area_{area}" else 0
    elif col.startswith("item_"):
        input_dict[col] = 1 if col == f"item_{item}" else 0
    elif col not in input_dict:
        input_dict[col] = 0  # for any missing columns

# Create input DataFrame
input_df = pd.DataFrame([input_dict])[feature_names]

# Predict
if st.button("Predict Production"):
    prediction = model.predict(input_df)[0]
    st.success(f"🔢 Estimated Production: {prediction:,.2f} tons")
