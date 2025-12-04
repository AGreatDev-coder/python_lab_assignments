import pandas as pd
import numpy as np

def generate_sample_data(filename='weather_data.csv'):
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    np.random.seed(42)
    temperature = np.random.normal(loc=25, scale=5, size=len(dates))
    rainfall = np.random.exponential(scale=2, size=len(dates))
    humidity = np.random.uniform(low=30, high=90, size=len(dates))
    
    data = {
        'Date': dates,
        'Temperature': temperature,
        'Rainfall': rainfall,
        'Humidity': humidity
    }
    
    df = pd.DataFrame(data)
    
    indices_to_drop = np.random.choice(df.index, size=10, replace=False)
    df.loc[indices_to_drop, 'Temperature'] = np.nan
    
    df.to_csv(filename, index=False)
    print(f"Sample data generated: {filename}")

def clean_data(df):
    df['Date'] = pd.to_datetime(df['Date'])
    
    df['Temperature'] = df['Temperature'].fillna(df['Temperature'].mean())
    df['Rainfall'] = df['Rainfall'].fillna(0)
    df['Humidity'] = df['Humidity'].ffill()
    
    required_columns = ['Date', 'Temperature', 'Rainfall', 'Humidity']
    df = df[required_columns]
    
    return df

def perform_statistical_analysis(df):
    stats = {
        'mean_temp': np.mean(df['Temperature']),
        'max_temp': np.max(df['Temperature']),
        'min_temp': np.min(df['Temperature']),
        'std_temp': np.std(df['Temperature']),
        'total_rainfall': np.sum(df['Rainfall']),
        'avg_humidity': np.mean(df['Humidity'])
    }
    return stats

def analyze_monthly_data(df):
    df['Month'] = df['Date'].dt.month_name()
    monthly_stats = df.groupby('Month').agg({
        'Temperature': 'mean',
        'Rainfall': 'sum',
        'Humidity': 'mean'
    }).reindex([
        'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ])
    return monthly_stats

def create_visualizations(df, monthly_stats):
    ax1 = df.plot(x='Date', y='Temperature', kind='line', title='Daily Temperature Trends', color='orange', figsize=(12, 6))
    ax1.set_ylabel('Temperature (C)')
    ax1.axhline(y=df['Temperature'].mean(), color='red', linestyle='--')
    ax1.figure.tight_layout()
    ax1.figure.savefig('temperature_trend.png')

    ax2 = monthly_stats['Rainfall'].plot(kind='bar', title='Total Monthly Rainfall', color='blue', figsize=(12, 6), rot=45)
    ax2.set_ylabel('Rainfall (mm)')
    ax2.set_xlabel('Month')
    ax2.figure.tight_layout()
    ax2.figure.savefig('monthly_rainfall.png')

    ax3 = df.plot.scatter(x='Temperature', y='Humidity', c='green', title='Temperature vs. Humidity', figsize=(10, 6), grid=True)
    ax3.figure.tight_layout()
    ax3.figure.savefig('temp_vs_humidity.png')

    axes = df.plot(x='Date', y=['Temperature', 'Rainfall'], subplots=True, figsize=(12, 10), title=['Temperature Over Time', 'Rainfall Over Time'])
    axes[0].set_ylabel('Temp (C)')
    axes[1].set_ylabel('Rainfall (mm)')
    axes[0].figure.tight_layout()
    axes[0].figure.savefig('combined_weather_plot.png')

def generate_report(stats, monthly_stats):
    with open('weather_analysis_report.txt', 'w') as f:
        f.write("WEATHER DATA ANALYSIS REPORT\n")
        f.write("============================\n\n")
        
        f.write("1. OVERALL STATISTICS\n")
        f.write("---------------------\n")
        f.write(f"Average Temperature: {stats['mean_temp']:.2f} C\n")
        f.write(f"Maximum Temperature: {stats['max_temp']:.2f} C\n")
        f.write(f"Minimum Temperature: {stats['min_temp']:.2f} C\n")
        f.write(f"Temperature Std Dev: {stats['std_temp']:.2f}\n")
        f.write(f"Total Rainfall:      {stats['total_rainfall']:.2f} mm\n")
        f.write(f"Average Humidity:    {stats['avg_humidity']:.2f} %\n\n")
        
        f.write("2. MONTHLY AGGREGATION\n")
        f.write("----------------------\n")
        f.write(monthly_stats.to_string())

def main():
    filename = 'weather_data.csv'
    
    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        generate_sample_data(filename)
        df = pd.read_csv(filename)
    
    cleaned_df = clean_data(df)
    
    cleaned_df.to_csv('weather_data.csv', index=False)
    
    stats = perform_statistical_analysis(cleaned_df)
    monthly_stats = analyze_monthly_data(cleaned_df)
    
    create_visualizations(cleaned_df, monthly_stats)
    
    generate_report(stats, monthly_stats)
    
    print("Analysis complete. Generated: cleaned data, plots, and report.")

if __name__ == "__main__":
    main()