# Copernicus DEM Downloader (AOI-based, Python)

A Python script to query and download **Copernicus DEM (GLO-30, DGED, COG)** tiles for a given **area of interest (AOI)** using the Copernicus Data Space Ecosystem STAC API and authenticated S3 access.  
Supports **parallel downloads** (all cores minus one) for efficient bulk retrieval.

---

## 🚀 Features
- Works with **Copernicus DEM GLO-30 DGED COG** collection (30 m resolution, Cloud-Optimized GeoTIFF).
- Uses **authenticated access** via S3 keys from your Copernicus Dataspace account.
- Supports **parallel downloads** for speed.
- Designed for reproducible scientific workflows in Python.
- Simple configuration at the top of the script (AOI path, layer name, output folder, and credentials).

---

## 🔑 Getting Credentials
To download Copernicus DEM tiles you need an account at [dataspace.copernicus.eu](https://dataspace.copernicus.eu/):

1. Register for a free account.  
2. Go to your **User Profile → Access Keys**.  
3. Generate an **Access Key** and **Secret Key** for S3 API access.  
4. Insert these keys in the script:
   ```python
   AWS_ACCESS_KEY = "YOUR_ACCESS_KEY"
   AWS_SECRET_KEY = "YOUR_SECRET_KEY"

Alternatively, you can set them as environment variables:

export CDSE_AWS_KEY=xxxx
export CDSE_AWS_SECRET=yyyy

⚙️ Dependencies

Install Python packages:

pip install boto3 pystac-client geopandas

You also need GDAL/fiona system libraries installed for geopandas.
▶️ Usage

    Place your AOI boundary in a GeoPackage (.gpkg) or Shapefile.

        The AOI layer name can be any (e.g. "AOI", "Border", "catchment").

        Update the layer_name variable in the script.

    Edit the script to set:

        gpkg_path → path to your AOI file

        layer_name → AOI layer name

        Ref → reference name for output folder

        out_base → folder where DEM tiles should be saved

        AWS_ACCESS_KEY / AWS_SECRET_KEY → Copernicus Dataspace credentials

    Run the script:

python CopDEM_Download.py

Downloaded DEM tiles will be stored in:

    <your_folder_path>/Copernicus-DEM/<Ref>/

📂 Output

    Raw DEM tiles (COG GeoTIFFs).

    Each file corresponds to one Copernicus DEM tile overlapping your AOI.

    You can mosaic and clip them using GDAL, rasterio, or terra in R.

🐛 Bug Reports

If you encounter issues, please report them via email:
mario.mota.ferreira[at]gmail.com

Use of AI

This script was written with the assistance of generative AI (OpenAI ChatGPT), adapted and validated for use with Copernicus Dataspace DEM data.
All responsibility for scientific correctness lies with the user.

📜 License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).
You are free to use, modify, and share the code under the terms of the GPL.

See the LICENSE
file for details.
