share-base-select-user =
    <b>1/2</b>
    Напишите <i><b>имя пользователя</b></i> или <i><b>ссылку</b></i> на вашего друга в Telegram, чтобы поделиться с ним <i><b>base</b></i> 💎

    <i>(Имя пользователя начинается с символа "<code>@</code>", например: <b>@durov</b>. Ссылка может выглядить вот так: https://t.me/durov)</i>

share-base-cannot-yourself =
    Вы не можете отправлять <i><b>base</b></i> самому себе!!
    Введите имя пользователя или ссылку вашего друга ещё раз.

share-base-username-not-found = Пользователь <b>@{ $username }</b> ещё не посещал наш магазин!!

share-base-username-incorrect =
    Ваше сообщение не содержит <i><b>имени пользователя</b></i> или <i><b>ссылки</b></i> на него!!
    Введите ещё раз <i><b>имя пользователя</b> (начинается с символа "<code>@</code>")</i> или <i><b>ссылку</b></i> на вашего друга в Telegram

share-base-select-amount-base =
    <b>2/2</b>
    Сколько <i><b>base</b></i> вы хотите отправить пользователю <b>@{ $username }</b>??

    { $amount_base }

share-base-sender-does-not-have-username =
    У вас отсутствует имя пользователя в Telegram!!

    Установите его в настройках, чтобы делиться base с другими.

    Настройки -> Изменить профиль -> Имя пользователя.

share-base-not-enough-base = У вас недостаточно base, чтобы отрпавить их @{ $username }!!

share-base-came-in =
    Вы получили { $bases } <i><b>base</b></i> 💎 от пользователя <b>@{ $username }</b>!!

    { $amount_base }

share-base-error =
    Произошла ошибка при отправке!!
    Возможно получатель заблокировал бота.

    Повторите попытку позже.

share-base-was-sent =
    Вы успешно отправили { $bases } <i><b>base</b></i> 💎 пользователю <b>@{ $username }</b>!!

    { $amount_base }

share-base-cancel = Вы отменили отправку base своему другу