
import requests

r = requests.post(
                # here goes your Base API URL
                "https://api.mailgun.net/v3/sandbox9d568c62a07a45b79b02eeb2189772e5.mailgun.org/messages",

                # Authentication part - A Tuple
                auth=("api", "9b8ff4bf62a246c0d9362a5731db2e08-07e2c238-2acae694"),

                # mail data will be used to send emails
                data={
                    "from":"bot@sandbox9d568c62a07a45b79b02eeb2189772e5.mailgun.org",
                    "to":["prabinbastakoti1@gmail.com"],
                    "subject":"Testing some awesomeness of Mailgun",
                    "text":"Mailgun Test."
                    })

print(r.status_code)