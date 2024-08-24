import requests


def send_text_data(txt):
    # APIのURLを設定
    # ローカルホスト用のURL
    # url = "http://127.0.0.1:8000"
    # Dockerコンテナ内のサービス用のURL
    url = "http://chatapi:8000"

    # パラメータを設定
    params = {"txt": txt}
    try:
        print(f"API Request: {params}")

        # GETリクエストを送信
        response = requests.get(url, params=params)

        # HTTPエラーが発生した場合に例外を発生させる
        response.raise_for_status()

        print(f"API Response: {response.text}")

        # レスポンスをJSON形式で返す
        return response.json()

    # 各種例外処理
    except requests.exceptions.HTTPError as http_err:
        # HTTPエラーが発生した場合の処理
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        # 接続エラーが発生した場合の処理
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        # タイムアウトエラーが発生した場合の処理
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        # その他のリクエストエラーが発生した場合の処理
        print(f"An error occurred: {req_err}")
    return None
