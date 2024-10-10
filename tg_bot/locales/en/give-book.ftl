give-book =
    <b>1/2</b>
    Введите <i><b>имя пользователя</b></i> или его <i><b>ID</b></i>, которому хотите подарить книгу

give-book-error-user-has-premium = Пользователь имеет статус { -books-base-premium } ⚜️

give-book-select-book =
    <b>2/2</b>
    Введите <i><b>артикул</b></i> книги, которой хотите подарить пользователю { $user_link } (<code>{ $id_user }</code>).

give-book-error-invalid-article =
    Артикул должен начинаться с символа <b>"#"</b> и иметь 4 цифры!!
    Введите артикул книги ещё раз

give-book-error-article-not-found =
    Книга с таким артикулом не найдена!!
    Введите артикул существуюшей книги ещё раз

give-book-error-user-already-has-this-book = У пользователя уже есть книга "<code>{ $title }</code>" (<code>{ $article }</code>)!!

give-book-success = Пользователь { $user_link } (<code>{ $id_user }</code>) получил книгу "<code>{ $title }</code>" (<code>{ $article }</code>)

give-book-success-message-for-user =
    Вы получили подарок от нашего магазина { -books-base }!!
    Книга "<code>{ $title }</code>" доступна в вашей личной книжной полке — /my_books

give-book-canceled = Вы отменили выдачу книги пользователю