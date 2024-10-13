add-book-article =
    <b>1/8</b>
    Enter the <i><b>article code</b></i> of the book to add it to the database

    Available article: <code>{ $free_article }</code>

add-book-error-invalid-article =
    The article code must start with the symbol <b>"#"</b> and contain 4 digits!!
    Enter the article code again

    Available article: <code>{ $free_article }</code>

add-book-error-article-already-exists =
    A book with this article code already exists!!
    Enter the article code again

    Available article: <code>{ $free_article }</code>

add-book-title =
    <b>2/8</b>
    Enter the <i><b>title</b></i> of the book

add-book-title-back =
    { add-book-title }

    <code>{ $title }</code>

add-book-error-title-too-long =
    The book title is too long!!
    Shorten it and enter the <i><b>title</b></i> again

add-book-error-invalid-title =
    The book title must not contain <b>quotation marks</b>!!
    Enter the book title again

add-book-error-title-already-exists =
    A book with the title <b>"{ $title }"</b> (<code>{ $article }</code>) already exists!!

    Are you sure you want to add the book?

add-book-authors =
    <b>3/8</b>
    Enter the <i><b>author(s)</b></i>

add-book-authors-back =
    { add-book-authors }

    <code>{ $authors }</code>

add-book-error-author-name-too-long =
    The author's name is too long!!
    Shorten it and enter the <i><b>author(s)</b></i> again

add-book-error-invalid-author-name =
    The author's name must not contain <b>quotation marks</b>!!
    Enter the author's name again

add-book-description =
    <b>4/8</b>
    Enter the <i><b>description</b></i> of the book

add-book-description-back =
    { add-book-description }

    <code>{ $description }</code>

add-book-error-description-too-long =
    The description is too long!!
    Shorten it and enter the <i><b>description</b></i> again

add-book-genres =
    <b>5/8</b>
    Enter the <i><b>genres</b></i> of the book

add-book-error-genre-name-too-long =
    The genre name is too long!!
    Shorten it and enter the <i><b>genres</b></i> again

add-book-error-invalid-genre-name =
    The genre name must not contain <b>quotation marks</b>!!
    Enter the genre name again

add-book-more-genres =
    Enter more <i><b>genres</b></i> or press <i>"Done"</i>

    <b>Example:</b>
    { $genres }

add-book-cover =
    <b>6/8</b>
    Send the <i><b>cover photo</b></i> of the book

add-book-files =
    <b>7/8</b>
    Send the <i><b>file</b></i> of the book

add-book-error-file-already-sent =
    You've already sent a file of this format!!
    Send another <i><b>file</b></i> or press <i>"Done"</i>

    <b>Formats:</b>
    { $formats }

add-book-more-files =
    Send another <i><b>file</b></i> or press <i>"Done"</i>

    <b>Formats:</b>
    { $formats }

add-book-select-price =
    <b>8/8</b>
    Select the <i><b>price</b></i> of the book

add-book-error-caption-too-long =
    The text is too long!!
    Shorten the description

    <code>{ $description }</code>

    (You have <b>{ $caption_length }</b>/1024 characters)

add-book-success = The book has been added!!

add-book-canceled = You have canceled the book addition