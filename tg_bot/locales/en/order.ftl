order-book-title =
    <b>1/2</b>
    Введите <i><b>название</b></i> книги, которую хотите заказать

order-error-book-title-too-long =
    Слишком большое название книги!!
    Сократите и введите <i><b>название</b></i> книги ещё раз

order-book-error-book-already-exists = В нашей библиотеке уже есть книга со схожим названием по вашему запросу: <b>"<code>{ $title }</code>"</b> <i>{ $authors }</i> (<code>{ $article }</code>)

order-author-name =
    <b>2/2</b>
    Теперь введите <i><b>автора</b></i> книги, которую хотите заказать

order-error-author-name-too-long =
    Слишком длинное имя у автора!!
    Введите <i><b>автора</b></i> книги ещё раз

order-success-message-for-user =
    Вы заказали книгу <b>"<code>{ $book_title }</code>"</b> от автора <i>{ $author_name }</i>, спасибо за заказ!!

    Номер вашего заказа: <code>№{ $id_order }</code>

    Благодаря <b>Вам</b> наша библиотека { -books-base } расширяется!!
    Бот отправит вам книгу, как только мы обработаем ваш заказ.

order-information-template =
    { $user_link } (<code>{ $id_user }</code>)

    <b>Книга:</b> <code>{ $book_title }</code>
    <b>Автор:</b> <code>{ $author_name }</code>

    <b>Номер заказа:</b> <code>№{ $id_order }</code>

order-success = Вы получили заказ от пользователя { order-information-template }

order-canceled = Вы отменили заказ

orders-absent = Заказы отсутствуют