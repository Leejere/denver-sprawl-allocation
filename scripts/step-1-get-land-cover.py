import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio as rio
from shapely.geometry import Polygon, Point

crs = "EPSG:2232"

land_cover_2009 = rio.open("data/land-cover/2009.tif")
land_cover_2019 = rio.open("data/land-cover/2019.tif")


def raster_to_shape(raster, crs, to_point=False, value_column="value"):
    data_array = raster.read(1)
    transform = raster.transform
    shapes_data = []
    height, width = data_array.shape

    if to_point:
        for row in range(height):
            for col in range(width):
                value = data_array[row, col]
                if np.isnan(value):
                    continue
                x, y = transform * (col + 0.5, row + 0.5)
                # Create a polygon for the cell
                point = Point(x, y)
                # Add the polygon and its value to the list
                shapes_data.append({"geometry": point, value_column: value})
        return gpd.GeoDataFrame(shapes_data, crs=crs)

    for row in range(height):
        for col in range(width):
            value = data_array[row, col]
            if np.isnan(value):
                continue
            x_min, y_max = transform * (col, row)
            x_max, y_min = transform * (col + 1, row + 1)
            # Create a polygon for the cell
            polygon = Polygon(
                [(x_min, y_min), (x_min, y_max), (x_max, y_max), (x_max, y_min)]
            )
            # Add the polygon and its value to the list
            shapes_data.append({"geometry": polygon, value_column: value})
    return gpd.GeoDataFrame(shapes_data, crs=crs)


fishnet = (
    raster_to_shape(
        land_cover_2009, crs, to_point=False, value_column="land_cover_2009"
    )
    .query("land_cover_2009 != 0")
    .copy()
)
points_2019 = (
    raster_to_shape(land_cover_2019, crs, to_point=True, value_column="land_cover_2019")
    .query("land_cover_2019 != 0")
    .copy()
)

# Join points to fishnet, no index right
fishnet = gpd.sjoin(fishnet, points_2019, how="left", predicate="contains").drop(
    columns=["index_right"]
)

developed = [21, 22, 23, 24]
land_covers = {
    "developed": [21, 22, 23, 24],
    "forest": [41, 42, 43],
    "farm": [81, 82],
    "wetland": [90, 95],
    "water": [11],
}
for year in [2009, 2019]:
    # First update whether developed bool
    fishnet[f"developed_{year}"] = fishnet[f"land_cover_{year}"].isin(developed)

    # Then update land cover
    fishnet[f"land_cover_type_{year}"] = "other"
    for land_cover, codes in land_covers.items():
        fishnet.loc[
            fishnet[f"land_cover_{year}"].isin(codes), f"land_cover_type_{year}"
        ] = land_cover

    fishnet.drop(columns=[f"land_cover_{year}"], inplace=True)

fishnet.to_file("data/fishnets/with_land_cover.geojson", driver="GeoJSON")
