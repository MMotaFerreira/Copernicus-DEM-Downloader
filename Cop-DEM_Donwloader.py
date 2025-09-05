import os
import boto3
from botocore.client import Config
import geopandas as gpd
from pystac_client import Client
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---------------------------
# User Configuration
# ---------------------------

# A short reference name for this run (used in output folder naming)
Ref = "My_AOI"

# Path to your AOI file (GeoPackage or shapefile)
gpkg_path = r"C:/Path/to/GeoPackage.gpkg" # <-- set to the actual GeoPackage name
layer_name = "AOI"  # <-- set to the actual layer name in your file

# Output folder (DEM tiles will be saved here)
out_base = r"C:/Path/to/Folder-DEM" # <-- set to a desired folder name
out_dir = os.path.join(out_base, Ref)
os.makedirs(out_dir, exist_ok=True)

# STAC collection for Copernicus DEM 30 m (DGED, GeoTIFF/COG)
stac_url = "https://stac.dataspace.copernicus.eu/v1"
collection_id = "cop-dem-glo-30-dged-cog"

# Copernicus Dataspace S3 credentials ⚠️
# Either set them here manually OR via environment variables (CDSE_AWS_KEY / CDSE_AWS_SECRET)
AWS_ACCESS_KEY = "YOUR_ACCESS_KEY" or os.getenv("CDSE_AWS_KEY")
AWS_SECRET_KEY = "YOUR_SECRET_KEY" or os.getenv("CDSE_AWS_SECRET")

# ---------------------------
# 1. Load AOI
# ---------------------------
AOI = gpd.read_file(gpkg_path, layer=layer_name).to_crs(4326)
bbox = AOI.total_bounds.tolist()

# ---------------------------
# 2. Query STAC API
# ---------------------------
catalog = Client.open(stac_url)
search = catalog.search(
    collections=[collection_id],
    bbox=bbox,
    limit=1000
)
items = list(search.get_items())
print(f"Found {len(items)} tiles in collection {collection_id}")

if not items:
    raise SystemExit("No DEM tiles found for this AOI.")

# ---------------------------
# 3. Connect to Copernicus Dataspace S3 (authenticated)
# ---------------------------
s3 = boto3.client(
    "s3",
    region_name="eu-central-1",
    endpoint_url="https://eodata.dataspace.copernicus.eu",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    config=Config(signature_version="s3v4")
)
bucket = "eodata"

# ---------------------------
# 4. Parallel download function
# ---------------------------
def download_tile(href):
    if href.startswith("s3://eodata/") and href.endswith(".tif"):
        key = href.replace("s3://eodata/", "")
        filename = os.path.join(out_dir, os.path.basename(key))

        if os.path.exists(filename):
            return f"Already exists: {filename}"

        try:
            resp = s3.get_object(Bucket=bucket, Key=key)
            with open(filename, "wb") as f:
                for chunk in resp["Body"].iter_chunks(chunk_size=1024*1024):
                    f.write(chunk)
            return f"✅ Downloaded: {filename}"
        except Exception as e:
            return f"❌ Failed: {key} ({e})"
    return None

# ---------------------------
# 5. Collect all URLs and run in parallel
# ---------------------------
urls = [
    asset.href
    for item in items
    for asset_key, asset in item.assets.items()
    if asset.href.endswith(".tif")
]

print(f"Starting download of {len(urls)} DEM tiles...")

# Detect available cores and subtract one (minimum 1)
num_workers = max(1, os.cpu_count() - 1)
print(f"Using {num_workers} parallel workers")

with ThreadPoolExecutor(max_workers=num_workers) as executor:
    futures = [executor.submit(download_tile, u) for u in urls]
    for future in as_completed(futures):
        print(future.result())

print("✅ All downloads finished.")
