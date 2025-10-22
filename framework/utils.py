
import base64
from datetime import date

def filter_deck_code(deck_code):
    # iterate on deck_code as word separated by space to find a base64 code starting with AA
    for word in deck_code.split():
        if word[:2] == "AA":
            try:
                base64.b64decode(word)
            except (ValueError, LookupError):
                continue
            return word

def filter_account(account):
    return account.split('#')[0]

def get_season_id():
    reference_date = date(year=2022, month=10, day=1)
    reference_season = 108
    current_date = date.today()
    # Calculate the number of months that have passed since the reference date
    months_since_reference = (current_date.year - reference_date.year) * 12 + current_date.month - reference_date.month
    # Calculate the season ID based on the number of months elapsed
    current_season = reference_season + months_since_reference
    return current_season
