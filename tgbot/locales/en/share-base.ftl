share-base-prompt-select-user =
    <b>1/2</b>
    Напишите <i><b>имя пользователя</b></i> или <i><b>ссылку</b></i> на вашего друга в Telegram, чтобы поделиться с ним <i><b>base</b></i> 💎

    <i>(Имя пользователя начинается с символа "<code>@</code>", например: <b>@durov</b>. Ссылка может выглядить вот так: t.me/durov)</i>

share-base-error-self-transfer =
    Вы не можете отправлять <i><b>base</b></i> самому себе!!
    Введите имя пользователя или ссылку вашего друга ещё раз.

share-base-error-user-not-found = Пользователь <b>@{ $username }</b> ещё не посещал наш магазин!!

share-base-error-invalid-username =
    Ваше сообщение не содержит <i><b>имени пользователя</b></i> или <i><b>ссылки</b></i> на него!!
    Введите ещё раз <i><b>имя пользователя</b> (начинается с символа "<code>@</code>")</i> или <i><b>ссылку</b></i> на вашего друга в Telegram

share-base-prompt-amount =
    <b>2/2</b>
    Сколько <i><b>base</b></i> вы хотите отправить пользователю <b>@{ $username }</b>??

    { base-balance }

share-base-error-insufficient-funds = У вас недостаточно base, чтобы отрпавить их @{ $username }!!

share-base-received =
    Вы получили { $base_received } <i><b>base</b></i> 💎 от пользователя { $user_link }!!

    { base-balance }

share-base-error-general =
    Произошла ошибка при отправке base!!
    Возможно получатель заблокировал бота.

    Повторите попытку позже.

share-base-success =
    Вы успешно отправили { $base_received } <i><b>base</b></i> 💎 пользователю <b>@{ $username }</b>!!

    { base-balance }

share-base-canceled = Вы отменили отправку base