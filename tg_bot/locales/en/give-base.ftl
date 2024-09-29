give-base-select-user =
    <b>1/2</b>
    Введите <i><b>имя пользователя</b></i> или его <i><b>ID</b></i>, которому хотите выдать <i>base</i> 💎

give-base-transfer-base =
    <b>2/2</b>
    Введите <i><b>количество base</b></i> 💎, которое хотите отправить пользователю { $user_link } (<code>{ $id_user }</code>).

    { user-balance }

give-base-error-invalid-base = Количество <i>base</i> 💎 должно быть целым положительным числом!!

give-base-success =
    Пользователь { $user_link } (<code>{ $id_user }</code>) получил { $base_received } <i>base</i> 💎

    { user-balance }

give-base-success-message-for-user =
    Вы получили { $base_received } <i>base</i> 💎

    { base-balance }

give-base-canceled = Вы отменили отправку base пользователю