import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, Point
from pygris import blocks
import cenpy

crs = "EPSG:2232"

counties = ["001", "005", "031", "035", "014", "039", "059", "093", "019", "047"]
datasets = {
    "2010": {
        "dataset": "DECENNIALPL2010",
        "variable": "P001001",
        "geo_column": "GEOID10",
    },
    "2020": {
        "dataset": "DECENNIALPL2020",
        "variable": "P1_001N",
        "geo_column": "GEOID20",
    },
}


def get_data_with_geo(connection, county, year, geo_column, variable):
    # Get data from the Census API
    query = connection.query(
        cols=[variable],
        geo_unit="block:*",
        geo_filter={"state": "08", "county": county},
    )
    query[geo_column] = query.state + query.county + query.tract + query.block
    query = query.rename(columns={variable: "population"}).drop(
        columns=["state", "county", "tract", "block"]
    )
    query.population = query.population.astype(int)

    # Get the block geometries
    blocks_gdf = blocks(
        state="08",
        county=county,
        year=int(year),
    )[[geo_column, "geometry"]]

    # Merge the data with the geometries
    query = blocks_gdf.merge(query, on=geo_column, how="left")
    return query.rename(
        columns={geo_column: "GEOID", "population": f"population_{year}"}
    )


# Create an empty DataFrame to store the results
population_2010 = pd.DataFrame()
population_2020 = pd.DataFrame()

# Loop through the census datasets and county FIPS codes to get block-level population data
for year, dataset in datasets.items():
    connection = cenpy.remote.APIConnection(dataset["dataset"])
    for county in counties:
        subset = get_data_with_geo(
            connection=connection,
            county=county,
            year=year,
            geo_column=dataset["geo_column"],
            variable=dataset["variable"],
        ).to_crs(crs)
        globals()[f"population_{year}"] = pd.concat(
            [globals()[f"population_{year}"], subset], ignore_index=True
        )
        print(f"Finished {year} {county}")


population_2010.to_file("data/population/2010.geojson", driver="GeoJSON")
population_2020.to_file("data/population/2020.geojson", driver="GeoJSON")
