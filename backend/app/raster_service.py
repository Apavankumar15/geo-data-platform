import rasterio
from rasterio.mask import mask
import geopandas as gpd
import os
import uuid
from app.config import OUTPUT_FOLDER

def clip_raster(asset_url, aoi_path):

    gdf = gpd.read_file(aoi_path)
    geometries = gdf.geometry.values

    with rasterio.open(asset_url) as src:
        out_image, out_transform = mask(src, geometries, crop=True)

        out_meta = src.meta.copy()
        out_meta.update({
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform
        })

        output_name = f"{uuid.uuid4()}.tif"
        output_path = os.path.join(OUTPUT_FOLDER, output_name)

        with rasterio.open(output_path, "w", **out_meta) as dest:
            dest.write(out_image)

    return output_path
