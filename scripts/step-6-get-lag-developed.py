import numpy as np
import pandas as pd
import geopandas as gpd
from pysal.lib import weights

crs = "EPSG:2232"

fishnet = gpd.read_file("data/fishnets/with_distance.geojson")
fishnet.crs = crs


def get_lag_developed(fishnet, to_lag_column, new_column_name):
    w_queen = weights.Queen.from_dataframe(fishnet)
    w_queen.transform = "r"

    binary = fishnet[to_lag_column].astype(int)
    lag = weights.lag_spatial(w_queen, binary)
    fishnet[new_column_name] = lag / np.array(list(w_queen.cardinalities.values()))
    return fishnet


for year in [2009, 2019]:
    fishnet = get_lag_developed(
        fishnet,
        to_lag_column=f"developed_{year}",
        new_column_name=f"lag_developed_{year}",
    )

fishnet.to_file("data/fishnets/with_lag_developed.geojson", driver="GeoJSON")
