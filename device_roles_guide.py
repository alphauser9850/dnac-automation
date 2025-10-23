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

def assign_specific_device_roles_guide(site_name):
    """
    Guide for assigning specific device roles with step-by-step instructions
    
    Args:
        site_name (str): Name of the site where devices are assigned
    
    Returns:
        dict: Response from DNA Center API
    """
    print(f"🔧 GUIDE: Assigning specific device roles for site '{site_name}'...")
    
    # Get sites to find the site hierarchy
    print("\n1. Getting sites...")
    sites_response = dnac.sites.get_site()
    sites = sites_response.response
    
    site_id = None
    site_hierarchy = None
    for site in sites:
        if site.name == site_name:
            site_id = site.id
            site_hierarchy = f"Global/{site_name}"
            break
    
    if not site_id:
        print(f"❌ Site '{site_name}' not found")
        return None
    
    print(f"✅ Found site '{site_name}' with ID: {site_id}")
    print(f"✅ Using hierarchy: '{site_hierarchy}'")
    
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
    
    print(f"\n📋 STEP-BY-STEP GUIDE:")
    print(f"\n3. First, assign devices to site:")
    print(f"   dnac.sites.assign_devices_to_site(")
    print(f"       site_id='{site_id}',")
    print(f"       device=[")
    print(f"           {{'deviceId': '{fb1_device.id}', 'ip': '{fb1_device.managementIpAddress}'}},")
    print(f"           {{'deviceId': '{fb2_device.id}', 'ip': '{fb2_device.managementIpAddress}'}}")
    print(f"       ]")
    print(f"   )")
    print(f"   ⏳ Wait 30-60 seconds for assignment to complete")
    
    print(f"\n4. Then provision devices (REQUIRED for role assignment):")
    print(f"   # Provision FB-1")
    print(f"   dnac.sda.provision_wired_device(")
    print(f"       deviceManagementIpAddress='{fb1_device.managementIpAddress}',")
    print(f"       siteNameHierarchy='{site_hierarchy}'")
    print(f"   )")
    print(f"   ")
    print(f"   # Provision FB-2")
    print(f"   dnac.sda.provision_wired_device(")
    print(f"       deviceManagementIpAddress='{fb2_device.managementIpAddress}',")
    print(f"       siteNameHierarchy='{site_hierarchy}'")
    print(f"   )")
    print(f"   ⏳ Wait 60-90 seconds for provisioning to complete")
    
    print(f"\n5. Then assign Control Plane role to FB-2:")
    print(f"   dnac.sda.add_control_plane_device(")
    print(f"       deviceManagementIpAddress='{fb2_device.managementIpAddress}',")
    print(f"       siteNameHierarchy='{site_hierarchy}',")
    print(f"       routeDistributionProtocol='LISP_BGP'")
    print(f"   )")
    
    print(f"\n6. Assign External Border role to FB-1:")
    print(f"   dnac.sda.adds_border_device(")
    print(f"       payload=[{{")
    print(f"           'deviceManagementIpAddress': '{fb1_device.managementIpAddress}',")
    print(f"           'siteNameHierarchy': '{site_hierarchy}',")
    print(f"           'borderSessionType': 'EXTERNAL',")
    print(f"           'internalAutonomouSystemNumber': '65001'")
    print(f"       }}]")
    print(f"   )")
    
    print(f"\n7. Assign Internal Border role to FB-2:")
    print(f"   dnac.sda.adds_border_device(")
    print(f"       payload=[{{")
    print(f"           'deviceManagementIpAddress': '{fb2_device.managementIpAddress}',")
    print(f"           'siteNameHierarchy': '{site_hierarchy}',")
    print(f"           'borderSessionType': 'INTERNAL',")
    print(f"           'internalAutonomouSystemNumber': '65001'")
    print(f"       }}]")
    print(f"   )")
    
    print(f"\n🎯 FINAL RESULT:")
    print(f"   - FB-1 (10.10.47.10): External Border Node")
    print(f"   - FB-2 (10.10.47.20): Control Plane + Internal Border Node")
    
    print(f"\n⚠️  IMPORTANT NOTES:")
    print(f"   1. Devices must be assigned to site BEFORE provisioning")
    print(f"   2. Devices must be PROVISIONED BEFORE role assignment")
    print(f"   3. Wait 30-60 seconds after device assignment")
    print(f"   4. Wait 60-90 seconds after device provisioning")
    print(f"   5. Ensure 'Wired Client IP Device Tracking' is enabled in Network Settings")
    print(f"   6. Run each step separately and wait for completion")
    
    return {"status": "guide_completed"}

if __name__ == "__main__":
    # Get site name from user input
    site_name = input("Enter the site name where devices are assigned: ").strip()
    
    if not site_name:
        print("❌ Site name is required")
        exit()
    
    # Show guide
    result = assign_specific_device_roles_guide(site_name)
    
    if result:
        print("\n🎉 Guide completed successfully!")
    else:
        print("\n❌ Guide failed!")
