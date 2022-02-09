import enum
import folium

class Map:

    def draw(self,coords, center=(37.95156660478402, 124.6757830999149), title='1.html'):
        map = folium.Map(location=center, zoom_start=9)
        folium.Marker(center, popup='center', tooltip=f"center").add_to(map)
        for idx, coords in enumerate(coords):
            coords = coords.strip()
            coords = tuple(coords.split(','))
            folium.Marker(coords, popup=idx, tooltip=f"Location {idx}").add_to(map)
        map.add_child(folium.ClickForMarker('Clicked'))
        map.save(title)
