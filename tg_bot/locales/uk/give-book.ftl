give-book =
    <b>1/2</b>
    Введіть <i><b>ім'я користувача</b></i> або його <i><b>ID</b></i>, якому хочете подарувати книгу

give-book-error-user-has-premium = Користувач має статус { -books-base-premium } ⚜️

give-book-select-book =
    <b>2/2</b>
    Введіть <i><b>артикул</b></i> книги, яку хочете подарувати користувачу { $user_link } (<code>{ $id_user }</code>).

give-book-error-invalid-article =
    Артикул повинен починатися з символу <b>"#"</b> і складатися з 4 цифр!!
    Введіть артикул книги ще раз

give-book-error-article-not-found =
    Книга з таким артикулом не знайдена!!
    Введіть артикул існуючої книги ще раз

give-book-error-user-already-has-this-book = У користувача вже є книга "<code>{ $title }</code>" (<code>{ $article }</code>)!!

give-book-success = Користувач { $user_link } (<code>{ $id_user }</code>) отримав книгу "<code>{ $title }</code>" (<code>{ $article }</code>)

give-book-success-message-for-user =
    Ви отримали подарунок від нашого магазину { -books-base }!!
    { book-available }

give-book-canceled = Ви скасували видачу книги користувачу