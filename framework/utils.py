
import base64

async def filter_deck_code(deck_code):
    # iterate on deck_code as word separated by space to find a base64 code starting with AA
    for word in deck_code.split():
        if word[:2] == "AA":
            try:
                base64.b64decode(word)
            except (ValueError, LookupError):
                continue
            return word

async def filter_account(account):
    return account.split('#')[0]
