import requests
import time
import os
from datetime import datetime, timedelta

TINYBIRD_URL = os.getenv('TINYBIRD_URL', None)
TINYBIRD_TOKEN = os.getenv('TINYBIRD_TOKEN', None)
ASTEROIDS_DATASOURCE_NAME = os.getenv('ASTEROIDS_DATASOURCE_NAME', None)
DATE_FORMAT = '%Y-%m-%d'

def save_asteroids(start_date = '2021-11-14'):
  start_date = datetime.strptime(start_date, DATE_FORMAT) if start_date else datetime.today()

  while start_date <= datetime.today():
      try:
          with open(f'asteroids_{start_date.strftime(DATE_FORMAT)}.ndjson', 'rb') as asteroids_file:
              url = f'{TINYBIRD_URL}?name={ASTEROIDS_DATASOURCE_NAME}&mode=append&format=ndjson&token={TINYBIRD_TOKEN}'
              response = requests.post(url, data=asteroids_file)
              print(f'** asteroids_{start_date.strftime(DATE_FORMAT)}: {response.status_code}')
          time.sleep(10)
      except Exception as e:
          print(f'Error: {e}')
          raise e

      start_date = start_date + timedelta(days=7)

if __name__ == '__main__':
    save_asteroids()
