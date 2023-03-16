from django import forms

class PredictionsForm(forms.Form):
    co2_emissions = forms.FloatField(label='CO2 Emissions (in metric tons)', required=True, min_value=0)
    temperature = forms.FloatField(label='Temperature (in °C)', required=True, min_value=-273.15)
    humidity = forms.FloatField(label='Humidity (in %)', required=True, min_value=0, max_value=100)
    pm25 = forms.FloatField(label='PM2.5 (in μg/m³)', required=False, min_value=0)
    pm10 = forms.FloatField(label='PM10 (in μg/m³)', required=False, min_value=0)