daily-action =
    Акция дня!!
    Только сегодня книга <b>50₽</b>

new-book-from-user = Добавлена новая книга по заказу пользователя!!

price = <b>Цена:</b> { $price ->
        [85] { $price }₽
       *[other] { $price }₽ <s>85₽</s>
    }

book-caption-template =
    { $intro_message }

    <b>"<code>{ $title }</code>"</b>
    <i>{ $authors }</i>

    <blockquote>{ $description }</blockquote>

    Доступные форматы: { $formats }
    { $price }
    Артикул: <code>{ $article }</code>
    { $genres }

free-with-premium = Бесплатно с { -books-base-premium } ⚜️