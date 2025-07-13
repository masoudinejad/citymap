from color_styles import get_style, list_styles
from pathlib import Path
import fiona
import geopandas as gpd
import matplotlib.pyplot as plt


def load_data(data_name):
    # File path
    data_path = Path(f"./data/{data_name}_data.gpkg")

    if not data_path.exists():
        print(f"Error: Data file {data_path} not found.")
        return
    available_layers = fiona.listlayers(str(data_path))
    # Create a dictionary to store the layers
    layers_data = {}

    for layer in available_layers:
        # Read the layer data using geopandas
        gdf = gpd.read_file(str(data_path), layer=layer)
        # Store in dictionary with layer name as key
        layers_data[layer] = gdf

    print(f"Loaded {len(layers_data)} layers from {data_path}")
    return layers_data


def make_plot(
    layers_data,
    city,
    country,
    dimension_cm=24,
    style_name="light_colorful",
    base_thickness=1,
):
    style = get_style(style_name)

    # Create initial figure with dimensions in inches (convert from cm)
    width_inches = dimension_cm / 2.54
    height_inches = dimension_cm / 2.54

    # Create figure
    fig, ax = plt.subplots(figsize=(width_inches, height_inches))
    ax.set_aspect("equal")

    # Plot the border layer if it exists
    if "boundary" in layers_data:
        border = layers_data["boundary"]
        border.plot(ax=ax, color=style["background"])
    if "streets" in layers_data:
        border = layers_data["streets"]
        local_streets = border[~border["highway"].isin(["motorway", "trunk"])]
        local_streets.plot(ax=ax, color=style["roads"], linewidth=0.3 * base_thickness)
        highways = border[border["highway"].isin(["motorway", "trunk"])]
        highways.plot(ax=ax, color=style["roads"], linewidth=base_thickness)
    if "water" in layers_data:
        water = layers_data["water"]
        if "natural" in water.columns:
            # Plot natural water bodies
            natural_water = water[water["natural"] == "water"]
            natural_water.plot(ax=ax, color=style["water"], edgecolor="none")
        if "waterway" in water.columns:
            # Plot waterway features
            waterways = water[water["waterway"].isin(["river", "canal", "stream"])]
            waterways.plot(
                ax=ax,
                color=style["water"],
                edgecolor="none",
                linewidth=0.7 * base_thickness,
            )
        if "landuse" in layers_data:
            landuse = layers_data["landuse"]
            # Filter for parks and similar green areas
            parks = landuse[
                landuse["landuse"].isin(
                    ["park", "garden", "grass", "recreation_ground"]
                )
            ]
            parks.plot(ax=ax, color=style["green"], edgecolor="none")
    # Set the figure background to transparent
    # fig.patch.set_alpha(0.0)
    fig.set_facecolor("white")
    ax.set_facecolor("white")

    # Add text to the lower left corner
    ax.text(
        0.03,
        0.03,
        f"{city}\n{country}",
        transform=ax.transAxes,
        fontsize=14,
        color="black",
        ha="left",
        va="bottom",
    )
    # Remove axes, ticks, and labels
    ax.set_axis_off()
    ax.margins(0)
    fig.subplots_adjust(
        left=0, bottom=0, right=1, top=1, wspace=0, hspace=0
    )  # remove padding

    return fig


def store_plot(data_name, fig):
    storage_path = Path("./maps", data_name)
    storage_path.mkdir(parents=True, exist_ok=True)
    output_name = f"{data_name}_map"
    # for format in ["png"]:
    for format in ["svg", "pdf", "png"]:
        file_path = storage_path / f"{output_name}.{format}"
        plt.savefig(
            file_path,
            format=format,
            dpi=600,
            bbox_inches=None,  # Don't use tight layout - preserve exact dimensions
            pad_inches=0,
            facecolor=fig.get_facecolor(),
        )
        print(f"Saved {file_path}")


def main(data_name, city, country, style_name, base_thickness, plot_dim):
    data = load_data(data_name)
    fig = make_plot(data, city, country, plot_dim, style_name, base_thickness)
    store_plot(data_name, fig)


if __name__ == "__main__":
    # Configuration parameters
    data_name = "Tehran"  # Name of the data file (without extension)
    country = "Iran"  # Country name for the plot
    style_name = "light_colorful"  # Color style to use
    base_thickness = 1.1  # Base line thickness for roads
    plot_dim = 24  # Dimension in cm
    main(data_name, data_name, country, style_name, base_thickness, plot_dim)
