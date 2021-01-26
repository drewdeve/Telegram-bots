help_message = '''
Through this bot you can buy a time machine to see how the purchase and payment in Telegram works.
Send a command /buy to go to buy.
You can learn the rules and regulations using the command /terms.
'''

start_message = 'Hi! This is a demonstration of the work of payments in Telegram!\n' + help_message

pre_buy_demo_alert = '''\
Since I'm now running in test mode, you need to use a card with the number '1111 1111 1111 1026' to pay for payment
Account to pay: 
'''

terms = '''\
*Thank you for choosing our bot. We hope you enjoy your new time machine!*

1. If the time machine is not delivered on time, please rethink your concept of time and try again.
2. If you find that the time machine is not working, please contact our future service workshops from the Trappist-1e exoplanet. They will be available anywhere between May 2075 and November 4000 AD.
3. If you want to return the money, be so kind to apply yesterday and we will immediately make a refund.
'''

tm_title = 'The Real Time Machine'
tm_description = '''\
Want to meet your great-great-great-great-grandparents?
Make a fortune on bets?
Shake Hammurabi's hand and walk through the hanging gardens of Semiramida?
Order the Time Machine from us right now!
'''

AU_error = '''\
Unfortunately, our couriers are afraid of kangaroos, and teleport can not send so far. 
Try to choose a different address!
'''

wrong_email = '''\
It seems to us that this email is not valid.
Try to specify another email
'''

successful_payment = '''
Cheers! The payment of the sum of `{total_amount} {currency}` is a success! Enjoy the new time machine!
Check out the refund rules in /terms
Buy another time machine for your friend - /buy
'''

MESSAGES = {
    'start': start_message,
    'help': help_message,
    'pre_buy_demo_alert': pre_buy_demo_alert,
    'terms': terms,
    'tm_title': tm_title,
    'tm_description': tm_description,
    'AU_error': AU_error,
    'wrong_email': wrong_email,
    'successful_payment': successful_payment,
}
