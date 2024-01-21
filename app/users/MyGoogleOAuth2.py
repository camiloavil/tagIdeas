from typing import Dict, Any, cast
from httpx_oauth.errors import GetIdEmailError
from httpx_oauth.clients.google import GoogleOAuth2, PROFILE_ENDPOINT

class MyGoogleOAuth2(GoogleOAuth2):
  def __init__(self,
               client_id: str,
               client_secret: str,
               ):
    super().__init__(client_id, client_secret)

  async def get_OAuth_info(self, token: str) -> Dict[str, Any]:
    print("Getting OAuth info")
    async with self.get_httpx_client() as client:
      response = await client.get(
        PROFILE_ENDPOINT,
        params={"personFields": "names,photos"},
        headers={**self.request_headers, "Authorization": f"Bearer {token}"},
      )

      if response.status_code >= 400:
        raise GetIdEmailError(response.json())
      data = cast(Dict[str, Any], response.json())
      print(data)

      first_name, last_name = next(
        (name.get('givenName'), name.get('familyName')) #displayName
        for name in data["names"]
        if name["metadata"]["primary"]
      )
      photo_url = next(
        photo["url"] for photo in data["photos"] if photo["metadata"]["primary"]
      )

      return {"first_name": first_name, "last_name": last_name, "photo_url": photo_url}
