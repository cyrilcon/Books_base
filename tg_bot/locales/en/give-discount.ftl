give-discount-prompt-select-user =
    <b>1/2</b>
    Введите <i><b>имя пользователя</b></i> или его <i><b>ID</b></i>, которому хотите выдать скидку

give-discount-error-user-already-has-discount =
    Пользователь уже имеет <b>{ $discount ->
        [100] купон на бесплатную книгу
       *[other] скидку { $discount }%
    }</b>!!

give-discount-prompt-select-discount =
    <b>2/2</b>
    Выберите <i><b>скидку</b></i>, которую хотите выдать пользователю { $user_link } (<code>{ $id_user }</code>)

give-discount-given =
    Вы получили <b>{ $discount ->
        [100] купон на бесплатную книгу
       *[other] скидку { $discount }%
    }</b>!!

give-discount-success =
    Вы выдали <b>{ $discount ->
        [100] купон на бесплатную книгу
       *[other] скидку { $discount }%
    }</b> пользователю { $user_link } (<code>{ $id_user }</code>)!!

give-discount-canceled = Вы отменили выдачу скидки пользователю