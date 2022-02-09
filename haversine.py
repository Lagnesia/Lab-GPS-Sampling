import math

class Haversine2D:
    '''
    use the haversine class to calculate the distance between
    two lat/lon coordnate pairs.
    output distance available in kilometers, meters, miles, and feet.
    example usage: Haversine([lat1,lon1],[lat2,lon2]).feet
    '''
    def __init__(self,coord1,coord2):
        lat1,lon1=coord1
        lat2,lon2=coord2
        
        R=6371000                               # radius of Earth in meters
        phi_1=math.radians(lat1)
        phi_2=math.radians(lat2)

        delta_phi=math.radians(lat2-lat1)
        delta_lambda=math.radians(lon2-lon1)

        a=math.sin(delta_phi/2.0)**2+\
           math.cos(phi_1)*math.cos(phi_2)*\
           math.sin(delta_lambda/2.0)**2
        c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
        
        self.meters=R*c                         # output distance in meters
        self.km=self.meters/1000.0              # output distance in kilometers
        self.miles=self.meters*0.000621371      # output distance in miles
        self.feet=self.miles*5280               # output distance in feet

class Haversine3D:
    """
    use the haversine class to calculate the distance between
    three lat/lon/alt coordnate pairs.
    output distance available in kilometers, meters, miles, and feet.
    example usage: Haversine([lat1,lon1,alt1],[lat2,lon2,alt2]).feet
    """
    def __init__(self, coord1, coord2):
        lat1, lon1, alt1 = coord1
        lat2, lon2, alt2 = coord2
        
        R = 6371000                             # radius of Earth in meters
        phi_1 = math.radians(lat1)
        phi_2 = math.radians(lat2)

        delta_phi       = math.radians(lat2-lat1)
        delta_lambda    = math.radians(lon2-lon1)

        a = math.sin(delta_phi/2.0) ** 2 \
            + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda/2.0) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        self.meters = math.sqrt((R*c)**2 + (alt1-alt2)**2)  # output distance in meters
        self.km     = self.meters / 1000.0                  # output distance in kilometers
        self.miles  = self.meters * 0.000621371             # output distance in miles
        self.feet   = self.miles * 5280                     # output distance in feet

class InverseHaversine2D:
    """
    calculate coord tuple(lat, lon) from coord1 tuple(lat1, lon1) and coord2 tuple(x, y)(meter, ENU)
    coord = coord1 + coord2
    """
    def __init__(self, coord1, coord2):
        lat1, lon1 = coord1
        x, y = coord2

        R = 6371000

        theta_y = (y / R) * (180 / math.pi)
        theta_x = (x / (R * math.cos(abs(math.radians(lat1)))) * (180 / math.pi))

        self._lat = lat1 + theta_y
        self._lon = lon1 + theta_x

    def getCoord(self):
        return (self._lat, self._lon)

class InverseHaversine3D:
    """
    calculate coord tuple(lat, lon, alt) from coord1 tuple(lat1, lon1, alt1) and coord2 tuple(x, y, z)(meter, ENU)
    coord = coord1 + coord2
    """
    def __init__(self, coord1, coord2):
        lat1, lon1, alt1 = coord1
        x, y, z = coord2

        R = 6371000

        theta_y = (y / R) * (180 / math.pi)
        theta_x = (x / (R * math.cos(abs(math.radians(lat1)))) * (180 / math.pi))

        self._lat = lat1 + theta_y
        self._lon = lon1 + theta_x
        self._alt = alt1 + z

    def getCoord(self):
        return (self._lat, self._lon, self._alt)