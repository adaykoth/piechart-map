import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from pathlib import Path

from load_data import load_data

def plot_pie_inset(data, ilon, ilat, ax, size, projection=ccrs.PlateCarree()):
    # Convert lon/lat to the projection used by the main axes
    lonr, latr = projection.transform_point(ilon, ilat, ccrs.Geodetic())

    # Create an inset axis at the transformed coordinates
    ax_sub = inset_axes(ax, width=size, height=size, loc=10,
                        bbox_to_anchor=(lonr, latr),
                        bbox_transform=ax.transData,
                        borderpad=0)
    # Plot pie chart in the inset axis
    wedges, texts = ax_sub.pie(data, colors=['red', 'blue', 'green', 'orange', 'purple', 'brown'],
                               )
    ax_sub.set_aspect("equal")

def create_ax(df):
    fig, ax = plt.subplots(1, 1, subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([min(df['X']) - 5, max(df['X']) + 5, min(df['Y']) - 5, max(df['Y']) + 5], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)
    ax.coastlines()
    ax.gridlines(draw_labels=True, color='gray', alpha=0.5, linestyle='--')
    return fig, ax

def plot_pie_chart(gdf, cluster_columns, ax):
    for index, row in gdf.iterrows():
        plot_pie_inset(row[cluster_columns].tolist(), row['X'], row['Y'], ax, row['Scaled_Size'],
                       projection=ccrs.PlateCarree())
    return ax

def main():
    data_path = Path('ht_overview_cluster_region.csv')
    # Load the data
    gdf, cluster_columns = load_data(data_path)

    # Create the main axes
    fig, ax = create_ax(gdf)

    # Plot the pie charts
    ax = plot_pie_chart(gdf, cluster_columns, ax)
    fig.savefig('pie_chart.png', dpi=300, bbox_inches='tight')

if __name__ == '__main__':
    main()