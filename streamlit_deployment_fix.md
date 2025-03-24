# Fixing Streamlit Cloud Deployment Configuration Error

You're encountering a `ValueError` in your Streamlit Cloud deployment, specifically in the configuration loading process. This is typically caused by missing environment variables or API keys.

## Step 1: Check Your Configuration Requirements

1. Look at your `.env.example` file to identify all required environment variables
2. The error is raised in `src/config.py` line 82, which suggests a critical configuration variable is missing

## Step 2: Set Up Secrets in Streamlit Cloud

1. Go to your Streamlit Cloud dashboard
2. Click on the deployed app
3. Click on the three dots (...) in the top-right corner
4. Select "Settings"
5. Scroll down to the "Secrets" section
6. Add all your environment variables from your `.env` file

For example, if your `.env` file contains:
```
GOOGLE_API_KEY=your_api_key_here
LLM_MODEL=gemini-2.0-pro-exp-02-05
MAX_TOKENS=4096
```

You would add them to the Streamlit secrets in TOML format:
```toml
GOOGLE_API_KEY = "your_api_key_here"
LLM_MODEL = "gemini-2.0-pro-exp-02-05"
MAX_TOKENS = "4096"
```

## Step 3: Check Your Config.py File

If setting the secrets doesn't resolve the issue, you may need to modify your `src/config.py` file to be more flexible with cloud deployments:

1. Make sure your code can fall back to default values for non-critical settings
2. Add better error messages that specify which variable is missing
3. Consider adding a check specifically for the Streamlit Cloud environment

Example modification:
```python
# Near line 82 in src/config.py
if critical_variable is None:
    config_error = f"Critical configuration variable '{variable_name}' is missing. Please set it in the environment or Streamlit secrets."
    raise ValueError(config_error)
```

## Step 4: Restart Your App

After adding the secrets:

1. Click "Save"
2. Restart your app by clicking on the three dots (...) and selecting "Reboot app"
3. Check the logs for any new errors

## Step 5: Debug Mode (If Needed)

If you're still having issues, you can add temporary debugging to your app to see which variables are missing:

```python
# At the top of your app.py
import os
import streamlit as st

# Display all environment variables for debugging
if "DEBUG_MODE" in os.environ and os.environ["DEBUG_MODE"] == "true":
    st.write("Environment variables:")
    # Filter out sensitive data
    safe_env = {k: "***" if "KEY" in k or "SECRET" in k else v 
                for k, v in os.environ.items()}
    st.write(safe_env)
    
    st.write("Streamlit secrets:")
    # Check if there are any secrets
    if hasattr(st, "secrets") and st.secrets:
        # Filter out sensitive data
        safe_secrets = {k: "***" if "key" in k.lower() or "secret" in k.lower() else v 
                       for k, v in st.secrets.items()}
        st.write(safe_secrets)
    else:
        st.write("No Streamlit secrets found")
```

Remember to remove this debug code after fixing the issue! 