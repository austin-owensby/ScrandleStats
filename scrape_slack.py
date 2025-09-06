from http.client import HTTPResponse
import json
import re
from urllib import request, parse

# Set me based on your organization's name that appears in the url
organization = ""

# Set me based to the Slack channel id
channel = ""

# Set me based on the cookie that appears in your request headers
cookie = ""

# Set me based on the token that appears in the request's form data
token = ""

route = f"https://{organization}.slack.com/api/conversations.history"
headers = {
    "Cookie": cookie
}

has_data = True
cursor = None

# Iterate over data from Slack
while has_data:
    request_body = {
        "token": token,
        "channel": channel
    }

    if cursor is not None:
        request_body["cursor"] = cursor

    request_object = request.Request(route, data=parse.urlencode(request_body).encode(), headers=headers)
    
    response: HTTPResponse
    with request.urlopen(request_object) as response:
        response_string = response.read().decode()
        response_json = json.loads(response_string)

        for message in response_json["messages"]:
            # We only care about messages that post a score which I'm defining as having these specific red or green block emojis
            if ":large_green_square:" in message["text"] or ":large_red_square:" in message["text"]:
                # Get the specific rating in the format of 8/10 or 10/10
                regex_result = re.search("(\\d{1,2})\\/10", message["text"])

                if regex_result is None:
                    # We were expecting to find a score but didn't, log out this message to handle special cases manually
                    print(message["ts"], message["text"])
                    continue

                score = regex_result.group(1)

                # This could be more efficient with a single write instead of on each loop, but it's a one off short running script so I'm not worrying about it
                with open("slack.csv", "a") as f:
                    f.write(f"{message["ts"]},{score}\n")

        # Keep parsing as long as we have data
        has_data = response_json["has_more"]

        if has_data:
            cursor = response_json["response_metadata"]["next_cursor"]
