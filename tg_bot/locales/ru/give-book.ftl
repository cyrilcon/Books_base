give-book =
    <b>1/2</b>
    Введите <i><b>имя пользователя</b></i> или его <i><b>ID</b></i>, которому хотите подарить книгу

give-book-error-user-has-premium = Пользователь имеет статус { -books-base-premium } ⚜️

give-book-select-book =
    <b>2/2</b>
    Введите <i><b>артикул</b></i> книги, которую хотите подарить пользователю { $user_link } (<code>{ $id_user }</code>).

give-book-error-invalid-article =
    Артикул должен начинаться с символа <b>"#"</b> и состоять из 4 цифр!!
    Введите артикул книги ещё раз

give-book-error-article-not-found =
    Книга с таким артикулом не найдена!!
    Введите артикул существующей книги ещё раз

give-book-error-user-already-has-this-book = У пользователя уже есть книга "<code>{ $title }</code>" (<code>{ $article }</code>)!!

give-book-success = Пользователь { $user_link } (<code>{ $id_user }</code>) получил книгу "<code>{ $title }</code>" (<code>{ $article }</code>)

give-book-success-message-for-user =
    Вы получили подарок от нашего магазина { -books-base }!!
    { book-available }

give-book-canceled = Вы отменили выдачу книги пользователю