
# 🧠 NEOTRUTH – AI-Powered Fake News Detection System

### 🔍 Overview
**NEOTRUTH** is an **AI-driven web application** that automatically detects whether a news article, social media post, or headline is *real or fake*.  
The system uses **Google Gemini AI**, a simulated **ML model**, and **Firebase Firestore** for real-time data storage.  
It empowers users to analyze the credibility of any text while offering **AI explanations**, **bias checks**, and **credible sources**.

---

## 🚀 Features

### 📰 Core Features
- **AI News Classification** – Detects whether a news text is *Real* or *Fake* with confidence.
- **AI Explanation Engine** – Provides a 2–3 sentence reason behind the classification.
- **Bias Detection** – Analyzes emotional, political, or commercial bias.
- **Credible Source Finder** – Finds 3–5 reliable news links for the topic using Gemini tools.
- **History Tracking** – Stores all past analyses in Firebase Firestore.

### 💡 Tech Highlights
- **Frontend:** HTML5, Tailwind CSS, Lucide Icons, Firebase Firestore
- **Backend:** Flask (Python), Google Gemini Generative AI API
- **Integration:** RESTful API calls between frontend and backend
- **Database:** Firebase (Cloud Firestore)
- **Authentication:** Anonymous Firebase Auth

---

## 🧩 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | HTML, Tailwind CSS, JavaScript (ES Modules) |
| **Backend** | Flask (Python) |
| **AI Engine** | Google Gemini 2.5 Flash Preview |
| **Database** | Firebase Firestore |
| **Auth** | Firebase Anonymous Authentication |
| **Hosting (optional)** | Firebase Hosting / Render / Localhost |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/neotruth.git
cd neotruth
```

### 2️⃣ Backend Setup
#### Prerequisites:
- Python 3.10+
- Flask
- Google Generative AI SDK

#### Install Dependencies
```bash
pip install flask flask-cors google-generativeai
```

#### Run the Server
```bash
python app.py
```
Your backend runs at → `http://127.0.0.1:5000/`

---

### 3️⃣ Frontend Setup
#### Run the HTML File
Simply open `index.html` with **Live Server** in VS Code or any local web server:
```
127.0.0.1:5500/index.html
```

#### Firebase Configuration
Inside `index.html`, replace the placeholder Firebase config with your project credentials:
```js
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  ...
};
```

---

## 🧠 API Endpoints

| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/` | GET | Health check route |
| `/analyze` | POST | Detects whether the text is fake or real |
| `/bias` | POST | Detects bias or political leaning in the text |
| `/sources` | POST | Finds 3–5 credible sources for the topic |

### Example:
**POST /analyze**
```json
{
  "text": "Breaking! Aliens land in New York according to secret sources."
}
```

**Response:**
```json
{
  "label": "Fake",
  "confidence": 82,
  "explanation": "The text uses sensational words like 'Breaking' and 'secret sources', which are typical of unverified claims."
}
```

---

## 🧾 Folder Structure

```
📂 NEOTRUTH
 ┣ 📜 app.py                # Flask backend with Gemini API
 ┣ 📜 index.html            # Frontend web UI (Tailwind + Firebase)
 ┣ 📜 README.md             # Documentation
 ┗ 📂 static / assets (optional)
```

---

## 🧑‍💻 Team NEOTRUTH

| Name | Role | Responsibility |
|------|------|----------------|
| Member 1 | AI Engineer | Gemini API integration & ML simulation |
| Member 2 | Frontend Developer | UI/UX with Tailwind & Lucide |
| Member 3 | Backend Developer | Flask server & API endpoints |

---

## 🌐 Demo Flow

1. Paste a news article or social media post.  
2. Click **“Analyze Text”** → backend runs the ML + Gemini model.  
3. View:
   - ✅ Real / ❌ Fake result  
   - 💬 AI explanation  
   - 🧭 Bias report  
   - 🔗 Credible news links  
4. The result auto-saves to **Firebase History** for future reference.

---

## 🔒 Security Notes
- Do **not** hardcode API keys (move them to `.env` for production).
- Use `CORS` carefully — current setup allows requests from `localhost:5500`.
- Never expose your Gemini or Firebase credentials publicly.

---

## 🧭 Future Enhancements
- Chrome Extension for instant fact-checking  
- Multi-language fake news detection  
- Graph-based credibility scoring system  
- Real-time media sentiment heatmap  

---

## 🏁 License
This project is licensed under the **MIT License**.  
You’re free to use, modify, and distribute it with proper attribution.
