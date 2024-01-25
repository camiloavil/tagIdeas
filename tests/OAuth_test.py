import httpx
import pytest

# from fastapi import status
import webbrowser
"""
"""

URL_BASE = 'https://tagideas.camiloavil.com'

@pytest.fixture(scope="function")
async def simple_client() -> httpx.AsyncClient:
  print("simple client Started")
  async with httpx.AsyncClient(base_url=URL_BASE) as client:
    yield client
  print("simple client Finished")

@pytest.mark.asyncio
async def test_get(simple_client: httpx.AsyncClient):
  response = await simple_client.get('/auth/google/authorize')
  assert response.status_code == 200
  authorization_url = response.json()['authorization_url']
  chrome_response = webbrowser.open(authorization_url)
  print(chrome_response)
  print(authorization_url)
  print(response.json())
  # assert response.json() == {"message": "Hello!"}
