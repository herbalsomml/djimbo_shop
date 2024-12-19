# - *- coding: utf- 8 - *-
import asyncio
import json
from io import BytesIO
from typing import Union

import ujson
from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiohttp import ClientConnectorCertificateError, FormData

from tgbot.database import Settingsx
from tgbot.utils.const_functions import gen_id, send_errors
from tgbot.utils.misc.bot_models import ARS
from tgbot.utils.misc_functions import send_admins


class DiscordAPI:
    def __init__(
            self,
            bot: Bot,
            arSession: ARS,
            update: Union[Message, CallbackQuery] = None,
            webhook_url: str = None,
            skipping_error: bool = False,
    ):
        if webhook_url is not None:
            webhook_url = webhook_url
        else:
            get_settings = Settingsx.get()

            webhook_url = get_settings.misc_discord_webhook_url

        if webhook_url.startswith("https://discord.com/api/"):
            webhook_url = webhook_url[33:]
        if webhook_url.startswith("discord.com/api/webhooks/"):
            webhook_url = webhook_url[25:]

        self.bot = bot
        self.arSession = arSession
        self.update = update
        self.skipping_error = skipping_error

        self.webhook_username = "Djimbo Shop | Free Bot"
        self.base_url = "https://djimbo.dev/dsapi"

        if "/" in webhook_url:
            self.webhook_id = webhook_url.split("/")[0]
            self.webhook_token = webhook_url.split("/")[1]
        else:
            self.webhook_id = ""
            self.webhook_token = ""

    # Рассылка админам о нерабочем вебхуке
    async def error_account_admin(self, error_code: str = "Unknown"):
        if not self.skipping_error:
            await send_admins(
                self.bot,
                f"<b>🖼 Дискорд вебхук недоступен. Как можно быстрее его замените</b>\n"
                f"❗️ Ошибка: <code>{error_code}</code>"
            )

    # Проверка вебхука
    async def check(self) -> tuple[bool, str]:
        request_url = f"{self.base_url}/webhooks/{self.webhook_id}/{self.webhook_token}"

        status, response = await self._request(
            request_url=request_url,
            request_method="GET",
        )

        if status and "channel_id" in response:
            discord_channel_id = response['channel_id']
            discord_hook_name = response['name']

            return True, discord_hook_name

        return False, ""

    # Загрузка фотографий
    async def upload_photo(self, photo_data: Union[BytesIO, bytes], photo_name: str = None) -> tuple[bool, str]:
        request_url = f"{self.base_url}/webhooks/{self.webhook_id}/{self.webhook_token}"

        if photo_name is None:
            photo_name = str(gen_id(24))

        if not photo_name.endswith(".png") or not photo_name.endswith(".jpg"):
            photo_name = f"{photo_name}.png"

        send_json = {
            'username': self.webhook_username,
            'content': '',
        }

        data = FormData()
        data.add_field('file', photo_data, filename=photo_name)
        data.add_field('payload_json', ujson.dumps(send_json))

        await asyncio.sleep(1)
        status, response = await self._request(
            request_url=request_url,
            request_method="POST",
            request_data=data,
        )

        if "id" in response:
            channel_id = response['channel_id']
            message_id = response['id']

            get_discord_forevercdn = await (
                DiscordDJ(
                    arSession=self.arSession,
                    bot=self.bot,
                )
            ).export_forevercdn()

            photo_url = f"{get_discord_forevercdn}/attachments/{channel_id}/{message_id}"

            return True, photo_url

        return False, "None"

    # Запрос
    async def _request(
            self,
            request_url: str,
            request_method: str,
            request_data: Union[dict, FormData] = None,
    ) -> tuple[bool, any]:
        session = await self.arSession.get_session()

        await asyncio.sleep(1)

        try:
            response = await session.request(
                method=request_method,
                url=request_url,
                data=request_data,
                headers={},
                ssl=False,
            )

            response_data = json.loads((await response.read()).decode())

            if response.status == 200:
                return True, response_data
            else:
                await self.error_account_admin(f"{response.status} - {str(response_data)}")

                return False, response_data
        except ClientConnectorCertificateError:
            await self.error_account_admin("CERTIFICATE_VERIFY_FAILED")

            return False, "CERTIFICATE_VERIFY_FAILED"
        except Exception as ex:
            await self.error_account_admin(str(ex))

            return False, str(ex)


# Извлечение ссылок для работы с локальным АПИ дискорда
class DiscordDJ:
    def __init__(self, arSession: ARS, bot: Bot):
        self.arSession = arSession
        self.bot = bot

        self.const_url = "https://djimbo.dev/autoshop_discord.json"

    # Экспорт публичного дискорд вебхука
    async def export_webhook(self) -> str:
        session = await self.arSession.get_session()

        try:
            response = await session.get(
                self.const_url,
                ssl=False,
            )
            response_data = json.loads((await response.read()).decode())
        except Exception as ex:
            await send_errors(self.bot, 7729051, f"Error getting Discord Webhook - {ex}")
            return "None"
        else:
            return response_data['webhook']

    # Экспорт ссылки на постоянный CDN
    async def export_forevercdn(self) -> str:
        session = await self.arSession.get_session()

        try:
            response = await session.get(
                self.const_url,
                ssl=False,
            )
            response_data = json.loads((await response.read()).decode())
        except Exception as ex:
            await send_errors(self.bot, 7729051, f"Error getting Discord ForeverCDN - {ex}")
            return "None"
        else:
            return response_data['forevercdn']
