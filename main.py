import time
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


DISCORD_WEBHOOK_URL = 'Your discord webhook url'


URL = 'https://www.mako.co.il/Collab/amudanan/alerts.json'


TRIGGER_PHRASES = ["region1", "region2"]


previous_data = []

def send_discord_alert(alert_message, thumbnail_url=None):
    embed = {
        "title": "Alert",
        "description": alert_message,
        "footer": {
            "text": "Made By Hatol"
        }
    }

    if thumbnail_url:
        embed["thumbnail"] = {
            "url": thumbnail_url
        }

    payload = {
        'embeds': [embed]
    }

    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code != 204:
        print(f"Failed to send alert to Discord. Status code: {response.status_code}")
        print(f"Response content: {response.text}")

def main():
    global previous_data

    response = requests.get(URL, verify=False)
    if response.status_code == 200:
        content = response.json()
        
        current_data = list(dict.fromkeys(content.get('data', [])))

        if any(any(phrase in item.lower() for phrase in TRIGGER_PHRASES) for item in current_data):
            alert_message = "Warning: Trigger phrase detected in the data."
            print(alert_message)
            send_discord_alert(alert_message)
            return

        differences = [item for item in current_data if item not in previous_data]

        if differences and current_data:
            alert_message = '\n'.join(differences)
            thumbnail_url = ""   
            print(alert_message)
            send_discord_alert(alert_message, thumbnail_url)
            previous_data = current_data.copy()

    else:
        print(f"Error: Received status code {response.status_code}")

if __name__ == '__main__':
    while True:
        try:
            main()
            time.sleep(1)
        except Exception as e:
            print(f"Error occurred: {e}. Restarting in 5 seconds...")
            time.sleep(5)
