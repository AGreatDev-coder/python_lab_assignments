Campus Energy-Use Dashboard

Project Overview

This Capstone Project implements an end-to-end pipeline for analyzing and visualizing campus energy consumption. It processes raw hourly meter readings from multiple buildings, aggregates the data using Object-Oriented Programming (OOP) principles, and generates a visual dashboard along with a statistical summary report.

Features

Data Ingestion: Automatically detects and reads CSV files from a data/ directory using pathlib.

Data Cleaning: Validates timestamps and energy readings, handling missing or corrupt data.

OOP Architecture: Uses Building, MeterReading, and BuildingManager classes to structure the analysis.

Statistical Analysis: Computes daily totals, weekly averages, and identifies peak load events.

Visualization: Generates a multi-chart dashboard (Trend Line, Bar Chart, Scatter Plot) using matplotlib.

Automated Reporting: Exports cleaned data and creates a text-based executive summary.

Prerequisites

Python 3.x

Pandas

NumPy

Matplotlib

To install the required libraries:

pip install pandas numpy matplotlib


Project Structure

.
├── energy_dashboard.py       # Main application script
├── README.md                 # Project documentation
├── data/                     # Directory for input CSV files
│   ├── Science_Block_usage.csv
│   └── Library_usage.csv
├── output/ (Generated)       # Output files
│   ├── cleaned_energy_data.csv
│   ├── building_summary.csv
│   ├── summary.txt
│   └── dashboard.png


Usage

Prepare Data: Ensure your input CSV files (e.g., Library_usage.csv, Science_Block_usage.csv) are placed in a folder named data in the same directory as the script.

Note: The script includes a setup_environment() function that will automatically create sample data if the directory doesn't exist.

Run the Script:

python energy_dashboard.py


View Results: Check the root directory (or output folder) for:

dashboard.png: Visual analysis of energy trends.

summary.txt: A text report highlighting total consumption and peak usage.

cleaned_energy_data.csv: The merged and processed dataset.

Input File Format

Input CSV files should have the following columns:

timestamp: Date and time of the reading (e.g., 2023-01-01 00:00:00)

kwh: Energy consumption in kilowatt-hours (float)

Author

[Ronak]