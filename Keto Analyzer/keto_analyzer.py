import requests
import time
import io
import zxingcpp
from PIL import Image
from fast_food_data import FAST_FOOD_HACKS

# --- CREDENTIALS ---
CLIENT_ID = "b826e72b8a094b7abbbbe03569a28dcd"
CLIENT_SECRET = "0693d8c758424dae80d7c47c824083c2"

# --- CONFIGURATION ---
HIDDEN_SUGARS = [
    "maltitol", "dextrose", "maltodextrin", "sugar", "cane sugar", 
    "corn syrup", "high fructose corn syrup", "agave", "honey", 
    "sucrose", "fructose", "fruit juice concentrate", "rice syrup",
    "barley malt", "dextrin"
]

def get_access_token():
    url = "https://oauth.fatsecret.com/connect/token"
    try:
        response = requests.post(
            url, 
            auth=(CLIENT_ID, CLIENT_SECRET),
            data={"grant_type": "client_credentials", "scope": "basic"}
        )
        if response.status_code == 200:
            return response.json().get('access_token')
        return None
    except Exception as e:
        print(f"Auth Error: {e}")
        return None

def calculate_keto_prime_score(net_carbs, fat, protein, ingredients_text):
    """
    THE FUTURE ALGORITHM:
    Calculates a 0-10 score based on macro ratios + ingredient quality.
    """
    # 1. The Macro Score (Based on Net Carbs)
    # Start at 10. Lose points for carbs.
    score = 10 - (net_carbs * 0.5) 
    
    # 2. The Ratio Bonus (Fat should be high)
    # If Fat > (Protein + Carbs), give a bonus
    if fat > (protein + net_carbs):
        score += 1.5

    # 3. The Ingredient Penalty
    if ingredients_text != 'n/a':
        for sugar in HIDDEN_SUGARS:
            if sugar in ingredients_text:
                score -= 2 # Big penalty for hidden sugars
    
    # Clamp score between 0 and 10
    score = max(0, min(10, score))
    return round(score, 1)

def format_food_verdict(food_id, food_name, token):
    headers = {'Authorization': f'Bearer {token}'}
    api_url = "https://platform.fatsecret.com/rest/server.api"
    
    # Get Details
    detail_params = {'method': 'food.get.v2', 'food_id': food_id, 'format': 'json'}
    res_detail = requests.get(api_url, params=detail_params, headers=headers)
    details_data = res_detail.json()
    
    if 'error' in details_data:
         return None 

    details = details_data.get('food', {})
    servings_obj = details.get('servings', {}).get('serving', [])
    
    # Get Image
    image_url = None
    images = details.get('food_images', {}).get('food_image', [])
    if isinstance(images, list) and len(images) > 0:
        image_url = images[0].get('image_url')
    elif isinstance(images, dict):
        image_url = images.get('image_url')

    if not servings_obj:
        return None
    
    serving = servings_obj[0] if isinstance(servings_obj, list) else servings_obj
    
    # Extract Data
    carbs = float(serving.get('carbohydrate', 0))
    fiber = float(serving.get('fiber', 0))
    fat = float(serving.get('fat', 0))
    protein = float(serving.get('protein', 0))
    sugar = float(serving.get('sugar', 0)) 
    calories = serving.get('calories', '0')
    ingredients_text = details.get('ingredients', 'N/A').lower()
    net_carbs = max(0, carbs - fiber)
    
    # --- FUTURE CALCULATION ---
    keto_prime_score = calculate_keto_prime_score(net_carbs, fat, protein, ingredients_text)
    
    # Score Visualizer (Health Bar)
    # 0-3: 🔴 | 4-6: 🟡 | 7-10: 🟢
    score_emoji = "🔴"
    if keto_prime_score > 4: score_emoji = "🟡"
    if keto_prime_score > 7: score_emoji = "🟢"

    # Hidden Sugars
    warnings = []
    if ingredients_text != 'n/a':
        for bad_sugar in HIDDEN_SUGARS:
            if bad_sugar in ingredients_text:
                warnings.append(bad_sugar.title())
    
    warning_block = ""
    if warnings:
        warning_str = ", ".join(warnings)
        warning_block = f"\n⚠️ **HIDDEN SUGAR WARNING**\nDetected: _{warning_str}_\n"

    text_response = (f"🍽 **{food_name.upper()}**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"{score_emoji} **KETO PRIME SCORE: {keto_prime_score}/10**\n"
            f"{warning_block}\n"
            f"📊 **NUTRITION**\n"
            f"• Net Carbs: `{net_carbs:.1f}g`\n"
            f"• Fat: `{fat:.0f}g` | Protein: `{protein:.0f}g`\n"
            f"• Calories: `{calories}`\n"
            f"_(Per: {serving.get('serving_description', 'serving')})_")

    # Return the clean stats for the database to use
    raw_stats = {
        'net_carbs': net_carbs,
        'fat': fat,
        'protein': protein,
        'calories': calories
    }

    return {
        "text": text_response,
        "image": image_url,
        "stats": raw_stats,
        "name": food_name
    }

def analyze_food_text(query):
    # Check Hacks
    clean_query = query.lower().strip()
    if clean_query in FAST_FOOD_HACKS:
        return {"text": FAST_FOOD_HACKS[clean_query], "image": None, "stats": None}

    # API Loop
    for attempt in range(5):
        token = get_access_token()
        if not token:
            time.sleep(2)
            continue 

        headers = {'Authorization': f'Bearer {token}'}
        api_url = "https://platform.fatsecret.com/rest/server.api"
        
        try:
            search_params = {'method': 'foods.search', 'search_expression': query, 'format': 'json', 'max_results': 5}
            res = requests.get(api_url, params=search_params, headers=headers)
            data = res.json()
            
            if 'error' in data:
                time.sleep(2)
                continue 

            foods_root = data.get('foods', {})
            food_list = foods_root.get('food', [])
            if isinstance(food_list, dict): food_list = [food_list]
            if not food_list: return {"text": f"❓ No match for '{query}'.", "image": None}

            for food_item in food_list:
                result_package = format_food_verdict(food_item['food_id'], food_item['food_name'], token)
                if result_package: return result_package

            return {"text": f"⚠️ No nutrition data for '{query}'.", "image": None}

        except Exception as e:
            time.sleep(2) 
            continue 
            
    return {"text": "⚠️ Connection unstable.", "image": None}

def analyze_barcode_image(image_bytes):
    try:
        img = Image.open(io.BytesIO(image_bytes))
        results = zxingcpp.read_barcodes(img)
        if not results: return {"text": "📸 No barcode found. Try again closer!", "image": None}
        
        barcode_data = results[0].text
        token = get_access_token()
        if not token: return {"text": "⚠️ API Auth failed.", "image": None}

        headers = {'Authorization': f'Bearer {token}'}
        api_url = "https://platform.fatsecret.com/rest/server.api"
        params = {'method': 'food.find_id_for_barcode', 'barcode': barcode_data, 'format': 'json'}
        res = requests.get(api_url, params=params, headers=headers)
        data = res.json()

        food_id = data.get('food_id', {}).get('value')
        if not food_id or food_id == "0":
             return {"text": f"📦 Barcode `{barcode_data}` not found in database.", "image": None}

        result_package = format_food_verdict(food_id, "SCANNED PRODUCT", token)
        if result_package: return result_package
        else: return {"text": "❌ Found barcode, but missing data.", "image": None}

    except Exception as e:
        return {"text": f"⚠️ Error: {str(e)}", "image": None}