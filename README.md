### Project Summary: NEOTRUTH - AI Powered Fake News Detector

This project is a full-stack, serverless application that combines traditional Machine Learning logic with advanced Generative AI to provide real-time analysis and fact-checking of news text.

**Key Technical Achievements:**

* **Full-Stack Deployment:** Successfully deployed a monorepo containing a static HTML/JS frontend and a Python Flask API backend to a single Vercel domain, using advanced `vercel.json` routing configurations.
* **Secure API Integration:** Implemented secure authentication by migrating the application to fetch sensitive API keys (`GEMINI_API_KEY`) from Vercel's Environment Variables, eliminating security risks and deployment failures associated with hardcoded secrets.
* **Multimodal AI Service:** Utilizes Google's Gemini API to power three core endpoints:
    * **Classification:** Provides a fast, initial 'Real' or 'Fake' verdict (simulated ML model).
    * **AI Explanation:** Uses `gemini-1.5-flash` to generate a journalistic critique of the text (tone, source legitimacy, bias).
    * **Grounding:** Uses the Search Tool (Grounding) feature to fetch relevant, up-to-date sources from the web for validation.
* **Error Stability:** Implemented robust Python exception handling to prevent server crashes (`500 Internal Server Error`) and successfully resolved persistent **404 Model Not Found errors** by identifying and migrating to the correct, stable model version (`gemini-1.5-flash-002`).
