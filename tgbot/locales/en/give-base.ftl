give-base-prompt-select-user =
    <b>1/2</b>
    Введите <i><b>имя пользователя</b></i> или его <i><b>ID</b></i>, которому хотите выдать <i>base</i> 💎

give-base-prompt-transfer =
    <b>2/2</b>
    Введите <i><b>количество base</b></i> 💎, которое хотите отправить пользователю { $user_link } (<code>{ $id_user }</code>).

give-base-received =
    Вы получили { $base_received } <i>base</i> 💎

    { base-balance }

give-base-error-invalid-base = Количество <i>base</i> 💎 должно быть целым положительным числом!!

give-base-success =
    Вы отправили { $base_received } <i>base</i> 💎 пользователю { $user_link } (<code>{ $id_user }</code>).

    Баланс пользователя: <b>{ $base_balance } <i>base</i></b> 💎

give-base-canceled = Вы отменили отправку base пользователю