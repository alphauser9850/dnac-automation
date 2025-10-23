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

def assign_specific_device_roles_demo(site_name):
    """
    Demo script showing how to assign specific device roles
    
    Args:
        site_name (str): Name of the site where devices are assigned
    
    Returns:
        dict: Response from DNA Center API
    """
    print(f"🔧 DEMO: Assigning specific device roles for site '{site_name}'...")
    
    # Get sites to find the site hierarchy
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
    
    # Get devices
    print("\n2. Getting devices...")
    devices_response = dnac.devices.get_device_list()
    devices = devices_response.response
    print(f"Found {len(devices)} devices")
    
    # Find specific devices
    fb1_device = None
    fb2_device = None
    
    for device in devices:
        if device.hostname == "FB-1.ccielab.net" and device.managementIpAddress == "10.10.47.10":
            fb1_device = device
        elif device.hostname == "FB-2.ccielab.net" and device.managementIpAddress == "10.10.47.20":
            fb2_device = device
    
    if not fb1_device:
        print("❌ FB-1 device (10.10.47.10) not found")
        return None
    
    if not fb2_device:
        print("❌ FB-2 device (10.10.47.20) not found")
        return None
    
    print(f"✅ Found FB-1: {fb1_device.hostname} ({fb1_device.managementIpAddress})")
    print(f"✅ Found FB-2: {fb2_device.hostname} ({fb2_device.managementIpAddress})")
    
    # Show the API calls that would be made
    print(f"\n3. API Calls that would be made:")
    
    print(f"\n📡 Control Plane assignment to FB-2:")
    print(f"   dnac.sda.add_control_plane_device(")
    print(f"       deviceManagementIpAddress='{fb2_device.managementIpAddress}',")
    print(f"       siteNameHierarchy='{site_hierarchy}',")
    print(f"       routeDistributionProtocol='LISP_BGP'")
    print(f"   )")
    
    print(f"\n🔗 External Border assignment to FB-1:")
    print(f"   dnac.sda.adds_border_device(")
    print(f"       payload=[{{")
    print(f"           'deviceManagementIpAddress': '{fb1_device.managementIpAddress}',")
    print(f"           'siteNameHierarchy': '{site_hierarchy}',")
    print(f"           'borderSessionType': 'EXTERNAL'")
    print(f"       }}]")
    print(f"   )")
    
    print(f"\n🔗 Internal Border assignment to FB-2:")
    print(f"   dnac.sda.adds_border_device(")
    print(f"       payload=[{{")
    print(f"           'deviceManagementIpAddress': '{fb2_device.managementIpAddress}',")
    print(f"           'siteNameHierarchy': '{site_hierarchy}',")
    print(f"           'borderSessionType': 'INTERNAL'")
    print(f"       }}]")
    print(f"   )")
    
    print(f"\n🎯 DEMO: Device role assignment plan!")
    print(f"📋 Summary:")
    print(f"   - FB-1 (10.10.47.10): External Border Node")
    print(f"   - FB-2 (10.10.47.20): Control Plane + Internal Border Node")
    
    return {"status": "demo_completed"}

if __name__ == "__main__":
    # Get site name from user input
    site_name = input("Enter the site name where devices are assigned: ").strip()
    
    if not site_name:
        print("❌ Site name is required")
        exit()
    
    # Assign device roles (demo)
    result = assign_specific_device_roles_demo(site_name)
    
    if result:
        print("\n🎉 Demo completed successfully!")
    else:
        print("\n❌ Demo failed!")
