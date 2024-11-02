import streamlit as st
from SimplerLLM.language.llm import LLM, LLMProvider
from SimplerLLM.tools.generic_loader import load_content
import json

# Initialize the LLM instance
llm_instance = LLM.create(provider=LLMProvider.OPENAI, model_name="gpt-3.5-turbo")

# Streamlit app layout with animation
st.title("🌟 Social Media Post Generator")
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://media.giphy.com/media/xT1R9ZbxqHQxN7FvEk/giphy.gif" alt="Cartoon Animation" style="width: 200px;"/>
    </div>
    """, unsafe_allow_html=True
)
st.write("Generate custom social media posts by providing either a URL or directly pasting text!")

# Input choice: URL or Text
input_choice = st.radio("Choose input type:", ("URL", "Direct Text"))

# Input fields based on choice
if input_choice == "URL":
    url = st.text_input("Enter the URL to summarize")
    content = load_content(url).content if url else ""
else:
    content = st.text_area("Paste the text you want to convert")

# Dropdown menu for selecting social media platform
platform = st.selectbox("Select Social Media Platform", 
                        ["Twitter", "Facebook", "LinkedIn", "Instagram", "YouTube"])

# Character limits and prompts based on selected platform
platform_settings = {
    "Twitter": {"char_limit": 280, "prompt": "Convert to an engaging 280 characters tweet."},
    "Facebook": {"char_limit": 500, "prompt": "Summarize for a Facebook post."},
    "LinkedIn": {"char_limit": 600, "prompt": "Summarize for a LinkedIn post, highlight key points professionally."},
    "Instagram": {"char_limit": 2200, "prompt": "Summarize for an Instagram caption, engaging and concise."},
    "YouTube": {"char_limit": 5000, "prompt": "Summarize for a YouTube video description, highlight key topics."}
}

# Show the character limit for the selected platform
st.write(f"Character limit for {platform}: {platform_settings[platform]['char_limit']}")

# Button to generate social media post
if st.button("Generate Post"):
    if content:
        try:
            # Create prompt based on selected platform
            platform_prompt = f"{platform_settings[platform]['prompt']} Post content: {content}"
            
            # Generate the social media post
            generated_text = llm_instance.generate_response(prompt=platform_prompt)

            # Truncate to character limit if needed
            if len(generated_text) > platform_settings[platform]['char_limit']:
                generated_text = generated_text[:platform_settings[platform]['char_limit']].strip() + "..."

            # Display the generated post
            st.subheader(f"Generated {platform} Post")
            st.write(generated_text)

            # Download button to download the post as a text file
            st.download_button(
                label="Download Post",
                data=generated_text,
                file_name=f"{platform}_post.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter content in the selected format.")

# Styling for a user-friendly interface
st.markdown("""
    <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stRadio, .stSelectbox {
            font-size: 18px;
            color: #333;
        }
        .stTextInput, .stTextArea {
            border-radius: 4px;
            padding: 8px;
            font-size: 16px;
        }
    </style>
    """, unsafe_allow_html=True)

st.info("This tool extracts key information and generates a custom post for the selected platform.")
