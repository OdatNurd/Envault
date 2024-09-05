import sublime

import textwrap


## ----------------------------------------------------------------------------


def log(msg, *args, dialog=False, error=False, status=False, **kwargs):
    """
    Generate a message to the console and optionally as either a message or
    error dialog. The message will be formatted and dedented before being
    displayed, and will be prefixed with its origin.
    """
    msg = textwrap.dedent(msg.format(*args, **kwargs)).strip()

    if error:
        print("Envault error:")
        return sublime.error_message(msg)

    for line in msg.splitlines():
        print("Envault: {msg}".format(msg=line))

    if status:
        sublime.status_message(msg)

    if dialog:
        sublime.message_dialog(msg)


## ----------------------------------------------------------------------------
