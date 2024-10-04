# __init__.py

from app.Classes import EmailModerator, BadWordModerator, LinkModerator, SwearingModerator, ContactModerator, \
    AIModerator


# from .SpamModerator import SpamModerator

def get_moderator_chain():
    # Создание и настройка цепочки модераторов
    moderator_chain = ContactModerator()
    email = EmailModerator()
    link = LinkModerator()
    swearing = SwearingModerator()
    bad_word = BadWordModerator()
    ai = AIModerator()
    # spam = SpamModerator()

    (
        moderator_chain.
        set_next(email).
        set_next(link).
        set_next(swearing).
        set_next(bad_word).
        # set_next(spam).
        set_next(ai)
    )

    return moderator_chain
