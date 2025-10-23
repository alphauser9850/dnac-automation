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

def assign_specific_device_roles(site_name):
    """
    Assign specific device roles based on device names/IPs
    
    Args:
        site_name (str): Name of the site where devices are assigned
    
    Returns:
        dict: Response from DNA Center API
    """
    print(f"🔧 Assigning specific device roles for site '{site_name}'...")
    
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
    
    # First, assign devices to the site (prerequisite for role assignment)
    print(f"\n3. Assigning devices to site first (prerequisite for role assignment)...")
    device_list = [
        {
            "deviceId": fb1_device.id,
            "ip": fb1_device.managementIpAddress
        },
        {
            "deviceId": fb2_device.id,
            "ip": fb2_device.managementIpAddress
        }
    ]
    
    try:
        response = dnac.sites.assign_devices_to_site(
            site_id=site_id,
            device=device_list
        )
        print(f"✅ Devices assigned to site: {response}")
    except Exception as e:
        print(f"❌ Device assignment to site failed: {e}")
        return None
    
    # Wait for assignment to complete
    import time
    print("\n4. Waiting for device assignment to complete...")
    print("   (This may take up to 30 seconds)")
    time.sleep(30)
    
    # Check if devices need provisioning
    print(f"\n5. Checking device provisioning status...")
    
    # Try to provision FB-1 (will fail if already provisioned)
    print(f"   Checking FB-1 ({fb1_device.managementIpAddress})...")
    try:
        response = dnac.sda.provision_wired_device(
            deviceManagementIpAddress=fb1_device.managementIpAddress,
            siteNameHierarchy=site_hierarchy
        )
        print(f"   ✅ FB-1 provisioning: {response}")
    except Exception as e:
        if "already provisioned" in str(e):
            print(f"   ✅ FB-1 already provisioned (skipping)")
        else:
            print(f"   ❌ FB-1 provisioning failed: {e}")
            return None
    
    # Try to provision FB-2 (will fail if already provisioned)
    print(f"   Checking FB-2 ({fb2_device.managementIpAddress})...")
    try:
        response = dnac.sda.provision_wired_device(
            deviceManagementIpAddress=fb2_device.managementIpAddress,
            siteNameHierarchy=site_hierarchy
        )
        print(f"   ✅ FB-2 provisioning: {response}")
    except Exception as e:
        if "already provisioned" in str(e):
            print(f"   ✅ FB-2 already provisioned (skipping)")
        else:
            print(f"   ❌ FB-2 provisioning failed: {e}")
            return None
    
    print(f"\n6. Devices are ready for role assignment!")
    
    # Assign Control Plane role to FB-2
    print(f"\n7. Assigning Control Plane role to FB-2...")
    try:
        response = dnac.sda.add_control_plane_device(
            deviceManagementIpAddress=fb2_device.managementIpAddress,
            siteNameHierarchy=site_hierarchy,
            routeDistributionProtocol="LISP_BGP"
        )
        print(f"✅ Control Plane assignment to FB-2: {response}")
    except Exception as e:
        if "already has fabric role assigned" in str(e):
            print(f"✅ FB-2 already has Control Plane role assigned (skipping)")
        else:
            print(f"❌ Control Plane assignment to FB-2 failed: {e}")
            return None
    
    # Assign Border Device role to FB-1 (External Border)
    print(f"\n8. Assigning Border Device role to FB-1 (External Border)...")
    try:
        response = dnac.sda.adds_border_device(
            payload=[{
                "deviceManagementIpAddress": fb1_device.managementIpAddress,
                "siteNameHierarchy": site_hierarchy,
                "borderSessionType": "EXTERNAL",
                "internalAutonomouSystemNumber": "65001",
                "externalConnectivitySettings": [{
                    "externalAutonomouSystemNumber": "65002",
                    "interfaceName": "GigabitEthernet0/0/1",
                    "interfaceDescription": "External Border Interface"
                }]
            }]
        )
        print(f"✅ Border Device assignment to FB-1: {response}")
    except Exception as e:
        if "already has fabric role assigned" in str(e):
            print(f"✅ FB-1 already has Border role assigned (skipping)")
        else:
            print(f"❌ Border Device assignment to FB-1 failed: {e}")
            return None
    
    # Assign Border Device role to FB-2 (Internal Border)
    print(f"\n9. Assigning Border Device role to FB-2 (Internal Border)...")
    try:
        response = dnac.sda.adds_border_device(
            payload=[{
                "deviceManagementIpAddress": fb2_device.managementIpAddress,
                "siteNameHierarchy": site_hierarchy,
                "borderSessionType": "INTERNAL",
                "internalAutonomouSystemNumber": "65001"
            }]
        )
        print(f"✅ Internal Border assignment to FB-2: {response}")
    except Exception as e:
        if "already has fabric role assigned" in str(e):
            print(f"✅ FB-2 already has Internal Border role assigned (skipping)")
        else:
            print(f"❌ Internal Border assignment to FB-2 failed: {e}")
            return None
    
    print(f"\n🎯 Device role assignment completed!")
    print(f"📋 Summary:")
    print(f"   - FB-1 (10.10.47.10): External Border Node")
    print(f"   - FB-2 (10.10.47.20): Control Plane + Internal Border Node")
    
    return {"status": "completed"}

if __name__ == "__main__":
    # Get site name from user input
    site_name = input("Enter the site name where devices are assigned: ").strip()
    
    if not site_name:
        print("❌ Site name is required")
        exit()
    
    # Assign device roles
    result = assign_specific_device_roles(site_name)
    
    if result:
        print("\n🎉 Device role assignment completed!")
    else:
        print("\n❌ Device role assignment failed!")
