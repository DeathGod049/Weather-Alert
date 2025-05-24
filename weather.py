import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

API_Key = os.environ['WA_API_Key']
account_sid = os.environ['SMS_ACC_ID']
auth_token = os.environ['SMS_ACC_Auth']

class Weather:
        def get_position(self, city):
                parameters = {
                        "q": city,
                        "appid": API_Key
                }
                pos_url = "http://api.openweathermap.org/geo/1.0/direct"
                response = requests.get(url=pos_url, params=parameters)
                try:
                        lat, lon = response.json()[0]["lat"], response.json()[0]["lon"]
                        return lat, lon
                except:
                        return False

        def get_weather(self, city_name):
                position = self.get_position(city_name)
                if not position:
                        return False
                parameters = {
                        "lat": position[0],
                        "lon": position[1],
                        "cnt": 4,
                        "appid": API_Key
                }
                forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
                response = requests.get(url=forecast_url, params=parameters)
                response.raise_for_status()
                return response.json()


# city_name = input("Enter city name: ")
city_name = "New York"
weather = Weather()
current_weather = weather.get_weather(city_name)
if not current_weather:
        print("City not found")
else:
        forecast = current_weather["list"]
        will_rain = False
        for item in forecast:
                if_rain = item["weather"][0]["id"]
                if if_rain < 700:
                        will_rain = f"It might start raining at approximately {item['dt_txt'][11:]}. Bring an ☔️!"
                        break

        if not will_rain:
                print("Cheers! You don't need an umbrella")
        else:
                proxy_client = TwilioHttpClient()
                proxy_client.session.proxies = {'https': os.environ['https_proxy']}
                client = Client(account_sid, auth_token, http_client=proxy_client)
                # client = Client(account_sid, auth_token)
                message = client.messages.create(
                        from_='<Twilio Number>',
                        to='<Recipient Number>',
                        body=will_rain
                )

                print(message.sid)
                print(message.status)

                print(will_rain)
