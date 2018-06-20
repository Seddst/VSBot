from core.types import User


def fill_template(msg: str, user: User):
    if user.username:
        msg = msg.replace('%username%', '@' + user.username)
    else:
        msg = msg.replace('%username%', (user.first_name or '') + ' ' + (user.last_name or ''))
    msg = msg.replace('%first_name%', user.first_name or '')
    msg = msg.replace('%last_name%', user.last_name or '')
    msg = msg.replace('%id%', str(user.id))
    msg = msg.replace('%ign%', (user.first_name or '') + ' ' + (user.last_name or ''))
    return msg
