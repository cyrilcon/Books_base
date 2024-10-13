my-account =
    <i>{ $full_name }</i>
    { $has_discount_or_premium }
    { base-balance }

    Спасибо, что пользуетесь нашим магазином!!
    Благодаря Вам наша библиотека <b>{ -books-base }</b> расширяется

my-account-has-premium = У вас активен статус <b>{ -books-base-premium }</b> ⚜️

my-account-has-discount = { $discount ->
        [100] У вас действует купон на бесплатную книгу
       *[other] У вас действует скидка <b>{ $discount }%</b>
    }