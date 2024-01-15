# import httpx
# import pytest

# from typing import Awaitable, Callable
# from fastapi import status

# """
# Define routes CRUD for testing
# """
# routes_CRUD: dict[str, dict[str, str]] = {
#   "get-all"   : {"method" : "GET",  "route":  "data/get-user-data"},
#   "get-inv"   : {"method" : "GET",  "route":  "data/investments"},
#   "add-inv"   : {"method" : "POST", "route":  "data/investments"},
#   "update-inv": {"method" : "PUT",  "route":  "data/investments"},
#   "delete-inv": {"method" : "DELETE","route": "data/investments"},

#   "add-order"    : {"method" : "POST",  "route": "data/investments/$id_inv$/orders"},
#   "get-order"    : {"method" : "GET",   "route": "data/investments/$id_inv$/orders"},
#   "update-order" : {"method" : "PUT",   "route": "data/investments/$id_inv$/orders/$id_order$"},
#   "delete-order" : {"method" : "DELETE","route": "data/investments/$id_inv$/orders/$id_order$"},
# }

# user_juan = {
#   "name": "Juan Perez",
#   "country": "NoWhere",
#   "timezone": "UTC",
#   "telegram_id": 234543,
#   "email": "juanperez@example.com",
#   "password": "perez123"
# }

# user_marco = {
#   "name": "Marco ramirez",
#   "country": "Here",
#   "timezone": "UTC",
#   "telegram_id": 213121,
#   "email": "marcoramirez@example.com",
#   "password": "ramirez123"
# }

# inves1 = {
#   "name": "Test Name Investment",
#   "comment": "Test Comment",
#   "amount": 0,
#   "crypto": "btc"
# }
# inves2 = {
#   "name": "Test Name Investment",
#   "comment": "Test Comment Etherium",
#   "amount": 1500,
#   "crypto": "eth"
# }
# inves_error1 = {
#   "name": "Test Name Error",
#   "comment": "Error Comment",
#   "amount": 0,
#   "crypto": "bitcoin"
# }
# inves_error2 = {
#   "name": "Test Name Error",
#   "comment": "Error Comment",
#   "amount": -10,
#   "crypto": "eth"
# }

# order1 = {
#   "otype" : "buy",
#   "price" : 35700.0,
#   "amount" : 120.0,
#   "status": 'waiting',
#   "comment": 'Just Buy some BTC when falls again'
# }
# order2 = {
#   "otype" : "buy",
#   "price" : 31000.0,
#   "amount" : 13.0,
#   "status": 'waiting',
#   "comment": 'Just Buy some BTC when falls again'
# }
# order3 = {
#   "otype" : "buy",
#   "price" : 30000.0,
#   "amount" : 20.0,
#   "status": 'waiting',
#   "comment": 'Just Buy some BTC when falls again'
# }
# order4 = {
#   "otype" : "sell",
#   "price" : 40000.0,
#   "amount" : 420.0,
#   "status": 'waiting',
#   "comment": 'Sell BTC before fall again'
# }
# order_error1 = {
#   "otype" : "patience",
#   "price" : 35700.0,
#   "amount" : 120.0,
#   "status": 'waiting',
#   "comment": 'Just Buy some BTC when falls again'
# }
# order_error2 = {
#   "otype" : "sell",
#   "price" : -35700.0,
#   "amount" : 120.0,
#   "status": 'waiting',
#   "comment": 'Just Buy some BTC when falls again'
# }
# order_error3 = {
#   "otype" : "sell",
#   "price" : 35700.0,
#   "amount" : -120.0,
#   "status": 'waiting',
#   "comment": 'Just Buy some BTC when falls again'
# }
# order_error4 = {
#   "otype" : "sell",
#   "price" : 35700.0,
#   "amount" : 120.0,
#   "status": 'enjoy',
#   "comment": 'Just Buy some BTC when falls again'
# }

# GetAuthenticatedAsyncClient = Callable[[dict], Awaitable[httpx.AsyncClient]]


# class Test_CRUD_investments:
#   # def setup_method(self):
#   #   print("Setup Test - add Users and it's Data")

