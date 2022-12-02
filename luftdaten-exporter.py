#!/usr/bin/python3 -u

import json
import time

import requests
from datetime import datetime
from prometheus_client import start_http_server, Gauge

sensor = Gauge('sensor_community', 'Sensor values of senor.community', ['type', 'id'])

if __name__ == '__main__':
    print("Luftdaten exporter v0.1\n")
    sensor_id = '37895'
    server_port = 3425

    print("Sensor id: " + str(sensor_id))
    print("Port     : " + str(server_port) + "\n")

    start_http_server(server_port)
    while True:
        response = json.loads(requests.get('https://data.sensor.community/airrohr/v1/sensor/' + sensor_id + '/')
                              .content.decode('UTF-8'))

        sorted_response = sorted(response, key=lambda x: datetime.strptime(x['timestamp'], '%Y-%m-%d %H:%M:%S'),
                                 reverse=True)

        sensor_info = sorted_response[0]['sensor']

        for sensor_data in sorted_response[0]['sensordatavalues']:
            sensor.labels(type=sensor_data['value_type'], id=sensor_info['id']).set(sensor_data['value'])

        time.sleep(300)
