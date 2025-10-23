from catalystcentersdk import CatalystCenterAPI

dnac = CatalystCenterAPI(
    base_url="https://10.10.10.48",
    username="admin",
    password="Password@123",
    verify=False
)

# List of devices to add
devices = [
    {"ip": "10.10.47.111", "hostname": "switch1"},
    {"ip": "10.10.47.112", "hostname": "switch2"},
    {"ip": "10.10.47.10", "hostname": "router1"},
    {"ip": "10.10.47.20", "hostname": "router2"}
]

# Add each device
for device in devices:
    print(f"Adding device: {device['hostname']} ({device['ip']})")
    
    device_response = dnac.devices.add_device(
        ipAddress=[device['ip']],
        userName="saif",
        password="Password@123",
        enablePassword="Password@123",
        cliTransport="ssh",
        netconfPort="830",
        snmpVersion="v2",
        snmpROCommunity="read",
        snmpRWCommunity="write",
        type="NETWORK_DEVICE"
    )
    
    print(f"✅ {device['hostname']} added: {device_response.response.taskId}")

print("All devices added successfully!")
