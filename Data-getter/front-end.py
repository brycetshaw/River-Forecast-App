import requests


def main():
    host = 'localhost'
    port = 5000
    url = f"http://{host}:{port}/get-data"

    params = {'data_group': "SPILLIMACHEEN RIVER NEAR SPILLIMACHEEN", 'start_time': '2020-02-15 19:00:00',
              'start_time': '2020-02-19 17:00:00'}

    r = requests.get(url, params)


# server_return = request.post(
#     server_ip,
#     headers=headers,
#     data=json.dumps(event_data)
# )


if __name__ == '__main__':
    main()
