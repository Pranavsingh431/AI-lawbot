"""
Debug tool for Streamlit Cloud deployments.
Run this script locally to identify configuration issues.
"""

import os
import sys
import streamlit as st
import json
from dotenv import load_dotenv

def main():
    st.set_page_config(page_title="Legal Advisor AI - Debug Mode", layout="wide")
    
    st.title("Legal Advisor AI - Cloud Deployment Debug Tool")
    st.write("This tool helps diagnose configuration issues with your Streamlit Cloud deployment.")
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Check for required Python modules
    st.header("1. Python Module Check")
    required_modules = [
        "streamlit", "google.generativeai", "langchain", "pandas", 
        "dotenv", "pdfplumber", "pymongo", "flask"
    ]
    
    module_status = {}
    for module in required_modules:
        try:
            __import__(module.split(".")[0])
            module_status[module] = "✅ Installed"
        except ImportError:
            module_status[module] = "❌ Missing"
    
    st.json(module_status)
    
    # Environment variables
    st.header("2. Environment Variables Check")
    
    # Critical environment variables that might be needed
    critical_vars = [
        "GOOGLE_API_KEY", "LLM_MODEL", "MAX_TOKENS", 
        "DEBUG_MODE", "LOG_LEVEL", "MAX_PDF_SIZE_MB"
    ]
    
    env_var_status = {}
    for var in critical_vars:
        value = os.environ.get(var)
        if value:
            if "KEY" in var or "SECRET" in var:
                env_var_status[var] = "✅ Set (value hidden)"
            else:
                env_var_status[var] = f"✅ Set to: {value}"
        else:
            env_var_status[var] = "❌ Not set"
    
    st.json(env_var_status)
    
    # Check Streamlit secrets
    st.header("3. Streamlit Secrets Check")
    
    if hasattr(st, 'secrets') and st.secrets:
        secrets_status = {}
        # Check for direct secrets
        for var in critical_vars:
            if var in st.secrets:
                if "KEY" in var or "SECRET" in var:
                    secrets_status[var] = "✅ Set (value hidden)"
                else:
                    secrets_status[var] = f"✅ Set to: {st.secrets[var]}"
            else:
                secrets_status[var] = "❌ Not set directly"
                
        # Check for secrets in the api_keys section
        if "api_keys" in st.secrets:
            st.write("API Keys section found in secrets")
            for var in critical_vars:
                if var in st.secrets.api_keys:
                    if "KEY" in var or "SECRET" in var:
                        secrets_status[f"api_keys.{var}"] = "✅ Set (value hidden)"
                    else:
                        secrets_status[f"api_keys.{var}"] = f"✅ Set to: {st.secrets.api_keys[var]}"
        
        st.json(secrets_status)
    else:
        st.warning("No Streamlit secrets found. This is expected in local development but should be set in Streamlit Cloud.")
    
    # File system check
    st.header("4. File System Check")
    
    expected_files = [
        "app.py", 
        "src/legal_bot.py", 
        "src/config.py", 
        "requirements.txt"
    ]
    
    file_status = {}
    for file_path in expected_files:
        if os.path.exists(file_path):
            file_status[file_path] = f"✅ Found ({os.path.getsize(file_path)} bytes)"
        else:
            file_status[file_path] = "❌ Missing"
    
    st.json(file_status)
    
    # Configuration recommendations
    st.header("5. Configuration Recommendations")
    
    recommendations = []
    
    # Check if Google API key is missing
    if os.environ.get("GOOGLE_API_KEY") is None and (not hasattr(st, 'secrets') or 
                                                    "GOOGLE_API_KEY" not in st.secrets and
                                                    ("api_keys" not in st.secrets or 
                                                     "GOOGLE_API_KEY" not in st.secrets.api_keys)):
        recommendations.append({
            "issue": "Missing Google API Key",
            "solution": "Add GOOGLE_API_KEY to your Streamlit Cloud secrets or environment variables"
        })
    
    # Recommend cloud config helper
    if not os.path.exists("src/config_cloud.py"):
        recommendations.append({
            "issue": "Missing config_cloud.py helper",
            "solution": "Add the config_cloud.py helper file to make configuration more robust in cloud environments"
        })
    
    # Check if config.py is using the right approach
    if os.path.exists("src/config.py"):
        with open("src/config.py", "r") as f:
            config_content = f.read()
            if "streamlit" not in config_content.lower():
                recommendations.append({
                    "issue": "config.py might not be checking Streamlit secrets",
                    "solution": "Update config.py to check both environment variables and Streamlit secrets"
                })
    
    st.json(recommendations)
    
    # Next steps
    st.header("6. Next Steps")
    
    st.markdown("""
    Based on the checks above, consider these next steps:
    
    1. **Fix Missing Configuration**: Add any missing configuration values to your Streamlit Cloud secrets
    2. **Update config.py**: Use the provided config_cloud.py and patch instructions to make your configuration more robust
    3. **Check Logs**: After making changes, check the Streamlit Cloud logs for more details
    4. **Test Locally First**: Test your changes locally before deploying to Streamlit Cloud
    
    For detailed instructions, refer to the streamlit_deployment_fix.md document provided.
    """)
    
    # Export results
    if st.button("Export Debug Results"):
        results = {
            "modules": module_status,
            "environment_variables": env_var_status,
            "file_system": file_status,
            "recommendations": recommendations
        }
        
        # Create a downloadable JSON file
        st.download_button(
            label="Download Debug Results",
            data=json.dumps(results, indent=2),
            file_name="streamlit_debug_results.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main() 