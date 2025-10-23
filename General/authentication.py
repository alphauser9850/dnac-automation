import os
from catalystcentersdk import CatalystCenterAPI
from catalystcentersdk.exceptions import AccessTokenError, ApiError

def create_dnac_connection():
    """
    Create a Catalyst Center API connection object.
    Uses environment variables if available, otherwise falls back to hardcoded values.
    """
    try:
        # Try to get credentials from environment variables first (best practice)
        username = os.getenv('CATALYST_CENTER_USERNAME', 'admin')
        password = os.getenv('CATALYST_CENTER_PASSWORD', 'Password@123')
        base_url = os.getenv('CATALYST_CENTER_BASE_URL', 'https://10.10.10.48')
        
        # Create API connection object
        api = CatalystCenterAPI(
            username=username,
            password=password,
            base_url=base_url,
            verify=False,  # Set to True in production with proper certificates
            debug=False    # Set to True for debugging API calls
        )
        
        print(f"Successfully connected to Catalyst Center at: {base_url}")
        return api
        
    except AccessTokenError as e:
        print(f"Authentication failed: {e}")
        return None
    except ApiError as e:
        print(f"API Error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

if __name__ == "__main__":
    # Create the API connection
    api = create_dnac_connection()
    
    if api:
        print("Authentication successful!")
        print(f"API object: {api}")
    else:
        print("Failed to authenticate with Catalyst Center")
