share-base =
    <b>1/2</b>
    Напишіть <i><b>ім'я користувача</b></i> або <i><b>посилання</b></i> на вашого друга в Telegram, щоб поділитися з ним <i><b>base</b></i> 💎

    <i>(Ім'я користувача починається з символу "<code>@</code>", наприклад: <b>@durov</b>. Посилання може виглядати ось так: t.me/durov)</i>

share-base-error-invalid-username =
    Ваше повідомлення не містить <i><b>ім'я користувача</b></i> або <i><b>посилання</b></i> на нього!!
    Введіть ще раз <i><b>ім'я користувача</b> (починається з символу "<code>@</code>")</i> або <i><b>посилання</b></i> на вашого друга в Telegram.

share-base-error-self-transfer =
    Ви не можете надсилати <i><b>base</b></i> самому собі!!
    Введіть ім'я користувача або посилання вашого друга ще раз

share-base-error-user-not-found =
    Користувач <b>@{ $username }</b> ще не відвідував наш магазин!!

    { invite }

share-base-error-user-has-premium =
    Ви не можете перевести <i><b>base</b></i>!!
    Користувач <b>@{ $username }</b> має статус { -books-base-premium } ⚜️

share-base-transfer =
    <b>2/2</b>
    Скільки <i><b>base</b></i> ви хочете надіслати користувачу <b>@{ $username }</b>??

    { base-balance }

share-base-error-insufficient-funds = У вас недостатньо base, щоб надіслати їх @{ $username }!!

share-base-error-general =
    Виникла помилка під час надсилання <i><b>base</b></i>!!
    Можливо, отримувач заблокував бота

    Повторіть спробу пізніше

share-base-success =
    Ви успішно надіслали { $base_received } <i><b>base</b></i> 💎 користувачу <b>@{ $username }</b>!!

    { base-balance }

share-base-success-message-for-user =
    Ви отримали { $base_received } <i><b>base</b></i> 💎 від користувача { $user_link }!!

    { base-balance }

share-base-success-message-for-admin =
    Користувач { $user_link_sender } (<code>{ $id_user_sender }</code>) перевів { $base_received } <i><b>base</b></i> 💎 користувачу { $user_link_recipient } (<code>{ $id_user_recipient }</code>)

    Баланс { $user_link_sender }: <b>{ $sender_base_balance } <i>base</i></b> 💎
    Баланс { $user_link_recipient }: <b>{ $recipient_base_balance } <i>base</i></b> 💎

share-base-canceled = Ви скасували надсилання base

share-base-unprocessed-messages = Виберіть кількість <b><i>base</i></b>, яке хочете надіслати користувачу, або скасуйте дію