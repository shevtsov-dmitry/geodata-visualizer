from flask import Flask, render_template
import folium
import pandas as pd

app = Flask(__name__)

# Step 1: Function to generate the map dynamically based on the selected group
def generate_map(selected_group):
    # Load the CSV file
    df = pd.read_csv("polygon_data.csv")

    # Create a base map
    mymap = folium.Map(location=[37.7749, -122.4194], zoom_start=13)

    # Filter the data for the selected group
    group_data = df[df["group"] == selected_group]

    # Extract coordinates
    coords = group_data[["latitude", "longitude"]].values.tolist()

    # Add the polygon
    folium.Polygon(
        locations=coords,
        color="blue" if selected_group == "blue" else "red",
        fill=True,
        fill_color="cyan" if selected_group == "blue" else "pink",
        fill_opacity=0.5,
        tooltip=f"{selected_group.capitalize()} Polygon"
    ).add_to(mymap)

    # Return the HTML representation of the map
    return mymap._repr_html_()

@app.route("/")
def home():
    # Default to "blue" polygon
    map_html = generate_map("blue")
    return render_template("index.html", map_html=map_html)

# Route to dynamically reload the map based on the group
@app.route("/<group>")
def update_map(group):
    return generate_map(group)

if __name__ == "__main__":
    app.run(debug=True)