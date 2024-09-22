add-book-prompt-article =
    <b>1/8</b>
    Введите <i><b>артикул</b></i> книги, чтобы добавить её в бд

    Свободный артикул: <code>{ $free_article }</code>

add-book-error-invalid-article =
    Артикул должен начинаться с символа <b>"#"</b> и иметь 4 цифры!!
    Введите артикул книги ещё раз

    Свободный артикул: <code>{ $free_article }</code>

add-book-error-article-already-exists =
    Книга с таким артикулом уже существует!!
    Введите артикул ещё раз

    Свободный артикул: <code>{ $free_article }</code>

add-book-prompt-title =
    <b>2/8</b>
    Введите <i><b>название</b></i> книги

add-book-error-title-too-long =
    Слишком большое название книги!!
    Сократите и введите <i><b>название</b></i> книги ещё раз

add-book-error-invalid-title =
    В названии книги не должно содержаться символов <b>"кавычек"</b>!!
    Введите название книги ещё раз

add-book-error-title-already-exists =
    Книга с названием <b>"{ $title }"</b> (<code>{ $article }</code>) уже существует!!

    Вы уверены, что хотите добавить книгу??

add-book-prompt-authors =
    <b>3/8</b>
    Введите <i><b>автора(ов)</b></i>

add-book-error-author-name-too-long =
    Слишком длинное имя у автора!!
    Сократите и введите <i><b>автора(ов)</b></i> ещё раз

add-book-error-invalid-author-name =
    В имени автора не должно содержаться символов <b>"кавычек"</b>!!
    Введите имя автора ещё раз

add-book-prompt-description =
    <b>4/8</b>
    Введите <i><b>описание</b></i> книги

add-book-error-description-too-long =
    Слишком большое описание!!
    Сократите и введите <i><b>описание</b></i> книги ещё раз

add-book-prompt-genres =
    <b>5/8</b>
    Введите <i><b>жанры</b></i> книги

add-book-error-genre-name-too-long =
    Слишком динное название жанра!!
    Сократите и введите <i><b>жанры</b></i> книги ещё раз

add-book-error-invalid-genre-name =
    В названии жанра не должно содержаться символов <b>"кавычек"</b>!!
    Введите название жанра ещё раз

add-book-prompt-more-genres =
    Введите ещё <i><b>жанры</b></i> или нажмите <i>"Готово"</i>

    <b>Пример:</b>
    { $genres }

add-book-prompt-cover =
    <b>6/8</b>
    Отправьте <i><b>фото обложки</b></i> книги

add-book-prompt-files =
    <b>7/8</b>
    Отправьте <i><b>файл</b></i> книги

add-book-error-file-already-sent =
    Вы уже отправляли файл этого формата!!
    Отправьте ещё <i><b>файл</b></i> или нажмите <i>"Готово"</i>

    <b>Форматы:</b>
    { $formats }

add-book-prompt-more-files =
    Отправьте ещё <i><b>файл</b></i> или нажмите <i>"Готово"</i>

    <b>Форматы:</b>
    { $formats }

add-book-select-price =
    <b>8/8</b>
    Выберите <i><b>цену</b></i> книги

add-book-error-caption-too-long =
    Слишком большой текст!!
    Сократите описание

    <code>{ $description }</code>

    (У вас <b>{ $caption_length }</b>/1024 символов)

add-book-success = Книга добавлена!!

add-book-canceled = Вы отменили добавление книги