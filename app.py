import streamlit as st
import os
import tempfile
import base64
from datetime import datetime
import time
import random

from src.legal_bot import LegalAdvisorBot
from src.config import Config
from src.logger import logger, log_user_interaction
from src.utils import save_uploaded_file, clean_temporary_file
from src.legal_glossary import get_legal_glossary_html, get_random_legal_term
from src.exceptions import (
    APIKeyError, 
    PDFExtractionError, 
    DocumentTooLargeError, 
    InvalidFileTypeError,
    handle_exception
)

# Set up logging for the Streamlit app
logger.info("Starting Streamlit application")

# Function to load and encode images for use in CSS
def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# Ensure the images directory exists
def ensure_assets_exist():
    # Check if required files exist
    required_files = [
        "src/assets/scales.svg",
        "src/assets/scales-dark.svg",
        "src/assets/bg_pattern.svg",
        "src/assets/bg_pattern_dark.svg",
        "src/assets/styles.css",
        "src/assets/script.js"
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            logger.warning(f"Required asset file not found: {file_path}")
            
    logger.info("Assets verification completed")

# Call the function to ensure assets exist
ensure_assets_exist()

# Get base64 encoded images
try:
    scales_img = get_base64_encoded_image("src/assets/scales.svg")
    scales_img_dark = get_base64_encoded_image("src/assets/scales-dark.svg")
    bg_pattern = get_base64_encoded_image("src/assets/bg_pattern.svg")
    bg_pattern_dark = get_base64_encoded_image("src/assets/bg_pattern_dark.svg")
except Exception as e:
    logger.error(f"Error loading images: {e}")
    scales_img = ""
    scales_img_dark = ""
    bg_pattern = ""
    bg_pattern_dark = ""

# Set page configuration and styling
st.set_page_config(
    page_title="Legal Advisor AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
# Generate a unique session ID if it doesn't exist
if "session_id" not in st.session_state:
    st.session_state.session_id = f"chat_{int(datetime.now().timestamp())}_{random.randint(1000, 9999)}"

# Initialize chat history tracking
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Load external CSS
def load_css(css_file):
    with open(css_file, "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

# Try to load external CSS
try:
    load_css("src/assets/styles.css")
    
    # Add body background with pattern for both light and dark modes
    st.markdown(f"""
    <style>
    body {{
        background-image: url("data:image/svg+xml;base64,{bg_pattern}");
        background-repeat: repeat;
    }}
    
    body.dark-mode-forced {{
        background-image: url("data:image/svg+xml;base64,{bg_pattern_dark}");
        background-repeat: repeat;
    }}
    
    body.light-mode-forced {{
        background-image: url("data:image/svg+xml;base64,{bg_pattern}");
        background-repeat: repeat;
    }}
    
    @media (prefers-color-scheme: dark) {{
        body:not(.light-mode-forced) {{
            background-image: url("data:image/svg+xml;base64,{bg_pattern_dark}");
            background-repeat: repeat;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)
    
except Exception as e:
    logger.error(f"Error loading CSS file: {e}")
    # Fallback minimal styling
    st.markdown("""
    <style>
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #2E4057;
        background-color: #FFFFFF;
    }
    @media (prefers-color-scheme: dark) {
        body {
            color: #E4E4E4;
            background-color: #1E1E1E;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Load JavaScript
def load_javascript():
    try:
        with open("src/assets/script.js", "r") as js_file:
            st.markdown(f"""
            <script>
            {js_file.read()}
            </script>
            """, unsafe_allow_html=True)
        logger.info("Successfully loaded JavaScript")
    except Exception as e:
        logger.error(f"Error loading JavaScript file: {e}")

# Initialize the bot
@st.cache_resource
def get_bot():
    try:
        return LegalAdvisorBot()
    except Exception as e:
        logger.error(f"Failed to initialize the bot: {e}")
        st.error(f"Error initializing the bot: {handle_exception(e)}")
        st.stop()

def chat_with_bot(bot, user_input):
    """
    Get a response from the bot, handling the case where get_response may not exist.
    
    Args:
        bot: The LegalAdvisorBot instance
        user_input (str): The user's input message
        
    Returns:
        str: The bot's response
    """
    logger.info(f"Getting bot response for input: {user_input[:50]}...")
    
    # Check if get_response method exists, otherwise use process_query
    if hasattr(bot, 'get_response'):
        return bot.get_response(user_input)
    else:
        logger.warning("get_response method not found, falling back to process_query")
        return bot.process_query(user_input)

# Main container - use a cleaner layout more like ChatGPT
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Add New Chat button (fixed position)
st.markdown(
    """
    <div class="new-chat-container">
        <span class="arrow-icon" aria-hidden="true"><i class="fas fa-chevron-right"></i></span>
        <button class="new-chat-button" id="newChatButton" aria-label="Start a new chat">
            <i class="fas fa-plus" aria-hidden="true"></i><span>New Chat</span>
        </button>
    </div>
    """,
    unsafe_allow_html=True
)

# Welcome banner for first-time visitors (only show when no interactions yet)
if len(st.session_state.get("messages", [])) == 0:
    st.markdown(f"""
    <div class="welcome-banner-minimal">
        <h1>Legal Advisor AI</h1>
        <p>Ask questions about legal matters or upload documents for analysis.</p>
    </div>
    """, unsafe_allow_html=True)

# Initialize the bot
bot = get_bot()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    welcome_msg = (
        "Welcome to Legal Advisor AI. I'm here to provide professional legal assistance with "
        "questions, documents, and research. How may I assist you with your legal matter today?"
    )
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
    logger.info("Initialized new chat session with welcome message")

# Sidebar with legal term glossary and options
with st.sidebar:
    # Professional sidebar header
    st.markdown(
        f"""
        <div class="legal-ribbon">
            <div class="legal-ribbon-content">
                <img src="data:image/svg+xml;base64,{scales_img}" alt="Legal Advisor AI" class="scales-icon">
                <h1>Legal Advisor AI</h1>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Add a separator
    st.markdown("<div class='sidebar-separator'></div>", unsafe_allow_html=True)
    
    # Chat history section
    st.markdown("<h3>CHAT HISTORY</h3>", unsafe_allow_html=True)
    
    # Display chat history items
    if len(st.session_state.chat_history) > 0:
        st.markdown('<div class="chat-history-container">', unsafe_allow_html=True)
        for idx, chat in enumerate(st.session_state.chat_history):
            chat_title = chat.get("title", f"Chat {idx+1}")
            chat_time = chat.get("time", datetime.now().strftime("%I:%M %p"))
            chat_id = chat.get("id", f"chat_{idx}")
            is_active = chat_id == st.session_state.session_id
            active_class = "active" if is_active else ""
            
            st.markdown(f"""
            <div class="chat-history-item {active_class}" data-chat-id="{chat_id}">
                <div class="chat-history-item-title">
                    {chat_title}
                    <div class="chat-history-item-time">{chat_time}</div>
                </div>
                <div class="chat-history-item-actions">
                    <button class="chat-history-delete" aria-label="Delete chat">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <i class="fas fa-history"></i>
            <p>No chat history yet</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Clear chat button
    if st.button("New conversation", key="reset_chat"):
        # Save current chat to history first if it has content
        if len(st.session_state.messages) > 1:  # More than just the welcome message
            # Get first user message as title
            first_user_msg = next((msg["content"] for msg in st.session_state.messages if msg["role"] == "user"), "New Chat")
            chat_title = first_user_msg[:30] + "..." if len(first_user_msg) > 30 else first_user_msg
            
            st.session_state.chat_history.append({
                "id": st.session_state.session_id,
                "title": chat_title,
                "time": datetime.now().strftime("%I:%M %p"),
                "messages": st.session_state.messages.copy()
            })
        
        # Clear messages in session state
        st.session_state.messages = []
        # Generate a new session ID
        st.session_state.session_id = f"chat_{int(datetime.now().timestamp())}_{random.randint(1000, 9999)}"
        # Force page refresh
        st.rerun()
    
    # Add a separator
    st.markdown("<div class='sidebar-separator'></div>", unsafe_allow_html=True)
    
    # File uploader
    st.markdown("<h3>DOCUMENT ANALYSIS</h3>", unsafe_allow_html=True)
    
    # File uploader for PDF documents with improved styling
    uploaded_file = st.file_uploader(
        "Upload legal document (PDF)",
        type=Config.ACCEPTED_FILE_TYPES,
        help="Upload a legal document for AI analysis"
    )
    
    if uploaded_file is not None:
        # Check file size
        file_size_mb = uploaded_file.size / (1024 * 1024)
        if file_size_mb > Config.MAX_PDF_SIZE_MB:
            st.markdown(
                f'<div class="status-msg error-msg">Document size exceeds limit. Maximum allowed size is {Config.MAX_PDF_SIZE_MB}MB.</div>',
                unsafe_allow_html=True
            )
            logger.warning(f"User attempted to upload a large file: {file_size_mb:.2f}MB")
        else:
            st.markdown(
                f'<div class="status-msg success-msg">Document uploaded: {uploaded_file.name} ({file_size_mb:.2f}MB)</div>',
                unsafe_allow_html=True
            )
            logger.info(f"File uploaded: {uploaded_file.name}, Size: {file_size_mb:.2f}MB")
        
            analyze_col1, analyze_col2 = st.columns([3, 1])
            with analyze_col1:
                if st.button("Analyze Document", use_container_width=True):
                    try:
                        # Add a user message indicating document analysis
                        user_msg = f"Please analyze the content of this legal document: {uploaded_file.name}"
                        st.session_state.messages.append({"role": "user", "content": user_msg})
                        
                        # Save the uploaded file temporarily
                        pdf_path = save_uploaded_file(uploaded_file)
                        
                        with st.spinner(""):
                            # Show professional loading indicator
                            st.markdown("""
                            <div class="loading-indicator">
                                <div class="loading-dot"></div>
                                <div class="loading-dot"></div>
                                <div class="loading-dot"></div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Get response from bot
                            try:
                                response = bot.analyze_document(pdf_path)
                                st.session_state.messages.append({"role": "assistant", "content": response})
                                
                                # Clean up temporary file
                                clean_temporary_file(pdf_path)
                                
                            except Exception as e:
                                error_msg = handle_exception(e)
                                st.session_state.messages.append({"role": "assistant", "content": f"❌ {error_msg}"})
                                logger.error(f"Document analysis error: {e}")
                                # Clean up temporary file if it exists
                                if 'pdf_path' in locals():
                                    clean_temporary_file(pdf_path)
                        
                        # Re-run the app to show the new messages
                        st.rerun()
                    
                    except Exception as e:
                        st.error(f"Error: {handle_exception(e)}")
                        logger.error(f"Error in document analysis flow: {e}")
    
    # Add a separator
    st.markdown("<div class='sidebar-separator'></div>", unsafe_allow_html=True)
    
    # Legal Term of the Day instead of full glossary
    st.markdown("<h3>LEGAL TERM OF THE DAY</h3>", unsafe_allow_html=True)
    
    # Get and display a random legal term
    term, definition = get_random_legal_term()
    st.markdown(
        f"""
        <div class="legal-term-of-day">
            <span style="font-weight: 600; color: var(--legal-term-color); font-size: 1.1em;">{term}</span>
            <p style="margin-top: 5px; color: var(--text-color);">{definition}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Example questions to demonstrate functionality
    st.markdown("<h3>EXAMPLES</h3>", unsafe_allow_html=True)
    
    # Add some example questions with better button styling
    examples = [
        "What are my rights if I'm facing wrongful termination?",
        "Can you explain the process of filing for bankruptcy?"
    ]
    
    for i, example in enumerate(examples):
        if st.button(example, key=f"example_{i}"):
            if example not in [msg["content"] for msg in st.session_state.messages if msg["role"] == "user"]:
                # Add the example as a user message
                st.session_state.messages.append({"role": "user", "content": example})
                
                with st.spinner(""):
                    # Get response from bot
                    response = bot.get_response(example)
                    
                    # Add assistant response
                    st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Re-run the app to show the new messages
                st.rerun()

# Display chat messages
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Function to display assistant response with typing effect
def display_assistant_response(response):
    # Add data-new-message attribute for JS to apply typing effect
    st.markdown(
        f'<div class="bot-message" data-new-message="true">{response}</div>',
        unsafe_allow_html=True
    )
    log_user_interaction("assistant", response[:100] + "..." if len(response) > 100 else response)

# Function to display user message
def display_user_message(message):
    st.markdown(
        f'<div class="user-message">{message}</div>',
        unsafe_allow_html=True
    )
    log_user_interaction("user", message[:100] + "..." if len(message) > 100 else message)

# Display chat history from session state
for message in st.session_state.messages:
    if message["role"] == "assistant":
        display_assistant_response(message["content"])
    else:
        display_user_message(message["content"])

# Close chat container
st.markdown('</div>', unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Ask a legal question...")

if user_input:
    # Capture current time for response timing
    start_time = time.time()
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    display_user_message(user_input)
    
    # Show professional loading indicator
    with st.spinner(""):
        st.markdown("""
        <div class="loading-indicator">
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Get response from bot
        response = chat_with_bot(bot, user_input)
        
        # Calculate response time
        response_time = time.time() - start_time
        logger.info(f"Bot response generated in {response_time:.2f} seconds")
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Display assistant response
    display_assistant_response(response)
    
    # Re-run to clear the input field
    st.rerun()

# Close main container
st.markdown('</div>', unsafe_allow_html=True)

# Theme toggle button
st.markdown(
    """
    <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme">
        <i class="fas fa-sun"></i>
    </button>
    """,
    unsafe_allow_html=True
)

# Load FontAwesome for icons
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
<link rel="icon" type="image/png" href="https://img.icons8.com/fluency/48/scales.png">
<link rel="apple-touch-icon" href="https://img.icons8.com/fluency/96/scales.png">
""", unsafe_allow_html=True)

# Load JavaScript last
load_javascript()
