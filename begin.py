import pip._vendor.requests as requests

# Making a GET request
r = requests.get('https://www.googleapis.com/calendar/v3/users/me/calendarList')
if r.status_code != 200:
    print("Error: Unsuccessful request\n")


# check status code for response received
# success code - 200
print(r)

# print content of request
print(r.content)
print("\nDone\n")
