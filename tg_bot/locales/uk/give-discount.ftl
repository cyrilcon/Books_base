give-discount =
    <b>1/2</b>
    Введіть <i><b>ім'я користувача</b></i> або його <i><b>ID</b></i>, якому хочете видати знижку

give-discount-error-user-has-premium = Користувач має статус { -books-base-premium } ⚜️

give-discount-error-user-already-has-discount =
    Користувач вже має <b>{ $discount_value ->
        [100] купон на безкоштовну книгу
       *[other] знижку { $discount_value }%
    }</b>!!

give-discount-select-discount =
    <b>2/2</b>
    Виберіть <i><b>знижку</b></i>, яку хочете видати користувачу { $user_link } (<code>{ $id_user }</code>)

give-discount-success =
    Користувачу { $user_link } (<code>{ $id_user }</code>) була видана <b>{ $discount_value ->
        [100] купон на безкоштовну книгу
       *[other] знижка { $discount_value }%
    }</b>

give-discount-success-message-for-user =
    Ви отримали <b>{ $discount_value ->
        [100] купон на безкоштовну книгу
       *[other] знижку { $discount_value }%
    }</b>!!

    Ви можете витратити { $discount_value ->
        [100] його
       *[other] її
    } під час наступної покупки.

give-discount-canceled = Ви скасували видачу знижки користувачу