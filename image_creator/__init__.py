from enum import Enum
from .card_counter import count_cards
from .cards_downloader import download_cards
from .cards_placer import place_cards
from .cost_getter import get_cost_of_deck
from .deck_retriever import retrieve_deck
from .rank_retriever import get_rank_data_range
from .rank_placer import place_rank_in_image


async def create_deck_picture(deck_code):
    try:
        response, deck_class, sideboard, icone = await retrieve_deck(deck_code)
    except Exception as e:
        print(e)
        return None
    if response == 0:
        return None

    await download_cards(response["cards"] + sideboard + icone)
    counters, mana = await count_cards(response["cards"])

    cost = await get_cost_of_deck(response["cards"] + sideboard)

    image = await place_cards(counters, mana, deck_class, cost, response, sideboard, icone)

    return image

async def create_rank_picture(account):
    data = await get_rank_data_range(account)
    if not data:
        return
    return await place_rank_in_image(account, data)


class ImageCreatorFunction(Enum):
    CREATE_DECK_PICTURE = create_deck_picture
    CREATE_RANK_PICTURE = create_rank_picture
