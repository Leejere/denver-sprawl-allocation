import numpy as np
import pandas as pd
import geopandas as gpd
from pygris import counties

crs = "EPSG:2232"

fishnet = gpd.read_file("data/fishnets/with_lag_developed.geojson")
fishnet.crs = crs

ten_counties = ["001", "005", "031", "035", "014", "039", "059", "093", "019", "047"]

msa = (
    counties(state="08", year=2020)
    .query("COUNTYFP.isin(@ten_counties)")
    .copy()[["NAME", "geometry"]]
    .to_crs(crs)
    .rename(columns={"NAME": "county"})
)

fishnet["centroid"] = fishnet.geometry.centroid
# Identify which county each cell is in
fishnet = (
    gpd.sjoin(fishnet.set_geometry("centroid"), msa, how="left", predicate="within")
    .drop(columns=["index_right", "centroid"])
    .set_geometry("geometry")
)

fishnet.to_file("data/fishnets/with_counties.geojson", driver="GeoJSON")
