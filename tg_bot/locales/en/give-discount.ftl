give-discount =
    <b>1/2</b>
    Enter the <i><b>username</b></i> or <i><b>ID</b></i> of the user you want to grant a discount to

give-discount-error-user-has-premium = The user has { -books-base-premium } ⚜️ status

give-discount-error-user-already-has-discount =
    The user already has <b>{ $discount_value ->
        [100] a coupon for a free book
       *[other] a discount of { $discount_value }%
    }</b>!!

give-discount-select-discount =
    <b>2/2</b>
    Select the <i><b>discount</b></i> you want to grant to user { $user_link } (<code>{ $id_user }</code>)

give-discount-success =
    User { $user_link } (<code>{ $id_user }</code>) has been granted <b>{ $discount_value ->
        [100] a coupon for a free book
       *[other] a discount of { $discount_value }%
    }</b>

give-discount-success-message-for-user =
    You received <b>{ $discount_value ->
        [100] a coupon for a free book
       *[other] a discount of { $discount_value }%
    }</b>!!

    You can use { $discount_value ->
        [100] it
       *[other] them
    } on your next purchase.

give-discount-canceled = You canceled the discount issuance to the user