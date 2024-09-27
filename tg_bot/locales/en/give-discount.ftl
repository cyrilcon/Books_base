give-discount-prompt-select-user =
    <b>1/2</b>
    Введите <i><b>имя пользователя</b></i> или его <i><b>ID</b></i>, которому хотите выдать скидку

give-discount-error-user-already-has-discount =
    Пользователь уже имеет <b>{ $discount_value ->
        [100] купон на бесплатную книгу
       *[other] скидку { $discount_value }%
    }</b>!!

give-discount-prompt-select-discount =
    <b>2/2</b>
    Выберите <i><b>скидку</b></i>, которую хотите выдать пользователю { $user_link } (<code>{ $id_user }</code>)

give-discount-success =
    Пользователю { $user_link } (<code>{ $id_user }</code>) <b>{ $discount_value ->
        [100] выдан купон на бесплатную книгу
       *[other] выдана скидка { $discount_value }%
    }</b>

give-discount-success-message-for-user =
    Вы получили <b>{ $discount_value ->
        [100] купон на бесплатную книгу
       *[other] скидку { $discount_value }%
    }</b>!!

    Вы можете истратить { $discount_value ->
        [100] его
       *[other] её
    } при следующей покупки.

give-discount-canceled = Вы отменили выдачу скидки пользователю