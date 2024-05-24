start-text =
    Hi{ $additional_text }!!
    Write the title or article of the book to buy or familiarize yourself with the product

book-does-not-exist =
    Запрашиваемая вами книга с артикулом <b>{ $article }</b> больше не доступна :(



search-found = Найдено несколько книг по запросу <b>"{ $request }"</b>:

search-not-found =
    По запросу <b>"{ $request }"</b> ничего не найдено

    Введите более точное название книги или выберите другой способ поиска



add-book-article =
    <b>1/8</b>
    Введите <i><b>артикул</b></i> книги, чтобы добавить её в бд

    Свободный артикул: <code>{ $free_article }</code>

add-book-incorrect-article =
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

add-book-complete = Книга добавлена!!

add-book-cancel = Вы отменили добавление книги



daily-action =
    Акция дня!!
    Только сегодня книга <b>50₽</b>

new-book-from-user = Добавлена новая книга по заказу пользователя!!

full-book-description =
    { $introductory_text }

    "<code><b>{ $title }</b></code>"
    <i>{ $authors }</i>

    { $description }

    Доступные форматы: { $formats }

    <b>Цена:</b> { $price }

    Артикул: <code>{ $article }</code>
    { $genres }



delete-book = Введите <i><b>артикул</b></i>, чтобы удалить книгу

delete-book-incorrect-article = Артикул должен начинаться с символа <b>"#"</b> и иметь 4 цифры!!

delete_book-not-found = Книга не найдена

delete-book-successful-deleted = Книга <i>"{ $title }"</i> (<code>{ $id_book }</code>) успешно удалена

delete-book-cancel = Вы отменили удаление книги



edit-book-select = Введите <i><b>артикул</b></i>, чтобы изменить данные о книге

edit-book-incorrect-article = Артикул должен начинаться с символа <b>"#"</b> и иметь 4 цифры!!

edit-book-does-not-exist =
    Книги с артикулом <b>{ $article }</b> не существует!!

edit-book-article =
    Введите новый <i><b>артикул</b></i>

    Текущий артикул: <code>{ $article }</code>

edit-book-article-already-exists =
    Книга с таким артикулом уже существует!!
    Введите артикул ещё раз

edit-book-title =
    Введите новое <i><b>название</b></i> книги

    Текущее название: <code>{ $title }</code>

edit-book-title-too-long =
    Слишком длинное название!!
    Сократите и введите название книги ещё раз

edit-book-authors =
    Введите нового <i><b>автора</b></i>

    Текущий автор: <code>{ $authors }</code>

edit-book-description =
    Введите новое <i><b>описание</b></i>

    Текущее описание:
    <code>{ $description }</code>

edit-book-description-too-long =
    Слишком большое описание!!
    Сократите и введите описание книги ещё раз

edit-book-genres =
    Введите новые <i><b>жанры</b></i>

    Текущие жанры:
    <code>{ $genres }</code>

edit-book-cover = Отправьте новое <i><b>фото обложки</b></i> книги

edit-book-too-long-text =
    Слишком большой текст!!
    (У вас <b>{ $post_text_length }</b>/1000 символов)

edit-book-files = Отправьте новый <i><b>файл</b></i> книги

edit-book-files-send-more =
    Отправьте ещё <i><b>файл</b></i> или нажмите <i>"Готово"</i>

    <b>Изменённые форматы:</b>
    { $formats }

edit-book-price = Выберите новую <i><b>цену</b></i> книги

edit-book-successfully-changed = Данные успешно изменены!!

edit-book-cancel = Вы отменили изменение данных о книге



booking-title =
    <b>1/2</b>
    Введите <i><b>название</b></i> книги, которой хотите заказать

booking-title-too-long =
    Слишком большое название книги!!
    Введите <i><b>название</b></i> книги ещё раз

booking-title-already-exists = В нашей библиотеке уже есть книга со схожим названием по вашему запросу: "<code>{ $title }</code>" <i>{ $authors }</i> (<code>{ $article }</code>)

booking-author =
    <b>2/2</b>
    Теперь введите <i><b>автора</b></i> книги, которой хотите заказать

booking-author-too-long =
    Слишком длинное имя у автора!!
    Введите <i><b>автора</b></i> книги ещё раз

booking-complete =
    Вы заказали книгу "<code>{ $title }</code>" от автора <i>{ $author }</i>, спасибо за заказ!!
    Номер вашего заказа: <code>№{ $id_booking }</code>

    Благодаря <b>Вам</b> наша библиотека Books_Base расширяется!!
    Мы обработаем ваш заказ за 24 часа, обычно это происходит гораздо быстрее.

booking-from-user =
    Вы получили заказ от пользователя
    { $url_user } (<code>{ $id_user }</code>)

    <b>Книга:</b> <code>{ $title }</code>
    <b>Автор:</b> <code>{ $author }</code>

    <b>Номер заказа:</b> <code>№{ $id_booking }</code>

booking-cancel = Вы отменили заказ



pagination-info =
    Это страница { $page } из { $all_pages } результатов поиска.

    Используйте стрелки вправо/влево для навигации между страницами.

    Чтобы ознакомиться с конкретной книгой, нажмите на её номер.

button-back = « Назад

button-cancel = Отмена

button-post = Опубликовать

button-done = Готово

button-clear = Стереть

button-do-not-publish = Не публиковать

button-not-from-a-user = Не от пользователя

button-edit-book-article = Артикул

button-edit-book-title = Название

button-edit-book-authors = Авторы

button-edit-book-descriptions = Описание

button-edit-book-genres = Жанры

button-edit-book-cover = Обложка

button-edit-book-files = Файлы

button-edit-book-price = Цена

button-yes = Да

button-show-book = Показать книгу

button-booking = Всё равно заказать

button-service = Обслужить

button-not-available = Нет в наличии

button-booking-again = Заказать ещё



error = Произошла ошибка :(