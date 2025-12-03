Weather Data Visualizer

Project Overview

This project analyzes and visualizes real-world weather data for New Delhi, India, for the year 2023. It serves as a solution to "Lab Assignment 4," demonstrating skills in data acquisition, cleaning, statistical analysis, and visualization using Python.

The tool processes raw daily weather records to compute key statistics (mean temperature, total rainfall, etc.) and generates visual charts to identify seasonal patterns and trends.

Dataset Description

The analysis uses weather_data.csv, which contains daily observations for New Delhi throughout 2023.

Source: Compiled from open-source meteorological data samples.

Columns:

Date: The date of observation (YYYY-MM-DD).

Temperature: Average daily temperature (°C).

Rainfall: Total daily precipitation (mm).

Humidity: Average relative humidity (%).

Tools & Libraries Used

Python 3.x: Core programming language.

Pandas: Used for data loading, cleaning, dataframe manipulation, and time-series handling.

NumPy: Used for efficient numerical calculations and statistical aggregation.

Matplotlib: Used (via Pandas plotting wrappers) to generate line charts, bar graphs, and scatter plots.

Project Structure

weather_visualizer.py: The main Python script containing functions for data generation, cleaning, analysis, and visualization.

weather_data.csv: The input dataset.

cleaned_weather_data.csv: (Generated) The processed dataset with missing values handled.

weather_analysis_report.txt: (Generated) A text file containing the calculated statistics.

Plots (Generated):

temperature_trend.png: Line graph of daily temperatures.

monthly_rainfall.png: Bar chart of aggregated monthly rainfall.

temp_vs_humidity.png: Scatter plot showing correlation between heat and humidity.

combined_weather_plot.png: Subplots showing temperature and rainfall over time.

How to Run

Ensure you have the required libraries installed:

pip install pandas numpy matplotlib


Place weather_data.csv in the same directory as the script.

Run the script:

python weather_visualizer.py


Check the output files in the directory for the results.

Key Insights

Temperature: Peaks in May/June before the monsoon cools the region down.

Rainfall: Heavily concentrated in the monsoon months (July-August).

Humidity: Shows a strong seasonal shift, rising significantly during the rainy season despite high temperatures.

Author

[Ronak }