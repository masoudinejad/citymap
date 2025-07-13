import json
from pathlib import Path
from shapely.geometry import Polygon
import geopandas as gpd
import osmnx as ox


def load_geojson(file_path):
    """Load GeoJSON file and return the coordinates"""
    with open(file_path, "r") as f:
        data = json.load(f)

    # Assuming the first feature and first polygon
    if "features" in data and len(data["features"]) > 0:
        geometry = data["features"][0]["geometry"]
        if geometry["type"] == "Polygon":
            return geometry["coordinates"][0]

    raise ValueError("Could not extract polygon coordinates from GeoJSON file")


def get_buffered_polygon(coordinates, buffer_distance=0.001):
    polygon = Polygon(coordinates)
    # Ensure the polygon is valid
    if not polygon.is_valid:
        print("Warning: Invalid polygon, attempting to fix...")
        polygon = polygon.buffer(0)  # Buffer of 0 can fix some invalid polygons
    # Create a buffered polygon
    buffered_polygon = polygon.buffer(buffer_distance)
    # Create a GeoDataFrame with the boundary polygon
    boundary_gdf = gpd.GeoDataFrame(geometry=[polygon], crs="EPSG:4326")
    return polygon, buffered_polygon, boundary_gdf


def clip_features_to_polygon(features_gdf, polygon, layer_name="unknown"):
    """Clip features to the polygon boundary and return only those that are within/intersect with the polygon"""
    if features_gdf.empty:
        print(f"No {layer_name} features to clip")
        return features_gdf

    try:
        # Create a GeoDataFrame with the clip polygon
        clip_polygon_gdf = gpd.GeoDataFrame(geometry=[polygon], crs="EPSG:4326")

        # Print info before clipping
        print(f"Original {layer_name} features: {len(features_gdf)}")

        # Perform the clip operation
        clipped_features = gpd.clip(features_gdf, clip_polygon_gdf)

        # Print info after clipping
        print(
            f"Clipped {layer_name} features: {len(clipped_features)} (removed {len(features_gdf) - len(clipped_features)})"
        )

        return clipped_features
    except Exception as e:
        print(f"Warning: Could not clip {layer_name} features: {e}")
        return features_gdf


def download_data(polygon, buffered_polygon, boundary_gdf, feature_tags=None):
    downloaded_data = {"boundary": boundary_gdf}
    # Download street network data
    print("Downloading street network data...")
    G = ox.graph_from_polygon(buffered_polygon, network_type="drive")
    nodes, edges = ox.graph_to_gdfs(G)
    downloaded_data["streets"] = clip_features_to_polygon(edges, polygon, "streets")
    downloaded_data["nodes"] = clip_features_to_polygon(nodes, polygon, "nodes")
    if feature_tags is not None:
        # Download additional features based on tags
        for tag, value in feature_tags.items():
            print(f"Downloading {tag} features...")
            features = ox.features_from_polygon(buffered_polygon, tags={tag: value})
            if not features.empty:
                clipped_features = clip_features_to_polygon(features, polygon, tag)
                downloaded_data[tag] = clipped_features
            else:
                print(f"No {tag} features found")
    return downloaded_data


def get_save_data(data_name, downloaded_data):
    output_folder = Path("./data")
    # Ensure the output folder exists
    output_folder.mkdir(parents=True, exist_ok=True)

    # Save all layers to a single GPKG file
    output_data_file = output_folder / f"{data_name}_data.gpkg"
    for layer_name, gdf in downloaded_data.items():
        if not gdf.empty:
            gdf.to_file(output_data_file, layer=layer_name, driver="GPKG")
            print(f"Saved {layer_name} to {output_data_file}")
        else:
            print(f"No data for layer {layer_name}, skipping save")


def main(data_name, feature_tags):
    file_path = Path(f"coordinates/{data_name}.json")
    coordinates = load_geojson(file_path)
    print(f"Loaded polygon with {len(coordinates)} points")
    polygon, buffered_polygon, boundary_gdf = get_buffered_polygon(coordinates)
    downloaded_data = download_data(
        polygon, buffered_polygon, boundary_gdf, feature_tags
    )
    get_save_data(data_name, downloaded_data)


if __name__ == "__main__":
    data_name = "Tehran"
    feature_tags = {
        # "building": True,
        # "amenity": True,
        # "landuse": ["reservoir", "basin"],
        "natural": ["water", "wetland", "bay", "spring"],
        "waterway": True,
        "water": True,
        "leisure": ["park", "garden", "nature_reserve"]
    }
    main(data_name, feature_tags)
