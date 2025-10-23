from catalystcentersdk import CatalystCenterAPI

dnac = CatalystCenterAPI(
    base_url="https://10.10.10.48",
    username="admin",
    password="Password@123",
    verify=False
)

def create_site(site_name, site_type="area"):
    """Create a new site"""
    response = dnac.sites.create_site(
        type=site_type,
        site={
            "area": {
                "name": site_name,
                "parentName": "Global"
            }
        }
    )
    print(f"✅ Site '{site_name}' created")
    print(f"📋 Response: {response}")
    return response

def update_site(site_id, new_name):
    """Update an existing site"""
    response = dnac.sites.update_site(
        site_id=site_id,
        site={
            "area": {
                "name": new_name
            }
        }
    )
    print(f"✅ Site updated to '{new_name}'")
    print(f"📋 Response: {response}")
    return response

def delete_site(site_id):
    """Delete a site"""
    response = dnac.sites.delete_site(site_id=site_id)
    print(f"✅ Site deleted")
    print(f"📋 Response: {response}")
    return response

def get_sites():
    """Get all sites"""
    response = dnac.sites.get_site()
    print(f"📋 Found {len(response.response)} sites:")
    for site in response.response:
        print(f"  - {site.name} (ID: {site.id})")
    return response

# Execute functions
print("🚀 Starting site operations...")

# Get existing sites
print("\n1. Getting existing sites:")
get_sites()

# Create a new site
print("\n2. Creating new site:")
create_response = create_site("My Test Area")

# Get sites again to see the new one
print("\n3. Getting sites after creation:")
sites_response = get_sites()

# Find the site ID for the newly created site
test_site_id = None
for site in sites_response.response:
    if site.name == "My Test Area":
        test_site_id = site.id
        break

if test_site_id:
    # Update the site
    print(f"\n4. Updating site (ID: {test_site_id}):")
    update_site(test_site_id, "My Updated Area")
    
    # Get sites to see the update
    print("\n5. Getting sites after update:")
    get_sites()
    
    # Delete the site
    print(f"\n6. Deleting site (ID: {test_site_id}):")
    delete_site(test_site_id)
    
    # Get sites to see the deletion
    print("\n7. Getting sites after deletion:")
    get_sites()
else:
    print("\n❌ Could not find the test site to update/delete")

print("\n🎯 Site operations completed!")
