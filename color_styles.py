# Color style collections for map visualization
# Each style includes colors for background, roads, buildings, water features, and natural areas

STYLES = {
    # Light Themes
    "light_minimal": {
        "name": "Minimal Light",
        "description": "Clean, minimalist style with subtle colors",
        "background": "#ffffff",  # Pure white
        "roads": "#000000",  # Black roads
        "buildings": "#d9d9d9",  # Light gray buildings
        "water": "#a6cbe8",  # Soft blue water
        "green": "#b5d2a7",  # Soft green
        "border": "#f5f5f5",  # Very light gray border
    },
    "light_vintage": {
        "name": "Vintage Light",
        "description": "Sepia-toned vintage map style",
        "background": "#f8f4e9",  # Cream paper
        "roads": "#796e65",  # Dark brown roads
        "buildings": "#d5c8b6",  # Tan buildings
        "water": "#b9d6cd",  # Mint green-blue water
        "green": "#aac092",  # Muted sage green
        "border": "#e8e0d0",  # Light tan border
    },
    "light_colorful": {
        "name": "Colorful Light",
        "description": "Vibrant colors on light background",
        "background": "#fcfcfc",  # Lighter off-white
        "roads": "#404040",  # Darker gray roads for contrast
        "buildings": "#ffcc99",  # More vibrant peach buildings
        "water": "#3399ff",  # More saturated blue water
        "green": "#66cc66",  # Brighter medium green
        "border": "#f0f0f0",  # Lighter gray border
    },
    "light_blueprint": {
        "name": "Blueprint",
        "description": "Technical drawing style with blue tones",
        "background": "#f5faff",  # Even lighter blue
        "roads": "#336699",  # Medium blue roads
        "buildings": "#99ccff",  # Light blue buildings
        "water": "#3399cc",  # Deeper blue water
        "green": "#ccffcc",  # Very light green
        "border": "#dbeeff",  # Pale blue border
    },
    # Dark Themes
    "dark_minimal": {
        "name": "Minimal Dark",
        "description": "Modern dark theme with high contrast",
        "background": "#121212",  # Very dark gray
        "roads": "#e0e0e0",  # Light gray roads
        "buildings": "#3a3a3a",  # Dark gray buildings
        "water": "#4db8ff",  # Medium bright blue
        "green": "#6ccf99",  # Medium bright green
        "border": "#333333",  # Dark gray border
    },
    "dark_nightmode": {
        "name": "Night Mode",
        "description": "Night-time map visualization",
        "background": "#0f1621",  # Very dark blue
        "roads": "#3a4559",  # Muted blue-gray roads
        "buildings": "#202a3a",  # Dark blue-gray buildings
        "water": "#1e3c58",  # Dark blue water
        "green": "#1e3325",  # Dark green
        "border": "#1c2635",  # Dark blue-gray border
    },
    "dark_neon": {
        "name": "Neon Dark",
        "description": "High-contrast neon colors on dark background",
        "background": "#0a0a0a",  # Nearly black
        "roads": "#ff00ff",  # Magenta roads
        "buildings": "#333333",  # Dark gray buildings
        "water": "#00ccff",  # Bright cyan water
        "green": "#33ff33",  # Bright green
        "border": "#222222",  # Dark gray border
    },
    "dark_ember": {
        "name": "Ember",
        "description": "Dark theme with warm color accents",
        "background": "#1a1a1a",  # Dark gray
        "roads": "#e0a868",  # Gold/amber roads
        "buildings": "#404040",  # Medium-dark gray buildings
        "water": "#407fb7",  # Muted blue water
        "green": "#5a8a5a",  # Muted green
        "border": "#2d2d2d",  # Medium-dark border
    },
}


def get_style(style_name="light_minimal"):
    """Returns a color style dictionary"""
    if style_name in STYLES:
        return STYLES[style_name]
    else:
        print(f"Style '{style_name}' not found. Using default style.")
        return STYLES["light_minimal"]


def list_styles():
    """Prints a list of available styles"""
    print("Available color styles:")
    for key, style in STYLES.items():
        print(f"- {key}: {style['name']} - {style['description']}")
