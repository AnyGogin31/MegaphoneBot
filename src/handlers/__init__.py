from .cmd_call import register_call_command_handler
from .cmd_mute import register_mute_command_handler
from .cmd_unmute import register_unmute_command_handler


_handler_registration_functions = [
    register_call_command_handler,
    register_mute_command_handler,
    register_unmute_command_handler,
]


def register_handlers(client):
    for register_function in _handler_registration_functions:
        register_function(client)
