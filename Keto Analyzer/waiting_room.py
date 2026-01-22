import requests

# --- CREDENTIALS ---
CLIENT_ID = "b826e72b8a094b7abbbbe03569a28dcd"
CLIENT_SECRET = "0693d8c758424dae80d7c47c824083c2"

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

def analyze_food_text(query):
    token = get_access_token()
    if not token:
        return "⚠️ Auth Error: My 'Passport' was rejected."

    headers = {'Authorization': f'Bearer {token}'}
    api_url = "https://platform.fatsecret.com/rest/server.api"
    
    try:
        # 1. Search for the food
        search_params = {
            'method': 'foods.search',
            'search_expression': query,
            'format': 'json',
            'max_results': 1
        }
        res = requests.get(api_url, params=search_params, headers=headers)
        data = res.json()
        
        # DEBUG: See the search result
        print(f"DEBUG: Search Result: {data}")

        foods_root = data.get('foods', {})
        food_list = foods_root.get('food')

        if not food_list:
            return f"❓ I couldn't find '{query}'."
        
        # Handle list vs dictionary
        target = food_list[0] if isinstance(food_list, list) else food_list
        food_id = target.get('food_id')
        food_name = target.get('food_name', 'Unknown')

        # 2. Get nutrition details
        detail_params = {
            'method': 'food.get.v2',
            'food_id': food_id,
            'format': 'json'
        }
        res_detail = requests.get(api_url, params=detail_params, headers=headers)
        details = res_detail.json().get('food', {})
        
        # DEBUG: See the nutrition data (This helps us verify the serving list)
        print(f"DEBUG: Nutrition Data for {food_name}: {details}")

        servings_root = details.get('servings', {})
        servings_data = servings_root.get('serving', [])
        
        # --- THE FIX: SAFETY CHECK FOR EMPTY LISTS ---
        if isinstance(servings_data, list) and len(servings_data) == 0:
            return f"⚠️ Found '{food_name}', but it has no serving data listed in the database."

        # Pick the first serving safely
        serving = servings_data[0] if isinstance(servings_data, list) else servings_data
        
        if not serving:
            return f"❓ Found '{food_name}', but nutritional info is blank."

        # 3. Keto Logic
        carbs = float(serving.get('carbohydrate', 0))
        fiber = float(serving.get('fiber', 0))
        net_carbs = max(0, carbs - fiber)
        
        status = "✅ Phase 1 (Keto Friendly)" if net_carbs <= 3 else "🔴 Phase 3/4 (High Carb)"

        return (f"🥗 **{food_name.upper()}**\n"
                f"Net Carbs: {net_carbs:.1f}g\n"
                f"Atkins Status: {status}\n"
                f"Serving: {serving.get('serving_description', '1 serving')}")

    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        return f"❓ Technical hiccup with '{query}'. Check terminal."