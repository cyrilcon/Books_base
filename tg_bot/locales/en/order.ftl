order =
    <b>1/2</b>
    Please enter the <i><b>title</b></i> of the book you want to order

order-error-book-title-too-long =
    The book title is too long!!
    Please shorten it and enter the <i><b>title</b></i> of the book again

order-book-error-book-already-exists = We already have a book with a similar title based on your request: <b>"<code>{ $title }</code>"</b> <i>{ $authors }</i> (<code>{ $article }</code>)

order-author-name =
    <b>2/2</b>
    Now enter the <i><b>author</b></i> of the book you want to order

order-error-author-name-too-long =
    The author's name is too long!!
    Please enter the <i><b>author</b></i> of the book again

order-success =
    You have ordered the book <b>"<code>{ $book_title }</code>"</b> by author <i>{ $author_name }</i>, thank you for your order!!

    Your order number is: <code>№{ $id_order }</code>

    Thanks to <b>you</b>, our library { -books-base } is expanding!!
    The bot will send you the book as soon as we process your order.

order-information-template =
    { $user_link } (<code>{ $id_user }</code>)

    <b>Book:</b> <code>{ $book_title }</code>
    <b>Author:</b> <code>{ $author_name }</code>

    <b>Order number:</b> <code>№{ $id_order }</code>

order-success-message-for-admin = You have received an order from user { order-information-template }

order-canceled = You have canceled the order

orders-absent = No orders available