## Email settings
## Change these values, then save as 'settings.py' to get started.

auth_key_mg = 'key-1234'  # your Mailgun API key
domain = 'sandbox12345.mailgun.org'
  # domain to send pings from (I use my Mailgun sandbox domain)
bot_email = 'zeno@sandbox12345.mailgun.org'  # bot email address
my_email = 'your@email.com'  # where you want to receive the reminders

# Some defaults
rate = 0.5  # Zeno sequence rate parameter, where Zeno sequence ==
             # deadline - timeframe * p ^ range(N)
Nmax = 20  # cap on the number of emails per reminder
dmax = 120  # max seconds before deadline the last reminder is sent