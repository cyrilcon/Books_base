base-store =
    Ласкаво просимо до <b>{ -base-store }</b>!!

    Тут ви можете обміняти свої <i><b>base</b></i> на знижки при наступній покупці. Отримуйте <i><b>base</b></i> за покупки в <b>{ -books-base }</b>.

    <u><i>Ціни:</i></u>
    Знижка <b>15%</b> на будь-яку книгу — <b>{ $price_discount_15 }</b> 💎
    Знижка <b>30%</b> на будь-яку книгу — <b>{ $price_discount_30 }</b> 💎
    Знижка <b>50%</b> на будь-яку книгу — <b>{ $price_discount_50 }</b> 💎
    <b>Безкоштовна книга — { $price_discount_100 }</b> 💎

    { $discount_value ->
        [100] <i>У вас уже є купон на <b>безкоштовну книгу</b>.
    Спочатку використайте цей купон, щоб здійснити новий обмін.

    Ви можете скасувати цей купон. Ваші витрачені base будуть повернені на рахунок.</i>
        [15] <i>У вас уже є <b>знижка { $discount_value }%</b>.
    Спочатку використайте цю знижку, щоб здійснити новий обмін.

    Ви можете скасувати активну знижку. Ваші витрачені base будуть повернені на рахунок.</i>
        [30] <i>У вас уже є <b>знижка { $discount_value }%</b>.
    Спочатку використайте цю знижку, щоб здійснити новий обмін.

    Ви можете скасувати активну знижку. Ваші витрачені base будуть повернені на рахунок.</i>
        [50] <i>У вас уже є <b>знижка { $discount_value }%</b>.
    Спочатку використайте цю знижку, щоб здійснити новий обмін.

    Ви можете скасувати активну знижку. Ваші витрачені base будуть повернені на рахунок.</i>
       *[other] { base-balance }
    }

base-store-error-user-has-premium = Вам не доступно { -base-store }, оскільки у вас активний статус <b>{ -books-base-premium }</b> ⚜️

base-store-error-exchange-unavailable = Ви не можете зараз обміняти base.

base-store-error-not-enough-base = У вас недостатньо base для обміну.

base-store-exchange-success =
    Ви обміняли <b>{ $price } <i>base</i></b> на <b>{ $discount_value ->
        [100] безкоштовну книгу
       *[other] знижку { $discount_value }%
    }</b>!!

    { base-balance }

base-store-exchange-success-message-for-admin =
    Користувач { $user_link } (<code>{ $id_user }</code>) обміняв <b>{ $price } <i>base</i></b> на <b>{ $discount_value ->
        [100] безкоштовну книгу
       *[other] знижку { $discount_value }%
    }</b>!!

    { user-balance }

base-store-cancel-discount-error = У вас вже немає жодної знижки!!

base-store-cancel-discount-success =
    Ви успішно скасували <b>{ $discount_value ->
        [100] купон на безкоштовну книгу
       *[other] знижку { $discount_value }%
    }</b>!!

    { base-balance }

base-store-cancel-discount-success-message-for-admin =
    Користувач { $user_link } (<code>{ $id_user }</code>) скасував <b>{ $discount_value ->
        [100] купон на безкоштовну книгу
       *[other] знижку { $discount_value }%
    }</b>.

    { user-balance }