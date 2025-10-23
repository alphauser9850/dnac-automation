from catalystcentersdk import CatalystCenterAPI
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Create DNA Center connection
dnac = CatalystCenterAPI(
    base_url="https://10.10.10.48",
    username="admin",
    password="Password@123",
    verify=False
)

def create_fabric(fabric_name, site_name):
    """
    Create a fabric by adding a site to it
    
    Args:
        fabric_name (str): Name of the fabric to create
        site_name (str): Name of the site to add to the fabric
    
    Returns:
        dict: Response from DNA Center API
    """
    print(f"🏗️ Creating fabric '{fabric_name}' with site '{site_name}'...")
    
    # Get sites to find the correct site hierarchy
    print("\n1. Getting sites...")
    sites_response = dnac.sites.get_site()
    sites = sites_response.response
    
    site_hierarchy = None
    for site in sites:
        if site.name == site_name:
            site_hierarchy = f"Global/{site_name}"
            break
    
    if not site_hierarchy:
        print(f"❌ Site '{site_name}' not found")
        return None
    
    print(f"✅ Found site '{site_name}', using hierarchy: '{site_hierarchy}'")
    
    # Try to create fabric
    print(f"\n2. Creating fabric...")
    try:
        response = dnac.sda.add_site(
            fabricName=fabric_name,
            siteNameHierarchy=site_hierarchy,
            fabricType="FABRIC_SITE"
        )
        print(f"✅ Fabric creation response: {response}")
        return response
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Failed to create fabric: {error_msg}")
        
        # Check for specific error messages and provide guidance
        if "Wired Client IP Device Tracking" in error_msg:
            print(f"\n📋 PREREQUISITE REQUIRED:")
            print(f"   Before creating a fabric, you need to enable:")
            print(f"   'Wired Client IP Device Tracking' in Network Settings")
            print(f"   ")
            print(f"   Steps:")
            print(f"   1. Go to DNA Center Web UI")
            print(f"   2. Navigate to: Design > Network Settings")
            print(f"   3. Go to: Telemetry > Wired Client Data Collection")
            print(f"   4. Enable 'Wired Client IP Device Tracking' for site '{site_name}'")
            print(f"   5. Then run this script again")
        
        return None

if __name__ == "__main__":
    # Get fabric name and site name from user input
    fabric_name = input("Enter the fabric name: ").strip()
    site_name = input("Enter the site name to add to fabric: ").strip()
    
    if not fabric_name or not site_name:
        print("❌ Both fabric name and site name are required")
        exit()
    
    # Create fabric
    result = create_fabric(fabric_name, site_name)
    
    if result:
        print("\n🎯 Fabric creation completed!")
    else:
        print("\n❌ Fabric creation failed!")
        print("\n💡 Check the prerequisites above and try again.")