base-store =
    Добро пожаловать в <b>{ -base-store }</b>!!

    Здесь вы можете обменять ваши <i><b>base</b></i> на скидки при следующей покупке. Получайте <i><b>base</b></i> за покупки в <b>{ -books-base }</b>.

    <u><i>Прайс:</i></u>
    Скидка <b>15%</b> на любую книгу — <b>{ $price_discount_15 }</b> 💎
    Скидка <b>30%</b> на любую книгу — <b>{ $price_discount_30 }</b> 💎
    Скидка <b>50%</b> на любую книгу — <b>{ $price_discount_50 }</b> 💎
    <b>Бесплатная книга — { $price_discount_100 }</b> 💎

    { $discount_value ->
        [100] <i>У вас уже действует купон на <b>бесплатную книгу</b>.
    Сперва используйте этот купон, чтобы совершить новый обмен.

    Вы можете отменить этот купон. Вам вернутся на счёт ваши потраченные base.</i>
        [15] <i>У вас уже действует <b>скидка { $discount_value }%</b>.
    Сперва используйте эту скидку, чтобы совершить новый обмен.

    Вы можете отменить действующую скидку. Вам вернутся на счёт ваши потраченные base.</i>
        [30] <i>У вас уже действует <b>скидка { $discount_value }%</b>.
    Сперва используйте эту скидку, чтобы совершить новый обмен.

    Вы можете отменить действующую скидку. Вам вернутся на счёт ваши потраченные base.</i>
        [50] <i>У вас уже действует <b>скидка { $discount_value }%</b>.
    Сперва используйте эту скидку, чтобы совершить новый обмен.

    Вы можете отменить действующую скидку. Вам вернутся на счёт ваши потраченные base.</i>
       *[other] { base-balance }
    }

base-store-error-user-has-premium = Вам не доступен { -base-store }, так как у вас действует статус <b>{ -books-base-premium }</b> ⚜️

base-store-error-exchange-unavailable = Вы не можете сейчас обменять base.

base-store-error-not-enough-base = У вас недостаточно base для обмена.

base-store-exchange-success =
    Вы обменяли <b>{ $price } <i>base</i></b> на <b>{ $discount_value ->
        [100] бесплатную книгу
       *[other] скидку { $discount_value }%
    }</b>!!

    { base-balance }

base-store-exchange-success-message-for-admin =
    Пользователь { $user_link } (<code>{ $id_user }</code>) обменял <b>{ $price } <i>base</i></b> на <b>{ $discount_value ->
        [100] бесплатную книгу
       *[other] скидку { $discount_value }%
    }</b>!!

    { user-balance }

base-store-cancel-discount-error = У вас уже нет никакой скидки!!

base-store-cancel-discount-success =
    Вы успешно отменили <b>{ $discount_value ->
        [100] купон на бесплатную книгу
       *[other] скидку { $discount_value }%
    }</b>!!

    { base-balance }

base-store-cancel-discount-success-message-for-admin =
    Пользователь { $user_link } (<code>{ $id_user }</code>) отменил <b>{ $discount_value ->
        [100] купон на бесплатную книгу
       *[other] скидку { $discount_value }%
    }</b>.

    { user-balance }