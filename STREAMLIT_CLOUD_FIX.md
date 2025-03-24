# Fixing Streamlit Cloud Deployment Error

## Error Summary

You're encountering a `ValueError` in your Streamlit Cloud deployment. The error originates in `src/config.py` line 82, which indicates a configuration loading issue, likely due to missing environment variables or API keys.

Error location:
```
File "/mount/src/ai-lawbot/src/config.py", line 82, in <module>
    raise ValueError(config_error)
```

## Quick Fix

1. Go to your Streamlit Cloud dashboard
2. Select your deployed app
3. Click on the three dots (...) menu
4. Select "Settings"
5. Scroll down to "Secrets"
6. Add the contents of the `.streamlit/secrets_template.toml` file
7. Update the API keys and other settings with your actual values
8. Click "Save"
9. Reboot your app

## Complete Solution

I've created several files to help you fix this issue:

1. `src/config_cloud.py` - A helper module for robust configuration loading
2. `src/config_patch.py` - Instructions to patch your existing config.py file
3. `streamlit_deployment_fix.md` - A detailed guide for fixing deployment issues
4. `.streamlit/secrets_template.toml` - Template for Streamlit Cloud secrets
5. `debug_cloud.py` - A diagnostic tool to identify configuration issues

### Step 1: Test Your Configuration Locally

Run the debug tool to identify any missing configuration:

```bash
streamlit run debug_cloud.py
```

This will show you which configuration variables are missing and need to be set in Streamlit Cloud.

### Step 2: Update Your Configuration System

1. Copy `src/config_cloud.py` to your project
2. Update your `src/config.py` file following the instructions in `src/config_patch.py`
3. Test locally to ensure it works

### Step 3: Set Up Streamlit Cloud Secrets

1. Copy the contents of `.streamlit/secrets_template.toml`
2. Add it to your Streamlit Cloud app's secrets section
3. Replace placeholder values with your actual API keys and configuration

### Step 4: Deploy to Streamlit Cloud

1. Commit and push your changes to GitHub
2. If you're using the deploy script, run:
   ```bash
   ./deploy.sh
   ```
   And select option 2 for Streamlit Cloud deployment

3. Reboot your app in Streamlit Cloud

## Why This Error Occurs

The error happens because Streamlit Cloud handles configuration differently from local development:

1. In local development, you use a `.env` file
2. In Streamlit Cloud, you need to use Streamlit's secrets management system
3. Your current `config.py` is likely only checking environment variables, not Streamlit secrets

The `config_cloud.py` helper provides functions that check both environment variables and Streamlit secrets, with proper fallbacks and error messages.

## Preventing Future Issues

1. Always use the `config_cloud.py` helpers for loading configuration
2. Keep your `.streamlit/secrets_template.toml` updated with any new configuration values
3. Test configuration changes locally before deploying to Streamlit Cloud
4. Use the debug tool to diagnose any configuration issues

## Need More Help?

If you continue to experience issues:

1. Check the Streamlit Cloud logs for more specific error messages
2. Run the debug tool locally and in Streamlit Cloud to compare configuration
3. Ensure your API keys are valid and have necessary permissions
4. Check if you need to update your dependencies in `requirements.txt` 