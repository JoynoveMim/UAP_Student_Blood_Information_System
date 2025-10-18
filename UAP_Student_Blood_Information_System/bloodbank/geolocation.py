from math import radians, sin, cos, sqrt, atan2
from django.db.models import Q

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two points using Haversine formula
    Returns distance in kilometers
    """
    R = 6371  # Earth's radius in kilometers
    
    lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c

def get_nearby_donors(latitude, longitude, max_distance_km=1, blood_group=None):
    """
    Find donors within max_distance_km radius
    This is a simplified version - for production use PostGIS
    """
    from .models import UserProfile
    
    donors = UserProfile.objects.filter(
        is_donor=True,
        is_available=True,
        latitude__isnull=False,
        longitude__isnull=False
    )
    
    if blood_group:
        donors = donors.filter(blood_group=blood_group)
    
    nearby_donors = []
    for donor in donors:
        distance = calculate_distance(
            latitude, longitude,
            donor.latitude, donor.longitude
        )
        if distance <= max_distance_km:
            donor.distance = round(distance, 2)  # Add distance to donor object
            nearby_donors.append(donor)
    
    return sorted(nearby_donors, key=lambda x: x.distance)

def geocode_address(address):
    """
    Convert address to coordinates using a geocoding service
    For now, we'll use a mock - integrate with Google Maps/OpenStreetMap later
    """
    # Mock coordinates for UAP areas
    uap_locations = {
        'uap campus': (23.8151, 90.4255),
        'kuratoli': (23.8151, 90.4255),
        'mirpur': (23.8067, 90.3683),
        'dhanmondi': (23.7465, 90.3760),
        'gulshan': (23.7940, 90.4154),
        'banani': (23.7940, 90.4054),
        'uttara': (23.8759, 90.3795),
    }
    
    address_lower = address.lower()
    for location, coords in uap_locations.items():
        if location in address_lower:
            return coords
    
    # Default to UAP campus if no match
    return (23.8151, 90.4255)