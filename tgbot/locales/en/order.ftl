order-step-1-book-title =
    <b>1/2</b>
    Введите <i><b>название</b></i> книги, которую хотите заказать

order-error-book-title-too-long =
    Слишком большое название книги!!
    Сократите и введите <i><b>название</b></i> книги ещё раз

order-book-title-exists = В нашей библиотеке уже есть книга со схожим названием по вашему запросу: <b>"<code>{ $book-title }</code>"</b> <i>{ $authors }</i> (<code>{ $article }</code>)

order-error-book-not-exist = Запрашиваемая вами книга с артикулом <code>{ $article }</code> больше не доступна 😕

order-step-2-author-name =
    <b>2/2</b>
    Теперь введите <i><b>автора</b></i> книги, которую хотите заказать

order-error-author-name-too-long =
    Слишком длинное имя у автора!!
    Введите <i><b>автора</b></i> книги ещё раз

order-success =
    Вы заказали книгу <b>"<code>{ $book_title }</code>"</b> от автора <i>{ $author_name }</i>, спасибо за заказ!!

    Номер вашего заказа: <code>№{ $id_order }</code>

    Благодаря <b>Вам</b> наша библиотека Books_Base расширяется!!
    Бот отправит вам книгу, как только мы обработаем ваш заказ.

order-information-template =
    { $user_link } (<code>{ $id_user }</code>)

    <b>Книга:</b> <code>{ $book_title }</code>
    <b>Автор:</b> <code>{ $author_name }</code>

    <b>Номер заказа:</b> <code>№{ $id_order }</code>

order-received-from-user =
    Вы получили заказ от пользователя
    { order-information-template }

order-canceled = Вы отменили заказ

orders-absent = Заказы отсутствуют

order-error-incorrect-number =
    Номер заказа некорректен!!
    Введите <i><b>номер заказа</b></i> ещё раз

order-error-not-found =
    Такого заказа не существует!!
    Введите <i><b>номер заказа</b></i> ещё раз