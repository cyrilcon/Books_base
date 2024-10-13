send-book =
    <b>1/2</b>
    Введіть <i><b>ім'я користувача</b></i> або його <i><b>ID</b></i>, якому хочете надіслати книгу

send-book-select-book =
    <b>2/2</b>
    Введіть <i><b>артикул</b></i> книги, яку хочете надіслати користувачу { $user_link } (<code>{ $id_user }</code>)

send-book-error-invalid-article =
    Артикул має починатися з символа <b>"#"</b> і складатися з 4 цифр!!
    Введіть артикул книги ще раз

send-book-error-article-not-found =
    Книга з таким артикулом не знайдена!!
    Введіть артикул існуючої книги ще раз

send-book-success = Книга "<code>{ $title }</code>" (<code>{ $article }</code>) надіслана користувачу { $user_link } (<code>{ $id_user }</code>)!!

send-book-canceled = Ви не надіслали книгу користувачу