serve-order-prompt-select-order =
    <b>1/2</b>
    Введите <i><b>номер заказа</b></i>, которому хотите обслужить

serve-order-error-invalid-order-number =
    Номер заказа некорректен!!
    Введите <i><b>номер заказа</b></i> ещё раз

serve-order-error-order-not-found =
    Заказ не найден!!
    Введите <i><b>номер заказа</b></i> ещё раз

serve-order-prompt-select-book =
    <b>2/2</b>
    Введите <i><b>артикул</b></i> книги, которой хотите отправить пользователю.

    { order-information-template }

serve-order-prompt-select-book-from-button = Введите <i><b>артикул</b></i> книги, которой хотите отправить пользователю.

serve-order-error-invalid-article =
    Артикул должен начинаться с символа <b>"#"</b> и иметь 4 цифры!!
    Введите артикул книги ещё раз

serve-order-error-article-not-found =
    Книга с таким артикулом не найдена!!
    Введите артикул существуюшей книги ещё раз

serve-order-error-order-already-served = Заказ уже обслужен или отменён!!

serve-order-served = Ваш заказ <code>№{ $id_order }</code>:

serve-order-success = Заказ <code>№{ $id_order }</code> обслужен!!

serve-order-book-unavailable-message-template =
    Добрый день!!
    К сожалению, мы не можем обслужить ваш заказ (<code>№{ $id_order }</code>), по причине – отсутствие книги "<code>{ $book_title }</code>" автора <i>{ $author_name }</i> у поставщика.

    Спасибо за понимание.
    Читайте и развиватесь!!

serve-order-message-sent = Сообщение отправлено!!

serve-order-canceled = Вы не обслужили заказ
