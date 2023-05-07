import numpy as np
import pandas as pd
import geopandas as gpd
from pygris import counties

crs = "EPSG:2232"

highways = gpd.read_file("data/other/colorado-highways.geojson")
highways = highways.to_crs(crs)

ten_counties = ["001", "005", "031", "035", "014", "039", "059", "093", "019", "047"]

msa = (
    counties(state="08", year=2020)
    .query("COUNTYFP.isin(@ten_counties)")
    .copy()[["NAME", "geometry"]]
)
msa = msa.to_crs(crs)
msa_union = msa.unary_union
highways_clipped = gpd.clip(highways, msa_union)
highways_clipped.to_file("data/other/msa-highways.geojson", driver="GeoJSON")
