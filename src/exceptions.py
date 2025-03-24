class LegalBotException(Exception):
    """Base exception class for all Legal Bot exceptions."""
    pass

class APIKeyError(LegalBotException):
    """Exception raised when API key is missing or invalid."""
    pass

class PDFExtractionError(LegalBotException):
    """Exception raised when there is an error extracting text from a PDF."""
    pass

class ModelResponseError(LegalBotException):
    """Exception raised when there is an error getting a response from the model."""
    pass

class DocumentTooLargeError(LegalBotException):
    """Exception raised when a document exceeds the maximum size limit."""
    pass

class InvalidFileTypeError(LegalBotException):
    """Exception raised when a file type is not supported."""
    pass

class ConfigurationError(LegalBotException):
    """Exception raised when there is a configuration error."""
    pass

# Helper functions for exception handling

def handle_exception(exception, default_message="An error occurred"):
    """
    Handle an exception and return appropriate error message.
    
    Args:
        exception (Exception): The exception to handle
        default_message (str): Default error message if the exception is not recognized
        
    Returns:
        str: Error message to display to the user
    """
    from src.logger import log_exception
    
    # Log the exception
    log_exception(exception)
    
    # Return an appropriate error message based on the exception type
    if isinstance(exception, APIKeyError):
        return "API key error: Please check your API key configuration."
    
    elif isinstance(exception, PDFExtractionError):
        return "Error processing PDF: Could not extract text from the document. Please make sure it's a valid, readable PDF."
    
    elif isinstance(exception, ModelResponseError):
        return "Error getting response from the AI model. Please try again later."
    
    elif isinstance(exception, DocumentTooLargeError):
        return "Document too large: Please upload a smaller document."
    
    elif isinstance(exception, InvalidFileTypeError):
        return "Invalid file type: Only PDF documents are supported."
    
    elif isinstance(exception, ConfigurationError):
        return "Configuration error: Please check the application configuration."
        
    else:
        # For unexpected exceptions, return the default message
        return f"{default_message}: {str(exception)}" 