import asyncio
import json
import os

import requests
from dotenv import load_dotenv

from src.batch.batch import Batch
from src.models.tweet import Tweet
from src.observers.log_observer import LogObserver
from src.observers.post_batch_observer import PostBatchObserver

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

load_dotenv()

bearer_token = os.getenv('BEARER_TOKEN')


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    params = {"expansions": "author_id"}
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print("get_rules")
    print(json.dumps(response.json(), indent=4), end="\n\n")
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print("delete_all_rules")
    print(json.dumps(response.json(), indent=4), end="\n\n")
    return response.json()


def set_rules(delete):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "@elonmusk", "tag": "mentionmusk", "expansions": "author_id"},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print("set_rules")
    print(json.dumps(response.json(), indent=4), end="\n\n")


async def get_stream(rules):
    tweet_fields = "?tweet.fields=author_id"
    response = requests.get(
        f"https://api.twitter.com/2/tweets/search/stream{tweet_fields}", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    batch = Batch(limit=10)
    batch.attach_observers(LogObserver())
    batch.attach_observers(PostBatchObserver())
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            tweet = Tweet(author_id=json_response["data"]["author_id"], tweet_id=json_response["data"]["id"])
            batch = await batch.add(tweet)


async def main():
    rules = get_rules()
    delete = delete_all_rules(rules)
    rules = set_rules(delete)
    await get_stream(rules)


if __name__ == "__main__":
    asyncio.run(main())
