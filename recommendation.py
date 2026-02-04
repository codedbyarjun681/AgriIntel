import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder

# --- 1. Load all necessary files ---
soil_model = pickle.load(open('soil_health_model.pkl', 'rb'))
crop_model = pickle.load(open('crop_recommendation_model.pkl', 'rb'))
dataset = pd.read_csv('Crop_recommendation.csv')

# --- 2. Define a database of common fertilizers and their nutrient content ---
fertilizer_db = {
    'Urea': {'N': 46, 'P': 0, 'K': 0},
    'DAP': {'N': 18, 'P': 46, 'K': 0},
    'MOP': {'N': 0, 'P': 0, 'K': 60},
    'SSP': {'N': 0, 'P': 16, 'K': 0} # Single Superphosphate
}

# --- 3. Function to translate nutrient needs into fertilizer products ---
def get_fertilizer_product_recommendation(n_need, p_need, k_need):
    recommendations = []
    
    if n_need > 0:
        urea_amount = n_need / (fertilizer_db['Urea']['N'] / 100)
        recommendations.append({
            'nutrient': 'Nitrogen (N)',
            'fertilizer_name': 'Urea',
            'suggested_amount_kg_per_hectare': f"{round(urea_amount, 2)}",
            'note': 'Urea is a primary source of Nitrogen.'
        })

    if p_need > 0:
        dap_amount_for_p = p_need / (fertilizer_db['DAP']['P'] / 100)
        ssp_amount_for_p = p_need / (fertilizer_db['SSP']['P'] / 100)
        recommendations.append({
            'nutrient': 'Phosphorus (P)',
            'fertilizer_name': 'DAP or SSP',
            'suggested_amount_kg_per_hectare': f"{round(dap_amount_for_p, 2)} (DAP) or {round(ssp_amount_for_p, 2)} (SSP)",
            'note': 'DAP also adds some Nitrogen. Use SSP for Phosphorus only.'
        })

    if k_need > 0:
        mop_amount = k_need / (fertilizer_db['MOP']['K'] / 100)
        recommendations.append({
            'nutrient': 'Potassium (K)',
            'fertilizer_name': 'Muriate of Potash (MOP)',
            'suggested_amount_kg_per_hectare': f"{round(mop_amount, 2)}",
            'note': 'MOP is the most common source of Potassium.'
        })
        
    return recommendations if recommendations else "No fertilizer needed based on current soil levels for this crop."

# --- 4. Define the Main Integrated AI Model Function ---
def get_crop_and_fertilizer_recommendation(N, P, K, temperature, humidity, ph, rainfall):
    soil_input = pd.DataFrame([[N, P, K, ph]], columns=['N', 'P', 'K', 'ph'])
    soil_health_prediction = soil_model.predict(soil_input)[0]

    soil_health_map = {'Low': 0, 'Medium': 1, 'High': 2}
    soil_health_encoded = soil_health_map.get(soil_health_prediction, 1)

    crop_input = pd.DataFrame([[N, P, K, temperature, humidity, ph, rainfall, soil_health_encoded]], 
                              columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'soil_health_encoded'])
    
    recommended_crop = crop_model.predict(crop_input)[0]

    crop_data = dataset[dataset['label'] == recommended_crop]
    avg_n = crop_data['N'].mean()
    avg_p = crop_data['P'].mean()
    avg_k = crop_data['K'].mean()

    n_recommend = max(0, avg_n - N)
    p_recommend = max(0, avg_p - P)
    k_recommend = max(0, avg_k - K)

    fertilizer_products = get_fertilizer_product_recommendation(n_recommend, p_recommend, k_recommend)

    report = {
        'soil_health_status': soil_health_prediction,
        'recommended_crop': recommended_crop,
        'fertilizer_products': fertilizer_products
    }
    
    return report