share-base =
    <b>1/2</b>
    Напишите <i><b>имя пользователя</b></i> или <i><b>ссылку</b></i> на вашего друга в Telegram, чтобы поделиться с ним <i><b>base</b></i> 💎

    <i>(Имя пользователя начинается с символа "<code>@</code>", например: <b>@durov</b>. Ссылка может выглядить вот так: t.me/durov)</i>

share-base-error-invalid-username =
    Ваше сообщение не содержит <i><b>имени пользователя</b></i> или <i><b>ссылки</b></i> на него!!
    Введите ещё раз <i><b>имя пользователя</b> (начинается с символа "<code>@</code>")</i> или <i><b>ссылку</b></i> на вашего друга в Telegram

share-base-error-self-transfer =
    Вы не можете отправлять <i><b>base</b></i> самому себе!!
    Введите имя пользователя или ссылку вашего друга ещё раз.

share-base-error-user-not-found = Пользователь <b>@{ $username }</b> ещё не посещал наш магазин!!

share-base-transfer =
    <b>2/2</b>
    Сколько <i><b>base</b></i> вы хотите отправить пользователю <b>@{ $username }</b>??

    { base-balance }

share-base-error-insufficient-funds = У вас недостаточно base, чтобы отрпавить их @{ $username }!!

share-base-error-general =
    Произошла ошибка при отправке base!!
    Возможно получатель заблокировал бота.

    Повторите попытку позже.

share-base-success =
    Вы успешно отправили { $base_received } <i><b>base</b></i> 💎 пользователю <b>@{ $username }</b>!!

    { base-balance }

share-base-success-message-for-user =
    Вы получили { $base_received } <i><b>base</b></i> 💎 от пользователя { $user_link }!!

    { base-balance }

share-base-success-message-for-admin =
    Пользователь { $user_link_sender } (<code>{ $id_user_sender }</code>) перевёл { $base_received } <i><b>base</b></i> 💎 пользователю { $user_link_recipient } (<code>{ $id_user_recipient }</code>)

    Баланс { $user_link_sender }: <b>{ $sender_base_balance } <i>base</i></b> 💎
    Баланс { $user_link_recipient }: <b>{ $recipient_base_balance } <i>base</i></b> 💎

share-base-canceled = Вы отменили отправку base

share-base-unprocessed-messages = Выберите количество <b><i>base</i></b>, которое хотите отправить пользователю или отмените действие.