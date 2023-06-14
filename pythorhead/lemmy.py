import requests
from loguru import logger

class Lemmy:

    auth_token = None
    api_base_url = None

    def __init__(self, api_base_url):
        self.api_base_url = api_base_url


    def log_in(self, username_or_email, password):
        payload = {
            "username_or_email": username_or_email,
            "password": password
        }
        try:
            re = requests.post(f"{self.api_base_url}/api/v3/user/login", json=payload)
            self.auth_token = re.json()["jwt"]
        except Exception as err:
            logger.error(f"Something went wrong while logginf in as {username_or_email}: {err}")
            return False
        return True

    def discover_community(self, community_name):
        try:
            req = requests.get(f"{self.api_base_url}/api/v3/community?name={community_name}")
            community_id = req.json()["community_view"]["community"]["id"]
        except Exception as err:
            logger.error(f"Error when looking up community '{community_name}': {err}")
            return None
        return community_id

    def post(self, community_id, post_name, post_url = None, post_body = None):
        new_post = {
            "auth": self.auth_token,
            "community_id": community_id,
            "name": post_name,
        }
        if post_url:
             new_post["url"] = post_url
        if post_body:
             new_post["body"] = post_body
        re = requests.post(f"{self.api_base_url}/api/v3/post", json=new_post)
        return re.ok