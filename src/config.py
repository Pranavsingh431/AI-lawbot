import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings for the Legal Advisor Bot application."""
    
    # API settings
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.0-pro-exp-02-05")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))
    
    # App settings
    APP_NAME = "Legal Advisor AI"
    APP_ICON = "⚖️"
    DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
    VERSION = "1.0.0"
    GITHUB_URL = "https://github.com/yourusername/legal-advisor-ai"
    
    # PDF settings
    MAX_PDF_SIZE_MB = int(os.getenv("MAX_PDF_SIZE_MB", "10"))
    ACCEPTED_FILE_TYPES = ["pdf"]
    
    # Memory settings
    MEMORY_TYPE = os.getenv("MEMORY_TYPE", "conversation_buffer")
    MAX_MEMORY_ITEMS = int(os.getenv("MAX_MEMORY_ITEMS", "10"))
    
    # Logging settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls) -> Optional[str]:
        """
        Validate required configuration settings.
        
        Returns:
            Optional[str]: Error message if configuration is invalid, None otherwise
        """
        if not cls.GOOGLE_API_KEY:
            return "GOOGLE_API_KEY is not set in environment!"
        return None
    
    @classmethod
    def get_llm_params(cls) -> Dict[str, Any]:
        """
        Get parameters for initializing the LLM.
        
        Returns:
            Dict[str, Any]: Parameters for LLM initialization
        """
        return {
            "model": cls.LLM_MODEL,
            "google_api_key": cls.GOOGLE_API_KEY,
            "max_output_tokens": cls.MAX_TOKENS,
        }
    
    @classmethod
    def get_memory_params(cls) -> Dict[str, Any]:
        """
        Get parameters for initializing memory.
        
        Returns:
            Dict[str, Any]: Parameters for memory initialization
        """
        params = {
            "memory_key": "chat_history",
            "input_key": "human_input",
            "return_messages": True,
        }
        
        if cls.MEMORY_TYPE == "conversation_buffer_window":
            params["k"] = cls.MAX_MEMORY_ITEMS
            
        return params

# Perform validation at import time
config_error = Config.validate()
if config_error:
    raise ValueError(config_error) 