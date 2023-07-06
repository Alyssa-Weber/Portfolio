# Weather Lookup
# Author Alyssa Weber
# 8/13/2022

# Weather Program
import requests
import json

api_key = 'e9cbf02f8341a8a133c588fe08c2248b'


# Prompts user to lookup weather by city or zipcode
# Calls corresponding functions to find and clean up data
# Calls the runagain function so users can use the lookup multiple times
# Includes error handling for input errors
def main():
    print('Welcome! I can look up the weather in your area.')
    lookup = input('Would you like to look up by city or zipcode?\n'
                   '--> ')
    lookup = lookup.lower()
    if lookup == 'zipcode':
        zipcode = input('zipcode: ')
        try:
            zipcode_lookup(zipcode)
            run_again()
        except:
            print('Invalid zipcode. Try again\n')
            main()
    elif lookup == 'city':
        city = input('City: ')
        state = input('State Abbreviation: ')
        try:
            city_lookup(city, state)
            run_again()
        except:
            print('Invalid City and/or State. Try again\n')
            main()
    else:
        print('Invalid entry. Try again\n')
        main()


# Uses a zipcode to find latitude and longitude, then calls the get_weather function
def zipcode_lookup(zipcode):
    zip_lookup = 'http://api.openweathermap.org/geo/1.0/zip?zip=' + zipcode + ',US&appid=' + api_key
    zipresponsse = requests.request("GET", zip_lookup)
    zipjson = json.loads(zipresponsse.text)
    lat = json.dumps(zipjson['lat'])
    lon = json.dumps(zipjson['lon'])
    get_weather(lat, lon)


# Uses a City and State lookup to find latitude and longitude, then calls the get_weather function
def city_lookup(city, state):
    cityinput_lookup = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + ',' + state + ',US&appid=' + api_key
    cityresponse = requests.request("GET", cityinput_lookup)
    cityjson = json.loads(cityresponse.text)
    citydict = cityjson['coord']
    lat = str(citydict['lat'])
    lon = str(citydict['lon'])
    get_weather(lat, lon)


# Uses latitude and longitude to find weather details
# Calls the function fahrenheitdisplay or celsiusdisplay to print the results based on user preference
def get_weather(lat, lon):
    weather_lookup = 'https://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + lon + '&appid=' + api_key
    weatherresponse = requests.request("GET", weather_lookup)
    weatherjson = json.loads(weatherresponse.text)
    city = json.dumps(weatherjson['name']).strip('"')
    weatherdict = weatherjson['main']
    weatherlist = list()
    display = input('\nWould you like your temperature in Celsius or Fahrenheit?\n'
                    '\tType C or F: ')
    display = display.upper()
    print('\n')
    if display == 'C':
        celsiusdisplay(weatherdict, weatherlist, city)
    elif display == 'F':
        fahrenheitdisplay(weatherdict, weatherlist, city)


# Converts Kelvin to Fahrenheit
# Prints weather details using Fahrenheit labels
def fahrenheitdisplay(dict, list, city):
    for key, val in dict.items():
        if key.startswith('temp') or key.startswith('feels'):
            val = int(val)
            far = int((9 / 5) * (val - 273) + 32)
            list.append(far)
        else:
            list.append(val)
    currenttemp = list[0]
    feelslike = list[1]
    mintemp = list[2]
    maxtemp = list[3]
    pressure = list[4]
    humidity = list[5]
    print('The temperature in {} is currently {} degrees Fahrenheit. '
          '\nHere are some other stats...'.format(city, currenttemp))
    print('\tFeels like: {} degrees'.format(feelslike),
          '\n\tHigh: {} degrees'.format(maxtemp),
          '\n\tLow: {} degrees'.format(mintemp),
          '\n\tPressure: {}'.format(pressure),
          '\n\tHumidity: {}%'.format(humidity), '\n')


# Converts Kelvin to Celcius
# Prints weather details using Celsius labels
def celsiusdisplay(dict, list, city):
    for key, val in dict.items():
        if key.startswith('temp') or key.startswith('feels'):
            val = int(val)
            cel = int(val - 273.15)
            list.append(cel)
        else:
            list.append(val)
    currenttemp = list[0]
    feelslike = list[1]
    mintemp = list[2]
    maxtemp = list[3]
    pressure = list[4]
    humidity = list[5]
    print('The temperature in {} is currently {} degrees Celsius. '
          '\nHere are some other stats...'.format(city, currenttemp))
    print('\tFeels like: {} degrees'.format(feelslike),
          '\n\tHigh: {} degrees'.format(maxtemp),
          '\n\tLow: {} degrees'.format(mintemp),
          '\n\tPressure: {}'.format(pressure),
          '\n\tHumidity: {}%'.format(humidity), '\n')


# Allows the user to run the program as many times as they would like
def run_again():
    runagain = input('Would you like to lookup the weather in a different location?\n'
                     '\tType yes or no: ')
    runagain = runagain.lower()
    if runagain == 'yes':
        print('\n')
        main()
    elif runagain == 'no':
        print('\n')
        print('Thank you for using the weather app today! Have a nice day')
    else:
        print('Invalid entry.Try again.\n')
        run_again()


if __name__ == '__main__':
    main()
