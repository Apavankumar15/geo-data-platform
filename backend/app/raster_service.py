import rasterio
from rasterio.mask import mask
import geopandas as gpd
import os
import uuid
from backend.app.config import OUTPUT_FOLDER


def clip_raster(asset_url, aoi_path):

    gdf = gpd.read_file(aoi_path)

    with rasterio.open(asset_url) as src:

        # ✅ FIX 1: Set CRS if missing
        if gdf.crs is None:
            gdf.set_crs(epsg=4326, inplace=True)

        # ✅ FIX 2: Convert CRS to raster CRS
        gdf = gdf.to_crs(src.crs)

        geometries = gdf.geometry.values

        try:
            out_image, out_transform = mask(src, geometries, crop=True)

        except Exception as e:
            return f"Error: {str(e)}"

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