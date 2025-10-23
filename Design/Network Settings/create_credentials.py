from catalystcentersdk import CatalystCenterAPI

dnac = CatalystCenterAPI(
    base_url="https://10.10.10.48",
    username="admin",
    password="Password@123",
    verify=False
)

# Create CLI credentials
cli_response = dnac.discovery.create_global_credentials(
    cliCredential=[
        {
            "username": "saif",
            "password": "Password@123",
            "enablePassword": "Password@123",
            "description": "Global CLI Credentials"
        }
    ]
)

# Create SNMPv2 Read credentials
snmp_read_response = dnac.discovery.create_global_credentials(
    snmpV2cRead=[
        {
            "description": "SNMPv2 Read Community",
            "readCommunity": "public"
        }
    ]
)

# Create SNMPv2 Write credentials
snmp_write_response = dnac.discovery.create_global_credentials(
    snmpV2cWrite=[
        {
            "description": "SNMPv2 Write Community",
            "writeCommunity": "private"
        }
    ]
)

print("CLI:", cli_response)
print("SNMP Read:", snmp_read_response)
print("SNMP Write:", snmp_write_response)
