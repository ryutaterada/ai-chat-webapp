import requests


def send_text_data(txt):
    print(f"API received: {txt}")
    # url = "http://127.0.0.1:8000"
    url = "http://chatapi:8000"
    params = {"txt": txt}
    response = requests.get(url, params=params)
    print(f"API response: {response.text}")
    return response.json()
