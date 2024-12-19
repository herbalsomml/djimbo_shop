# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message

from tgbot.database import Settingsx, Userx
from tgbot.keyboards.inline_admin import settings_status_finl, settings_finl
from tgbot.services.api_discord import DiscordDJ, DiscordAPI
from tgbot.utils.const_functions import ded
from tgbot.utils.misc.bot_models import FSM, ARS
from tgbot.utils.misc_functions import send_admins, insert_tags

router = Router(name=__name__)


# Изменение данных
@router.message(F.text == "🖍 Изменить данные")
async def settings_data_edit(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b>🖍 Изменение данных бота</b>",
        reply_markup=settings_finl(),
    )


# Выключатели бота
@router.message(F.text == "🕹 Выключатели")
async def settings_status_edit(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b>🕹 Включение и выключение основных функций</b>",
        reply_markup=settings_status_finl(),
    )


################################################################################
################################## ВЫКЛЮЧАТЕЛИ #################################
# Включение/выключение тех работ
@router.callback_query(F.data.startswith("settings_status_work:"))
async def settings_status_work(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    get_status = call.data.split(":")[1]

    get_user = Userx.get(user_id=call.from_user.id)
    Settingsx.update(status_work=get_status)

    if get_status == "True":
        send_text = "🔴 Отправил бота на технические работы"
    else:
        send_text = "🟢 Вывел бота из технических работ"

    await send_admins(
        bot=bot,
        text=ded(f"""
            👤 Администратор <a href='tg://user?id={get_user.user_id}'>{get_user.user_name}</a>
            {send_text}
        """),
        not_me=get_user.user_id,
    )

    await call.message.edit_reply_markup(reply_markup=settings_status_finl())


# Включение/выключение покупок
@router.callback_query(F.data.startswith("settings_status_buy:"))
async def settings_status_buy(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    get_status = call.data.split(":")[1]

    get_user = Userx.get(user_id=call.from_user.id)
    Settingsx.update(status_buy=get_status)

    if get_status == "True":
        send_text = "🟢 Включил покупки в боте"
    else:
        send_text = "🔴 Выключил покупки в боте"

    await send_admins(
        bot=bot,
        text=ded(f"""
            👤 Администратор <a href='tg://user?id={get_user.user_id}'>{get_user.user_name}</a>
            {send_text}
        """),
        not_me=get_user.user_id,
    )

    await call.message.edit_reply_markup(reply_markup=settings_status_finl())


# Включение/выключение пополнений
@router.callback_query(F.data.startswith("settings_status_pay:"))
async def settings_status_pay(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    get_status = call.data.split(":")[1]

    get_user = Userx.get(user_id=call.from_user.id)
    Settingsx.update(status_refill=get_status)

    if get_status == "True":
        send_text = "🟢 Включил пополнения в боте"
    else:
        send_text = "🔴 Выключил пополнения в боте"

    await send_admins(
        bot,
        f"👤 Администратор <a href='tg://user?id={get_user.user_id}'>{get_user.user_name}</a>\n"
        f"{send_text}",
        not_me=get_user.user_id,
    )

    await call.message.edit_reply_markup(reply_markup=settings_status_finl())


################################################################################
############################### ИЗМЕНЕНИЕ ДАННЫХ ###############################
# Изменение FAQ
@router.callback_query(F.data == "settings_edit_faq")
async def settings_faq_edit(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await state.set_state("here_settings_faq")
    await call.message.edit_text(
        ded("""
            <b>❔ Введите новый текст для FAQ</b>
            ❕ Вы можете использовать заготовленный синтаксис и HTML разметку:
            ▪️ <code>{username}</code>  - логин пользоваля
            ▪️ <code>{user_id}</code>   - айди пользователя
            ▪️ <code>{firstname}</code> - имя пользователя
        """)
    )


# Изменение поддержки
@router.callback_query(F.data == "settings_edit_support")
async def settings_support_edit(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await state.set_state("here_settings_support")
    await call.message.edit_text(
        "<b>☎️ Отправьте юзернейм для поддержки</b>\n"
        "❕ Юзернейм пользователя/бота/канала/чата",
    )


# Изменение отображения/скрытия категорий без товаров
@router.callback_query(F.data.startswith("settings_edit_hide_category:"))
async def settings_edit_hide_category(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    status = call.data.split(":")[1]

    Settingsx.update(misc_hide_category=status)

    await call.message.edit_text(
        "<b>🖍 Изменение данных бота</b>",
        reply_markup=settings_finl(),
    )


# Изменение отображения/скрытия позиций без товаров
@router.callback_query(F.data.startswith("settings_edit_hide_position:"))
async def settings_edit_hide_position(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    status = call.data.split(":")[1]

    Settingsx.update(misc_hide_position=status)

    await call.message.edit_text(
        "<b>🖍 Изменение данных бота</b>",
        reply_markup=settings_finl(),
    )


# Изменение дискорд вебхука
@router.callback_query(F.data == "settings_edit_discord_webhook")
async def settings_discord_edit(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    get_discord_public_webhook = await (
        DiscordDJ(
            arSession=arSession,
            bot=bot,
        )
    ).export_webhook()

    await state.set_state("here_settings_discord_webhook")
    await call.message.edit_text(
        ded(f"""
            <b>🖼 Отправьте новый вебхук дискорда</b>
            ❕ Для удаления вебхука введите <code>0</code>
            ❕ Вы можете использовать публичный вебхук, но ответственность за его использование лежит только на вас
            ▪️ Публичный вебхук: <code>{get_discord_public_webhook}</code>
        """)
    )


################################################################################
################################ ПРИНЯТИЕ ДАННЫХ ###############################
# Принятие FAQ
@router.message(F.text, StateFilter("here_settings_faq"))
async def settings_faq_get(message: Message, bot: Bot, state: FSM, arSession: ARS):
    get_message = insert_tags(message.from_user.id, message.text)

    try:
        await (await message.answer(get_message)).delete()
    except:
        return await message.answer(
            "<b>❌ Ошибка синтаксиса HTML</b>\n"
            "❔ Введите новый текст для FAQ",
        )

    await state.clear()
    Settingsx.update(misc_faq=message.text)

    await message.answer(
        "<b>🖍 Изменение данных бота</b>",
        reply_markup=settings_finl(),
    )


# Принятие поддержки
@router.message(F.text, StateFilter("here_settings_support"))
async def settings_support_get(message: Message, bot: Bot, state: FSM, arSession: ARS):
    get_support = message.text

    if get_support.startswith("@"):
        get_support = get_support[1:]

    Settingsx.update(misc_support=get_support)
    await state.clear()

    await message.answer(
        "<b>🖍 Изменение данных бота</b>",
        reply_markup=settings_finl(),
    )


# Принятие дискорд вебхука
@router.message(F.text, StateFilter("here_settings_discord_webhook"))
async def settings_discord_get(message: Message, bot: Bot, state: FSM, arSession: ARS):
    get_discord_webhook = message.text

    # Удаление вебхука
    if get_discord_webhook == "0":
        Settingsx.update(
            misc_discord_webhook_url="None",
            misc_discord_webhook_name="None",
        )

        return await message.answer(
            "<b>⚙️ Настройки бота</b>",
            reply_markup=settings_finl(),
        )

    # Добавление нового вебхука
    cache_message = await message.answer("<b>♻️ Проверка дискорд вебхука..</b>")

    if "api" in get_discord_webhook and "webhooks" in get_discord_webhook:
        discord_webhook_status, discord_webhook_name = await (DiscordAPI(
            bot=bot,
            arSession=arSession,
            update=message,
            webhook_url=get_discord_webhook,
            skipping_error=True,
        )).check()

        if discord_webhook_status:
            await state.clear()

            Settingsx.update(
                misc_discord_webhook_url=message.text,
                misc_discord_webhook_name=discord_webhook_name,
            )

            return await cache_message.edit_text(
                "<b>⚙️ Настройки бота</b>",
                reply_markup=settings_finl(),
            )

    # Обработка ошибки добавления вебхука
    get_discord_public_webhook = await (
        DiscordDJ(
            arSession=arSession,
            bot=bot,
        )
    ).export_webhook()

    await cache_message.edit_text(
        ded(f"""
            <b>❌ Указан некорректный вебхук</b>
            ➖➖➖➖➖➖➖➖➖➖
            🖼 Отправьте новый вебхук дискорда
            ❕ Для удаления вебхука введите <code>0</code>
            ❕ Вы можете использовать публичный вебхук, но ответственность за его использование лежит только на вас
            ▪️ Публичный вебхук: <code>{get_discord_public_webhook}</code>
        """)
    )
