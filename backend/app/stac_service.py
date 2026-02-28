from pystac_client import Client
import planetary_computer
from backend.app.config import STAC_URL

def search_scene(collection, bbox, date_range, cloud):
    catalog = Client.open(STAC_URL)

    search = catalog.search(
        collections=[collection],
        bbox=bbox,
        datetime=date_range,
        query={"eo:cloud_cover": {"lt": cloud}},
    )

    items = list(search.get_items())
    if not items:
        return None

    item = planetary_computer.sign(items[0])
    return item
