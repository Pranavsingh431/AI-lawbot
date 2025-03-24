# Legal Advisor AI Chatbot

A powerful AI-powered legal assistant that can analyze legal documents and answer legal questions with detailed explanations.

## Features

- **Legal Question Answering**: Ask any legal question and get a detailed explanation in simple language
- **Document Analysis**: Upload legal documents (PDF) for comprehensive analysis
- **Conversation Memory**: Maintains context throughout your conversation
- **User-friendly Interface**: Easy-to-use web interface built with Streamlit
- **Robust Error Handling**: Comprehensive error handling and logging
- **Configurable Settings**: Easily customize the application through environment variables

## Project Structure

```
law-chatbot/
├── src/
│   ├── __init__.py
│   ├── legal_bot.py     # Core legal chatbot functionality
│   ├── config.py        # Configuration management
│   ├── utils.py         # Utility functions
│   ├── logger.py        # Logging configuration
│   └── exceptions.py    # Custom exceptions and error handling
├── experiment/
│   └── bot.ipynb        # Jupyter notebook for experimentation
├── logs/                # Application logs directory
├── app.py               # Streamlit web application
├── .env                 # Environment variables (create from .env.example)
├── .env.example         # Example environment file
├── requirements.txt     # Project dependencies
├── setup.py             # Package setup file
├── Dockerfile           # Docker container definition
├── docker-compose.yml   # Docker Compose configuration
├── deploy.sh            # Deployment automation script
├── DEPLOYMENT.md        # Comprehensive deployment guide
└── README.md            # Project documentation
```

## Setup and Installation

### Prerequisites

- Python 3.8+ 
- Google API key for Gemini model

### Installation Steps

1. Clone this repository:
   ```
   git clone <repository-url>
   cd law-chatbot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your configuration (copy from `.env.example`):
   ```
   cp .env.example .env
   ```
   Then edit the `.env` file to add your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage

### Web Interface

Run the Streamlit app:

```
streamlit run app.py
```

This will launch a local web server, and you can access the application in your browser at http://localhost:8501.

### Command Line Interface

For a simple command-line interface, you can use:

```
python -m src.legal_bot
```

## Deployment Options

You can deploy the Legal Advisor AI chatbot in several ways:

### Quick Deployment

Use our deployment script:

```bash
chmod +x deploy.sh
./deploy.sh
```

### Deployment Options

- **Local Development**: Run locally with Python and Streamlit
- **Docker**: Deploy using Docker for containerized deployment
- **Streamlit Cloud**: Host on Streamlit's platform
- **Heroku**: Deploy to Heroku cloud platform
- **AWS**: Deploy on Amazon Web Services

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## Configuration Options

You can customize the application by setting the following environment variables in your `.env` file:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| GOOGLE_API_KEY | Your Google API key (required) | None |
| LLM_MODEL | The Gemini model to use | gemini-2.0-pro-exp-02-05 |
| MAX_TOKENS | Maximum tokens for model response | 4096 |
| DEBUG_MODE | Enable debug features | False |
| LOG_LEVEL | Logging level (INFO, DEBUG, etc.) | INFO |
| MAX_PDF_SIZE_MB | Maximum PDF file size in MB | 10 |
| MEMORY_TYPE | Type of conversation memory | conversation_buffer |
| MAX_MEMORY_ITEMS | Maximum items in conversation history | 10 |

## Using the Chatbot

1. **Ask Legal Questions**: Type your legal questions in the chat input box
2. **Upload Documents**: Use the sidebar to upload legal documents (PDF format) for analysis
3. **Analyze Documents**: Click the "Analyze Document" button after uploading a PDF
4. **Clear Conversation**: Use the "Clear Conversation" button to start fresh

## Example Questions

- "What are my rights as a tenant if my landlord refuses to make repairs?"
- "Explain the concept of 'force majeure' in contract law."
- "What legal steps should I take after a car accident?"
- "What are the key elements required for a valid contract?"

## Logs and Debugging

Logs are stored in the `logs/` directory with a filename format of `legal_bot_YYYY-MM-DD.log`. 

If you enable DEBUG_MODE in your `.env` file, you'll get access to additional debugging features in the Streamlit interface.

## Limitations

- The AI provides general legal information but is not a substitute for professional legal advice.
- The accuracy of document analysis depends on the quality and format of the PDF.
- Currently supports only PDF documents for analysis.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 