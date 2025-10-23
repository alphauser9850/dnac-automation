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

def create_fabric_and_assign_roles(site_name):
    """
    Create a fabric from site name and assign device roles
    
    Args:
        site_name (str): Name of the site to create fabric from
    
    Returns:
        dict: Response from DNA Center API
    """
    print(f"🏗️ Creating fabric from site '{site_name}' and assigning device roles...")
    
    # Get sites to find the site
    print("\n1. Getting sites...")
    sites_response = dnac.sites.get_site()
    sites = sites_response.response
    
    site_id = None
    site_hierarchy = None
    for site in sites:
        if site.name == site_name:
            site_id = site.id
            site_hierarchy = site.name
            break
    
    if not site_id:
        print(f"❌ Site '{site_name}' not found")
        return None
    
    print(f"✅ Found site '{site_name}' with ID: {site_id}")
    
    # Get devices
    print("\n2. Getting devices...")
    devices_response = dnac.devices.get_device_list()
    devices = devices_response.response
    print(f"Found {len(devices)} devices")
    
    # Display devices for role assignment
    print("\n3. Available devices for role assignment:")
    for i, device in enumerate(devices, 1):
        print(f"  {i}. {device.hostname} ({device.managementIpAddress})")
    
    # First, assign devices to the site
    print("\n4. Assigning devices to site first...")
    device_list = []
    for device in devices:
        device_list.append({
            "deviceId": device.id,
            "ip": device.managementIpAddress
        })
    
    try:
        response = dnac.sites.assign_devices_to_site(
            site_id=site_id,
            device=device_list
        )
        print(f"✅ Devices assigned to site: {response}")
    except Exception as e:
        print(f"❌ Device assignment to site failed: {e}")
        return None
    
    # Wait a moment for assignment to complete
    import time
    print("\n5. Waiting for device assignment to complete...")
    time.sleep(10)
    
    # Now assign device roles
    print("\n6. Assigning device roles...")
    
    # Assign first device as Control Plane Device
    if len(devices) > 0:
        control_plane_device = devices[0]
        print(f"\n📡 Assigning Control Plane role to: {control_plane_device.hostname}")
        try:
            response = dnac.sda.add_control_plane_device(
                deviceManagementIpAddress=control_plane_device.managementIpAddress,
                siteNameHierarchy=site_hierarchy,
                routeDistributionProtocol="LISP_BGP"
            )
            print(f"✅ Control Plane assignment: {response}")
        except Exception as e:
            print(f"❌ Control Plane assignment failed: {e}")
    
    # Assign second device as Border Device (with proper parameters)
    if len(devices) > 1:
        border_device = devices[1]
        print(f"\n🔗 Assigning Border Device role to: {border_device.hostname}")
        try:
            response = dnac.sda.adds_border_device(
                payload=[{
                    "deviceManagementIpAddress": border_device.managementIpAddress,
                    "siteNameHierarchy": site_hierarchy,
                    "borderSessionType": "EXTERNAL"
                }]
            )
            print(f"✅ Border Device assignment: {response}")
        except Exception as e:
            print(f"❌ Border Device assignment failed: {e}")
    
    # Assign remaining devices as Edge Devices
    if len(devices) > 2:
        edge_devices = devices[2:]
        print(f"\n🌐 Assigning Edge Device roles to {len(edge_devices)} devices:")
        for device in edge_devices:
            print(f"  - {device.hostname}")
            try:
                response = dnac.sda.add_edge_device(
                    deviceManagementIpAddress=device.managementIpAddress,
                    siteNameHierarchy=site_hierarchy
                )
                print(f"    ✅ Edge assignment: {response}")
            except Exception as e:
                print(f"    ❌ Edge assignment failed: {e}")
    
    print(f"\n🎯 Fabric creation and device role assignment completed for site '{site_name}'!")
    return {"status": "completed"}

if __name__ == "__main__":
    # Get site name from user input
    site_name = input("Enter the site name to create fabric from: ").strip()
    
    if not site_name:
        print("❌ No site name provided")
        exit()
    
    # Create fabric and assign roles
    result = create_fabric_and_assign_roles(site_name)
    
    if result:
        print("\n🎉 Fabric creation and device role assignment completed!")
    else:
        print("\n❌ Fabric creation and device role assignment failed!")