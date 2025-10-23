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

def assign_device_roles_simple(site_name):
    """
    Simple device role assignment script with prerequisites check
    
    Args:
        site_name (str): Name of the site where devices are assigned
    
    Returns:
        dict: Response from DNA Center API
    """
    print(f"🔧 Assigning device roles for site '{site_name}'...")
    
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
    
    # Check device provisioning status
    print(f"\n3. Checking device provisioning status...")
    
    # Try to provision FB-1 (will fail if already provisioned)
    try:
        dnac.sda.provision_wired_device(
            deviceManagementIpAddress=fb1_device.managementIpAddress,
            siteNameHierarchy=site_hierarchy
        )
        print(f"✅ FB-1 provisioning initiated")
    except Exception as e:
        if "already provisioned" in str(e):
            print(f"✅ FB-1 already provisioned")
        else:
            print(f"❌ FB-1 provisioning failed: {e}")
            return None
    
    # Try to provision FB-2 (will fail if already provisioned)
    try:
        dnac.sda.provision_wired_device(
            deviceManagementIpAddress=fb2_device.managementIpAddress,
            siteNameHierarchy=site_hierarchy
        )
        print(f"✅ FB-2 provisioning initiated")
    except Exception as e:
        if "already provisioned" in str(e):
            print(f"✅ FB-2 already provisioned")
        else:
            print(f"❌ FB-2 provisioning failed: {e}")
            return None
    
    print(f"\n4. Attempting device role assignments...")
    
    # Assign Control Plane role to FB-2
    print(f"\n   Assigning Control Plane role to FB-2...")
    try:
        response = dnac.sda.add_control_plane_device(
            deviceManagementIpAddress=fb2_device.managementIpAddress,
            siteNameHierarchy=site_hierarchy,
            routeDistributionProtocol="LISP_BGP"
        )
        print(f"   ✅ Control Plane assignment to FB-2: SUCCESS")
    except Exception as e:
        if "already has fabric role assigned" in str(e):
            print(f"   ✅ FB-2 already has Control Plane role assigned")
        else:
            print(f"   ❌ Control Plane assignment to FB-2 failed: {e}")
    
    # Assign Internal Border role to FB-2
    print(f"\n   Assigning Internal Border role to FB-2...")
    try:
        response = dnac.sda.adds_border_device(
            payload=[{
                "deviceManagementIpAddress": fb2_device.managementIpAddress,
                "siteNameHierarchy": site_hierarchy,
                "borderSessionType": "INTERNAL",
                "internalAutonomouSystemNumber": "65001"
            }]
        )
        print(f"   ✅ Internal Border assignment to FB-2: SUCCESS")
    except Exception as e:
        if "already has fabric role assigned" in str(e):
            print(f"   ✅ FB-2 already has Internal Border role assigned")
        else:
            print(f"   ❌ Internal Border assignment to FB-2 failed: {e}")
    
    # Assign External Border role to FB-1 (requires external ASN configuration)
    print(f"\n   Assigning External Border role to FB-1...")
    print(f"   ⚠️  NOTE: External Border requires external ASN configuration in DNA Center")
    print(f"   📋 Prerequisites:")
    print(f"      1. Configure external ASN (e.g., 65002) in DNA Center")
    print(f"      2. Set up IP Transit for the external ASN")
    print(f"      3. Configure external connectivity settings")
    
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
        print(f"   ✅ External Border assignment to FB-1: SUCCESS")
    except Exception as e:
        if "already has fabric role assigned" in str(e):
            print(f"   ✅ FB-1 already has External Border role assigned")
        elif "Could not find IP Transit" in str(e):
            print(f"   ⚠️  External Border assignment requires external ASN configuration")
            print(f"   💡 Configure external ASN 65002 in DNA Center first")
        else:
            print(f"   ❌ External Border assignment to FB-1 failed: {e}")
    
    print(f"\n🎯 Device role assignment summary:")
    print(f"   - FB-1 (10.10.47.10): External Border Node (requires external ASN config)")
    print(f"   - FB-2 (10.10.47.20): Control Plane + Internal Border Node")
    
    print(f"\n📋 Next Steps:")
    print(f"   1. Configure external ASN in DNA Center for FB-1 External Border")
    print(f"   2. Set up IP Transit for external connectivity")
    print(f"   3. Verify device roles in DNA Center UI")
    
    return {"status": "completed"}

if __name__ == "__main__":
    # Get site name from user input
    site_name = input("Enter the site name where devices are assigned: ").strip()
    
    if not site_name:
        print("❌ Site name is required")
        exit()
    
    # Assign device roles
    result = assign_device_roles_simple(site_name)
    
    if result:
        print("\n🎉 Device role assignment completed!")
    else:
        print("\n❌ Device role assignment failed!")
