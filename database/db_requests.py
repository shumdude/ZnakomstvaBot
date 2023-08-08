from typing import Any
from .models import Profile


async def add_profile(user_id: int, name: str, age: int, info: str, telegram_id: str):
    return await Profile.create(user_id=user_id,
                                name=name,
                                age=age,
                                info=info,
                                telegram_id=telegram_id)


async def get_profile_by_id(user_id: int):
    return await Profile.get_or_none(user_id=user_id)


async def get_profile_by_offset(offset: int):
    return await Profile.all().offset(offset).limit(1).first()


async def get_offset_by_id(user_id: int):
    return await Profile.get_or_none(user_id=user_id).values_list("offset", flat=True)


async def edit_profile_by_id(user_id: int, data: dict[str, Any]):
    profile: Profile = await Profile.get_or_none(user_id=user_id)
    if data["offset"]:
        profile.offset = data["offset"]
    return await profile.save()


async def get_profile_list_length():
    return await Profile.all().count()
