broadcast-write-message = Введите сообщение для рассылки

broadcast-success =
    Отправлено { $success_count }/{ $users_count } сообщений

    { $blacklisted_users_count ->
        [one] { $blacklisted_users_count } пользователь заблокирован
        [few] { $blacklisted_users_count } пользователя заблокировано
       *[other] { $blacklisted_users_count } пользователей заблокировано
    }

broadcast-canceled = Отправка рассылки отменина