import pandas as pd
import plotly.express as px
import requests
import json
import streamlit as st

# Set page config to wide mode and set page title
st.set_page_config(page_title="Canterbury Air Quality Index Real-time Monitoring", layout="wide")

# Custom CSS to style the select_slider and table
st.markdown("""
    <style>
        .stSlider > div[data-baseweb="slider"] > div > div > div > div {
            background: #0c6e6e; /* Grey background for slider */
            color: white; /* Slider value color */
            padding: 10px; /* Padding for slider value */
            border-radius: 5px; /* Border radius for slider value */
            font-style: bold; /* Bold font for slider value */
        }
        .stSlider > div[data-baseweb="slider"] > div > div > div > div > div {
            background: #0c6e6e; /* Highlight color for selected value */
        }
        .stSlider label {
            color: #0c6e6e; /* Slider label color */
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        thead th {
            background-color: #0c6e6e;
            color: white;
            padding: 10px;
        }
        tbody tr:nth-child(odd) {
            background-color: #f2f2f2;
        }
        tbody tr:nth-child(even) {
            background-color: #ffffff;
        }
        tbody td {
            padding: 10px;
        }
        tbody th {
            display: none; /* Hide index */
        }
    </style>
""", unsafe_allow_html=True)

# GraphQL query
query = """
{
  stationItems {
    StationCode
    StationName
    StationShortName
    StationLocation
    StationCity
    StationLatitude
    StationLongitude
    MonitorChannel
    MonitorName
    MonitorTypeCode
    MonitorTypeDescription
    MonitorFullName
  }
}
"""

# Fetch data from GraphQL API
response = requests.post("http://localhost:4000/graphql", json={"query": query})

if response.status_code == 200:
    data = response.json()
    if "errors" in data:
        st.error(f"GraphQL error: {data['errors']}")
    else:
        # Parse JSON data
        df = pd.DataFrame(data["data"]["stationItems"])

        # Streamlit app
        st.title("Canterbury Air Quality Monitoring Stations Visualization")

        station_names = df["StationName"].unique()
        selected_station = st.select_slider("Slide to select station", options=station_names, value="Ashburton")
        st.header(f"Current Station {selected_station}")
        station_details = df[df["StationName"] == selected_station]


        # Convert the DataFrame to HTML and set the width to 100%
        station_details_html = station_details.to_html(index=False)
        st.markdown(f'<div style="overflow-x: auto; width: 100%; margin-bottom: 2rem;">{station_details_html}</div>', unsafe_allow_html=True)

        # Filter data for the selected station
        filtered_df = df[df["StationName"] == selected_station]

        # Plot scatter plot for the selected station
        st.header(f"Monitor Channels - {selected_station}")
        fig = px.scatter(
            filtered_df,
            x="MonitorFullName",
            y="MonitorChannel",
            color="MonitorFullName",
            labels={
                "MonitorFullName": "Monitor Full Name",
                "MonitorChannel": "Monitor Channel"
            }
        )

        fig.update_traces(marker=dict(size=15))

        fig.update_layout(
            xaxis_title="Monitor Full Name",
            yaxis_title="Monitor Channel",
            legend_title="Monitor Full Name",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(fig, use_container_width=True)


        st.header("Monitoring Station pollution Distribution")
        monitor_count = (
            df.groupby("StationName")["MonitorTypeCode"]
            .count()
            .reset_index(name="MonitorCount")
        )
        fig_bar = px.bar(
            monitor_count,
            x="StationName",
            y="MonitorCount",
            title="Number of Monitoring Items per Station",
            color="StationName",
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        fig_bar.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Load GeoJSON file for New Zealand regions
        with open("./gadm41_NZL_2.json") as f:
            nz_geojson = json.load(f)

        # 创建一个新列并为其分配一个常数值
        df['size'] = 10

        fig = px.scatter_mapbox(df, 
                        lat='StationLatitude', 
                        lon='StationLongitude', 
                        color='StationShortName',
                        hover_data=df.columns,  # 显示所有数据
                        size='size',  # 设置点的大小
                        center={"lat": -43.91224, "lon": 171.7552},
                        mapbox_style="carto-positron", 
                        zoom=8)  # 增加地图的缩放级别

        fig.update_traces(marker=dict(size=49, symbol='circle'))  # 设置气球弹出效果

        fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=900  # 提高地图的高度
        )

        st.plotly_chart(fig, use_container_width=True)

else:
    st.error(f"Failed to fetch data from GraphQL API: {response.status_code}")
