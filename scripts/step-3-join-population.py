import numpy as np
import pandas as pd
import geopandas as gpd

crs = "EPSG:2232"

# Read fishnet that includes land cover info
fishnet = gpd.read_file("data/fishnets/with_land_cover.geojson")
fishnet.crs = "EPSG:2232"

population_2010 = gpd.read_file("data/population/2010.geojson")
population_2020 = gpd.read_file("data/population/2020.geojson")

population_2010.crs = crs
population_2020.crs = crs


def areal_interpolation(fishnet, block_population, population_column):
    # Get population density by block
    block_population["area"] = block_population.geometry.area
    block_population["density"] = (
        block_population[population_column] / block_population["area"]
    )

    # Spatial join. This creates some divided fishnet cells
    fishnet["fishnet_id"] = np.arange(len(fishnet))
    overlay = gpd.overlay(fishnet, block_population, how="intersection")
    overlay["intersected_area"] = overlay.geometry.area

    # Calculate the population in each (broken) cell
    overlay["intersected_population"] = overlay["intersected_area"] * overlay["density"]

    # Piece the cells back together
    grouped = overlay.groupby("fishnet_id")["intersected_population"].sum()
    grouped.name = population_column

    return fishnet.merge(
        grouped, left_on="fishnet_id", right_index=True, how="left"
    ).drop(columns=["fishnet_id"])


fishnet_with_population = areal_interpolation(
    fishnet, population_2010, "population_2010"
)

fishnet_with_population = areal_interpolation(
    fishnet_with_population, population_2020, "population_2020"
)

fishnet_with_population.to_file(
    "data/fishnets/with_population.geojson", driver="GeoJSON"
)
