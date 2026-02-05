import pandas as pd
import pickle

df = pd.read_csv("Crop_recommendation.csv")

with open("crop_recommendation_model.pkl", "rb") as f:
    model = pickle.load(f)

input_df = pd.read_csv("npk_input.csv")

temperature = df["temperature"].mean()
humidity = df["humidity"].mean()
ph = df["ph"].mean()
rainfall = df["rainfall"].mean()

X = pd.DataFrame({
    "N": input_df["N"],
    "P": input_df["P"],
    "K": input_df["K"],
    "temperature": temperature,
    "humidity": humidity,
    "ph": ph,
    "rainfall": rainfall,
    "soil_health_encoded": 1
})

probs = pd.DataFrame(
    model.predict_proba(X),
    columns=model.classes_
)

output = pd.DataFrame({
    "rice_percentage": (probs.get("rice", 0) * 100).round(2),
    "maize_percentage": (probs.get("maize", 0) * 100).round(2),
    "cotton_percentage": (probs.get("cotton", 0) * 100).round(2)
})

output.to_csv("crop_probability_output.csv", index=False)
