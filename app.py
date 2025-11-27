import os
import google.generativeai as genai
import random
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- App Setup ---
app = Flask(__name__)
# Allow requests from your frontend
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5500", "http://localhost:5500", "https://*.vercel.app"]}})

# --- AI Configuration ---
try:
    # 1. SECURITY FIX: Get API key from Vercel's environment variables
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    
    if not GEMINI_API_KEY:
        print("Warning: GEMINI_API_KEY not found in environment variables.")
    else:
        genai.configure(api_key=GEMINI_API_KEY)

    # 2. FINAL STABILITY FIX: Use the most actively supported and stable Gemini 2.5 Flash alias 
    generation_model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Tool configuration for search grounding
    grounding_model = genai.GenerativeModel(
        'gemini-2.5-flash', 
        tools=[genai.types.Tool(google_search_retrieval={})]
    )
    
    print("Gemini models configured successfully.")

except Exception as e:
    # 3. CRASH FIX: Log the error, but set models to None instead of crashing the server
    print(f"Error configuring Gemini: {e}")
    generation_model = None
    grounding_model = None

# --- Helper Function: Simulate ML Model (for initial verdict) ---
def simulate_ml_model(text):
    fake_keywords = ['hoax', 'shocking', 'unbelievable', 'conspiracy', 'deep state']
    real_keywords = ['reported', 'according to', 'study finds', 'official', 'government']
    
    score = 0.5  # Neutral
    text_lower = text.lower()
    
    for kw in fake_keywords:
        if kw in text_lower:
            score -= 0.3
    for kw in real_keywords:
        if kw in text_lower:
            score += 0.2
            
    score += (random.random() - 0.5) * 0.2
    
    label = "Fake" if score < 0.5 else "Real"
    confidence = (1 - score) * 100 if label == "Fake" else score * 100
    confidence = max(60, min(99, confidence))
    
    return {"label": label, "confidence": round(confidence)}

# --- Helper Function: Generic Gemini Call (FIXED) ---
def call_gemini(model, system_prompt, user_query):
    if not model:
        return "Error: AI model not configured correctly (API key missing or configuration failed).", None

    try:
        model_tools = model.tools if hasattr(model, 'tools') else None
        
        model_instance = genai.GenerativeModel(
            model.model_name,
            system_instruction=system_prompt,
            tools=model_tools
        )
        response = model_instance.generate_content(user_query)
        
        # Check if model_tools is not None before checking for grounding metadata
        if model_tools and response.candidates and response.candidates[0].grounding_metadata and response.candidates[0].grounding_metadata.grounding_attributions:
            return response.text, response.candidates[0].grounding_metadata.grounding_attributions

        return response.text, None

    except Exception as e:
        print(f"Gemini API call failed: {e}")
        # Check if response exists and has feedback
        if 'response' in locals() and hasattr(response, 'prompt_feedback') and response.prompt_feedback.block_reason:
            return f"Error: Content blocked by safety settings. Reason: {response.prompt_feedback.block_reason.name}", None
        return f"Error: Could not get response from AI. Details: {str(e)}", None

# --- API Endpoints ---

@app.route("/")
def health_check():
    return "NEOTRUTH Backend API is running!"

@app.route("/analyze", methods=['POST'])
def analyze_text():
    text = request.json.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # 1. Simulate ML Model
        ml_result = simulate_ml_model(text)
        
        # 2. Get AI Explanation
        system_prompt = f"""You are an expert fact-checker. A user has provided a news snippet, and an ML model has classified it as "{ml_result['label']}".
Your job is to provide a brief, human-friendly explanation of WHY the text might be considered {ml_result['label']}.
Focus on common red flags (e.g., emotional language, lack of sources) or green flags (e.g., neutral tone, cited sources).
DO NOT simply agree with the model. Provide independent reasoning. Keep it to 2-3 sentences."""
        
        explanation, _ = call_gemini(generation_model, system_prompt, text)
        
        # 3. Combine and return
        result = {
            "label": ml_result['label'],
            "confidence": ml_result['confidence'],
            "explanation": explanation
        }
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in /analyze: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/bias", methods=['POST'])
def check_bias():
    text = request.json.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    system_prompt = "You are a neutral political and media analyst. Analyze the following text for any potential bias (e.g., political, commercial, selection bias, emotional language). State your findings clearly. If no significant bias is found, state that. Be concise."
    
    bias_report, _ = call_gemini(generation_model, system_prompt, text)
    
    return jsonify({"report": bias_report})

@app.route("/sources", methods=['POST'])
def find_sources():
    text = request.json.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    system_prompt = "You are a research assistant. Based on the user's text, find 3-5 recent, credible news articles or reports from reputable sources that discuss the same core topic. Provide only the title and the URL for each. Do not analyze the user's text."
    user_query = f"Find credible sources related to this topic: {text}"
    
    # This uses the grounding model with the Google Search tool
    text_response, sources = call_gemini(grounding_model, system_prompt, user_query)
    
    formatted_sources = []
    if sources:
        for source in sources:
            # The structure of grounding_attributions is .web
            if source.web:
                formatted_sources.append({
                    "uri": source.web.uri,
                    "title": source.web.title or "No Title Found"
                })

    # Fallback to text if no structured sources
    if not formatted_sources and text_response:
        return jsonify({"sources": [], "text_fallback": text_response})

    return jsonify({"sources": formatted_sources, "text_fallback": text_response})

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)
