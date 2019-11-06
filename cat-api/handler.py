import json
import urllib.parse
import requests

CAT_API = "https://api.thecatapi.com/images/search?mime_types=gif"


def handle(req):
    slash_command = urllib.parse.parse_qs(req)
    try:
        r = requests.get("{}".format(CAT_API))
        if r.status_code == 200:
            url = r.json()[0]['url']
            requests.post(slash_command['response_url'][0],
                          json.dumps({
                              "response_type": "in_channel",
                              "replace_original": False,
                              "text": "CATS...",
                              "attachments": [
                                  {
                                      "fallback": "cats",
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
        return requests.get("{}".format(CAT_API)).json()[0]['url']
