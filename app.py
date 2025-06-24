import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- Page and API Configuration ---

st.set_page_config(
    page_title="AI Accessibility Advocate",
    page_icon="♿",
    layout="wide",
)

# Configure the Google AI API
try:
    # Get API key from Streamlit secrets
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        API_CONFIGURED = True
    else:
        API_CONFIGURED = False
except Exception as e:
    API_CONFIGURED = False
    st.error(f"Failed to configure Google AI: {e}")

def get_model():
    """Gets the Gemini model from secrets or uses a default."""
    model_name = st.secrets.get('MODEL_NAME', 'gemini-1.5-flash')
    return genai.GenerativeModel(model_name)

# --- Main Application UI ---

st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #4CAF50, #2196F3);
    color: white;
    padding: 1rem;
    border-radius: 0.5rem;
    text-align: center;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>♿ AI Accessibility Advocate</h1>
    <p>Your simple AI assistant for digital accessibility.</p>
</div>
""", unsafe_allow_html=True)


# --- Sidebar ---

with st.sidebar:
    st.header("🔧 Controls")
    if API_CONFIGURED:
        st.success("✅ Google AI API Connected")
    else:
        st.error("❌ Google AI API Key Not Found")
        st.info("""
            **To get started:**
            1. Create a file named `secrets.toml` in a `.streamlit` directory.
            2. Add your Google AI API key like this:
            ```toml
            GOOGLE_API_KEY = "your-key-here"
            ```
            3. Relaunch the app.
        """)
    st.markdown("---")
    st.header("💡 Example Prompts")
    st.info("What color contrast ratio do I need for WCAG AA?")
    st.info("How do I write effective alt text?")
    st.info("How can I make my website keyboard navigable?")


# --- Main Content Tabs ---

tab1, tab2 = st.tabs(["💬 Chat Assistant", "🖼️ Image Analyzer"])

# --- Chat Assistant Tab ---
with tab1:
    st.header("Ask Your Accessibility Question")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("How can I improve my website's accessibility?"):
        if not API_CONFIGURED:
            st.warning("Please configure your Google AI API key in the sidebar to use the chat.")
        else:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        model = get_model()
                        # Use the same model for chat
                        chat_prompt = f"You are an expert on web accessibility. Provide a helpful, concise answer to the following question: {prompt}"
                        response = model.generate_content(chat_prompt)
                        response_text = response.text
                        st.markdown(response_text)
                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": response_text})
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

# --- Image Analyzer Tab ---
with tab2:
    st.header("Analyze Image Accessibility")
    uploaded_file = st.file_uploader(
        "Upload an image to check for accessibility.", type=['png', 'jpg', 'jpeg']
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Analyze Image"):
            if not API_CONFIGURED:
                st.warning("Please configure your Google AI API key in the sidebar to analyze images.")
            else:
                with st.spinner("Analyzing..."):
                    try:
                        model = get_model()
                        prompt = """
                        You are an expert in web accessibility. Analyze this image and provide:
                        1.  A concise and effective alt text description.
                        2.  Any potential accessibility issues (e.g., low contrast text in the image).
                        3.  Suggestions for improvement.
                        """
                        response = model.generate_content([prompt, image])
                        st.markdown("### 📋 Analysis Results")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"An error occurred during analysis: {e}")