#   # @pytest.mark.asyncio
#   # async def test_setup(self, client_auth: GetAuthenticatedAsyncClient):
#   #   client_user_auth_juan = await client_auth(user_juan)

#   @pytest.mark.asyncio
#   @pytest.mark.parametrize(
#     "user,data,status_code",
#     [
#       (user_juan,{}, status.HTTP_422_UNPROCESSABLE_ENTITY),
#       (user_juan,inves1, status.HTTP_201_CREATED),
#       (user_juan,inves2, status.HTTP_201_CREATED),
#       (user_juan,inves2, status.HTTP_409_CONFLICT),
#       (user_juan,inves_error1, status.HTTP_422_UNPROCESSABLE_ENTITY),
#       (user_juan,inves_error2, status.HTTP_422_UNPROCESSABLE_ENTITY),
#     ]
#   )
#   async def test_add_investments(self,
#                                 client_auth: GetAuthenticatedAsyncClient,
#                                 user: dict[str, str|int],
#                                 data: dict,
#                                 status_code: status):
#     client_user_auth_juan = await client_auth(user)
#     response = await client_user_auth_juan.request(routes_CRUD["add-inv"]["method"],
#                                                    routes_CRUD["add-inv"]["route"],
#                                                    json=data)
#     response_json :dict = response.json()
#     assert response.status_code == status_code
#     if response.status_code == status.HTTP_201_CREATED:
#       assert response_json["_id"] is not None
#       assert {(data[key] == response_json[key]) for key in data.keys()} == {True}

#   @pytest.mark.asyncio
#   async def test_get_put_investments(self, client_auth: GetAuthenticatedAsyncClient):
#     client_user_auth_juan = await client_auth(user_juan)
#     response = await client_user_auth_juan.request(routes_CRUD["get-inv"]["method"],
#                                                    routes_CRUD["get-inv"]["route"])
#     assert response.status_code == status.HTTP_200_OK
#     response_data: list[dict] = response.json()
#     test_data = [inves1, inves2]
#     for i in range(len(response_data)):
#       assert response_data[i]["_id"] is not None, "ID should not be None"
#       assert {(test_data[i][key] == response_data[i][key]) for key in test_data[i].keys()} == {True}, "Data should be the same"
#     """
#     Now let's change the atributes of the first investment. to test the update route
#     """
#     new_data = response_data.copy()
#     for dat_inv in new_data:
#       dat_inv["name"] += "-add some test"
#       dat_inv["amount"] -= 1000
#       dat_inv["comment"] += "-add some test"
#     """
#     Now let's check if the updated data can be put in the API
#     one of the test data is wrong and should not be updated
#     """
#     for new_investment in new_data:
#       response = await client_user_auth_juan.request(method = routes_CRUD["update-inv"]["method"],
#                                                     url = routes_CRUD["update-inv"]["route"]+f"/{new_investment['_id']}",
#                                                     json=new_investment)
#       response_data_changed :dict = response.json()
#       """
#       Check if the bad update pass or not
#       """
#       if new_investment['amount'] < 0:
#         assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, "Status code should be 422 on Update Investment"
#       else:
#         assert response.status_code == status.HTTP_202_ACCEPTED, "Status code should be 202 on Update Investment"
#         assert {(new_investment[key] == response_data_changed[key]) for key in new_investment.keys()} == {True}, "Data should be the same"
#         assert all(new_investment[key] == response_data_changed[key] for key in new_investment.keys()) # == {True}, "Data should be the same"
#         """
#         Now let's check if the investment is in the database
#         """
#         response_inv = await client_user_auth_juan.request(routes_CRUD["get-inv"]["method"],
#                                                            routes_CRUD["get-inv"]["route"]+f"/{new_investment['_id']}",)
#                                                           #  params=param_query)
#         assert response_inv.status_code == status.HTTP_200_OK
#         assert response_inv.json() == new_investment

