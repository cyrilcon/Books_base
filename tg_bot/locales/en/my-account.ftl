my-account =
    <i>{ $full_name }</i>
    { $has_discount_or_premium }
    { base-balance }

    Thank you for using our store!!
    Thanks to you, our library <b>{ -books-base }</b> is expanding.

my-account-has-premium = You have an active status of <b>{ -books-base-premium }</b> ⚜️

my-account-has-discount = { $discount ->
        [100] You have a coupon for a free book
       *[other] You have a discount of <b>{ $discount }%</b>
    }