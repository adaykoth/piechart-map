import pandas as pd
import geopandas as gpd

from numpy import log10
from pathlib import Path

def load_data(path:Path):
    # Load CSV data
    df = pd.read_csv(path, sep=';', decimal=',', quotechar='"')

    # Convert the DataFrame to a GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['X'], df['Y']))
    gdf['Log_Size'] = log10(gdf['N'] + 1)  # Add 1 to avoid log(0)
    gdf['Scaled_Size'] = gdf['Log_Size'] / gdf['Log_Size'].max() * 0.4

    # Prepare the data for pie charts
    cluster_columns = ['Cluster2', 'Cluster1', 'Cluster4', 'Cluster5', 'Cluster3', 'Cluster6']
    return gdf, cluster_columns
