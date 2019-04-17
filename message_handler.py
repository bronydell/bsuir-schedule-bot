from core.logic import on_message
from vk_api.bot_longpoll import VkBotEventType
from replyer import VKReply, TGReply


def on_vk_event(client, event):
    if event.type in [VkBotEventType.MESSAGE_EDIT, VkBotEventType.MESSAGE_NEW]:
        on_message(VKReply(client, event), event.object.text)


def on_tg_event(client, event):
    on_message(TGReply(client, event), event.effective_message.text)
