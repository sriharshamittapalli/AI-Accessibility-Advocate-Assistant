"""
AI-Powered Accessibility Advocate Assistant
Using Google Generative AI SDK with Streamlit
Cost-optimized with caching and offline content
"""

import streamlit as st
import google.generativeai as genai
import os
import time
import hashlib
from PIL import Image
import io

# Cost optimization settings
RATE_LIMIT_DELAY = 2  # seconds between API calls
MAX_CACHE_SIZE = 100
FALLBACK_TO_OFFLINE = True

# Offline knowledge base for common questions
ACCESSIBILITY_KNOWLEDGE = {
    "color contrast": {
        "question": "What color contrast ratio do I need for WCAG AA compliance?",
        "answer": """
## WCAG AA Color Contrast Requirements

**For Normal Text:**
- **Minimum ratio: 4.5:1** against background
- Applies to text smaller than 18pt (or 14pt bold)

**For Large Text:**
- **Minimum ratio: 3:1** against background  
- Applies to text 18pt+ or 14pt+ bold

**For UI Components & Graphics:**
- **Minimum ratio: 3:1** for:
  - Form input borders
  - Icons that convey information
  - Charts and graphs
  - Focus indicators

### Testing Tools:
- **WebAIM Contrast Checker**: https://webaim.org/resources/contrastchecker/
- **Colour Contrast Analyser**: Free desktop tool
- **Chrome DevTools**: Built-in accessibility audit

### Common Color Combinations (AA Compliant):
- Black text (#000000) on white (#FFFFFF) = 21:1 ✅
- Dark gray (#595959) on white = 4.54:1 ✅  
- Blue (#0066CC) on white = 4.56:1 ✅
- White text on dark blue (#003366) = 12.63:1 ✅
        """
    },
    "alt text": {
        "question": "How do I write effective alt text for images?",
        "answer": """
## Writing Effective Alt Text

**Key Principles:**
1. **Be descriptive but concise** (typically under 125 characters)
2. **Include the image's purpose** in context
3. **Don't start with "Image of" or "Picture of"**
4. **Describe what's important** for understanding

### Examples:

**Decorative Images:**
```html
<img src="border-decoration.png" alt="">
```
*Use empty alt="" for purely decorative images*

**Informative Images:**
```html
<!-- Poor -->
<img src="chart.png" alt="Chart">

<!-- Good -->
<img src="chart.png" alt="Sales increased 25% from Q1 to Q2 2024">
```

**Functional Images (buttons, links):**
```html
<!-- Poor -->
<img src="search-icon.png" alt="Search icon">

<!-- Good -->
<img src="search-icon.png" alt="Search">
```

**Complex Images:**
- Provide brief alt text + detailed description nearby
- Consider using `aria-describedby` for longer descriptions

### Alt Text Checklist:
- ✅ Does it convey the image's meaning?
- ✅ Is it contextually relevant?
- ✅ Would it make sense if read aloud?
- ✅ Is it concise but complete?
        """
    },
    "keyboard navigation": {
        "question": "How can I make my website keyboard navigable?",
        "answer": """
## Keyboard Navigation Best Practices

**Essential Requirements:**
1. **All interactive elements must be keyboard accessible**
2. **Logical tab order** through content
3. **Visible focus indicators** on all focusable elements
4. **No keyboard traps** (user can always navigate away)

### Key Standards:

**Tab Navigation:**
- `Tab`: Move to next focusable element
- `Shift + Tab`: Move to previous element
- `Enter/Space`: Activate buttons and links
- `Arrow keys`: Navigate within components (menus, tabs)
- `Escape`: Close dialogs and menus

**Focus Management:**
```css
/* Visible focus indicator */
button:focus, a:focus {
    outline: 2px solid #0066CC;
    outline-offset: 2px;
}

/* Never remove focus entirely */
/* DON'T DO: *:focus { outline: none; } */
```

**HTML Structure:**
```html
<!-- Proper heading hierarchy -->
<h1>Main Page Title</h1>
  <h2>Section Title</h2>
    <h3>Subsection</h3>

<!-- Skip links for screen readers -->
<a href="#main-content" class="sr-only">Skip to main content</a>

<!-- Proper form labeling -->
<label for="email">Email Address</label>
<input type="email" id="email" name="email">
```

**Testing:**
- Navigate your site using only the Tab key
- Ensure all functionality is available via keyboard
- Check that focus indicators are clearly visible
        """
    },
    "forms": {
        "question": "What are the key principles of accessible form design?",
        "answer": """
## Accessible Form Design

**Essential Elements:**

### 1. Labels and Instructions
```html
<!-- Always use explicit labels -->
<label for="firstname">First Name *</label>
<input type="text" id="firstname" name="firstname" required>

<!-- Group related fields -->
<fieldset>
    <legend>Contact Information</legend>
    <!-- form fields here -->
</fieldset>
```

### 2. Error Handling
```html
<!-- Clear error messages -->
<label for="email">Email Address *</label>
<input type="email" id="email" aria-describedby="email-error" required>
<div id="email-error" role="alert">
    Please enter a valid email address
</div>
```

### 3. Required Field Indicators
- Mark required fields clearly (*, "required", etc.)
- Use `required` attribute and `aria-required="true"`
- Don't rely on color alone to indicate required fields

### 4. Input Instructions
```html
<label for="password">Password</label>
<input type="password" id="password" aria-describedby="pwd-help">
<div id="pwd-help">
    Must be 8+ characters with uppercase, lowercase, and numbers
</div>
```

### 5. Accessible Form Controls

**Checkboxes & Radio Buttons:**
```html
<fieldset>
    <legend>Preferred Contact Method</legend>
    <input type="radio" id="contact-email" name="contact" value="email">
    <label for="contact-email">Email</label>
    
    <input type="radio" id="contact-phone" name="contact" value="phone">
    <label for="contact-phone">Phone</label>
</fieldset>
```

**WCAG Guidelines:**
- 3.3.1: Error Identification (A)
- 3.3.2: Labels or Instructions (A)  
- 3.3.3: Error Suggestion (AA)
- 3.3.4: Error Prevention (AA)
        """
    }
}

