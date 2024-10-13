get-profile = Введіть <i><b>ім'я користувача</b></i> або його <i><b>ID</b></i>, інформацію про яку ви хочете отримати

get-profile-template =
    { $status_icons } { $user_link } (<code>{ $id_user }</code>) { $language_code ->
        [en] 🇬🇧
        [uk] 🇺🇦
        [ru] 🇷🇺
       *[other] 🏳️ <code>{ $language_code }</code>
    }

    { $discount ->
        [100] Має купон на безкоштовну книгу
        [0] Не має ніяких знижок
       *[other] Має знижку <b>{ $discount }%</b>
    }

    { user-balance }

    Дата реєстрації:
    <code>{ $registration_datetime }</code>

    Остання активність:
    <code>{ $last_activity_datetime }</code>

get-profile-status-icon-admin = 👮🏻

get-profile-status-icon-blacklisted = 🚫

get-profile-status-icon-premium = ⚜️

get-profile-canceled = Ви скасували отримання профілю