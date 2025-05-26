import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from django.shortcuts import render
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, 'my_app', 'covid_data.csv')
STATIC_DIR = os.path.join(BASE_DIR, 'my_app', 'static')

def generate_random_colors(n):
    return ["#" + ''.join(random.choices('0123456789ABCDEF', k=6)) for _ in range(n)]


def index(request):
    df = pd.read_csv(CSV_PATH)

    # Ensure column names are clean
    df.columns = df.columns.str.strip().str.lower()
    
    countries = df['country'].unique()
    selected_country = request.GET.get('country', countries[0])
    country_data = df[df['country'] == selected_country].iloc[0]

    # Make sure the static directory exists
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)

    # Generate random colors
    bar_colors = generate_random_colors(len(['Confirmed', 'Deaths', 'Recovered', 'Active']))
    pie_colors = generate_random_colors(len([country_data['confirmed'], country_data['deaths'], country_data['recovered'], country_data['active']]))

    # BAR CHART
    plt.figure(figsize=(6, 4))
    plt.bar(['Confirmed', 'Deaths', 'Recovered', 'Active'], [
        country_data['confirmed'],
        country_data['deaths'],
        country_data['recovered'],
        country_data['active']
    ], color=bar_colors)
    plt.title(f'COVID-19 Stats in {selected_country}')
    plt.tight_layout()
    bar_path = os.path.join(STATIC_DIR, 'bar.png')
    plt.savefig(bar_path)
    plt.close()

    # PIE CHART
    plt.figure(figsize=(6, 4))
    plt.pie(
        [country_data['confirmed'], country_data['deaths'], country_data['recovered'], country_data['active']],
        labels=['Confirmed', 'Deaths', 'Recovered', 'Active'],
        explode=[0.0,0.0,0.0,0.3],
        shadow=True,
        wedgeprops={"linewidth": 2},
        autopct='%1.1f%%',
        colors=pie_colors
    )
    plt.title(f'COVID-19 Distribution in {selected_country}')
    pie_path = os.path.join(STATIC_DIR, 'pie.png')
    plt.savefig(pie_path)
    plt.close()

    context = {
        'countries': countries,
        'selected_country': selected_country
    }
    return render(request, 'index.html', context)
