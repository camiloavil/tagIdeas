# from fastapi.testclient import TestClient
# from app.app import app

# # client = TestClient("app.app:app")
# client = TestClient(app)

# prefix = "data/"
# api_routes = [
#     'get_user_data',
#     'get_investments',
#     'add_investment',
#     'add_order/BTC',
#     ]

# def test_routes():
#     print("Testing routes")
#     for route in api_routes:
#         response = client.get(prefix + route)
#         print(f"{prefix}{route} - {response.status_code}")
#         assert response.status_code != 404