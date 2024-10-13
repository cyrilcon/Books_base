daily-action =
    Акція дня!!
    Тільки сьогодні книга <b>50₽</b>

new-book-from-user = Додана нова книга за запитом користувача!!

price = <b>Ціна:</b> { $price ->
        [85] { $price }₽
       *[other] { $price }₽ <s>85₽</s>
    }

book-caption-template =
    { $intro_message }

    <b>"<code>{ $title }</code>"</b>
    <i>{ $authors }</i>

    { $description }

    Доступні формати: { $formats }
    { $price }
    Артикул: <code>{ $article }</code>
    { $genres }

free-with-premium = Безкоштовно з { -books-base-premium } ⚜️