#   @pytest.mark.asyncio
#   async def test_put_investment_another_user(self, client_auth: GetAuthenticatedAsyncClient):
#     client_user_auth = await client_auth(user_juan)
#     response = await client_user_auth.request(routes_CRUD["get-inv"]["method"],
#                                               routes_CRUD["get-inv"]["route"])
#     assert response.status_code == status.HTTP_200_OK
#     data_juan = response.json()
#     client_user_auth = await client_auth(user_marco)
#     data_changed_by_marco = [{ **dic, 'name' : ' changed by Marco'}for dic in data_juan]
#     for each_investment in data_changed_by_marco:
#       response = await client_user_auth.request(method = routes_CRUD["update-inv"]["method"],
#                                                       url = routes_CRUD["update-inv"]["route"]+f"/{each_investment['_id']}",
#                                                       json=each_investment)
#       assert response.status_code == status.HTTP_204_NO_CONTENT

#   @pytest.mark.asyncio
#   async def test_delete_investments(self, client_auth: GetAuthenticatedAsyncClient):
#     """ Get all investments and delete them one by one"""
#     authenticated_client = await client_auth(user_juan)
#     response = await authenticated_client.request(method = routes_CRUD["get-inv"]["method"],
#                                                   url = routes_CRUD["get-inv"]["route"])
#     response_json :list[dict] = response.json()
#     assert response.status_code == status.HTTP_200_OK
#     for i in range(len(response_json)):
#       response = await authenticated_client.request(routes_CRUD["delete-inv"]["method"],
#                                                     routes_CRUD["delete-inv"]["route"]+f"/{response_json[i]['_id']}",)
#       assert response.status_code == status.HTTP_202_ACCEPTED
#       assert response.json() == {"status" : "Done"}

# class Test_ordersCRUD:


#   @pytest.mark.asyncio
#   async def test_set_investment(self, client_auth: GetAuthenticatedAsyncClient):
#     authenticated_client = await client_auth(user_juan)
#     """
#     Testing Add Investment
#     """
#     print(inves1)
#     response = await authenticated_client.request(routes_CRUD["add-inv"]["method"],
#                                                   routes_CRUD["add-inv"]["route"],
#                                                   json=inves1)
#     assert response.status_code == status.HTTP_201_CREATED
#     inves1.update({"id": response.json()['_id']})

#   @pytest.mark.asyncio
#   @pytest.mark.parametrize(
#     "order,status_code_answer,description",
#     [
#       (order1, status.HTTP_201_CREATED,"Order Correct"),
#       (order2, status.HTTP_201_CREATED,"Order Correct"),
#       (order_error1, status.HTTP_422_UNPROCESSABLE_ENTITY,"Error1 Order"),
#       (order_error2, status.HTTP_422_UNPROCESSABLE_ENTITY,"Error2 Order"),
#       (order3, status.HTTP_201_CREATED,"Order Correct"),
#       (order4, status.HTTP_201_CREATED,"Order Correct"),
#       (order_error3, status.HTTP_422_UNPROCESSABLE_ENTITY,"Error3 Order"),
#       (order_error4, status.HTTP_422_UNPROCESSABLE_ENTITY,"Error4 Order"),
#     ]
#   )
#   async def test_add_get_orders(self, client_auth: GetAuthenticatedAsyncClient,
#                                 order: dict,
#                                 status_code_answer: status,
#                                 description: str):
#     authenticated_client = await client_auth(user_juan)
#     """
#     Testing Add Order to Investment
#     """
#     print(f"TEST {description}")
#     response = await authenticated_client.request(method = routes_CRUD["add-order"]["method"],
#                                                   url= routes_CRUD['add-order']['route'].replace('$id_inv$', inves1['id']),
#                                                   json=order)
#     assert response.status_code == status_code_answer
#     # print(f"add {order} \nresponse: {response.json()}")
#     if status_code_answer == status.HTTP_201_CREATED:
#       assert all((response.json()[key] == order[key]) for key in order.keys()), "Data should be the same"
#       order.update({"id": response.json()['id']})
#     else:
#       order.update({"id": "SOME_FAKE_ID"})

#     """
#     Testing Get order by id and it's Investment id
#     """
#     response_get = await authenticated_client.request(method = routes_CRUD["get-order"]["method"],
#                                       url = routes_CRUD["get-order"]["route"].replace('$id_inv$', inves1['id'])+f"/{order['id']}",)
#     if status_code_answer == status.HTTP_201_CREATED:
#       assert response_get.status_code == status.HTTP_200_OK
#       assert all((response_get.json()[key] == order[key]) for key in order.keys()), "Data should be the same"
#     else:
#       assert response_get.status_code == status.HTTP_204_NO_CONTENT

