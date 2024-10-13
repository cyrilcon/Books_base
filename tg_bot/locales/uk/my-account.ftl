my-account =
    <i>{ $full_name }</i>
    { $has_discount_or_premium }
    { base-balance }

    Дякуємо, що користуєтеся нашим магазином!!
    Завдяки вам наша бібліотека <b>{ -books-base }</b> розширюється.

my-account-has-premium = У вас активний статус <b>{ -books-base-premium }</b> ⚜️

my-account-has-discount = { $discount ->
        [100] У вас є купон на безкоштовну книгу
       *[other] У вас є знижка <b>{ $discount }%</b>
    }