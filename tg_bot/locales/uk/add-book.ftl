add-book-article =
    <b>1/8</b>
    Введіть <i><b>артикул</b></i> книги, щоб додати її до бази даних

    Вільний артикул: <code>{ $free_article }</code>

add-book-error-invalid-article =
    Артикул повинен починатися з символу <b>"#"</b> і містити 4 цифри!!
    Введіть артикул книги ще раз

    Вільний артикул: <code>{ $free_article }</code>

add-book-error-article-already-exists =
    Книга з таким артикулом вже існує!!
    Введіть артикул ще раз

    Вільний артикул: <code>{ $free_article }</code>

add-book-title =
    <b>2/8</b>
    Введіть <i><b>назву</b></i> книги

add-book-title-back =
    { add-book-title }

    <code>{ $title }</code>

add-book-error-title-too-long =
    Занадто довга назва книги!!
    Скоротіть її і введіть <i><b>назву</b></i> ще раз

add-book-error-invalid-title =
    У назві книги не повинно бути <b>лапок</b>!!
    Введіть назву книги ще раз

add-book-error-title-already-exists =
    Книга з назвою <b>"{ $title }"</b> (<code>{ $article }</code>) вже існує!!

    Ви впевнені, що хочете додати книгу?

add-book-authors =
    <b>3/8</b>
    Введіть <i><b>автора(ів)</b></i>

add-book-authors-back =
    { add-book-authors }

    <code>{ $authors }</code>

add-book-error-author-name-too-long =
    Занадто довге ім'я автора!!
    Скоротіть його і введіть <i><b>автора(ів)</b></i> ще раз

add-book-error-invalid-author-name =
    У імені автора не повинно бути <b>лапок</b>!!
    Введіть ім'я автора ще раз

add-book-description =
    <b>4/8</b>
    Введіть <i><b>опис</b></i> книги

add-book-description-back =
    { add-book-description }

    <code>{ $description }</code>

add-book-error-description-too-long =
    Занадто довгий опис!!
    Скоротіть і введіть <i><b>опис</b></i> книги ще раз

add-book-genres =
    <b>5/8</b>
    Введіть <i><b>жанри</b></i> книги

add-book-error-genre-name-too-long =
    Занадто довга назва жанру!!
    Скоротіть її і введіть <i><b>жанри</b></i> книги ще раз

add-book-error-invalid-genre-name =
    У назві жанру не повинно бути <b>лапок</b>!!
    Введіть назву жанру ще раз

add-book-more-genres =
    Введіть ще <i><b>жанри</b></i> або натисніть <i>"Готово"</i>

    <b>Приклад:</b>
    { $genres }

add-book-cover =
    <b>6/8</b>
    Надішліть <i><b>фото обкладинки</b></i> книги

add-book-files =
    <b>7/8</b>
    Надішліть <i><b>файл</b></i> книги

add-book-error-file-already-sent =
    Ви вже надсилали файл цього формату!!
    Надішліть ще <i><b>файл</b></i> або натисніть <i>"Готово"</i>

    <b>Формати:</b>
    { $formats }

add-book-more-files =
    Надішліть ще <i><b>файл</b></i> або натисніть <i>"Готово"</i>

    <b>Формати:</b>
    { $formats }

add-book-select-price =
    <b>8/8</b>
    Виберіть <i><b>ціну</b></i> книги

add-book-error-caption-too-long =
    Занадто довгий текст!!
    Скоротіть опис

    <code>{ $description }</code>

    (У вас <b>{ $caption_length }</b>/1024 символів)

add-book-success = Книгу додано!!

add-book-canceled = Ви скасували додавання книги