get-profile = Enter the <i><b>username</b></i> or <i><b>ID</b></i> of the user whose information you want to retrieve

get-profile-template =
    { $status_icons } { $user_link } (<code>{ $id_user }</code>) { $language_code ->
        [en] 🇬🇧
        [uk] 🇺🇦
        [ru] 🇷🇺
       *[other] 🏳️ <code>{ $language_code }</code>
    }

    { $discount ->
        [100] Has a coupon for a free book
        [0] Has no discounts
       *[other] Has a discount of <b>{ $discount }%</b>
    }

    { user-balance }

    Registration date:
    <code>{ $registration_datetime }</code>

    Last activity:
    <code>{ $last_activity_datetime }</code>

get-profile-status-icon-admin = 👮🏻

get-profile-status-icon-blacklisted = 🚫

get-profile-status-icon-premium = ⚜️

get-profile-canceled = You have canceled the profile retrieval