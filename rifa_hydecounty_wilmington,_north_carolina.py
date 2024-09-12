# -*- coding: utf-8 -*-
"""Rifa- hydecounty/wilmington, North Carolina

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NIqi9RX0daQ9ddDM90reNJL63AkQBO6S

Rifa- hydecounty/wilmington, North Carolina
"""

!apt-get install -y python3-gdal
!pip install rasterio
!pip install osmnx
!pip install mapclassify folium matplotlib

import osmnx as ox
from osgeo import gdal
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from shapely.geometry import LineString
from rasterio.mask import mask
import rasterio
# import contextily as ctx
# !pip install

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# !pip install osmnx # install the osmnx library
import osmnx as ox # import the library and alias it as 'ox' for easier use
place_name = "Wilmington, North Carolina, USA"
G = ox.graph_from_place(place_name, network_type='drive')
ox.plot_graph(G)

!pip install osmnx # install the osmnx library
import osmnx as ox # import the library and alias it as 'ox' for easier use
place_name = "Hyde County, NC, USA" # Changed the place name to be more specific and corrected potential typo
graph = ox.graph_from_place(place_name, network_type='drive')
ox.plot_graph(graph)

Wilmington_drive = ox.speed.add_edge_speeds(G)
Wilmington_drive = ox.speed.add_edge_travel_times(G)

"""Re-imported the modules and apply elevation data:"""

#This code now works
Wilmington_drive = ox.elevation.add_node_elevations_raster(Wilmington_drive, 'USGS_13_n35w078_20151130.tif', cpus=1)
Wilmington_drive = ox.add_edge_grades(Wilmington_drive, add_absolute=True)

Wilmington_drive_node, Wilmington_drive_edge = ox.graph_to_gdfs(Wilmington_drive)

Wilmington_drive_node

Wilmington_drive_edge

Wilmington_drive_node = Wilmington_drive_node.reset_index()
print(Wilmington_drive_node.columns)
Wilmington_drive_node

# Reset the index to turn 'u', 'v', 'key' into columns
Wilmington_drive_edge = Wilmington_drive_edge.reset_index()

# Now 'u', 'v', and 'key' will be columns in the DataFrame
print(Wilmington_drive_edge.columns)

Wilmington_drive_edge

# Create a GeoDataFrame
df = pd.DataFrame(Wilmington_drive_node)
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['x'], df['y']))

# Plotting the GeoDataFrame
fig, ax = plt.subplots(1, 1, figsize=(10, 6))
gdf.plot(column='elevation', ax=ax, legend=True, cmap='viridis', markersize=100, legend_kwds={'label': "Elevation (m)"})

# Customize plot appearance
plt.title('Nodes Colored by Elevation')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()
ox.plot_graph(G)

# Define the threshold for roads that are likely to flood
flooded_threshold = 5

# Filter the rows where 'grade_abs' is less than the flooded threshold
flooded_edges = Wilmington_drive_edge[Wilmington_drive_edge['grade_abs'] < flooded_threshold]

# Display the filtered DataFrame with roads likely to flood
print(flooded_edges)

# Optionally, save the filtered data to a new CSV file
flooded_edges.to_csv('flooded_edges.csv', index=False)

# Ensure the DataFrame index is reset
Wilmington_drive_node = Wilmington_drive_node.reset_index()

# Print column names to identify the elevation column
print(Wilmington_drive_node.columns)

# Assuming 'elevation' is the name of the column with elevation data
highest_elevation = Wilmington_drive_node['elevation'].max()

print(f"The highest elevation in the DataFrame is: {highest_elevation}")

print(Wilmington_drive_edge.columns)

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np

# Define thresholds and color mapping
flooded_threshold = 5  # Elevation <= 5 meters are flooded
prone_threshold = 12   # Elevation between 5 and 12 meters are prone to flooding

node_color_map = {
    'flooded': 'blue',
    'prone': 'red',
    'safe': 'green',
    'unknown': 'gray'
}

# Function to classify nodes based on elevation
def classify_node_by_elevation(elevation):
    if np.isnan(elevation):
        return 'unknown'  # Handle NaN values
    elif elevation <= flooded_threshold:
        return 'flooded'
    elif flooded_threshold < elevation <= prone_threshold:
        return 'prone'
    else:
        return 'safe'

# Load the CSV file into a DataFrame (assuming it contains columns for 'elevation' and 'osmid')
csv_file = ' Wilmington_drive_edge.csv.csv'  # Replace with the actual CSV file path
#san_drive_node = pd.read_csv(csv.file)

# Apply classification
Wilmington_drive_node['flood_status'] = Wilmington_drive_node['elevation'].apply(classify_node_by_elevation)
Wilmington_drive_node['color'] = Wilmington_drive_node['flood_status'].map(node_color_map)

# Extract the flooded data
flooded_data = Wilmington_drive_node[Wilmington_drive_node['flood_status'] == 'flooded']

# Save the flooded data to a new CSV file (optional)
flooded_data.to_csv('flooded_data.csv', index=False)

# Plotting function
def plot_flooded_areas():
    fig, ax = plt.subplots(figsize=(12, 12))

    # Plot the road network (background)
    Wilmington_drive_edge.plot(ax=ax, color='black', linewidth=0.5, alpha=0.5, label='Road Network')

    # Plot the nodes color-coded by flood status
    for status, color in node_color_map.items():
        subset = Wilmington_drive_node[Wilmington_drive_node['flood_status'] == status]
        if not subset.empty:
            subset.plot(ax=ax, color=color, markersize=20, alpha=0.8, label=status)

    # Set aspect ratio to auto to avoid errors
    ax.set_aspect('auto')

    # Add title and labels
    plt.title("Flood Risk Based on Elevation")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    # Create custom legend handles
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=status)
               for status, color in node_color_map.items()]

    # Add the legend to the plot
    ax.legend(handles=handles, title="Flood Status", loc='upper right')

    # Show the plot
    plt.show()

