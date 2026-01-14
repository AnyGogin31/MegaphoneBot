from .cmd_call import register_handler as register_call_command_handlers
from .cmd_mute import register_handler as register_mute_command_handlers
from .cmd_unmute import register_handler as register_unmute_command_handlers


_handler_registration_functions = [
    register_call_command_handlers,
    register_mute_command_handlers,
    register_unmute_command_handlers,
]


def register_handlers(client):
    for register_function in _handler_registration_functions:
        register_function(client)
