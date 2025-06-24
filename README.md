# 🌟 AI-Powered Accessibility Advocate Assistant

> **Empowering Digital Inclusion Through AI**  
> Using Google Generative AI SDK with Streamlit for accessible digital experiences.

## 📖 Overview

The **AI-Powered Accessibility Advocate Assistant** is a streamlined application that uses Google's Generative AI to provide expert accessibility guidance, image analysis, and compliance recommendations. Built with Streamlit for an accessible user interface.

## 🎯 Features

### 💬 AI Accessibility Consultant
- **Expert Guidance**: Get comprehensive accessibility advice using Google Gemini
- **WCAG 2.1 Compliance**: Guidelines for A, AA, and AAA levels
- **Best Practices**: Universal design principles and inclusive development
- **Interactive Chat**: Real-time assistance with accessibility questions

### 🖼️ Image Accessibility Analyzer
- **Visual Analysis**: Upload images for accessibility assessment
- **Alt Text Generation**: AI-powered descriptive text suggestions
- **Color Contrast Review**: Automated contrast ratio evaluation
- **Compliance Check**: WCAG guideline adherence verification

### 📚 Resource Library
- **Quick Reference**: WCAG guidelines and testing tools
- **Color Contrast Standards**: Detailed requirements for different content types
- **Keyboard Navigation**: Essential accessibility patterns
- **Testing Tools**: Comprehensive list of accessibility testing resources

## 🛠️ Technology Stack

- **Google Generative AI SDK**: Powered by Gemini 2.0 Flash
- **Streamlit**: Accessible web interface framework
- **Pillow**: Image processing capabilities
- **Python 3.9+**: Core runtime environment

## 🚀 Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd accessibility-advocate-assistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Google AI API

Create `.streamlit/secrets.toml` in your project root:

```toml
GOOGLE_API_KEY = "your-google-ai-studio-api-key"
MODEL_NAME = "gemini-2.0-flash-exp"
```

#### Getting Your API Key:
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. **Important**: Configure API restrictions:
   - Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
   - Edit your API key
   - Under **API restrictions**, add "Generative Language API"
   - Save changes

## 🏃 Running the Application

### Start the Streamlit App
```bash
streamlit run app.py
```

Access the application at: http://localhost:8501

### Quick Launch
```bash
python launch.py
```

## 📖 Usage Examples

### Accessibility Guidance
- "What color contrast ratio do I need for WCAG AA compliance?"
- "How do I write effective alt text for complex images?"
- "What are the key principles of accessible form design?"
- "How can I make my website keyboard navigable?"

### Image Analysis
1. Upload any image (PNG, JPG, GIF, BMP)
2. Get instant accessibility analysis
3. Receive alt text suggestions
4. Review color contrast recommendations

### Quick Reference
- WCAG 2.1 guidelines and levels
- Color contrast requirements
- Keyboard navigation patterns
- Accessibility testing tools

## 🔧 Development

### Project Structure
```
├── app.py                    # Main Streamlit application
├── launch.py                 # Application launcher
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation
└── .streamlit/
    └── secrets.toml          # API configuration (create this)
```

### Key Features
- **Google Generative AI Integration**: Direct SDK usage for reliable AI responses
- **Streamlit Secrets Management**: Secure API key handling
- **Accessible UI Design**: Following accessibility best practices in the interface
- **Multi-Modal Analysis**: Text and image accessibility assessment

## 📚 Accessibility Standards Supported

- **WCAG 2.1**: Web Content Accessibility Guidelines (A, AA, AAA)
- **Section 508**: US Federal accessibility requirements
- **ADA Compliance**: Americans with Disabilities Act guidance
- **Universal Design**: Inclusive design principles

## 🔧 Troubleshooting

### API Key Issues
If you see "API_KEY_SERVICE_BLOCKED" errors:
1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Edit your API key
3. Under **API restrictions**, ensure "Generative Language API" is enabled
4. Save and restart the application

### Common Setup Issues
- Ensure Python 3.9+ is installed
- Check that `.streamlit/secrets.toml` exists and contains valid API key
- Verify internet connection for API calls

## 📞 Support

For technical issues or accessibility questions, the application provides:
- Real-time AI assistance through the chat interface
- Comprehensive resource library
- Example prompts and use cases
- Status indicators for system health

## 🌟 Contributing

This application demonstrates best practices for:
- Accessible web application design
- Google Generative AI SDK integration
- Streamlit secrets management
- Multi-modal AI assistance

Built to promote digital inclusion and accessibility awareness in the AI community. 