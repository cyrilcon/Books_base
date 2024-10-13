get-profile = Введите <i><b>имя пользователя</b></i> или его <i><b>ID</b></i>, информацию о котором вы хотите получить

get-profile-template =
    { $status_icons } { $user_link } (<code>{ $id_user }</code>) { $language_code ->
        [en] 🇬🇧
        [uk] 🇺🇦
        [ru] 🇷🇺
       *[other] 🏳️ <code>{ $language_code }</code>
    }

    { $discount ->
        [100] Имеет купон на бесплатную книгу
        [0] Не имеет никаких скидок
       *[other] Имеет скидку <b>{ $discount }%</b>
    }
    
    { user-balance }

    Дата регистрации:
    <code>{ $registration_datetime }</code>

    Последняя активность:
    <code>{ $last_activity_datetime }</code>

get-profile-status-icon-admin = 👮🏻

get-profile-status-icon-blacklisted = 🚫

get-profile-status-icon-premium = ⚜️

get-profile-canceled = Вы отменили получение профиля