take-discount-select-user = Введите <i><b>имя пользователя</b></i> или его <i><b>ID</b></i>, у которого хотите отобрать скидку

take-discount-error-user-already-has-not-discount = Пользователь { $user_link } (<code>{ $id_user }</code>) уже не имел скидки

take-discount-success =
    Вы изъяли <b>{ $discount ->
        [100] купон на бесплатную книгу
       *[other] скидку { $discount }%
    }</b> у пользователя { $user_link } (<code>{ $id_user }</code>)

take-discount-canceled = Вы не изъяили скидку у пользователя