# Call the function to plot
plot_flooded_areas()

# Print the flooded data
print(flooded_data)

print(Wilmington_drive_node.columns)

import pandas as pd

# Load the data
# san_drive_edge = pd.read_csv('san_drive_edge.csv')  # already loaded
# san_drive_node = pd.read_csv('san_drive_node.csv')  # already loaded

# Check column names in both DataFrames
print("Wilmington_drive_node columns:", Wilmington_drive_node.columns)
print("Wilmington_drive_edge columns:", Wilmington_drive_edge.columns)

# Assuming the node ID column in san_drive_node is 'node_id' or 'osmid'
node_column = 'osmid'  # Replace this with the actual name of the node ID column from your output

# Merge the node data to get the elevation of both u and v endpoints
Wilmington_drive_edge = Wilmington_drive_edge.merge(
    Wilmington_drive_node[[node_column, 'elevation']],
    left_on='u',
    right_on=node_column,
    how='left'
).rename(columns={'elevation': 'elevation_u'})

Wilmington_drive_edge = Wilmington_drive_edge.merge(
    Wilmington_drive_node[[node_column, 'elevation']],
    left_on='v',
    right_on=node_column,
    how='left'
).rename(columns={'elevation': 'elevation_v'})

# Now check the merged DataFrame
print(Wilmington_drive_edge[['u', 'v', 'elevation_u', 'elevation_v']].head())

def label_flood_risk(df, threshold):
    """
    Labels each edge in the dataframe based on the elevation of u and v endpoints.

    Parameters:
    df : pandas.DataFrame
        DataFrame containing 'elevation_u' and 'elevation_v' columns.
    threshold : float
        The elevation threshold below which nodes are considered flooded.

    Returns:
    pandas.DataFrame
        DataFrame with a new column 'flood_risk' indicating flood status.
    """
    def classify_edge(elevation_u, elevation_v):
        if elevation_u < threshold and elevation_v < threshold:
            return 'flooded'
        elif elevation_u >= threshold and elevation_v >= threshold:
            return 'safe'
        else:
            return 'partially-flooded'

    df['flood_risk'] = df.apply(lambda row: classify_edge(row['elevation_u'], row['elevation_v']), axis=1)
    return df

# Example usage:
Wilmington_drive_edge = label_flood_risk(Wilmington_drive_edge, threshold=10)
print(Wilmington_drive_edge[['u', 'v', 'elevation_u', 'elevation_v', 'flood_risk']].head())

def label_flood_risk(df, threshold):
    """
    Labels each edge in the dataframe based on the elevation of u and v endpoints.

    Parameters:
    df : pandas.DataFrame
        DataFrame containing 'elevation_u' and 'elevation_v' columns.
    threshold : float
        The elevation threshold below which nodes are considered flooded.

    Returns:
    pandas.DataFrame
        DataFrame with a new column 'flood_risk' indicating flood status.
    """
    def classify_edge(elevation_u, elevation_v):
        if elevation_u < threshold and elevation_v < threshold:
            return 'flooded'
        elif elevation_u >= threshold and elevation_v >= threshold:
            return 'safe'
        else:
            return 'partially-flooded'

    df['flood_risk'] = df.apply(lambda row: classify_edge(row['elevation_u'], row['elevation_v']), axis=1)
    return df

# Example usage:
Wilmington_drive_edge = label_flood_risk(Wilmington_drive_edge, threshold=12)
print(Wilmington_drive_edge[['u', 'v', 'elevation_u', 'elevation_v', 'flood_risk']].head())

"""Safe Elevation

"""

def label_flood_risk(df, threshold):
    """
    Labels each edge in the dataframe based on the elevation of u and v endpoints.

    Parameters:
    df : pandas.DataFrame
        DataFrame containing 'elevation_u' and 'elevation_v' columns.
    threshold : float
        The elevation threshold below which nodes are considered flooded.

    Returns:
    pandas.DataFrame
        DataFrame with a new column 'flood_risk' indicating flood status.
    """
    def classify_edge(elevation_u, elevation_v):
        if elevation_u < threshold and elevation_v < threshold:
            return 'flooded'
        elif elevation_u >= threshold and elevation_v >= threshold:
            return 'safe'
        else:
            return 'partially-flooded'

    df['flood_risk'] = df.apply(lambda row: classify_edge(row['elevation_u'], row['elevation_v']), axis=1)
    return df

# Example usage:
Wilmington_drive_edge = label_flood_risk(Wilmington_drive_edge, threshold=2)
print(Wilmington_drive_edge[['u', 'v', 'elevation_u', 'elevation_v', 'flood_risk']].head())

# Plot the road network with colors based on the updated flood classification
fig, ax = plt.subplots(figsize=(12, 12))
# Assign colors based on classification
color_map = {
    'flooded': 'blue',
    'partially-flooded': 'yellow',
    'safe': 'green'
}

for status, color in color_map.items():
    subset = Wilmington_drive_edge[Wilmington_drive_edge['flood_risk'] == status]
    subset.plot(ax=ax, color=color, label=status)

# Add legend and title
plt.legend(title="Flood Status by Grade")
plt.title("Road Network with Flood Risk Classification by Grade")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.show()