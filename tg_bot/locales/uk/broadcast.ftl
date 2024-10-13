broadcast = Введіть повідомлення для розсилки

broadcast-success =
    Відправлено { $success_count }/{ $users_count } повідомлень

    { $blacklisted_users_count ->
        [one] { $blacklisted_users_count } користувач заблокований
        [few] { $blacklisted_users_count } користувача заблоковано
       *[other] { $blacklisted_users_count } користувачів заблоковано
    }

broadcast-canceled = Відправка розсилки скасована