from utilsaio import TestStates

help_message = "In order to change the user's current state, " \
                f'send a "/setstate x" command, where x is number from 0 to {len(TestStates.all()) - 1}.\n' \
                'To reset the current state, send "/setstate" without arguments.'

start_message = "Hi! This is a demonstration of FSM's work.\n" + help_message
invalid_key_message = "Key '{key}' doesn't fit.\n" + help_message
state_change_success_message = 'Current state has been successfully changed'
state_reset_message = 'The state has been successfully reset'
current_state_message = 'Current state - "{current_state}" that satisfies the state of "one of{states}"'

MESSAGES = {
    'start': start_message,
    'help': help_message,
    'invalid_key': invalid_key_message,
    'state_change': state_change_success_message,
    'state_reset': state_reset_message,
    'current_state': current_state_message,
}