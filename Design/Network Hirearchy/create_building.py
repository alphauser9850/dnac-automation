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

def create_building(building_name, parent_name="Global", address="123 Main Street", latitude=34.2746, longitude=-119.2290):
    """
    Create a building in DNA Center
    
    Args:
        building_name (str): Name of the building to create
        parent_name (str): Parent site name (default: "Global")
        address (str): Building address
        latitude (float): Building latitude
        longitude (float): Building longitude
    
    Returns:
        dict: Response from DNA Center API
    """
    print(f"🏗️ Creating building '{building_name}' under '{parent_name}'...")
    
    try:
        response = dnac.sites.create_site(
            type="building",
            site={
                "building": {
                    "name": building_name,
                    "parentName": parent_name,
                    "address": address,
                    "latitude": latitude,
                    "longitude": longitude
                }
            }
        )
        print(f"✅ Building creation response: {response}")
        return response
        
    except Exception as e:
        print(f"❌ Failed to create building: {e}")
        return None

if __name__ == "__main__":
    # Create BLDG-1 building
    result = create_building(
        building_name="BLDG-1",
        parent_name="Global",
        address="123 Main Street, Ventura, CA 93001",
        latitude=34.2746,
        longitude=-119.2290
    )
    
    if result:
        print("\n🎯 Building creation completed!")
    else:
        print("\n❌ Building creation failed!")
