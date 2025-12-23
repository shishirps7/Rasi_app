import streamlit as st
# import json 
import datetime
import os
from dotenv import load_dotenv
from google import genai

# Page config
st.set_page_config(page_title="AI Astrology Consultation", page_icon="🔮")
st.title("🔮 AI Astrology Consultation")

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("GEMINI_API_KEY not found")
    st.stop()

# Initialize session state
if "show_form" not in st.session_state:
    st.session_state.show_form = True
if "response" not in st.session_state:
    st.session_state.response = None

# Show form if flag is True
if st.session_state.show_form:
    name = st.text_input("Enter your name")
    date = st.date_input(
        "Enter your date of birth",
        min_value=datetime.date(1800, 1, 1),
        max_value=datetime.date.today(),
    )
    time = st.time_input("Enter your time of birth")
    problem = st.text_area("What problems are you facing?")
    types_of_solution = st.text_area("What kind of solutions are you looking for?")

client = genai.Client()

# Submit button logic
if st.session_state.show_form and st.button("Submit"):
    if not name or not problem:
        st.warning("Please fill in your name and problem")
    else:
        st.session_state.show_form = False  # hide form
        prompt = f"""
You are an experienced vedic astrology guide. Use vedic astrology principles to provide insights and solutions based on the user's details and problems. # noqa

Person details:
Name: {name}
Date of Birth: {date}
Time of Birth: {time}

Problem:
{problem}

Expected solution type:
{types_of_solution}

Provide:
1. Astrological insight
2. Practical guidance
3. Remedies or next steps

Keep the tone calm and supportive.
"""
        # Show spinner while generating guidance
        with st.spinner("Generating your astrological guidance..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            st.session_state.response = response.text  # store response in session

# Display the response if it exists and form is hidden
if not st.session_state.show_form and st.session_state.response:
    st.subheader("🧿 Guidance")
    st.write(st.session_state.response)

# Add Query Again button
if not st.session_state.show_form and st.button("Add Query Again"):
    st.session_state.show_form = True          # show form again
    st.session_state.response = None           # remove previous response
      # remove previous response


# def load_rashi_data():
#     with open("rashi.json", "r") as f:
#         return json.load(f)


# rashi_data = load_rashi_data()


# def find_rashi(name: str):
#     if not name:
#         return None

#     name = name.lower().strip()

#     for length in range(4, 0, -1):
#         prefix = name[:length]

#         for rashi, syllables in rashi_data.items():
#             if prefix in syllables:
#                 return rashi

#     return "Unknown"


# st.set_page_config(page_title="Rashi Finder", page_icon="🔮")

# st.title("🔮 AstroApp")
# st.write("Enter your name (English transliteration)")

# name = st.text_input("Your name")

# if st.button("Find Rashi"):
#     result = find_rashi(name)

#     if result is None:
#         st.warning("Please enter a valid name.")
#     elif result == "Unknown":
#         st.error("Could not determine Rashi from the name.")
#     else:
#         st.success(f"✨ Your Rashi is **{result}**")
