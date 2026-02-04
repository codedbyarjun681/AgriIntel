import pandas as pd
import lightgbm as lgb
import pickle
from sklearn.preprocessing import LabelEncoder

# --- 1. Load the Dataset ---
df = pd.read_csv('Crop_recommendation.csv')

# --- 2. Train and Save the Soil Health Classification Model ---

def classify_soil_health(row):
    n_score = 0
    p_score = 0
    k_score = 0
    if row['N'] > 90: n_score = 2
    elif row['N'] > 60: n_score = 1
    if row['P'] > 50: p_score = 2
    elif row['P'] > 40: p_score = 1
    if row['K'] > 40: k_score = 2
    elif row['K'] > 30: k_score = 1
    
    total_score = n_score + p_score + k_score
    if total_score >= 5: return 'High'
    elif total_score >= 3: return 'Medium'
    else: return 'Low'

df['soil_health'] = df.apply(classify_soil_health, axis=1)

soil_features = ['N', 'P', 'K', 'ph']
soil_target = 'soil_health'
X_soil = df[soil_features]
y_soil = df[soil_target]

# 🔹 CUDA ENABLED
soil_model = lgb.LGBMClassifier(
    random_state=42,
    device='gpu'
)

soil_model.fit(X_soil, y_soil)

with open('soil_health_model.pkl', 'wb') as file:
    pickle.dump(soil_model, file)

print("Stage 1: Soil health model trained and saved as soil_health_model.pkl")

# --- 3. Train and Save the Integrated Crop Recommendation Model ---

df['soil_health_encoded'] = LabelEncoder().fit_transform(df['soil_health'])

crop_features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'soil_health_encoded']
crop_target = 'label'
X_crop = df[crop_features]
y_crop = df[crop_target]

# 🔹 CUDA ENABLED
crop_model = lgb.LGBMClassifier(
    random_state=42,
    device='gpu'
)

crop_model.fit(X_crop, y_crop)

with open('crop_recommendation_model.pkl', 'wb') as file:
    pickle.dump(crop_model, file)

print("Stage 2: Integrated crop recommendation model trained and saved as crop_recommendation_model.pkl")
