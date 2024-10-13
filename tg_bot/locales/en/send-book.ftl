send-book =
    <b>1/2</b>
    Enter the <i><b>username</b></i> or <i><b>ID</b></i> of the user you want to send the book to

send-book-select-book =
    <b>2/2</b>
    Enter the <i><b>article</b></i> of the book you want to send to user { $user_link } (<code>{ $id_user }</code>)

send-book-error-invalid-article =
    The article must start with the character <b>"#"</b> and consist of 4 digits!!
    Please enter the article of the book again

send-book-error-article-not-found =
    The book with that article was not found!!
    Please enter the article of an existing book again

send-book-success = The book "<code>{ $title }</code>" (<code>{ $article }</code>) has been sent to user { $user_link } (<code>{ $id_user }</code>)!!

send-book-canceled = You did not send the book to the user