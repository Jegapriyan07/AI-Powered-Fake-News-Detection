import os
import google.generativeai as genai
import random
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- App Setup ---
app = Flask(__name__)
# Allow requests from your frontend
# Note: For production, you might want to restrict origins further or use environment variables
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5500", "http://localhost:5500", "https://*.vercel.app"]}})

# --- AI Configuration ---
try:
    # Get API key from environment variable (Securely)
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    
    if not GEMINI_API_KEY:
        print("Warning: GEMINI_API_KEY not found in environment variables.")
    else:
        genai.configure(api_key=GEMINI_API_KEY)

    # Configure models - UPDATED TO VALID STABLE MODEL NAME
    # This specific version solves the 404 'model not found' issue.
    generation_model = genai.GenerativeModel('gemini-1.5-flash-002')
    
    # Tool configuration
    grounding_model = genai.GenerativeModel(
        'gemini-1.5-flash-002', 
        tools=[genai.types.Tool(google_search_retrieval={})]
    )
    
    print("Gemini models configured successfully.")

except Exception as e:
    # DO NOT EXIT - Log the error but let the app start
    print(f"Error configuring Gemini: {e}")
    generation_model = None
    grounding_model = None

# --- Helper Function: Simulate ML Model (from original JS) ---
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
        return "Error: AI model not configured correctly (check API key).", None

    try:
        # Check if the model has a 'tools' attribute. If not, pass None.
        model_tools = model.tools if hasattr(model, 'tools') else None
        
        # Create a new model instance for each request
        model_instance = genai.GenerativeModel(
            model.model_name,
            system_instruction=system_prompt,
            tools=model_tools  # Use the checked model_tools variable
        )
        response = model_instance.generate_content(user_query)
        
        # Check if model_tools is not None before checking for grounding metadata
        if model_tools and response.candidates and response.candidates[0].grounding_metadata.grounding_attributions:
            return response.text, response.candidates[0].grounding_metadata.grounding_attributions

        return response.text, None

    except Exception as e:
        print(f"Gemini API call failed: {e}")
        # Check if response exists and has feedback
        if 'response' in locals() and hasattr(response, 'prompt_feedback') and response.prompt_feedback.block_reason:
            return f"Error: Content blocked by safety settings. Reason: {response.prompt_feedback.block_reason.name}", None
        return f"Error: Could not get response from AI. Details: {str(e)}", None

# --- API Endpoints ---