def setup_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="AI Accessibility Advocate",
        page_icon="♿",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better accessibility
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
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4CAF50;
        margin: 1rem 0;
    }
    .success-card {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .error-card {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .offline-content {
        background: #e7f3ff;
        border: 1px solid #b3d9ff;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def setup_google_ai():
    """Setup Google Generative AI with API key from Streamlit secrets."""
    try:
        # Get API key from Streamlit secrets
        if 'GOOGLE_API_KEY' in st.secrets:
            api_key = st.secrets['GOOGLE_API_KEY']
            if api_key and api_key != "your-google-ai-studio-api-key-here":
                genai.configure(api_key=api_key)
                return True
        return False
    except Exception as e:
        st.error(f"Failed to configure Google AI: {e}")
        return False

def get_model():
    """Get the configured Gemini model (cost-optimized)."""
    # Use more cost-effective model
    model_name = st.secrets.get('MODEL_NAME', 'gemini-2.0-flash')
    return genai.GenerativeModel(model_name)

def get_cache_key(prompt):
    """Generate cache key for prompt."""
    return hashlib.md5(prompt.encode()).hexdigest()

def get_cached_response(prompt):
    """Get cached response if available."""
    if "response_cache" not in st.session_state:
        st.session_state.response_cache = {}
    
    cache_key = get_cache_key(prompt)
    return st.session_state.response_cache.get(cache_key)

def cache_response(prompt, response):
    """Cache API response."""
    if "response_cache" not in st.session_state:
        st.session_state.response_cache = {}
    
    # Limit cache size
    if len(st.session_state.response_cache) >= MAX_CACHE_SIZE:
        # Remove oldest entry
        oldest_key = next(iter(st.session_state.response_cache))
        del st.session_state.response_cache[oldest_key]
    
    cache_key = get_cache_key(prompt)
    st.session_state.response_cache[cache_key] = response

def check_rate_limit():
    """Check if we need to rate limit API calls."""
    if "last_api_call" not in st.session_state:
        st.session_state.last_api_call = 0
    
    time_since_last = time.time() - st.session_state.last_api_call
    if time_since_last < RATE_LIMIT_DELAY:
        time.sleep(RATE_LIMIT_DELAY - time_since_last)
    
    st.session_state.last_api_call = time.time()

def find_offline_answer(prompt):
    """Find matching offline content for common questions."""
    prompt_lower = prompt.lower()
    
    for topic, content in ACCESSIBILITY_KNOWLEDGE.items():
        if topic in prompt_lower:
            return content["answer"]
    
    # Check for specific keywords
    keywords_map = {
        "contrast": "color contrast",
        "ratio": "color contrast", 
        "alt": "alt text",
        "alternative text": "alt text",
        "keyboard": "keyboard navigation",
        "tab": "keyboard navigation",
        "focus": "keyboard navigation",
        "form": "forms",
        "input": "forms",
        "label": "forms"
    }
    
    for keyword, topic in keywords_map.items():
        if keyword in prompt_lower and topic in ACCESSIBILITY_KNOWLEDGE:
            return ACCESSIBILITY_KNOWLEDGE[topic]["answer"]
    
    return None

def display_header():
    """Display the main application header."""
    st.markdown("""
    <div class="main-header">
        <h1>♿ AI-Powered Accessibility Advocate Assistant</h1>
        <p>Making digital content accessible to everyone using Google Gemini</p>
    </div>
    """, unsafe_allow_html=True)

def check_api_status():
    """Check if Google AI API is properly configured and working."""
    if not setup_google_ai():
        return False, "API key not found in secrets"
    
    try:
        model = get_model()
        # Simple test without using quota
        return True, "API configured (quota-optimized mode)"
    except Exception as e:
        error_msg = str(e)
        if "API_KEY_SERVICE_BLOCKED" in error_msg or "403" in error_msg:
            return False, "API key blocked for Generative Language API"
        return False, f"API error: {error_msg}"

def show_sidebar_status():
    """Display API status and configuration in sidebar."""
    st.sidebar.markdown("### 🔧 System Status")
    
    api_working, status_msg = check_api_status()
    
    if api_working:
        st.sidebar.success("✅ Google AI API Connected")
        model_name = st.secrets.get('MODEL_NAME', 'gemini-2.0-flash')
        st.sidebar.info(f"📍 Model: {model_name}")
        st.sidebar.info("💰 Cost-optimized with caching")
    else:
        st.sidebar.error("❌ API Configuration Issue")
        st.sidebar.error(status_msg)
        
        if "not found" in status_msg:
            with st.sidebar.expander("📋 Setup Instructions"):
                st.markdown("""
                **To configure API:**
                
                1. Create `.streamlit/secrets.toml` file
                2. Get API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
                3. Add to secrets.toml:
                ```toml
                GOOGLE_API_KEY = "your-key-here"
                MODEL_NAME = "gemini-2.0-flash"
                ```
                """)
        elif "blocked" in status_msg:
            with st.sidebar.expander("🔧 Fix API Key Issue"):
                st.markdown("""
                **API Key Restrictions:**
                
                1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
                2. Edit your API key
                3. **API Restrictions** → Add "Generative Language API"
                4. Save and restart the app
                """)

def accessibility_chat():
    """Main chat interface for accessibility questions."""
    st.header("💬 Ask Your Accessibility Questions")
    
    # Check API status first
    api_working, _ = check_api_status()
    
    if not api_working:
        st.warning("⚠️ API not available - showing offline content only")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            if message.get("is_offline"):
                st.markdown('<div class="offline-content">📚 Offline Content</div>', unsafe_allow_html=True)
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about accessibility guidelines, best practices, or get help with specific issues..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            # Check for cached response first
            cached_response = get_cached_response(prompt)
            if cached_response:
                st.info("🔄 Retrieved from cache (no API cost)")
                st.write(cached_response)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": cached_response,
                    "is_cached": True
                })
                return
            
            # Check for offline content
            offline_answer = find_offline_answer(prompt)
            if offline_answer:
                st.markdown('<div class="offline-content">📚 Offline Content (no API cost)</div>', unsafe_allow_html=True)
                st.markdown(offline_answer)
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": offline_answer,
                    "is_offline": True
                })
                return
            
            # Use API if available and not rate limited
            if api_working:
                with st.spinner("Getting AI-powered accessibility guidance..."):
                    try:
                        check_rate_limit()  # Implement rate limiting
                        
                        model = get_model()
                        
                        # Shorter, more focused prompt to reduce costs
                        accessibility_prompt = f"""
                        You are an accessibility expert. Provide a concise, actionable answer for:
                        
                        {prompt}
                        
                        Focus on:
                        1. Direct answer
                        2. Relevant WCAG guidelines  
                        3. Practical steps
                        
                        Keep response under 300 words.
                        """
                        
                        response = model.generate_content(accessibility_prompt)
                        response_text = response.text
                        
                        st.write(response_text)
                        
                        # Cache the response
                        cache_response(prompt, response_text)
                        
                        # Add to chat history
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": response_text
                        })
                        
                    except Exception as e:
                        error_msg = str(e)
                        if "429" in error_msg or "quota" in error_msg.lower():
                            st.error("⚠️ API quota exceeded. Showing available offline content:")
                            # Try to provide offline fallback
                            general_info = """
                            **Common Accessibility Resources:**
                            
                            - **WCAG 2.1 Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/
                            - **WebAIM**: https://webaim.org/ (excellent tutorials and tools)
                            - **a11y Project**: https://www.a11yproject.com/ (practical checklist)
                            - **MDN Accessibility**: https://developer.mozilla.org/en-US/docs/Web/Accessibility
                            
                            For specific questions, try the example prompts in the sidebar or check the Resources tab.
                            """
                            st.markdown(general_info)
                            st.session_state.chat_history.append({
                                "role": "assistant",
                                "content": general_info,
                                "is_offline": True
                            })
                        else:
                            st.error(f"Error: {error_msg}")
            else:
                st.info("💡 API not available. Try the example questions in the sidebar or check the Resources tab for common accessibility information.")

