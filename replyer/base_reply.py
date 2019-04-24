from abc import ABC


class BaseReply(ABC):
    chat_type = "Abstract"

    def send_text(self, text):
        """
        Send text as response
        :param text: Message's text
        """
        pass

    def get_chat_type(self):
        """
        Get message's chat type (chat's network)
        :return: Chat's type
        """
        return self.chat_type

    def get_chat_id(self):
        """
        Get message's chat ID (source chat, if you say so)
        :return: Chat ID
        """
        return None

    def get_message_author(self):
        """
        Get full author chat ID
        :return: Author chat ID
        """
        return None

    def get_message_author_name(self):
        """
        Get full sender's name
        :return: Full sender's name
        """
        return None