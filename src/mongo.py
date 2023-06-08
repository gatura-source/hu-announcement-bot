from motor.motor_asyncio import AsyncIOMotorClient


class DepartmentDatabase:
    CONNECTION_STRING: str

    def __init__(self, connection_string: str):
        self.CONNECTION_STRING = connection_string
        pass

    def __fetch_collection(self) -> AsyncIOMotorClient:
        client = AsyncIOMotorClient(self.CONNECTION_STRING)
        db = client['hu-announcement-db']
        collection = db['announcements']
        return collection

    async def find(self, department_id: str) -> list[dict]:
        collection = self.__fetch_collection()
        document = await collection.find_one({'department_id': department_id})

        if not document:
            await collection.insert_one({'department_id': department_id, 'announcement_list': []})
            return []

        return document['announcement_list']

    async def update(self, department_id: str, announcement_list: list[dict]) -> None:
        collection = self.__fetch_collection()
        await collection.find_one_and_update({'department_id': department_id},
                                             {'$set': {'announcement_list': announcement_list}})


class UserDatabase:
    CONNECTION_STRING: str

    def __init__(self, connection_string: str):
        self.CONNECTION_STRING = connection_string

    def __fetch_collection(self) -> AsyncIOMotorClient:
        client = AsyncIOMotorClient(self.CONNECTION_STRING)
        db = client['hu-announcement-db']
        collection = db['user_configs']
        return collection

    async def new_user(self, user_id: int, first_name: str, last_name: str, default_departments: list[str],
                       language: str = "tr", holiday_mode: bool = False, dnd: bool = False) -> dict:
        collection = self.__fetch_collection()
        user = {
            'user_id': user_id,
            'first_name': first_name,
            'last_name': last_name,
            'departments': default_departments,
            'language': language,
            'dnd': dnd,
            'holiday_mode': holiday_mode
        }
        await collection.insert_one(user)
        return user

    async def find(self, user_id: int) -> dict:
        collection = self.__fetch_collection()
        return await collection.find_one({'user_id': user_id})

    async def find_all(self) -> list[int]:
        user_configs = self.__fetch_collection()
        users_cursor = user_configs.find({})
        user_list = await users_cursor.to_list(None)  # ChatGPT wrote here, I'm not sure why await find() didn't work
        user_id_list = [user['user_id'] for user in user_list]
        return user_id_list

    async def toggle_language(self, user_id: int, langauge: str) -> None:
        collection = self.__fetch_collection()
        await collection.find_one_and_update({'user_id': user_id},
                                             {'$set': {'language': langauge}})

    async def toggle_dnd(self, user_id: int) -> None:
        collection = self.__fetch_collection()
        await collection.find_one_and_update({'user_id': user_id},
                                             [{'$set': {'dnd': {'$not': '$dnd'}}}])

    async def toggle_holiday_mode(self, user_id: int) -> None:
        collection = self.__fetch_collection()
        await collection.find_one_and_update({'user_id': user_id},
                                             [{'$set': {'holiday_mode': {'$not': '$holiday_mode'}}}])

    async def update_subscriptions(self, user_id: int, departments: list[str]) -> None:
        user_configs = self.__fetch_collection()
        await user_configs.find_one_and_update({'user_id': user_id},
                                               {'$set': {'departments': departments}})

    async def get_subscribers(self, department_name: str) -> list[dict]:
        user_configs = self.__fetch_collection()
        users_cursor = user_configs.find({'departments': department_name, 'holiday_mode': False})
        user_list = await users_cursor.to_list(None)  # ChatGPT wrote here, I'm not sure why await find() didn't work
        return user_list