#   @pytest.mark.asyncio
#   async def test_getall_put_orders_with_investment(self, client_auth: GetAuthenticatedAsyncClient):
#     authenticated_client = await client_auth(user_juan)
#     """
#     Test Get Orders by quering the Investment
#     """
#     response = await authenticated_client.request(method = routes_CRUD["get-order"]["method"],
#                                                   url = routes_CRUD["get-order"]["route"].replace('$id_inv$', inves1['id']),)
#     assert response.status_code == status.HTTP_200_OK
#     orders_saved = response.json()
#     """
#     Test update Orders changing some values
#     """
#     orders_ids = [order['id'] for order in orders_saved]
#     #### Data is complete on all the keys acording Order_invest_update model
#     orders_saved[0].update({"amount": -100})    #Error Data
#     orders_saved[1].update({"price": -35100})   #Error Data
#     orders_saved[2].update({"comment": "This is a new comment"})   #Correct Data
#     orders_saved[3].update({"amount": 500,"comment": "This is a new comment"})  #Correct Data
#     #### Data is incomplete on some keys
#     orders_saved.append({'id': orders_ids[0],'amount': 500})   #Correct Data
#     orders_saved.append({'id': orders_ids[1],'price': 35220})   #Correct Data
#     states_espected = [status.HTTP_422_UNPROCESSABLE_ENTITY,
#                        status.HTTP_422_UNPROCESSABLE_ENTITY,
#                        status.HTTP_202_ACCEPTED,
#                        status.HTTP_202_ACCEPTED,
#                        status.HTTP_202_ACCEPTED,
#                        status.HTTP_202_ACCEPTED,
#                       ]
#     for i in range(len(orders_saved)):
#       order = orders_saved[i]
#       # print(f"{i+1} -> let's update {order}")
#       response = await authenticated_client.request(method = routes_CRUD["update-order"]["method"],
#                           url = routes_CRUD["update-order"]["route"].replace('$id_inv$', inves1['id']).replace('$id_order$', order['id']),
#                           json = order)
#       # print(f"status code: {response.status_code}")
#       # print(f"response: {response.json()}")
#       assert response.status_code == states_espected[i]
#       if states_espected[i] == status.HTTP_202_ACCEPTED:
#         response = await authenticated_client.request(method = routes_CRUD["get-order"]["method"],
#                                       url = routes_CRUD["get-order"]["route"].replace('$id_inv$', inves1['id'])+f"/{order['id']}",)
#         assert all((response.json()[key] == order[key]) for key in order.keys()), "Data should be the same"

#   @pytest.mark.asyncio
#   async def test_delete_orders(self, client_auth: GetAuthenticatedAsyncClient):
#     authenticated_client = await client_auth(user_juan)
#     """
#     Test Get Orders by quering the Investment
#     """
#     response = await authenticated_client.request(method = routes_CRUD["get-order"]["method"],
#                                                   url = routes_CRUD["get-order"]["route"].replace('$id_inv$', inves1['id']),)
#     assert response.status_code == status.HTTP_200_OK
#     orders_saved = response.json()
#     """
#     Test delete Orders
#     """
#     # orders_ids = [order['id'] for order in orders_saved]
#     for i, order in enumerate(orders_saved):
#       # order = orders_saved[i]
#       print(f"{i+1} -> let's delete {order}")
#       response_del = await authenticated_client.request(method = routes_CRUD["delete-order"]["method"],
#                           url = routes_CRUD["delete-order"]["route"].replace('$id_inv$', inves1['id']).replace('$id_order$', order['id']),)
#       assert response_del.status_code == status.HTTP_202_ACCEPTED
#       response_get = await authenticated_client.request(method = routes_CRUD["get-order"]["method"],
#                           url= routes_CRUD["get-order"]["route"].replace('$id_inv$', inves1['id'])+f"/{order['id']}")
#       print(f"status code: {response_get.status_code}")
#       assert response_get.status_code == status.HTTP_204_NO_CONTENT
