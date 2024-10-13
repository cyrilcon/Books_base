take-base =
    <b>1/2</b>
    Enter the <i><b>username</b></i> or <i><b>ID</b></i> of the user from whom you want to take <i>base</i> 💎

take-base-deduct-base =
    <b>2/2</b>
    Enter the <i><b>amount of base</b></i> 💎 you want to take from user { $user_link } (<code>{ $id_user }</code>)

    { user-balance }

take-base-error-invalid-base = The amount of <i>base</i> 💎 must be a whole positive number!!

take-base-success =
    { $user_link } (<code>{ $id_user }</code>) has had { $base_deducted } <i>base</i> 💎 taken

    { user-balance }

take-base-canceled = You did not take base from the user