import urllib.parse
import requests
import json

DOG_API = "https://dog.ceo/api/breeds/image/random"


def handle(req):
    slash_command = urllib.parse.parse_qs(req)
    try:
        r = requests.get("{}".format(DOG_API))
        if r.status_code == 200:
            url = r.json()['message']
            requests.post(slash_command['response_url'][0],
                          json.dumps({
                              "response_type": "in_channel",
                              "replace_original": False,
                              "text": "NOT CATS...",
                              "attachments": [
                                  {
                                      "fallback": "not cats",
                                      "image_url": url
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
    except KeyError:
        return requests.get("{}".format(DOG_API)).json()[0]['url']
