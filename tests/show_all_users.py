from libs.ShivaApi import Iam

# Init clients
shiva_iam_client = Iam(url="https://shiva.cloud-temple.com",
                       token_id="74175d17-df60-4621-918b-ecd01a7a2c43",
                       token_secret="b7fd8f84-6d30-4496-90fd-7f2c0df531a4")



# Show all Virtual machine
users_list = shiva_iam_client.get_users()

for user in users_list:
    print(user)
