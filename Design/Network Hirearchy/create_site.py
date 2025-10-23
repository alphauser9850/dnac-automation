from catalystcentersdk import CatalystCenterAPI

dnac = CatalystCenterAPI(
    base_url="https://10.10.10.48",
    username="admin",
    password="Password@123",
    verify=False
)

# Create a site (area)
site_response = dnac.sites.create_site(
    type="area",
    site={
        "area": {
            "name": "Ventura",
            "parentName": "Global"
        }
    }
)

print("Site created:", site_response)
