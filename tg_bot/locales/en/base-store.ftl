base-store =
    Welcome to <b>{ -base-store }</b>!!

    Here you can exchange your <i><b>base</b></i> for discounts on your next purchase. Earn <i><b>base</b></i> by purchasing from <b>{ -books-base }</b>.

    <u><i>Price List:</i></u>
    15% discount on any book — <b>{ $price_discount_15 }</b> 💎
    30% discount on any book — <b>{ $price_discount_30 }</b> 💎
    50% discount on any book — <b>{ $price_discount_50 }</b> 💎
    <b>Free book — { $price_discount_100 }</b> 💎

    { $discount_value ->
        [100] <i>You already have a coupon for a <b>free book</b>.
    Use this coupon first to make a new exchange.

    You can cancel this coupon. Your spent base will be refunded.</i>
        [15] <i>You already have a <b>{ $discount_value }% discount</b>.
    Use this discount first to make a new exchange.

    You can cancel the active discount. Your spent base will be refunded.</i>
        [30] <i>You already have a <b>{ $discount_value }% discount</b>.
    Use this discount first to make a new exchange.

    You can cancel the active discount. Your spent base will be refunded.</i>
        [50] <i>You already have a <b>{ $discount_value }% discount</b>.
    Use this discount first to make a new exchange.

    You can cancel the active discount. Your spent base will be refunded.</i>
       *[other] { base-balance }
    }

base-store-error-user-has-premium = The { -base-store } is not available to you as you have an active <b>{ -books-base-premium }</b> status ⚜️.

base-store-error-exchange-unavailable = You cannot exchange base right now.

base-store-error-not-enough-base = You don't have enough base to make an exchange.

base-store-exchange-success =
    You exchanged <b>{ $price } <i>base</i></b> for a <b>{ $discount_value ->
        [100] free book
       *[other] { $discount_value }% discount
    }</b>!!

    { base-balance }

base-store-exchange-success-message-for-admin =
    User { $user_link } (<code>{ $id_user }</code>) exchanged <b>{ $price } <i>base</i></b> for a <b>{ $discount_value ->
        [100] free book
       *[other] { $discount_value }% discount
    }</b>!!

    { user-balance }

base-store-cancel-discount-error = You don't have any active discount!!

base-store-cancel-discount-success =
    You successfully canceled <b>{ $discount_value ->
        [100] the free book coupon
       *[other] the { $discount_value }% discount
    }</b>!!

    { base-balance }

base-store-cancel-discount-success-message-for-admin =
    User { $user_link } (<code>{ $id_user }</code>) canceled <b>{ $discount_value ->
        [100] the free book coupon
       *[other] the { $discount_value }% discount
    }</b>.

    { user-balance }