
import requests
import logging

import os

API_TOKEN = os.environ['LIFX_API_KEY']


# Replace with your personal LIFX API token
# API_TOKEN = 'c2aae87a2d0a3bb6476370893d71ffa409d6ac07c8fe40c72b69f14d6c5b6dd6'

HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}'
}

BASE_URL = 'https://api.lifx.com/v1'


def get_lights():
    response = requests.get(f'{BASE_URL}/lights/all', headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return []


def toggle_light(id):
    response = requests.post(f'{BASE_URL}/lights/{id}/toggle', headers=HEADERS)
    if response.status_code == 200 or response.status_code == 207:
        result = response.json()
        for r in result['results']:
            if r['status'] != 'ok':
                error_message = f"Error toggling light {r['id']}: {r['status']}"
                logging.error(error_message)
                print(error_message)
        return result
    else:
        print(f"Error: {response.status_code}")
        return None


def set_color(id, color, brightness=None, duration=None):
    payload = {
        'color': color,
    }
    if brightness is not None:
        payload['brightness'] = brightness
    if duration is not None:
        payload['duration'] = duration

    response = requests.put(f'{BASE_URL}/lights/{id}/state', headers=HEADERS, data=payload)
    if response.status_code == 200 or response.status_code == 207:
        result = response.json()
        for r in result['results']:
            if r['status'] != 'ok':
                error_message = f"Error updating light {r['id']} color: {r['status']}"
                logging.error(error_message)
                print(error_message)
        return result
    else:
        print(f"Error: {response.status_code}")
        return None

def main():
    lights = get_lights()
    if not lights:
        print("No lights found.")
        return

    print("Available lights:")
    for i, light in enumerate(lights):
        print(f"{i + 1}. {light['label']} (ID: {light['id']})")

    while True:
        try:
            choices = input("Enter the light numbers to control (space-separated) or 0 to exit: ").split()
            if len(choices) == 1 and choices[0] == '0':
                break

            selected_lights = []
            for choice in choices:
                if 0 < int(choice) <= len(lights):
                    selected_lights.append(lights[int(choice) - 1])
                else:
                    print(f"Invalid choice: {choice}. Skipping.")
            
            if not selected_lights:
                print("No valid lights selected. Try again.")
                continue

            print("\nAvailable actions:")
            print("1. Toggle")
            print("2. Edit Color")

            action = int(input("Enter the action number or 0 to go back: "))
            if action == 1:
                for light in selected_lights:
                    result = toggle_light(light['id'])
                    if result:
                        print(f"{light['label']} toggled.")
            elif action == 2:
                new_color = input("Enter new color (e.g. red, green, blue, #FF00FF): ")
                brightness = float(input("Enter new brightness (0.0 to 1.0): "))
                duration = float(input("Enter transition duration in seconds: "))
                for light in selected_lights:
                    result = set_color(light['id'], new_color, brightness, duration)
                    if result:
                        print(f"{light['label']}'s color updated.")
            elif action == 0:
                continue
            else:
                print("Invalid action. Try again.")
        except ValueError:
            print("Invalid input. Try again.")


