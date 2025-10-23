from catalystcentersdk import CatalystCenterAPI

dnac = CatalystCenterAPI(
    base_url="https://10.10.10.48",
    username="admin",
    password="Password@123",
    verify=False
)

# Add a network device
device_response = dnac.devices.add_device(
    ipAddress=["10.10.47.10"],  # Device IP address
    userName="saif",              # CLI username
    password="Password@123",      # CLI password
    enablePassword="Password@123", # Enable password
    cliTransport="ssh",           # SSH transport
    netconfPort="830",            # NETCONF port
    snmpVersion="v2",             # SNMP version
    snmpROCommunity="read",     # SNMP read community
    snmpRWCommunity="write",    # SNMP write community
    type="NETWORK_DEVICE"         # Device type
)

print("Device added:", device_response)
