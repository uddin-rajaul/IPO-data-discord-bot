import scrape
from scrape import get_data_by_status


def handle_response(message) ->str:
    message = message.lower()

    if message.content.startswith('!status'):
        status = message.content.split(' ')[1]
        if status == 'open':
            # call the function to filter data for 'open' status
            open_data = get_data_by_status('open')
            return message.channel.send(open_data)
        elif status == 'coming_soon':
            # call the function to filter data for 'coming_soon' status
            coming_soon_data = get_data_by_status('coming_soon')
            return message.channel.send(coming_soon_data)
        else:
            return message.channel.send('Invalid status. Please enter either "open" or "coming_soon".')

    elif message.content.startswith('!help'):
        # send a message explaining the available commands
        help_message = 'Available commands: \n !status [status_type] - Get data by status (open or coming_soon)\n !help - Display available commands'
        return message.channel.send(help_message)