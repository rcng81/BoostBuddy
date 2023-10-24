import requests


def get_daily_quote():
  response = requests.get("https://zenquotes.io/api/random")
  if response.status_code == 200:
    # The API returns data in JSON format, so you need to parse the response.
    data = response.json()
    quote = data[0]['q']  # The quote text itself
    author = data[0]['a']  # The author of the quote
    return f'`"{quote}" - {author}`'
  else:
    return "Sorry, I couldn't retrieve a quote at this time!"


# Test the function
#print(get_daily_quote())