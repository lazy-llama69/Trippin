import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import pdfplumber
from itinerary import generate_pdf, convert_markdown_to_html
# Load environment variables from .env file
load_dotenv()

# Configure Gemini API key from environment variable
# api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=st.secrets['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-2.0-flash')
# Function to extract text from PDF
def extract_pdf_text(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()  # Extract text from each page
    return text

def glowing():
    # Streamlit UI for PDF upload
    itinerary = st.chat_input("Paste your itinerary here")
    uploaded_file = st.file_uploader("Upload a PDF itinerary", type="pdf")

    if uploaded_file is not None:
        # Display the file name and basic file info
        st.write(f"File Name: {uploaded_file.name}")
        
        # Extract text from the uploaded PDF
        itinerary = extract_pdf_text(uploaded_file)
        
    # st.text_area("Extracted Text", pdf_text, height=300)
    prompt = f"""
    You are a highly skilled travel assistant. You have been given a raw travel itinerary that may be incomplete, unorganized, or lacking in details. Your task is to:

    1. Analyze the itinerary and ensure it has a clear structure.
    2. Improve the organization and readability by following the example format. 
    3. Suggest any additional activities, tourist attractions, or dining options that could enhance the experience.
    4. Ensure that the details match the preferences of the trip and there are no discrepancies
    5. Adjust the tone to make it more engaging and fun for travelers. 

    Here is the raw itinerary text (without any changes):

    {itinerary}

    Here is a example of the format to be followed leniently for the **revised itinerary**
    **Travel Name**: "Journey to Paris: A Culinary Adventure"

    #Day 1: Arrival in Paris \n
    10:00-11:00 | Visit the **Eiffel Tower** \n
    11:00-11:30 | Enjoy a meal at **Le Cinq** (Michelin Star restaurant) \n
    11:30-12:00 | Relax at **Tuileries Gardens** \n
    
    
    #Day 2: Exploring Marrakech \n
    10:00-12:00 | Visit the iconic **Jardin Majorelle** \n
    12:00-13:30 | Discover the historic **Bahia Palace** \n
    13:30-15:30 | Explore the bustling **Jemaa el-Fnaa** square \n
    15:30-16:30 | Try tasty street food at Food Stalls in **Jemaa el-Fnaa** \n

    
    #Day 3: Sweet Sights and Sounds \n
    08:00-10:00 | Explore Gummy Bear Forest \n
    10:00-12:00 | Visit the Marshmallow Mountains \n
    18:00-22:00 | Lunch at Caramel Cove \n

    
    #Day 4: Chocolate River Cruise \n
    08:00-10:00 | Scenic Chocolate River Cruise \n
    10:00-11:00 | Discover the Rock Candy Caves \n
    11:00-18:00 | Indulge in a Chocolate Fondue Party at Choco Lagoon \n

    
    #Day 5: Farewell to the Sweet Paradise \n
    08:00-10:00 | Breakfast at Pancake Palace \n
    10:00-12:00 | Last-minute shopping at the Bonbon Bazaar \n
    12:00-20:00 | Sweet Departure with Goodie Bag from Wonka's Factory Shop \n
    
    #Additional Suggestions:
    bullet point: Buy Myki card for the Australian public transport
    bullet point: Take off your shoes when entering people's homes. 

    Your goal is to create a **revised itinerary** that is well-organized, more engaging, and has additional recommendations for each day. Make sure to break it down day by day and make each activity exciting.
    """
    # Check if the PDF was successfully processed
    if itinerary:
        st.write("PDF extracted successfully. Sending it to Gemini for improvement...")

        # Generate response using Gemini API
        try:
            response = model.generate_content(
                prompt,  
                generation_config=genai.types.GenerationConfig(
                    temperature=1.5, 
                ),
            )
            
            # Display the assistant's improved itinerary
            st.subheader("Improved Itinerary:")
            st.write(response.text)
            formatted_itinerary = convert_markdown_to_html(response.text)
            pdf = generate_pdf(formatted_itinerary)
            st.write("")
            st.download_button("Download Itinerary as PDF", data=pdf, file_name="itinerary.pdf", mime="application/pdf",type="primary")
        except Exception as e:
            st.error(f"Error generating response: {e}")
    else:
        st.error("No text extracted from the PDF. Please upload a valid PDF with text.")


        

