
import requests

r = requests.post(
                # here goes your Base API URL
                "https://api.mailgun.net/v3/sandbox9d568c62a07a45b79b02eeb2189772e5.mailgun.org/messages",

                # Authentication part - A Tuple
                auth=("api", "key-c7991841f928ef2c6f73706ff5ead2d5"),

                # mail data will be used to send emails
                data={
                    "from":"bot@sandbox9d568c62a07a45b79b02eeb2189772e5.mailgun.org",
                    "to":["prabinbastakoti1@gmail.com"],
                    "subject":"Testing some awesomeness of Mailgun",
                    "text":"Mailgun Test."
                    })

print(r.status_code)