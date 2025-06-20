from pocketbase import PocketBase

class BeszelApiClient:
    def __init__(self, url, username, password):
        self._url = url.rstrip("/")
        self._username = username
        self._password = password
        self._client = None

    def login(self):
        self._client = PocketBase(self._url)
        self._client.collection("users").auth_with_password(self._username, self._password)

    def get_systems(self):
        records = self._client.collection("systems").get_full_list()
        return records