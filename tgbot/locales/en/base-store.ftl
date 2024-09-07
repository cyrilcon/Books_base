base-store =
    Добро пожаловать в <b>Base_store</b>!!

    Здесь вы можете обменять ваши <i><b>base</b></i> на скидки при слудующей покупке. Получайте <i><b>base</b></i> за покупки в <b>Books_base</b>

    <u><i>Прайс:</i></u>
    Скидка <b>15%</b> на любую книгу — <b>20</b> 💎
    Скидка <b>30%</b> на любую книгу — <b>35</b> 💎
    Скидка <b>50%</b> на любую книгу — <b>45</b> 💎
    <b>Бесплатная книга — 55</b> 💎

    { $account_information }

base-store-user-has-premium = <i>Вы не можете обменивать <b>base</b>, так как у вас действует статус <b>Books_base Premium</b> ⚜️</i>

base-store-user-has-free-book =
    <i>У вас уже действует купон на <b>бесплатную книгу</b>
    Сперва истратьте этот купон, чтобы совершить новый обмен</i>

base-store-user-has-discount =
    <i>У вас уже действует <b>скидка { $discount }%</b>
    Сперва истратьте эту скидку, чтобы совершить новый обмен</i>

base-store-error-exchange-unavailable = Вы не можете сейчас обменять base.

base-store-exchange-base =
    На что вы хотите обменять <i><b>base</b></i>??

    Скидка <b>15%</b>  —  <b>20</b> 💎
    Скидка <b>30%</b>  —  <b>35</b> 💎
    Скидка <b>50%</b>  —  <b>45</b> 💎
    <b>Бесплатная книга  —  55</b> 💎

    { base-balance }

base-store-error-not-enough-base = У вас недостаточно base для обмена

base-store-exchange-success =
    Вы обменяли <b>{ $price } <i>base</i></b> на <b>{ $discount ->
        [100] Бесплатную книгу
       *[other] Скидку { $discount }%
    }</b>!!

    { base-balance }