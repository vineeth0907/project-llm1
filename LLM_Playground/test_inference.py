import requests
import json

HUGGINGFACE_TOKEN = "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"  # Replace with your actual token

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_TOKEN}"
}

MODEL_ENDPOINTS = {
    "mistralai/Mistral-7B-Instruct-v0.1": "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
    "mistralai/Mistral-7B-Instruct-v0.2": "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
}

def get_chat_response(model_name, messages):
    prompt = ""
    for msg in messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        prompt += f"{role}: {msg['content']}\n"
    prompt += "Assistant:"

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7,
            "do_sample": True,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(MODEL_ENDPOINTS[model_name], headers=headers, json=payload, timeout=30)
        
        # Handle non-200 status codes
        if response.status_code != 200:
            try:
                error_data = response.json()
                error_msg = error_data.get('error', 'Unknown error')
            except json.JSONDecodeError:
                error_msg = f"HTTP {response.status_code}: {response.text[:100]}"
            return f"❌ API Error: {error_msg}"
        
        # Try to parse JSON response
        try:
            result = response.json()
        except json.JSONDecodeError as e:
            return f"❌ JSON Parse Error: Invalid response from API - {str(e)}"
        
        # Extract generated text
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "").strip()
        elif isinstance(result, dict):
            return result.get("generated_text", "").strip()
        else:
            return f"❌ Unexpected Response Format: {str(result)[:100]}"
            
    except requests.exceptions.Timeout:
        return "❌ Timeout Error: Request took too long (>30 seconds)"
    except requests.exceptions.ConnectionError:
        return "❌ Connection Error: Could not connect to Hugging Face API"
    except requests.exceptions.RequestException as e:
        return f"❌ Request Error: {str(e)}"
    except Exception as e:
        return f"❌ Unexpected Error: {str(e)}" 