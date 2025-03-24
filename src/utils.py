import os
import PyPDF2
import tempfile
import hashlib
from typing import Optional, Dict, Any, List

def extract_text_from_pdf(pdf_path: str) -> Optional[str]:
    """
    Extract text from a PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF or None if extraction fails
    """
    text = ""
    try:
        # Open the PDF file
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Get the number of pages
            num_pages = len(pdf_reader.pages)
            
            # Extract text from each page
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"  # Add spacing between pages
                    
        return text if text.strip() else None
    except Exception as e:
        from src.logger import logger
        logger.error(f"Error extracting text from PDF: {e}")
        return None

def save_uploaded_file(uploaded_file) -> str:
    """
    Save an uploaded file to a temporary location.
    
    Args:
        uploaded_file: The uploaded file object from Streamlit
        
    Returns:
        str: Path to the saved temporary file
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            return tmp_file.name
    except Exception as e:
        from src.logger import logger
        logger.error(f"Error saving uploaded file: {e}")
        raise

def clean_temporary_file(file_path: str) -> bool:
    """
    Remove a temporary file from the file system.
    
    Args:
        file_path (str): Path to the file to be removed
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if os.path.exists(file_path):
            os.unlink(file_path)
            return True
        return False
    except Exception as e:
        from src.logger import logger
        logger.error(f"Error deleting temporary file: {e}")
        return False

def get_file_hash(file_path: str) -> str:
    """
    Generate a hash of a file for caching purposes.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: Hash value of the file
    """
    try:
        md5_hash = hashlib.md5()
        with open(file_path, "rb") as f:
            # Read and update hash in chunks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
        return md5_hash.hexdigest()
    except Exception as e:
        from src.logger import logger
        logger.error(f"Error generating file hash: {e}")
        return ""

def format_response(response_data: Dict[str, Any]) -> str:
    """
    Format the response from the legal bot into a readable markdown format.
    
    Args:
        response_data (Dict[str, Any]): Response data from the bot
        
    Returns:
        str: Formatted response in markdown
    """
    try:
        # If the response is already a string, return it
        if isinstance(response_data, str):
            return response_data
            
        # If it's a dictionary with a 'text' key, use that
        if isinstance(response_data, dict):
            if 'text' in response_data:
                return response_data['text']
            elif 'output' in response_data:
                return response_data['output']
            elif 'response' in response_data:
                return response_data['response']
            elif 'answer' in response_data:
                return response_data['answer']
            elif 'result' in response_data:
                return response_data['result']
            
        # Otherwise, convert the dictionary to a formatted string
        formatted = ""
        for key, value in response_data.items():
            if key not in ["memory", "input"]:  # Skip memory and input keys
                formatted += f"**{key.replace('_', ' ').title()}**:\n{value}\n\n"
        
        return formatted if formatted else str(response_data)
    except Exception as e:
        from src.logger import logger
        logger.error(f"Error formatting response: {e}")
        return str(response_data) 