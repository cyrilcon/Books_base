order =
    <b>1/2</b>
    Введіть <i><b>назву</b></i> книги, яку хочете замовити

order-error-book-title-too-long =
    Занадто велика назва книги!!
    Сократіть та введіть <i><b>назву</b></i> книги ще раз

order-book-error-book-already-exists = У нашій бібліотеці вже є книга зі схожою назвою за вашим запитом: <b>"<code>{ $title }</code>"</b> <i>{ $authors }</i> (<code>{ $article }</code>)

order-author-name =
    <b>2/2</b>
    Тепер введіть <i><b>автора</b></i> книги, яку хочете замовити

order-error-author-name-too-long =
    Занадто довге ім’я автора!!
    Введіть <i><b>автора</b></i> книги ще раз

order-success =
    Ви замовили книгу <b>"<code>{ $book_title }</code>"</b> від автора <i>{ $author_name }</i>, дякуємо за замовлення!!

    Номер вашого замовлення: <code>№{ $id_order }</code>

    Завдяки <b>вам</b> наша бібліотека { -books-base } розширюється!!
    Бот надішле вам книгу, як тільки ми обробимо ваше замовлення.

order-information-template =
    { $user_link } (<code>{ $id_user }</code>)

    <b>Книга:</b> <code>{ $book_title }</code>
    <b>Автор:</b> <code>{ $author_name }</code>

    <b>Номер замовлення:</b> <code>№{ $id_order }</code>

order-success-message-for-admin = Ви отримали замовлення від користувача { order-information-template }

order-canceled = Ви скасували замовлення

orders-absent = Замовлення відсутні