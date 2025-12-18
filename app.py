import streamlit as st
import json


def load_rashi_data():
    with open("rashi.json", "r") as f:
        return json.load(f)


rashi_data = load_rashi_data()


def find_rashi(name: str):
    if not name:
        return None

    name = name.lower().strip()

    for length in range(4, 0, -1):
        prefix = name[:length]

        for rashi, syllables in rashi_data.items():
            if prefix in syllables:
                return rashi

    return "Unknown"


st.set_page_config(page_title="Rashi Finder", page_icon="🔮")

st.title("🔮 Rashi Finder")
st.write("Enter your name (English transliteration)")

name = st.text_input("Your name")

if st.button("Find Rashi"):
    result = find_rashi(name)

    if result is None:
        st.warning("Please enter a valid name.")
    elif result == "Unknown":
        st.error("Could not determine Rashi from the name.")
    else:
        st.success(f"✨ Your Rashi is **{result}**")
