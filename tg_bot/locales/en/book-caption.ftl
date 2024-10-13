daily-action =
    Deal of the Day!!
    Today only, the book is <b>50₽</b>

new-book-from-user = A new book has been added at the user's request!!

price = <b>Price:</b> { $price ->
        [85] { $price }₽
       *[other] { $price }₽ <s>85₽</s>
    }

book-caption-template =
    { $intro_message }

    <b>"<code>{ $title }</code>"</b>
    <i>{ $authors }</i>

    { $description }

    Available formats: { $formats }
    { $price }
    Article number: <code>{ $article }</code>
    { $genres }

free-with-premium = Free with { -books-base-premium } ⚜️