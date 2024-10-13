broadcast = Enter a message for the broadcast

broadcast-success =
    Sent { $success_count }/{ $users_count } messages

    { $blacklisted_users_count ->
        [one] { $blacklisted_users_count } user is blocked
        *[other] { $blacklisted_users_count } users are blocked
    }

broadcast-canceled = The broadcast sending has been canceled