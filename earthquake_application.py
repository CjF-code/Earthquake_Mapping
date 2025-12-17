import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import eq_functions as ef

if not st.session_state:
    st.session_state["earthquakes"] = None

st.header("Earthquake visualisation")

with st.sidebar:
    st.subheader("Visulaisation Parameters")

    # Min and max earthquake magnitude for visulaisation
    min_magnitude, max_magnitude = st.select_slider(
        "Magnitude range",
        options=np.round(np.arange(4.0, 10.1, 0.1), 1),
        value=(4.0, 10.0),
    )

    defualt_date = datetime.today() - timedelta(days=30)
    start_date = st.date_input("Investigation Start Date", value=defualt_date.date())

    # Calculate the difference in days between start_date and today
    days_difference = (datetime.today().date() - start_date).days

    st.write(
        f"The selected investigation period spans the past {days_difference} days."
    )

    if st.button("Save Parameters"):
        # Obtain data for earthquake within filters
        st.session_state.earthquakes = ef.generate_earthquake_data(
            days_difference, min_magnitude, max_magnitude
        )

        st.write(
            f"{len(st.session_state.earthquakes)} earthquakes match your filter criteria."
        )

# Create list to be turned into a df for plotting earthquake data, with a size and colour parameter for the interactive map
earthquake_data = [
    {
        "magnitude": eq_obj.magnitude,
        "location": eq_obj.location,
        "longitude": eq_obj.longitude,
        "latitude": eq_obj.latitude,
        "depth": eq_obj.depth,
        "time": eq_obj.time,
        "name": eq_obj.name,
        "scale_for_graph": ef.estimate_affected_population(eq_obj.latitude,eq_obj.longitude,eq_obj.magnitude)/30,
        "colour": plt.cm.YlOrRd((eq_obj.magnitude - 4) / (7.5 - 4))[:3],
    }
    for eq_obj in st.session_state.earthquakes
]

earthquake_df = pd.DataFrame(earthquake_data)

st.write("*Coloured by magnitude, sized by estimated affected population*")

# Plot earthquake data in interactive map
st.map(
    earthquake_df,
    latitude="latitude",
    longitude="longitude",
    size="scale_for_graph",
    color="colour",
)

# Define list of names within filters
earthquake_names = earthquake_df.name

# Select a name to display more info
more_info_request = st.selectbox("More info:", options=earthquake_names)
requested_earthquake = earthquake_df[
    earthquake_df["name"] == more_info_request
].reset_index()


# Display of additional information
col1, col2 = st.columns([2, 3])
with col1:
    st.write(f"**Location of earthquake:**")
    st.write(f"**Date of earthquake:**")
    st.write(f"**Magnitude of arthquake:**")
    st.write(F"**Estimated affected population:**")

with col2:
    st.write(requested_earthquake["location"][0])
    st.write(requested_earthquake["time"][0])
    st.write(f"{requested_earthquake['magnitude'][0]}")
    st.write(f"{requested_earthquake['scale_for_graph'][0]:,}")
