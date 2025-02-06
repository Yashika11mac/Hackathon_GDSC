# 🌍 EcoTrack AI - your personal carbon emissions calculator

## 📌 Overview
This project was developed during a hackathon to estimate a user's carbon footprint based on their lifestyle choices. We use **Vertex AI** to make predictions based on our own trained models, **Gemini API** to provide personalized recommendations, and **Google Docs API** to save the generated report for easy access and printing.

## 🚀 How It Works
1. Users input their lifestyle data (diet, travel habits, energy consumption, etc.).
2. The data is sent to **Vertex AI** via API, where a **custom-trained machine learning model** predicts their carbon emissions.
3. The **Gemini API** generates practical recommendations on reducing emissions.
4. The results are **saved to Google Docs** using 2-OAuth authentication, allowing users to print and display them as reminders.
   
## 📊 Model Performance (Vertex AI)
| Metric  |  Value  |
|---------|---------|
| MAE     | 272.374 |
| MAPE    |  13.154 |
| R²      |  0.798  |
| RMSE    | 472.668 |
| RMSLE   |  0.191  |

## 🛠️ Installation & Setup
### Prerequisites
- Python 3.8+
- Google Cloud account with Vertex AI & Docs API enabled
- Credentials JSON file for authentication

### Installation
1. Clone the repository:
   git clone https://github.com/Hackathon_GDSC.git
   cd Hackathon_GDSC
2. Install dependencies:
   pip install -r requirements.txt
3. Set up Google authentications
4. Run the streamlit app:
   streamlit run app.py

## 🤖 Technologies Used
- Streamlit (User Interface)
- Google Vertex AI (Machine Learning Model)
- Google Gemini API (AI-generated recommendations)
- Google Docs API (Saving reports)
OAuth 2.0 Authentication (Secure access)
