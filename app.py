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
genai.configure(api_key="AIzaSyBrNu40flvWuEt18lIIrRtCYwKO2IL9Tso")  # Replace with your actual API key
vertex_credentials = service_account.Credentials.from_service_account_file("VertexAI_credentials.json")

PROJECT_ID = "apt-terrain-449617-a4"
LOCATION = "us-central1"  
ENDPOINT_ID = "6548578005336195072"

def predict_with_vertex_ai(input_data):
    endpoint = aiplatform.Endpoint(endpoint_name=f"projects/{PROJECT_ID}/locations/{LOCATION}/endpoints/{ENDPOINT_ID}")

    instance = {"struct": input_data}  # Wrapping in "struct" may be required
    response = endpoint.predict(instances=[instance])  # Ensure list format

    return response.predictions[0] if response.predictions else "No response from model."



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



# EMISSION_FACTORS = {
#     "Canada": {
#         "Transportation": 0.12,  # kgCO2/km
#         "Electricity": 0.15,  # kgCO2/kWh
#         "Diet": 2.5,  # kgCO2/meal
#         "Waste": 0.2  # kgCO2/kg
#     }
# }


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



input_data = {
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
}

if st.button("Calculate Carbon Emission"):
    prediction = predict_with_vertex_ai(input_data)
    st.header("📊 Carbon Emission Results")
    st.success(f"Your estimated carbon emission: {prediction} tonnes CO2 per month")

    # col3, col4 = st.columns(2)

    # with col3:
    #     st.subheader("Carbon Emissions by Category")
    #     st.info(f"🚗 Transportation: {transportation_emissions} tonnes CO2 per year")
    #     st.info(f"💡 Electricity: {electricity_emissions} tonnes CO2 per year")
    #     st.info(f"🍽️ Diet: {diet_emissions} tonnes CO2 per year")
    #     st.info(f"🗑️ Waste: {waste_emissions} tonnes CO2 per year")

    # with col4:
    #     st.subheader("Total Carbon Footprint")
    #     st.success(f"🌍 Your total carbon footprint is: {total_emissions} tonnes CO2 per year")
    #     st.warning("In 2021, CO2 emissions per capita for Canada was 1.9 tons of CO2 per capita.")

    average_canadian_carbon_footprint = 1.46  
    prompt = f"""
    My total carbon footprint is {prediction} tonnes CO2 per month.
    - Transportation: {transport} tonnes
    - Electricity: {energy_efficiency} 
    - Diet: {diet} tonnes
    - Waste: {waste_bag_count} bags
    - Recycling: {', '.join(recycling)}  # Materials recycled (if applicable)
    - Vehicle Type: {vehicle_type}
    - Social Activity: {social_activity} events per month
    - Monthly Grocery Bill: ${grocery_bill}
    - Frequency of Air Travel: {air_travel_frequency} flights per month
    - Vehicle Monthly Distance: {vehicle_distance} km
    - Waste Bag Size: {waste_bag_size} liters
    - Waste Bag Weekly Count: {waste_bag_count}
    - Screen Time (TV/PC): {screen_time} hours per day
    - New Clothes Monthly: {new_clothes} items
    - Internet Usage: {internet_usage} hours per day
    - Energy Efficiency Rating: {energy_efficiency} (out of 10)
    
    Please provide:
    1. A full report of my carbon footprint based on the provided factors.
    2. A short summary of my carbon footprint.
    3. Practical tips on how I can reduce my carbon footprint.
"""

    # Plotting carbon footprint comparison
    fig, ax = plt.subplots()
    categories = ["Your Carbon Footprint", "Avg Canadian Footprint"]
    values = [prediction, average_canadian_carbon_footprint]

    ax.bar(categories, values, color=['green', 'blue'])
    ax.set_ylabel("Tonnes of CO2 per month")
    ax.set_title("Carbon Footprint Comparison")

    # Convert plot to image
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    image = Image.open(buf)

    # Display chart in Streamlit
    st.image(image, caption="Your Carbon Footprint vs. Average Canadian Footprint")


    try:
        # AI response
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        st.subheader("🤖 AI-Generated Summary & Suggestions")
        st.write(response.text)

        # Save results to Google Docs
        st.subheader("📄 Save Results to Google Docs")
        doc_content = f"Carbon Footprint Summary:\n\n{response.text}\n\nEmissions:\nTotal: {prediction} tonnes CO2 per year"
        
        # Authenticate and create a Google Doc
        service = authenticate_google_docs()
        doc_id = create_google_doc(service, doc_content)
        if doc_id:
            st.success(f"✅ Results saved to Google Docs: [View Document](https://docs.google.com/document/d/{doc_id})")
        else:
            st.error("⚠️ Failed to save to Google Docs.")

    except Exception as e:
        st.error("⚠️ Error generating AI response. Check API key and connection.")
