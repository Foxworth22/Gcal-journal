import pip._vendor.requests as requests

# Making a GET request
r = requests.get('https://api.github.com/users/naveenkrnl')
if r.status_code != 200:
    print("Error: Unsuccessful request")


# check status code for response received
# success code - 200
print(r)

# print content of request
print(r.content)
print("\nDone\n")
