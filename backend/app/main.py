from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os
import geopandas as gpd
from backend.app.stac_service import search_scene
from backend.app.raster_service import clip_raster
from backend.app.config import UPLOAD_FOLDER

app = FastAPI()

@app.post("/download")
async def download_data(
    file: UploadFile = File(...),
    collection: str = Form(...),
    date_range: str = Form(...),
    cloud: int = Form(...)
):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    gdf = gpd.read_file(file_path)
    bbox = gdf.total_bounds.tolist()

    item = search_scene(collection, bbox, date_range, cloud)

    if not item:
        return {"error": "No scenes found"}

    asset_url = list(item.assets.values())[0].href

    output_path = clip_raster(asset_url, file_path)

    return {"output_file": output_path}
