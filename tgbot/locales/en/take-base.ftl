take-base-prompt-select-user =
    <b>1/2</b>
    Введите <i><b>имя пользователя</b></i> или его <i><b>ID</b></i>, у которого хотите изъять <i>base</i> 💎

take-base-prompt-deduct-base =
    <b>2/2</b>
    Введите <i><b>количество base</b></i> 💎, которое хотите изъять у пользователя { $user_link } (<code>{ $id_user }</code>).

    { user-balance }

take-base-error-invalid-base = Количество <i>base</i> 💎 должно быть целым положительным числом!!

take-base-success =
    Вы изъяли { $base_deducted } <i>base</i> 💎 у пользователя { $user_link } (<code>{ $id_user }</code>).

    { user-balance }

take-base-canceled = Вы не изъяили base у пользователя