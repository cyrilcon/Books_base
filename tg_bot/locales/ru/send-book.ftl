send-book =
    <b>1/2</b>
    Введите <i><b>имя пользователя</b></i> или его <i><b>ID</b></i>, которому хотите отправить книгу

send-book-select-book =
    <b>2/2</b>
    Введите <i><b>артикул</b></i> книги, которую хотите отправить пользователю { $user_link } (<code>{ $id_user }</code>)

send-book-error-invalid-article =
    Артикул должен начинаться с символа <b>"#"</b> и состоять из 4 цифр!!
    Введите артикул книги ещё раз

send-book-error-article-not-found =
    Книга с таким артикулом не найдена!!
    Введите артикул существующей книги ещё раз

send-book-success = Книга "<code>{ $title }</code>" (<code>{ $article }</code>) отправлена пользователю { $user_link } (<code>{ $id_user }</code>)!!

send-book-canceled = Вы не отправили книгу пользователю