def image_accessibility_analyzer():
    """Analyze uploaded images for accessibility issues."""
    st.header("🖼️ Image Accessibility Analyzer")
    
    # Show cost warning
    st.warning("⚠️ Image analysis uses API quota. Consider using alt text guidelines below for common cases.")
    
    # Provide offline guidance first
    with st.expander("📚 Alt Text Guidelines (No API Required)"):
        st.markdown(ACCESSIBILITY_KNOWLEDGE["alt text"]["answer"])
    
    # Check API status first
    api_working, _ = check_api_status()
    
    if not api_working:
        st.error("❌ Image analysis requires API access. Please configure your Google AI API key first (see sidebar)")
        return
    
    uploaded_file = st.file_uploader(
        "Upload an image to analyze for accessibility issues",
        type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
        help="Upload any image to get accessibility analysis and recommendations"
    )
    
    if uploaded_file is not None:
        # Display the image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Add cost confirmation
        if st.button("🔍 Analyze Image (Uses API Quota)", type="primary"):
            with st.spinner("Analyzing image for accessibility issues..."):
                try:
                    check_rate_limit()  # Rate limiting
                    
                    model = get_model()
                    
                    # Shorter prompt to reduce costs
                    prompt = """
                    Analyze this image for accessibility and provide:
                    1. Descriptive alt text (under 125 characters)
                    2. Key accessibility issues
                    3. Quick improvement suggestions
                    
                    Keep response concise and actionable.
                    """
                    
                    response = model.generate_content([prompt, image])
                    
                    st.markdown("### 📋 Accessibility Analysis Results")
                    st.write(response.text)
                    
                except Exception as e:
                    error_msg = str(e)
                    if "429" in error_msg or "quota" in error_msg.lower():
                        st.error("⚠️ API quota exceeded. Please refer to the alt text guidelines above.")
                    else:
                        st.error(f"Error analyzing image: {error_msg}")

