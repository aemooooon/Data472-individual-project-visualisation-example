# Canterbury Air Quality Monitoring Stations Visualization

This project is part of the Data472 - Data Engineer course, created as an individual project example. As a volunteer for the central data collection team, this project serves as a data visualization example for other individual students.

## Project Overview

The Canterbury Air Quality Monitoring Stations Visualization project aims to visualize real-time data from various air quality monitoring stations in Canterbury. The project utilizes data fetched from a GraphQL API and presents it through an interactive Streamlit dashboard. The visualization includes detailed information about each monitoring station, pollution distribution, and geographical representation using a map.

[Online Live Demo](http://visual.hua.nz/)

## Features

- **Real-time Data Fetching:** Fetches air quality data from a GraphQL API, which is also provided as an [example](https://github.com/Data472-Individual-Project-Pipeline/DATA472-Individual-Project-Example) for another individual student.
- **Interactive Dashboard:** Utilizes Streamlit to create an interactive web application.
- **Data Visualization:** Visualizes data using Plotly for scatter plots, bar charts, and Canterbury Geo map visualizations.
- **Geospatial Analysis:** Displays monitoring stations on a map with geographical context.

## Installation

### Prerequisites

- Python 3.6+
- Node.js (for GraphQL server, if applicable)
- Yarn (for GraphQL server, if applicable)

### Steps

1. Clone the repository:
    ```sh
    git clone https://github.com/aemoooooon/Data472-individual-project-visualisation-example.git
    cd Data472-individual-project-visualisation-example
    ```

2. Set up a virtual environment and install dependencies:
    ```sh
    python -m venv aqi_env
    source aqi_env/bin/activate  # On Windows, use `aqi_env\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Run the Streamlit application:
    ```sh
    streamlit run app.py
    ```

## Usage

1. Open the Streamlit application in your browser.
2. Use the slider to select a monitoring station.
3. Explore the interactive plots and map visualizations to analyze air quality data.

## Project Structure

- `app.py`: Main application file containing the Streamlit code.
- `requirements.txt`: Python dependencies required for the project.
- `gadm41_NZL_2.json`: GeoJSON file for New Zealand regions.
- `.gitignore`: Git ignore file to exclude unnecessary files from the repository.

## Data Source

The data for this project is fetched from a GraphQL API. The GraphQL query used to fetch the data is as follows:

```graphql
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
```

## Contact

If you have any questions, please feel free to contact the Central Collection Team or project maintainer Hua at aemooooon@gmail.com
