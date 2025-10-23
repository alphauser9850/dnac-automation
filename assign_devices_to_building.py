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

def assign_devices_to_building(building_name):
    """
    Assign all devices to a specific building
    
    Args:
        building_name (str): Name of the building to assign devices to
    
    Returns:
        dict: Response from DNA Center API
    """
    print(f"🔗 Assigning devices to building '{building_name}'...")
    
    # Get sites to find the building
    print("\n1. Getting sites...")
    sites_response = dnac.sites.get_site()
    sites = sites_response.response
    
    building_site_id = None
    for site in sites:
        if site.name == building_name:
            building_site_id = site.id
            break
    
    if not building_site_id:
        print(f"❌ Building '{building_name}' not found")
        return None
    
    print(f"✅ Found building '{building_name}' with ID: {building_site_id}")
    
    # Get devices
    print("\n2. Getting devices...")
    devices_response = dnac.devices.get_device_list()
    devices = devices_response.response
    print(f"Found {len(devices)} devices")
    
    # Prepare device list for assignment
    print("\n3. Preparing device list...")
    device_list = []
    for device in devices:
        print(f"  - {device.hostname} ({device.managementIpAddress})")
        device_list.append({
            "deviceId": device.id,
            "ip": device.managementIpAddress
        })
    
    # Assign devices to building
    print(f"\n4. Assigning {len(device_list)} devices to '{building_name}'...")
    try:
        response = dnac.sites.assign_devices_to_site(
            site_id=building_site_id,
            device=device_list
        )
        print(f"✅ Device assignment response: {response}")
        return response
        
    except Exception as e:
        print(f"❌ Device assignment failed: {e}")
        return None

if __name__ == "__main__":
    # Assign devices to BLDG-1 building
    result = assign_devices_to_building("BLDG-1")
    
    if result:
        print("\n🎯 Device assignment completed!")
    else:
        print("\n❌ Device assignment failed!")
