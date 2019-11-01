import json
import urllib.parse
import requests

API = "https://icanhazdadjoke.com/slack"


def handle_inbound(resp):
    return resp.json()['attachments'][0]['text']


def handle(req):
    slash_command = urllib.parse.parse_qs(req)
    try:
        r = requests.get("{}".format(API))
        if r.status_code == 200:
            url = handle_inbound(r)
            requests.post(slash_command['response_url'][0],
                          json.dumps({
                              "response_type": "in_channel",
                              "replace_original": False,
                              "text": "",
                              "attachments": [
                                  {
                                      "fallback": "jokes...",
                                      "text": url
                                  }
                              ],
                              "unfurl_media": "true",
                              "unfurl_links": "true"
                          }), headers={"Content-Type": "application/json"})
        else:
            return "Sorry something awful went wrong."
    except requests.exceptions.Timeout:
        return "Sorry, the server is taking too long to respond"
    except requests.exceptions.RequestException as e:
        return "Sorry something awful went wrong." + str(e)

