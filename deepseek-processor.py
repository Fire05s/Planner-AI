import requests


API_KEY = 'KEY'


class APIException(Exception):
    # exception for calls related to DeepSeek's API
    pass


def ask_model(api_key: str, query: str) -> str | None:
    # given the user's API key and query, get DeepSeek's response
    API_URL = 'https://openrouter.ai/api/v1/chat/completions'

    # define the headers for the API request
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # initialize the data sent to DeepSeek
    data = {
        "model": "deepseek/deepseek-chat:free",
        "messages":[{"role":"system", "content": "You are very curt and only ever speak a few words. Use as few words as possible when replying."},
                    {"role": "user", "content": query}]
    }

    # send the data to DeepSeek
    response = requests.post(API_URL, json = data, headers = headers)

    # return the response if the API call succeeded; otherwise, raise an exception
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise APIException("Failed to fetch data from API. Status Code: " + str(response.status_code))



if __name__ == "__main__":
    while True:
        msg = input("Send message: ")

        if msg == 'q':
            break

        try:
            print(ask_model(API_KEY, msg))
        except APIException as e:
            print(e)