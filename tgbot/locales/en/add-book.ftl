add-book-article =
    <b>1/8</b>
    Введите <i><b>артикул</b></i> книги, чтобы добавить её в бд

    Свободный артикул: <code>{ $free_article }</code>

add-book-article-incorrect =
    Артикул должен начинаться с символа <b>"#"</b> и иметь 4 цифры!!

    Свободный артикул: <code>{ $free_article }</code>

add-book-article-already-exists =
    Книга с таким артикулом уже существует!!
    Введите артикул ещё раз

    Свободный артикул: <code>{ $free_article }</code>

add-book-title =
    <b>2/8</b>
    Введите <i><b>название</b></i> книги

add-book-title-incorrect =
    В названии книги не должно содержаться символов <b>"#"</b> и <b>"кавычек"</b>!!
    Введите название книги ещё раз

add-book-title-too-long =
    Слишком длинное название!!
    Сократите и введите название книги ещё раз

add-book-title-already-exists =
    Книга с названием <b>"{ $title }"</b> (<code>{ $article }</code>) уже существует!!

    Вы уверены, что хотите добавить книгу??

add-book-authors =
    <b>3/8</b>
    Введите <i><b>автора(ов)</b></i>

add-book-description =
    <b>4/8</b>
    Введите <i><b>описание</b></i> книги

add-book-description-too-long =
    Слишком большое описание!!
    Сократите и введите описание книги ещё раз

add-book-genres =
    <b>5/8</b>
    Введите <i><b>жанры</b></i> книги

add-book-genres-example =
    Введите ещё <i><b>жанры</b></i> или нажмите <i>"Готово"</i>

    <b>Пример:</b>
    { $ready_made_genres }

add-book-cover =
    <b>6/8</b>
    Отправьте <i><b>фото обложки</b></i> книги

add-book-files =
    <b>7/8</b>
    Отправьте <i><b>файл</b></i> книги

add-book-files-send-more =
    Отправьте ещё <i><b>файл</b></i> или нажмите <i>"Готово"</i>

    <b>Форматы:</b>
    { $formats }

add-book-files-already-sent =
    Вы уже отправляли файл этого формата!!
    Отправьте ещё <i><b>файл</b></i> или нажмите <i>"Готово"</i>

    <b>Форматы:</b>
    { $formats }

add-book-price =
    <b>8/8</b>
    Выберите <i><b>цену</b></i> книги

add-book-too-long-text =
    Слишком большой текст!!
    Сократите описание

    <code>{ $description }</code>

    (У вас <b>{ $post_text_length }</b>/1000 символов)

add-book-completed = Книга добавлена!!

add-book-cancel = Вы отменили добавление книги