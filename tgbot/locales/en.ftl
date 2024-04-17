start-text =
    Hi{ $additional_text }!!
    Write the title or article of the book to buy or familiarize yourself with the product

help-text =
    Telegram slot machine has 4 icons: BAR, grapes, lemon and number 7. In total, there are 64 combinations.
    Decoding of dice value is described <a href='https://github.com/MasterGroosha/telegram-casino-bot/blob/aiogram3/bot/dice_check.py'>here</a>.

    Source code of the bot is available on <a href='https://github.com/MasterGroosha/telegram-casino-bot'>GitHub</a>

stop-text = Keyboard removed. To start from scratch, press /start, to get keyboard and continue: /spin

bar = BAR
grapes = grapes
lemon = lemon
seven = seven

spin-button-text = 🎰 Try it!

spin-fail = You lost the bet.
spin-success =
    You won {$score_change ->
         [one] {$score_change} point
        *[many] {$score_change} points
    }!

after-spin =
    Your combination: { $combo_text } (№{ $dice_value }).
    { $result_text } New score: <b>{ $new_score }</b>.

zero-balance =
    Your balance is zero. Accept your fate and get back to your business, or press /start to start over. To remove keyboard, press /stop.

# If you don't want to send sticker when balance is zero, disable feature in bot configuration
zero-balance-sticker = CAACAgIAAxkBAAEWXv5lAUAm76JOjvehtp18Gxb3if0eVQAC-hEAAknF8EuBzj23_M8x3jAE

menu-start = Restart Casino
menu-spin = Show keyboard and make a spin
menu-stop = Remove keyboard
menu-help = Information about this bot
