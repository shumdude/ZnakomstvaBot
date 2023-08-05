from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from settings import LEXICON

next_button: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON["next"], callback_data="next")
my_info_button: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON["my_info"], callback_data="my_info")
start_search_button: InlineKeyboardButton = InlineKeyboardButton(text=LEXICON["start_search"],
                                                                 callback_data="start_search")

buttons: list[InlineKeyboardButton] = [next_button, my_info_button]

search_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
search_kb_builder.row(*buttons, width=1)
search_kb: InlineKeyboardMarkup = search_kb_builder.as_markup()

start_search_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
start_search_kb_builder.row(start_search_button, width=1)
start_search_kb: InlineKeyboardMarkup = start_search_kb_builder.as_markup()