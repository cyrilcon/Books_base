serve-order-select-order =
    <b>1/2</b>
    Enter the <i><b>order number</b></i> you want to serve

serve-order-error-invalid-order-number =
    The order number is incorrect!!
    Please enter the <i><b>order number</b></i> again

serve-order-error-order-not-found =
    Order not found!!
    Please enter the <i><b>order number</b></i> again

serve-order-select-book =
    <b>2/2</b>
    { serve-order-select-book-from-button }

    { order-information-template }

serve-order-select-book-from-button = Enter the <i><b>article</b></i> of the book you want to send to the user

serve-order-error-invalid-article =
    The article must start with the character <b>"#"</b> and have 4 digits!!
    Please enter the article of the book again

serve-order-error-article-not-found =
    No book found with that article!!
    Please enter the article of an existing book again

serve-order-error-order-already-served-or-canceled = The order has already been served or canceled!!

serve-order-success-message-for-user = Your order <code>№{ $id_order }</code>:

serve-order-success = Order <code>№{ $id_order }</code> has been served!!

serve-order-book-unavailable =
    Good day!!
    Unfortunately, we cannot serve your order (<code>№{ $id_order }</code>) due to the absence of the book "<code>{ $book_title }</code>" by author <i>{ $author_name }</i> from the supplier

    Thank you for your understanding
    Keep reading and developing!!

serve-order-message-sent = Message sent!!

serve-order-canceled = You did not serve the order