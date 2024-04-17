start-text =
    Привіт{ $additional_text }!!!
    Напиши назву або артикул книги, щоб купити або ознайомиться з товаром"

help-text =
    В казино доступно 4 элемента: BAR, виноград, лимон и цифра семь. Комбинаций, соответственно, 64.
    Для распознавания комбинации используется четверичная система, а пример кода для получения комбинации по значению от Bot API можно увидеть <a href='https://gist.github.com/MasterGroosha/963c0a82df348419788065ab229094ac'>здесь</a>.

    Исходный код бота доступен на <a href='https://github.com/MasterGroosha/telegram-casino-bot'>GitHub</a> и на <a href='https://git.groosha.space/shared/telegram-casino-bot'>GitLab</a>."

stop-text = Клавиатура удалена. Начать заново: /start, вернуть клавиатуру и продолжить: /spin

bar = BAR
grapes = виноград
lemon = лимон
seven = семь

spin-button-text = 🎰 Испытать удачу!

spin-fail = К сожалению, вы не выиграли.
spin-success =
    Вы выиграли {$score_change ->
         [one] {$score_change} очко
         [few] {$score_change} очка
        *[many] {$score_change} очков
    }!

after-spin =
    Ваша комбинация: { $combo_text } (№{ $dice_value }).
    { $result_text } Ваш счёт: <b>{ $new_score }</b>.

zero-balance =
    Ваш баланс равен нулю. Вы можете смириться с судьбой и продолжить жить своей жизнью, а можете нажать /start, чтобы начать всё заново. Или /stop, чтобы просто убрать клавиатуру.

# Если не хотите использовать стикер, укажите это в конфиге
zero-balance-sticker = CAACAgIAAxkBAAEFGxpfqmqG-MltYIj4zjmFl1eCBfvhZwACuwIAAuPwEwwS3zJY4LIw9B4E

menu-start = Перезапустить казино
menu-spin = Показать клавиатуру и сделать бросок
menu-stop = Убрать клавиатуру
menu-help = Справочная информация
