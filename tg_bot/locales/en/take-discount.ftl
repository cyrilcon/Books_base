take-discount = Введите <i><b>имя пользователя</b></i> или его <i><b>ID</b></i>, у которого хотите отобрать скидку

take-discount-error-user-already-has-not-discount = Пользователь { $user_link } (<code>{ $id_user }</code>) уже не имел скидки

take-discount-success =
    У пользователя { $user_link } (<code>{ $id_user }</code>) { $discount ->
        [100] изъят <b>купон на бесплатную книгу</b>
       *[other] изъята <b>скидка { $discount }%</b>
    }

take-discount-canceled = Вы не изъяили скидку у пользователя