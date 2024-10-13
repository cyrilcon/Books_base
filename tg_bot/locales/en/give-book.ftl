give-book =
    <b>1/2</b>
    Enter the <i><b>username</b></i> or <i><b>ID</b></i> of the user you want to gift a book to

give-book-error-user-has-premium = The user has { -books-base-premium } ⚜️ status

give-book-select-book =
    <b>2/2</b>
    Enter the <i><b>article</b></i> of the book you want to gift to user { $user_link } (<code>{ $id_user }</code>).

give-book-error-invalid-article =
    The article must start with the character <b>"#"</b> and consist of 4 digits!!
    Please enter the article of the book again

give-book-error-article-not-found =
    No book found with that article!!
    Please enter the article of an existing book again

give-book-error-user-already-has-this-book = The user already has the book "<code>{ $title }</code>" (<code>{ $article }</code>)!!

give-book-success = User { $user_link } (<code>{ $id_user }</code>) received the book "<code>{ $title }</code>" (<code>{ $article }</code>)

give-book-success-message-for-user =
    You received a gift from our store { -books-base }!!
    { book-available }

give-book-canceled = You canceled the book gift to the user