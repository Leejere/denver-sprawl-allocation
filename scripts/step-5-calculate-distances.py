import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio as rio
from shapely.geometry import Point

from scipy.spatial import cKDTree

crs = "EPSG:2232"

fishnet = gpd.read_file("data/fishnets/with_population.geojson")
fishnet.crs = crs

highways = gpd.read_file("data/other/msa-highways.geojson")
highways.crs = crs

rail_stations_url = "https://services5.arcgis.com/1fZoXlzLW6FCIUcE/arcgis/rest/services/RTD_GIS_Current_Runboard/FeatureServer/1/query?outFields=*&where=1%3D1&f=geojson"
rail_stations = gpd.read_file(rail_stations_url).to_crs(crs)

facilities_url = "https://services5.arcgis.com/1fZoXlzLW6FCIUcE/arcgis/rest/services/RTD_GIS_Current_Runboard/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"
facilities = gpd.read_file(facilities_url).to_crs(crs)

rail_stations_future_url = "data/other/rail_stations_new.shp"
rail_stations_future = gpd.read_file(rail_stations_future_url).to_crs(crs)

facilities_future_url = "data/other/facilities_new.shp"
facilities_future = gpd.read_file(facilities_future_url).to_crs(crs)

template_raster_path = "data/land-cover/2009.tif"


def get_info_from_template_raster(template_raster_path):
    raster = rio.open(template_raster_path)
    transform = raster.transform
    data = raster.read(1)

    # Create a series of points, to be later joined distances
    non_zero_rows, non_zero_cols = np.nonzero(data)
    x_coords = transform[2] + non_zero_cols * transform[0] + transform[0] / 2
    y_coords = transform[5] + non_zero_rows * transform[4] + transform[4] / 2

    distance_base_points = [
        Point(x, y) for x, y in zip(x_coords.ravel(), y_coords.ravel())
    ]

    return transform, non_zero_rows, non_zero_cols, distance_base_points


(
    transform,
    non_zero_rows,
    non_zero_cols,
    distance_base_points,
) = get_info_from_template_raster(template_raster_path)


# This takes the relationship between raster coordinates and actual coordinates,
# using the `transform` attribute of the raster as the bridge
def coords_to_pixel_positions(coords, transform):
    return [
        (int((x - transform[2]) / transform[0]), int((y - transform[5]) / transform[4]))
        for x, y in coords
    ]


# This extracts points from the a line gdf and returns a list of points
def get_point_list_from_lines_gdf(line_gdf):
    points = []
    for line in line_gdf.geometry:
        if line.geom_type == "MultiLineString":
            for subline in line:
                points.extend(subline.coords)
        elif line.geom_type == "LineString":
            points.extend(line.coords)
    return points


# This extracts points from a Point gdf and returns a list of points
def get_point_list_from_points_gdf(point_gdf):
    points = []
    for point in point_gdf.geometry:
        points.append(point.coords[0])
    return points


# This takes a list of points, and transforms it into pixel positions relating
# to the raster, and then returns the corresponding cKDTree object
def get_tree_from_gdf(gdf, transform, is_lines=False):
    if is_lines:
        points = get_point_list_from_lines_gdf(gdf)
    else:
        points = get_point_list_from_points_gdf(gdf)
    pixels = coords_to_pixel_positions(points, transform)
    return cKDTree(pixels)


# Creates a list of distances, the sequence of which matches `distance_base_points`
# Get an array of nearest distances
def tree_to_distances(tree, non_zero_rows, non_zero_cols, transform):
    nearest_distances = []
    for row, col in zip(non_zero_rows, non_zero_cols):
        dist, _ = tree.query((col, row))
        nearest_distances.append(dist * transform[0])
    return nearest_distances


def distance_to_nearest(target_gdf, name, is_lines=False):
    tree = get_tree_from_gdf(target_gdf, transform, is_lines=is_lines)
    distances = tree_to_distances(tree, non_zero_rows, non_zero_cols, transform)
    distances_points = pd.DataFrame(
        {"geometry": distance_base_points, "distance": distances}
    )
    return gpd.GeoDataFrame(distances_points, crs=crs).rename(
        columns={"distance": f"{name}_distance"}
    )


def join_nearest_distance(fishnet, target_gdf, name, is_lines=False):
    distances = distance_to_nearest(target_gdf, name, is_lines=is_lines)
    return gpd.sjoin(fishnet, distances, how="left", predicate="intersects").drop(
        columns=["index_right"]
    )


to_join = [
    (highways, "highway"),
    (rail_stations, "rail_station"),
    (facilities, "facility"),
    (rail_stations_future, "rail_station_future"),
    (facilities_future, "facility_future"),
]

# Join
for gdf, name in to_join:
    fishnet = join_nearest_distance(fishnet, gdf, name, is_lines=(name == "highway"))

fishnet.to_file("data/fishnets/with_distance.geojson", driver="GeoJSON")
