import os
import streamlit as st
import google.generativeai as genai
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
from google.oauth2 import service_account
import google.cloud.aiplatform as aiplatform
import base64

# Define the scopes for Google Docs API
SCOPES = ['https://www.googleapis.com/auth/documents']
genai.configure(api_key="your-api-key")  # Replace with your actual API key
vertex_credentials = service_account.Credentials.from_service_account_file("VertexAI_credentials.json")
vertex_credential_path = "./Hackathon_GDSC/VertexAI_credentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = vertex_credential_path

PROJECT_ID = "your-vertexAI-projectID"
LOCATION = "us-central1"  
ENDPOINT_ID = "your-vertexAI-endpointID"
 

def predict_with_vertex_ai(input_data):
    endpoint = aiplatform.Endpoint(endpoint_name=f"projects/{PROJECT_ID}/locations/{LOCATION}/endpoints/{ENDPOINT_ID}")

    instance = input_data  # Wrapping in "struct" may be required
    response = endpoint.predict(instances=instance)  # Ensure list format

    return response.predictions[0]



def authenticate_google_docs():
    """Authenticate and return the Google Docs API service."""
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=52022)
    return build("docs", "v1", credentials=creds)

def create_google_doc(service, content):
    """Create a new Google Doc with the provided content."""
    try:
        doc = service.documents().create().execute()
        document_id = doc["documentId"]

        # Insert content into the document
        service.documents().batchUpdate(
            documentId=document_id,
            body={"requests": [{"insertText": {"location": {"index": 1}, "text": content}}]}
        ).execute()

        return document_id
    except HttpError as err:
        print(f"Error creating document: {err}")
        return None


# Set wide layout and page name
st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")

# Streamlit app code
st.title("Personal Carbon Calculator App ⚠️")

# User inputs
st.subheader("👤 Body Type")
body_type = st.selectbox("Select", ["underweight", "normal", "obese", "overweight"])

st.subheader("⚧️ Sex")
sex = st.selectbox("Select", ["Male", "Female"])

st.subheader("🥗 Diet")
diet = st.selectbox("Select", ["vegetarian", "vegan", "omnivore", "pescatarian"])

st.subheader("🚿 Shower Frequency (Times per Day)")
shower_frequency = st.selectbox("Select", ["less frequently", "more frequently", "daily", "twice a day"])

st.subheader("🔥 Heating Energy Source")
heating_source = st.selectbox("Select", ["natural gas", "wood", "coal", "electricity"])

st.subheader("🚗 Transport Mode")
transport = st.selectbox("Select", ["walk/bicycle", "public", "private", "Walking"])


st.subheader("🎉 Social Activity")
social_activity = st.selectbox("Select", ["never", "sometimes", "often"])

st.subheader("🛒 Monthly Grocery Bill ($)")
grocery_bill = st.number_input("Enter Amount", min_value=0, value=0)

st.subheader("✈️ Air Travel (Flights per Month)")
air_travel_frequency = st.selectbox("Select", ["never", "rarely", "frequently", "very frequently"])

st.subheader("🚗 Vehicle Monthly Distance (Km)")
vehicle_distance = st.slider("Km", 0, 20000, 0, key="vehicle_distance_slider")

st.subheader("🗑️ Waste Bag Size (Liters)")
waste_bag_size = st.selectbox("Select", ["small", "medium", "large", "extra large"])

st.subheader("♻️ Waste Bag Weekly Count")
waste_bag_count = st.slider("Count", 0, 10, 0, key="waste_bag_count_slider")

st.subheader("📺 TV/PC Usage (Hours per Day)")
screen_time = st.slider("Hours", 0, 24, 0, key="screen_time_slider")

st.subheader("👕 New Clothes Purchased Monthly")
new_clothes = st.slider("Count", 0, 500, 0, key="new_clothes_slider")

st.subheader("🌐 Internet Usage (Hours per Day)")
internet_usage = st.slider("Hours", 0, 24, 0, key="internet_usage_slider")

st.subheader("⚡ Energy Efficiency ")
energy_efficiency = st.selectbox("Select", ["No", "Sometimes", "Yes"])



# Ensure all values are explicitly converted to strings
input_data = [{
    "Body_Type": str(body_type),
    "Sex": str(sex),
    "Diet": str(diet),
    "How_Often_Shower": str(shower_frequency),
    "Heating_Energy_Source": str(heating_source),
    "Transport": str(transport),
    "Social_Activity": str(social_activity),
    "Monthly_Grocery_Bill": str(grocery_bill),
    "Frequency_of_Traveling_by_Air": str(air_travel_frequency),
    "Vehicle_Monthly_Distance_Km": str(vehicle_distance),
    "Waste_Bag_Size": str(waste_bag_size),
    "Waste_Bag_Weekly_Count": str(waste_bag_count),
    "How_Long_TV_PC_Daily_Hour": str(screen_time),
    "How_Many_New_Clothes_Monthly": str(new_clothes),
    "How_LongInternet_Daily_Hour": str(internet_usage),
    "Energy_efficiency": str(energy_efficiency)
}]

prompt = f"""
    
    Please provide:
    1. A short summary of average Canadian.
    2. Practical tips on how I can reduce my carbon footprint.
"""
try:
  
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        st.subheader("🤖 AI-Generated Summary & Suggestions")
        st.write(response.text)

        # Save results to Google Docs
        st.subheader("📄 Save Results to Google Docs")
        doc_content = f"Carbon Footprint Summary:\n\n{response.text}\n"
        
        # Authenticate and create a Google Doc
        service = authenticate_google_docs()
        doc_id = create_google_doc(service, doc_content)
        if doc_id:
            st.success(f"✅ Results saved to Google Docs: [View Document](https://docs.google.com/document/d/{doc_id})")
        else:
            st.error("⚠️ Failed to save to Google Docs.")

except Exception as e:
        st.error("⚠️ Error generating AI response. Check API key and connection.")


# Function to pass the data to the model and handle the prediction
if st.button("Calculate Carbon Emission"):
    try:
        prediction = predict_with_vertex_ai(input_data)  # Pass as list of strings
        st.header("📊 Carbon Emission Results")
        prediction_value = prediction.get("value", 0) 
        prediction_value = prediction_value/360
        st.success(f"Your estimated carbon emission: {prediction_value} tonnes CO2 per month")
        
        st.subheader("📊 Carbon Footprint Comparison")
        st.bar_chart({
            "Your Carbon Footprint": [prediction_value],
            "Average Canadian Footprint": [14.3]
        })
        
    except Exception as e:
        st.error(f"Error in prediction: {e}")
