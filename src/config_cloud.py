"""
Configuration utilities for Streamlit Cloud deployments.
This module provides helpers for loading configuration variables in different environments,
with special handling for Streamlit Cloud.
"""

import os
import streamlit as st
from typing import Dict, Any, Optional

def get_config_value(key: str, default: Any = None, required: bool = False) -> Any:
    """
    Get a configuration value from environment variables or Streamlit secrets.
    Prioritizes environment variables over Streamlit secrets.
    
    Args:
        key: The configuration key to look up
        default: Default value if the key is not found
        required: Whether the configuration value is required
        
    Returns:
        The configuration value, or the default if not found
        
    Raises:
        ValueError: If the key is required but not found
    """
    # Try environment variables first
    value = os.environ.get(key)
    
    # If not in environment, try Streamlit secrets
    if value is None and hasattr(st, 'secrets'):
        # Streamlit secrets are grouped by section, so try both directly and nested
        if key in st.secrets:
            value = st.secrets[key]
        # Look in sections too (common for API keys)
        elif "api_keys" in st.secrets and key in st.secrets["api_keys"]:
            value = st.secrets["api_keys"][key]
            
    # If still not found, use default or raise error if required
    if value is None:
        if required and default is None:
            raise ValueError(
                f"Required configuration variable '{key}' not found in environment "
                f"variables or Streamlit secrets. Please add this to your deployment configuration."
            )
        return default
        
    return value

def load_all_config() -> Dict[str, Any]:
    """
    Load all configuration values from environment variables and Streamlit secrets.
    Environment variables take precedence over Streamlit secrets.
    
    Returns:
        Dict of all configuration values
    """
    config = {}
    
    # First load from Streamlit secrets if available
    if hasattr(st, 'secrets'):
        # Flatten the secrets dict
        for key, value in st.secrets.items():
            if isinstance(value, dict):
                # Handle nested sections
                for nested_key, nested_value in value.items():
                    config[nested_key] = nested_value
            else:
                config[key] = value
    
    # Then override with environment variables
    for key, value in os.environ.items():
        config[key] = value
    
    return config

def get_api_key(name: str, required: bool = True) -> Optional[str]:
    """
    Helper specifically for API keys, checks common naming patterns.
    
    Args:
        name: Base name of the API key (e.g., "GOOGLE" for "GOOGLE_API_KEY")
        required: Whether the API key is required
        
    Returns:
        The API key value, or None if not found and not required
    """
    # Try different common formats for API keys
    possible_names = [
        f"{name}_API_KEY",
        f"{name}_KEY",
        f"{name.lower()}_api_key",
        f"{name.lower()}_key",
        name,
    ]
    
    for key_name in possible_names:
        value = get_config_value(key_name, required=False)
        if value:
            return value
    
    if required:
        raise ValueError(
            f"Required API key for '{name}' not found. Please add one of these to your "
            f"configuration: {', '.join(possible_names)}"
        )
    
    return None

def check_required_config(required_keys: list) -> None:
    """
    Check that all required configuration values are present.
    
    Args:
        required_keys: List of required configuration keys
        
    Raises:
        ValueError: If any required keys are missing
    """
    missing_keys = []
    
    for key in required_keys:
        try:
            get_config_value(key, required=True)
        except ValueError:
            missing_keys.append(key)
    
    if missing_keys:
        raise ValueError(
            f"Missing required configuration values: {', '.join(missing_keys)}. "
            f"Please add these to your environment variables or Streamlit secrets."
        )

def is_cloud_environment() -> bool:
    """
    Check if the current environment is Streamlit Cloud.
    
    Returns:
        True if running on Streamlit Cloud, False otherwise
    """
    # Streamlit Cloud sets specific environment variables
    return (
        "STREAMLIT_SHARING" in os.environ or
        "STREAMLIT_RUN_PATH" in os.environ or
        "STREAMLIT_SERVER_URL" in os.environ
    ) 