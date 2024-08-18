import logging

import requests


logger = logging.getLogger(__name__)


def get_ngrok_url() -> str:
    ngrok_url = ""
    try:
        response = requests.get("http://host.docker.internal:4040/api/tunnels")
        if response.status_code == 200:
            data = response.json()
            if data["tunnels"]:
                ngrok_url = data["tunnels"][0]["public_url"]
                logger.info(f"Ngrok was set. Url: {ngrok_url}")
            else:
                logger.warning("No tunnels found.")
        else:
            logger.warning(f"Failed to get tunnels: {response.status_code}")
        return ngrok_url
    except requests.exceptions.ConnectionError:
        logger.warning("Ngrok wasn't set.")
