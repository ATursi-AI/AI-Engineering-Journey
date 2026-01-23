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

# --- CORE LOGIC: THE JUDGE ---
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
    
    # --- NEW: IMAGE EXTRACTION ---
    # FatSecret hides images in a specific 'food_images' wrapper
    image_url = None
    images = details.get('food_images', {}).get('food_image', [])
    if isinstance(images, list) and len(images) > 0:
        image_url = images[0].get('image_url') # Get first image
    elif isinstance(images, dict):
        image_url = images.get('image_url')

    if not servings_obj:
        return None
    
    # Get Primary Serving
    serving = servings_obj[0] if isinstance(servings_obj, list) else servings_obj
    
    # Data Extraction
    carbs = float(serving.get('carbohydrate', 0))
    fiber = float(serving.get('fiber', 0))
    fat = float(serving.get('fat', 0))
    protein = float(serving.get('protein', 0))
    sugar = float(serving.get('sugar', 0)) 
    calories = serving.get('calories', '0')
    ingredients_text = details.get('ingredients', 'N/A').lower()

    net_carbs = max(0, carbs - fiber)
    
    # Verdict Logic
    keto_status = ""
    if net_carbs <= 4:
        keto_status = "🟢 Strict Keto"
    elif net_carbs <= 9:
        keto_status = "🟡 Dirty Keto (Moderate)"
    else:
        keto_status = "🔴 Avoid for Keto"

    atkins_status = ""
    if net_carbs <= 5:
        atkins_status = "✅ Phase 1 (Induction) Friendly"
    elif net_carbs <= 12:
        atkins_status = "⚠️ Phase 2 (Balancing) Only"
    else:
        atkins_status = "🚫 Maintenance Phase Only"

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

    # --- FORMATTED TEXT ---
    text_response = (f"🍽 **{food_name.upper()}**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🥑 **VERDICT**\n"
            f"Keto: {keto_status}\n"
            f"Atkins: {atkins_status}\n"
            f"{warning_block}\n"
            f"📊 **NUTRITION**\n"
            f"• Net Carbs: `{net_carbs:.1f}g`\n"
            f"• Fiber: `{fiber:.1f}g` | Sugar: `{sugar:.1f}g`\n"
            f"• Fat: `{fat:.0f}g` | Protein: `{protein:.0f}g`\n"
            f"• Calories: `{calories}`\n"
            f"_(Per: {serving.get('serving_description', 'serving')})_")

    # Return a Dictionary (Package)
    return {
        "text": text_response,
        "image": image_url
    }

# --- MAIN FUNCTION 1: TEXT ANALYZER ---
def analyze_food_text(query):
    # 0. Check Hacks (Hacks don't have images yet, return text only)
    clean_query = query.lower().strip()
    if clean_query in FAST_FOOD_HACKS:
        return {"text": FAST_FOOD_HACKS[clean_query], "image": None}

    # API Loop
    for attempt in range(5):
        token = get_access_token()
        if not token:
            time.sleep(2)
            continue 

        headers = {'Authorization': f'Bearer {token}'}
        api_url = "https://platform.fatsecret.com/rest/server.api"
        
        try:
            # 1. Search
            search_params = {
                'method': 'foods.search',
                'search_expression': query,
                'format': 'json',
                'max_results': 5 
            }
            res = requests.get(api_url, params=search_params, headers=headers)
            data = res.json()
            
            if 'error' in data:
                time.sleep(2)
                continue 

            foods_root = data.get('foods', {})
            food_list = foods_root.get('food', [])

            if isinstance(food_list, dict):
                food_list = [food_list]
            
            if not food_list:
                return {"text": f"❓ I couldn't find any match for '{query}'.", "image": None}

            # 2. Loop through results until one works
            for food_item in food_list:
                result_package = format_food_verdict(food_item['food_id'], food_item['food_name'], token)
                if result_package:
                    return result_package

            return {"text": f"⚠️ I found entries for '{query}', but they had no nutritional data.", "image": None}

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(2) 
            continue 
            
    return {"text": "⚠️ Connection unstable. Please try again.", "image": None}

# --- MAIN FUNCTION 2: BARCODE ANALYZER ---
def analyze_barcode_image(image_bytes):
    try:
        # 1. Read Image
        img = Image.open(io.BytesIO(image_bytes))
        
        # 2. Decode Barcode (Using zxing-cpp)
        results = zxingcpp.read_barcodes(img)
        
        if not results:
            return {"text": "📸 I couldn't see a barcode clearly. Please try to get close, flat, and well-lit!", "image": None}
        
        barcode_data = results[0].text
        print(f"🔍 Scanned Barcode: {barcode_data}")

        # 3. Call API
        token = get_access_token()
        if not token:
            return {"text": "⚠️ API Auth failed.", "image": None}

        headers = {'Authorization': f'Bearer {token}'}
        api_url = "https://platform.fatsecret.com/rest/server.api"

        params = {
            'method': 'food.find_id_for_barcode',
            'barcode': barcode_data,
            'format': 'json'
        }
        res = requests.get(api_url, params=params, headers=headers)
        data = res.json()

        # 4. Check if Found
        food_id = data.get('food_id', {}).get('value')
        
        if not food_id or food_id == "0":
             return {"text": f"📦 I scanned barcode `{barcode_data}`, but it's not in my database yet.", "image": None}

        # 5. Get Verdict
        result_package = format_food_verdict(food_id, "SCANNED PRODUCT", token)
        if result_package:
            return result_package
        else:
            return {"text": "❌ Found the barcode, but nutrition data was missing.", "image": None}

    except Exception as e:
        return {"text": f"⚠️ Error processing image: {str(e)}", "image": None}