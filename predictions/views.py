from django.shortcuts import render
from django.shortcuts import render
from .forms import PredictionsForm
import pandas as pd
import matplotlib.pyplot as plt
import requests
import matplotlib
matplotlib.use('Agg')


def get_realtime_data():
    url = 'https://api.openaq.org/v1/latest'
    params = {
        'city': 'Delhi',
        'parameter': ['pm25', 'pm10'],
        'limit': 1,
    }
    response = requests.get(url, params=params)
    data = response.json()
    if 'results' not in data or len(data['results']) == 0:
        return None, None
    pm25 = 0
    pm10 = 0
    measurements = data['results'][0].get('measurements')
    if measurements:
        for measurement in measurements:
            parameter = measurement.get('parameter')
            if parameter == 'pm25':
                pm25 = measurement.get('value', 0)
            elif parameter == 'pm10':
                pm10 = measurement.get('value', 0)
    return pm25, pm10
def calculate_predictions(request):
    if request.method == 'POST':
        form = PredictionsForm(request.POST)
        if form.is_valid():
            co2_emissions = form.cleaned_data['co2_emissions']
            temperature = form.cleaned_data['temperature']
            humidity = form.cleaned_data['humidity']
            if request.POST.get('use_realtime_data'):
                pm25, pm10 = get_realtime_data()

                if pm25 is None or pm10 is None:
                    pm25 = 0
                    pm10 = 0
            else:
                pm25 = form.cleaned_data['pm25']
                pm10 = form.cleaned_data['pm10']
            if co2_emissions is None:
                co2_emissions = 0

            greenhouse_gas_emissions = co2_emissions * 3.67
            air_pollution = (pm25 * 0.035) + (pm10 * 0.05) + (co2_emissions * 0.0025)
            context = {
                'co2_emissions': co2_emissions,
                'greenhouse_gas_emissions': greenhouse_gas_emissions,
                'pm25': pm25,
                'pm10': pm10,
                'air_pollution': air_pollution,
            }
            if request.POST.get('use_realtime_data'):
                url = 'https://api.openaq.org/v1/measurements'
                params = {
                    'city': 'Delhi',
                    'parameter': ['pm25', 'pm10'],
                    'limit': 1000,
                }
                response = requests.get(url, params=params)
                data = response.json()
                print(data)
                pm25_values = []
                pm10_values = []
                co2_emissions_values = []
                for result in data['results']:
                    measurements = result.get('measurements')
                    if measurements:
                        pm25_values.append(measurements[0].get('value', 0))
                        pm10_values.append(measurements[1].get('value', 0))
                        co2_emissions_values.append(measurements[0].get('value',0))

                df = pd.DataFrame({'PM2.5': pm25_values, 'PM10': pm10_values})
                fig, ax = plt.subplots()
                df.plot.line(ax=ax)
                ax.set_xlabel('Time')
                ax.set_ylabel('Concentration (μg/m³)')
                ax.set_title('Real-time Air Quality Data for Delhi')
                fig.savefig('realtime_data_plot.png')
                plt.close(fig)
                with open('realtime_data_plot.png', 'rb') as f:
                    context['realtime_data_plot'] = f.read()
                    context['form'] = form
        return render(request, '"J:\My Drive\Destiny\site\destiny\evs_project\index.html"', context)
    else:
        form = PredictionsForm()
        context = {'form': form}
        return render(request, '"J:\My Drive\Destiny\site\destiny\evs_project\index.html"', context)