from libs.ShivaApi import Iam

# Init clients
shiva_iam_client = Iam(url="https://shiva.cloud-temple.com",
                       token_id="",
                       token_secret="")

# Show all Virtual machine
users_list = shiva_iam_client.get_users()

for user in users_list:
    print(user)
