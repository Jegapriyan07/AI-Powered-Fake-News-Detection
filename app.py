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
