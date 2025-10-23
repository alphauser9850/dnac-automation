from catalystcentersdk import CatalystCenterAPI

dnac = CatalystCenterAPI(
    base_url="https://10.10.10.48",
    username="admin",
    password="Password@123",
    verify=False
)

# Get list of all devices
devices = dnac.devices.get_device_list()

print("📋 Devices currently in DNA Center:")
print(f"Total devices: {len(devices.response)}")

for device in devices.response:
    print(f"✅ {device.hostname} - {device.managementIpAddress} - {device.reachabilityStatus} - {device.siteName}")



