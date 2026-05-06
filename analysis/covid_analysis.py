import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def generate_visualizations(data_path, output_dir):
    print("Loading data for analysis...")
    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'])
    
    # Filter out dates where global data is missing (last few days of archived data)
    # We find the last date where the World entity has total_cases > 0
    world_data = df[df['iso_code'] == 'OWID_WRL']
    valid_world_data = world_data[world_data['total_cases'] > 0]
    if valid_world_data.empty:
        # Fallback to any data if World entity is missing/empty
        latest_date = df[df['total_cases'] > 0]['date'].max()
    else:
        latest_date = valid_world_data['date'].max()
    
    print(f"Latest valid data date: {latest_date}")
    
    # Trim the dataset to only include data up to the latest valid date
    df = df[df['date'] <= latest_date]
    
    # Remove early data where cases were 0 for most of the world to make plots cleaner
    df = df[df['date'] >= '2020-01-01']
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 1. Global Trends (Cases & Deaths)
    print("Generating Graph 1 & 2: Global Trends...")
    global_daily = df.groupby('date')[['total_cases', 'total_deaths', 'new_cases', 'new_deaths']].sum().reset_index()
    
    plt.figure()
    plt.plot(global_daily['date'], global_daily['total_cases'], label='Total Cases', color='blue')
    plt.title('Global Total COVID-19 Cases Over Time')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.legend()
    plt.savefig(f"{output_dir}/global_total_cases.png")
    plt.close()

    plt.figure()
    plt.plot(global_daily['date'], global_daily['total_deaths'], label='Total Deaths', color='red')
    plt.title('Global Total COVID-19 Deaths Over Time')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.legend()
    plt.savefig(f"{output_dir}/global_total_deaths.png")
    plt.close()

    # 3 & 4. Daily Impact
    print("Generating Graph 3 & 4: Daily Impact...")
    plt.figure()
    plt.bar(global_daily['date'], global_daily['new_cases'], color='skyblue')
    plt.title('Global Daily New COVID-19 Cases')
    plt.savefig(f"{output_dir}/daily_new_cases.png")
    plt.close()

    plt.figure()
    plt.bar(global_daily['date'], global_daily['new_deaths'], color='salmon')
    plt.title('Global Daily New COVID-19 Deaths')
    plt.savefig(f"{output_dir}/daily_new_deaths.png")
    plt.close()

    # 5 & 6. Top Countries
    print("Generating Graph 5 & 6: Top Countries...")
    latest_data = df[df['date'] == df['date'].max()]
    # Filter out non-country entities
    countries_only = latest_data[~latest_data['iso_code'].str.startswith('OWID_')]
    
    top_10_cases = countries_only.nlargest(10, 'total_cases')
    plt.figure()
    sns.barplot(data=top_10_cases, x='total_cases', y='location', palette='viridis')
    plt.title('Top 10 Countries by Total COVID-19 Cases')
    plt.savefig(f"{output_dir}/top_10_cases.png")
    plt.close()

    top_10_deaths = countries_only.nlargest(10, 'total_deaths')
    plt.figure()
    sns.barplot(data=top_10_deaths, x='total_deaths', y='location', palette='magma')
    plt.title('Top 10 Countries by Total COVID-19 Deaths')
    plt.savefig(f"{output_dir}/top_10_deaths.png")
    plt.close()

    # 7. Case Fatality Rate (CFR)
    print("Generating Graph 7: CFR...")
    countries_only['cfr'] = (countries_only['total_deaths'] / countries_only['total_cases']) * 100
    top_cfr = countries_only[countries_only['total_cases'] > 1000000].nlargest(10, 'cfr') # Only countries with >1M cases
    plt.figure()
    sns.barplot(data=top_cfr, x='cfr', y='location', palette='rocket')
    plt.title('Top 10 Countries by Case Fatality Rate (%) (Countries with >1M cases)')
    plt.savefig(f"{output_dir}/cfr_top_countries.png")
    plt.close()

    # 8. Vaccination Growth
    print("Generating Graph 8: Vaccination Growth...")
    vax_daily = df.groupby('date')['total_vaccinations'].sum().reset_index()
    plt.figure()
    plt.plot(vax_daily['date'], vax_daily['total_vaccinations'], color='green')
    plt.title('Global Total COVID-19 Vaccinations Over Time')
    plt.savefig(f"{output_dir}/vaccination_growth.png")
    plt.close()

    # 9. Vaccine vs Deaths Correlation
    print("Generating Graph 9: Vaccine Efficacy...")
    plt.figure()
    sns.scatterplot(data=countries_only, x='people_fully_vaccinated_per_hundred', y='total_deaths_per_million', hue='continent')
    plt.title('Vaccination Rate vs. Mortality per Million')
    plt.savefig(f"{output_dir}/vax_vs_deaths.png")
    plt.close()

    # 10. GDP vs Mortality
    print("Generating Graph 10: GDP vs Mortality...")
    plt.figure()
    sns.scatterplot(data=countries_only, x='gdp_per_capita', y='total_deaths_per_million', hue='continent')
    plt.xscale('log')
    plt.title('GDP per Capita vs. Mortality per Million (Log Scale)')
    plt.savefig(f"{output_dir}/gdp_vs_mortality.png")
    plt.close()

    # 11. Elderly Pop vs Mortality
    print("Generating Graph 11: Elderly Population vs Mortality...")
    plt.figure()
    sns.scatterplot(data=countries_only, x='aged_65_older', y='total_deaths_per_million', hue='continent')
    plt.title('Percentage of Population Aged 65+ vs. Mortality per Million')
    plt.savefig(f"{output_dir}/elderly_vs_mortality.png")
    plt.close()

    # 12. Stringency Index (India Example)
    print("Generating Graph 12: Stringency Index...")
    india_data = df[df['location'] == 'India']
    fig, ax1 = plt.subplots()
    ax1.plot(india_data['date'], india_data['new_cases'], color='blue', label='New Cases')
    ax1.set_ylabel('New Cases', color='blue')
    ax2 = ax1.twinx()
    ax2.plot(india_data['date'], india_data['stringency_index'], color='red', alpha=0.5, label='Stringency Index')
    ax2.set_ylabel('Stringency Index', color='red')
    plt.title('COVID-19 Stringency Index vs. New Cases in India')
    plt.savefig(f"{output_dir}/stringency_vs_cases.png")
    plt.close()

    # 13. Continent Distribution
    print("Generating Graph 13: Continent Distribution...")
    continent_data = latest_data[latest_data['iso_code'].isin(['OWID_AFR', 'OWID_ASI', 'OWID_EUR', 'OWID_NAM', 'OWID_SAM', 'OWID_OCE'])]
    plt.figure()
    sns.barplot(data=continent_data, x='total_deaths', y='location', palette='Set2')
    plt.title('Total Deaths by Continent')
    plt.savefig(f"{output_dir}/continent_distribution.png")
    plt.close()

    # 14. Hospitalization Trends (USA)
    print("Generating Graph 14: Hospitalization...")
    usa_data = df[df['location'] == 'United States']
    plt.figure()
    plt.plot(usa_data['date'], usa_data['hosp_patients'], label='Hospital Patients')
    plt.plot(usa_data['date'], usa_data['icu_patients'], label='ICU Patients', color='orange')
    plt.title('Hospital and ICU Patients Trends in the USA')
    plt.legend()
    plt.savefig(f"{output_dir}/hospitalization_trends.png")
    plt.close()

    # 15. Testing vs Positivity
    print("Generating Graph 15: Testing...")
    plt.figure()
    sns.scatterplot(data=countries_only, x='total_tests_per_thousand', y='positive_rate', hue='continent')
    plt.title('Total Tests per Thousand vs. Positive Rate')
    plt.savefig(f"{output_dir}/testing_vs_positivity.png")
    plt.close()

    # 16. Life Expectancy correlation
    print("Generating Graph 16: Life Expectancy...")
    plt.figure()
    sns.scatterplot(data=countries_only, x='life_expectancy', y='total_deaths_per_million', hue='continent')
    plt.title('Life Expectancy vs. Mortality per Million')
    plt.savefig(f"{output_dir}/life_expectancy_correlation.png")
    plt.close()

if __name__ == "__main__":
    PROCESSED_DATA = "data/processed/cleaned_covid_data.csv"
    OUTPUT_ASSETS = "report/assets"
    generate_visualizations(PROCESSED_DATA, OUTPUT_ASSETS)
    print("All visualizations generated.")
