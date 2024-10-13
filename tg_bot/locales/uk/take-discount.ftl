take-discount = Введіть <i><b>ім'я користувача</b></i> або його <i><b>ID</b></i>, у якого хочете забрати знижку

take-discount-error-user-already-has-not-discount = Користувач { $user_link } (<code>{ $id_user }</code>) вже не мав знижки

take-discount-success =
    У користувача { $user_link } (<code>{ $id_user }</code>) { $discount ->
        [100] забрано <b>купон на безкоштовну книгу</b>
       *[other] забрано <b>знижку { $discount }%</b>
    }

take-discount-canceled = Ви не забрали знижку у користувача