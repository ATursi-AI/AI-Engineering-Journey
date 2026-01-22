import requests
import time

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
    # RETRY LOOP: IP Stability (Preserving T-Mobile Fix)
    for attempt in range(5):
        token = get_access_token()
        if not token:
            time.sleep(2)
            continue 

        headers = {'Authorization': f'Bearer {token}'}
        api_url = "https://platform.fatsecret.com/rest/server.api"
        
        try:
            # --- STEP 1: SEARCH ---
            search_params = {
                'method': 'foods.search',
                'search_expression': query,
                'format': 'json',
                'max_results': 5 
            }
            res = requests.get(api_url, params=search_params, headers=headers)
            data = res.json()
            
            if 'error' in data:
                print(f"⚠️ Search Blocked ({attempt+1}/5): {data['error']['message']}")
                time.sleep(2)
                continue 

            foods_root = data.get('foods', {})
            food_list = foods_root.get('food', [])

            if isinstance(food_list, dict):
                food_list = [food_list]
            
            if not food_list:
                return f"❓ I couldn't find any match for '{query}'."

            # --- STEP 2: DETAILS LOOP ---
            for food_item in food_list:
                food_id = food_item['food_id']
                food_name = food_item['food_name']
                
                detail_params = {'method': 'food.get.v2', 'food_id': food_id, 'format': 'json'}
                res_detail = requests.get(api_url, params=detail_params, headers=headers)
                details_data = res_detail.json()
                
                if 'error' in details_data:
                     raise Exception(f"IP Blocked during Detail Fetch: {details_data['error']['message']}")

                details = details_data.get('food', {})
                servings_obj = details.get('servings', {}).get('serving', [])
                
                if not servings_obj:
                    continue 
                
                # Get Primary Serving
                serving = servings_obj[0] if isinstance(servings_obj, list) else servings_obj
                
                # --- DATA EXTRACTION ---
                carbs = float(serving.get('carbohydrate', 0))
                fiber = float(serving.get('fiber', 0))
                fat = float(serving.get('fat', 0))
                protein = float(serving.get('protein', 0))
                sugar = float(serving.get('sugar', 0)) 
                calories = serving.get('calories', '0')
                
                net_carbs = max(0, carbs - fiber)
                
                # --- LOGIC ENGINE ---
                
                # KETO VERDICT
                keto_status = ""
                if net_carbs <= 4:
                    keto_status = "🟢 Strict Keto"
                elif net_carbs <= 9:
                    keto_status = "🟡 Dirty Keto (Moderate)"
                else:
                    keto_status = "🔴 Avoid for Keto"

                # ATKINS VERDICT (Phase logic)
                atkins_status = ""
                if net_carbs <= 5:
                    atkins_status = "✅ Phase 1 (Induction) Friendly"
                elif net_carbs <= 12:
                    atkins_status = "⚠️ Phase 2 (Balancing) Only"
                else:
                    atkins_status = "🚫 Maintenance Phase Only"

                # --- OUTPUT GENERATION ---
                return (f"🍽 **{food_name.upper()}**\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"🥑 **VERDICT**\n"
                        f"Keto: {keto_status}\n"
                        f"Atkins: {atkins_status}\n\n"
                        f"📊 **NUTRITION**\n"
                        f"• Net Carbs: `{net_carbs:.1f}g`\n"
                        f"• Fiber: `{fiber:.1f}g` | Sugar: `{sugar:.1f}g`\n"
                        f"• Fat: `{fat:.0f}g` | Protein: `{protein:.0f}g`\n"
                        f"• Calories: `{calories}`\n"
                        f"_(Per: {serving.get('serving_description', 'serving')})_")

            return f"⚠️ I found 5 entries for '{query}', but they were empty."

        except Exception as e:
            print(f"DEBUG ERROR: {e}")
            time.sleep(2) 
            continue 
            
    return "⚠️ Connection unstable. Please try again."