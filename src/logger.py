import logging
import os
import sys
from datetime import datetime

# Create logs directory if it doesn't exist
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)

# Get current date for the log file name
current_date = datetime.now().strftime("%Y-%m-%d")
log_file = os.path.join(log_dir, f"legal_bot_{current_date}.log")

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

# Create a logger specific for our application
logger = logging.getLogger("legal_bot")
logger.setLevel(logging.INFO)

def get_logger(name):
    """
    Get a logger with the given name.
    
    Args:
        name (str): Name for the logger, typically the module name
        
    Returns:
        logging.Logger: A configured logger
    """
    child_logger = logger.getChild(name)
    return child_logger

def log_exception(e, context=""):
    """
    Log an exception with optional context information.
    
    Args:
        e (Exception): The exception to log
        context (str): Additional context about where the exception occurred
    """
    import traceback
    error_details = traceback.format_exc()
    context_msg = f" - {context}" if context else ""
    logger.error(f"Exception{context_msg}: {str(e)}\n{error_details}")

def log_api_request(endpoint, params, success):
    """
    Log information about API requests.
    
    Args:
        endpoint (str): The API endpoint that was called
        params (dict): Parameters that were sent (sensitive data should be redacted)
        success (bool): Whether the request was successful
    """
    # Redact any sensitive information
    safe_params = {k: v if k != "api_key" else "[REDACTED]" for k, v in params.items()}
    
    status = "SUCCESS" if success else "FAILED"
    logger.info(f"API Request - Endpoint: {endpoint} - Status: {status} - Params: {safe_params}")

def log_user_interaction(query, response_length, document=None):
    """
    Log information about user interactions with the chatbot.
    
    Args:
        query (str): The user's query
        response_length (int): Length of the response
        document (str, optional): Name of document if one was analyzed
    """
    doc_info = f" - Document: {document}" if document else ""
    logger.info(f"User Interaction - Query: '{query}'{doc_info} - Response Length: {response_length}")

# Export the main logger
__all__ = ["logger", "get_logger", "log_exception", "log_api_request", "log_user_interaction"] 