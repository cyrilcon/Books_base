take-discount = Enter the <i><b>username</b></i> or <i><b>ID</b></i> of the user from whom you want to take the discount

take-discount-error-user-already-has-not-discount = User { $user_link } (<code>{ $id_user }</code>) already did not have a discount

take-discount-success =w
    The discount has been taken from user { $user_link } (<code>{ $id_user }</code>) { $discount ->
        [100] <b>coupon for a free book</b> has been taken
       *[other] <b>discount of { $discount }%</b> has been taken
    }

take-discount-canceled = You did not take the discount from the user