def accessibility_resources():
    """Display accessibility resources and quick references."""
    st.header("📚 Accessibility Resources & Quick Reference")
    
    # Show offline knowledge base
    st.subheader("🔄 Common Questions (No API Required)")
    
    for topic, content in ACCESSIBILITY_KNOWLEDGE.items():
        with st.expander(f"❓ {content['question']}"):
            st.markdown(content['answer'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
        <h3>🎯 WCAG 2.1 Quick Reference</h3>
        <ul>
        <li><strong>Level A:</strong> Minimum level of accessibility</li>
        <li><strong>Level AA:</strong> Standard level (legal requirement)</li>
        <li><strong>Level AAA:</strong> Enhanced level</li>
        </ul>
        
        <h4>Four Principles (POUR):</h4>
        <ul>
        <li><strong>Perceivable:</strong> Information presented in ways users can perceive</li>
        <li><strong>Operable:</strong> Interface components users can operate</li>
        <li><strong>Understandable:</strong> Information and UI operation are understandable</li>
        <li><strong>Robust:</strong> Content can be interpreted by assistive technologies</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
        <h3>🔧 Testing Tools</h3>
        <ul>
        <li><strong>WAVE:</strong> Web accessibility evaluation</li>
        <li><strong>axe DevTools:</strong> Browser extension for testing</li>
        <li><strong>Lighthouse:</strong> Built-in Chrome accessibility audit</li>
        <li><strong>Color Oracle:</strong> Color blindness simulator</li>
        <li><strong>NVDA/JAWS:</strong> Screen reader testing</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
        <h3>📏 Color Contrast Requirements</h3>
        <ul>
        <li><strong>AA Level:</strong> 4.5:1 for normal text</li>
        <li><strong>AA Level:</strong> 3:1 for large text (18pt+ or 14pt+ bold)</li>
        <li><strong>AAA Level:</strong> 7:1 for normal text</li>
        <li><strong>AAA Level:</strong> 4.5:1 for large text</li>
        </ul>
        
        <h4>Non-text Elements:</h4>
        <ul>
        <li><strong>Graphics:</strong> 3:1 contrast ratio</li>
        <li><strong>UI Components:</strong> 3:1 contrast ratio</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
        <h3>⌨️ Keyboard Navigation</h3>
        <ul>
        <li><strong>Tab:</strong> Move to next focusable element</li>
        <li><strong>Shift+Tab:</strong> Move to previous element</li>
        <li><strong>Enter/Space:</strong> Activate buttons/links</li>
        <li><strong>Arrow Keys:</strong> Navigate within components</li>
        <li><strong>Escape:</strong> Cancel or close dialogs</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

def show_example_prompts():
    """Display example prompts in the sidebar."""
    st.sidebar.markdown("### 💡 Example Questions")
    st.sidebar.caption("Many answered offline (no API cost)")
    
    examples = [
        "What color contrast ratio do I need for WCAG AA compliance?",
        "How do I write effective alt text for complex images?", 
        "What are the key principles of accessible form design?",
        "How can I make my website keyboard navigable?",
        "What are the requirements for accessible video content?",
        "How do I structure headings for screen readers?",
        "What are the best practices for accessible tables?",
        "How can I test my website with screen readers?"
    ]
    
    for i, example in enumerate(examples):
        if st.sidebar.button(example, key=f"example_{i}"):
            st.session_state.chat_history.append({"role": "user", "content": example})
            st.rerun()

def main():
    """Main application function."""
    setup_page()
    display_header()
    
    # Show cost optimization info
    st.info("💰 **Cost-Optimized Mode**: Common questions answered offline, API calls cached and rate-limited")
    
    # Sidebar
    show_sidebar_status()
    show_example_prompts()
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["💬 Chat Assistant", "🖼️ Image Analysis", "📚 Resources"])
    
    with tab1:
        accessibility_chat()
    
    with tab2:
        image_accessibility_analyzer()
    
    with tab3:
        accessibility_resources()

if __name__ == "__main__":
    main() 