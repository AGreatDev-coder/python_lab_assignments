import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def setup_environment():
    data_dir = Path('data')
    # Use pathlib to check/create directory
    if not data_dir.exists():
        data_dir.mkdir()
        
        buildings = ['Science_Block', 'Library', 'Admin_Building', 'Dormitory_A']
        start_date = '2023-01-01'
        end_date = '2023-12-31'
        date_range = pd.date_range(start=start_date, end=end_date, freq='H')
        
        for building in buildings:
            np.random.seed(len(building))
            base_load = np.random.uniform(10, 50)
            variation = np.random.normal(0, 5, len(date_range))
            daily_pattern = np.tile(np.sin(np.linspace(0, 3 * np.pi, 24)) * 10 + 10, len(date_range) // 24 + 1)[:len(date_range)]
            
            kwh_readings = base_load + daily_pattern + variation
            kwh_readings = np.maximum(kwh_readings, 0)
            
            df = pd.DataFrame({
                'timestamp': date_range,
                'kwh': kwh_readings
            })
            
            # Use pathlib / operator for path joining
            filename = data_dir / f"{building}_usage.csv"
            df.to_csv(filename, index=False)

class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh

class Building:
    def __init__(self, name):
        self.name = name
        self.readings = []
        self.df = None

    def add_readings_from_df(self, df):
        self.df = df
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.df.set_index('timestamp', inplace=True)
        self.df['Building'] = self.name

    def get_daily_totals(self):
        return self.df['kwh'].resample('D').sum()

    def get_weekly_average(self):
        return self.df['kwh'].resample('W').mean()

    def get_summary_stats(self):
        return {
            'Building': self.name,
            'Total_kWh': self.df['kwh'].sum(),
            'Mean_Daily_kWh': self.get_daily_totals().mean(),
            'Max_Reading': self.df['kwh'].max(),
            'Min_Reading': self.df['kwh'].min()
        }

class BuildingManager:
    def __init__(self):
        self.buildings = {}
        self.combined_df = pd.DataFrame()

    def ingest_data(self, directory_path):
        # Use pathlib to create a Path object
        dir_path = Path(directory_path)
        # Use glob to find all csv files
        files = list(dir_path.glob('*.csv'))
        
        all_data = []
        
        for file in files:
            try:
                # Extract filename without extension using .stem
                building_name = file.stem.replace('_usage', '')
                # Read directly from the Path object
                df = pd.read_csv(file)
                
                if 'timestamp' not in df.columns or 'kwh' not in df.columns:
                    raise ValueError(f"Invalid columns in {file}")

                building = Building(building_name)
                building.add_readings_from_df(df)
                self.buildings[building_name] = building
                all_data.append(building.df)
                
            except Exception as e:
                print(f"Error processing {file}: {e}")

        if all_data:
            self.combined_df = pd.concat(all_data)
        else:
            raise FileNotFoundError("No valid data found to process.")

    def export_data(self):
        self.combined_df.to_csv('cleaned_energy_data.csv')
        
        summary_list = [b.get_summary_stats() for b in self.buildings.values()]
        summary_df = pd.DataFrame(summary_list)
        summary_df.to_csv('building_summary.csv', index=False)
        return summary_df

    def generate_report(self, summary_df):
        total_consumption = self.combined_df['kwh'].sum()
        highest_consumer = summary_df.loc[summary_df['Total_kWh'].idxmax()]
        
        peak_time = self.combined_df['kwh'].idxmax()
        peak_value = self.combined_df['kwh'].max()
        peak_building = self.combined_df.loc[peak_time, 'Building']

        with open('summary.txt', 'w') as f:
            f.write("CAMPUS ENERGY CONSUMPTION REPORT\n")
            f.write("================================\n\n")
            f.write(f"Total Campus Consumption: {total_consumption:,.2f} kWh\n")
            f.write(f"Highest Consuming Building: {highest_consumer['Building']} ({highest_consumer['Total_kWh']:,.2f} kWh)\n")
            f.write(f"Peak Load Event: {peak_value:.2f} kWh at {peak_time} in {peak_building}\n\n")
            f.write("Building Summaries:\n")
            f.write(summary_df.to_string(index=False))

    def visualize_data(self):
        plt.style.use('ggplot')
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Merge top two subplots for the trend line
        ax1 = axes[0, 0]
        ax1.axis('off') 
        axes[0, 0].remove() 
        axes[0, 1].remove()
        ax1 = fig.add_subplot(2, 1, 1)

        daily_totals = self.combined_df.groupby([pd.Grouper(freq='D'), 'Building'])['kwh'].sum().unstack()
        daily_totals.plot(ax=ax1, alpha=0.7)
        ax1.set_title('Daily Energy Consumption Trend')
        ax1.set_ylabel('Total kWh')
        ax1.legend(loc='upper right')

        # Bottom Left: Bar Chart
        ax2 = fig.add_subplot(2, 2, 3)
        weekly_avg = self.combined_df.groupby('Building')['kwh'].resample('W').mean().groupby('Building').mean()
        weekly_avg.plot(kind='bar', ax=ax2, color='skyblue', edgecolor='black')
        ax2.set_title('Average Weekly Usage per Building')
        ax2.set_ylabel('Average kWh')
        ax2.tick_params(axis='x', rotation=45)

        # Bottom Right: Scatter Plot
        ax3 = fig.add_subplot(2, 2, 4)
        daily_max = self.combined_df.groupby([self.combined_df.index.hour, 'Building'])['kwh'].mean().unstack()
        for column in daily_max.columns:
            ax3.scatter(daily_max.index, daily_max[column], label=column, alpha=0.6)
        ax3.set_title('Average Peak Hour Consumption')
        ax3.set_xlabel('Hour of Day')
        ax3.set_ylabel('Average kWh')
        ax3.legend()

        plt.tight_layout()
        plt.savefig('dashboard.png')
        plt.close()

def main():
    setup_environment()
    
    manager = BuildingManager()
    manager.ingest_data('data')
    
    summary_df = manager.export_data()
    manager.generate_report(summary_df)
    manager.visualize_data()

if __name__ == "__main__":
    main()