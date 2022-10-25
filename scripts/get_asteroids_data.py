import requests
import json
import os
from datetime import datetime, timedelta

ASTEROIDS_URL = os.getenv('ASTEROIDS_URL', None)
ASTEROIDS_API_KEY = os.getenv('ASTEROIDS_API_KEY', None)
DATE_FORMAT = '%Y-%m-%d'


def get_asteroids(start_date = '2021-10-17'):
  start_date = datetime.strptime(start_date, DATE_FORMAT) if start_date else datetime.today()
  end_date = start_date + timedelta(days=7) if start_date else datetime.today()

  while start_date < datetime.today():
    FULL_URL = f'{ASTEROIDS_URL}?start_date={start_date.strftime(DATE_FORMAT)}&end_date={end_date.strftime(DATE_FORMAT)}&ASTEROIDS_API_KEY={ASTEROIDS_API_KEY}'
    response = requests.get(FULL_URL)

    try:
        with open(f'asteroids_{start_date.strftime(DATE_FORMAT)}.ndjson', 'w') as ndjson_file:
            asteroids_data = json.loads(response.text)
            near_earth_objects = asteroids_data.get('near_earth_objects', {})
            for date, objects in near_earth_objects.items():
                for object in objects:
                    close_approach_data = object.get('close_approach_data', None)
                    if close_approach_data:
                        close_approach_to_earth_data = close_approach_data[0]

                        object_data = {
                            "date": date,
                            "id": object.get('id'),
                            "nasa_jpl_url": object.get('nasa_jpl_url'),
                            "absolute_magnitude_h": float(object.get('absolute_magnitude_h')),
                            "kilometers_per_second": float(close_approach_to_earth_data.get('relative_velocity', {}).get('kilometers_per_second', 0.0)),
                            "orbiting_body": 'Earth'
                        }
                        ndjson_file.write(f'{json.dumps(object_data)}\n')
        start_date = start_date + timedelta(days=7)
        end_date = start_date + timedelta(days=7)
    except Exception as e:
        print(f'Error: {e}')
        raise e


if __name__ == '__main__':
    get_asteroids()