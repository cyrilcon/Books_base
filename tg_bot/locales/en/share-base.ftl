share-base =
    <b>1/2</b>
    Enter the <i><b>username</b></i> or <i><b>link</b></i> to your friend on Telegram to share <i><b>base</b></i> 💎 with them.

    <i>(The username starts with the symbol "<code>@</code>", for example: <b>@durov</b>. The link can look like this: t.me/durov)</i>

share-base-error-invalid-username =
    Your message does not contain a <i><b>username</b></i> or a <i><b>link</b></i> to it!!
    Please enter the <i><b>username</b> (which starts with the symbol "<code>@</code>")</i> or a <i><b>link</b></i> to your friend on Telegram again.

share-base-error-self-transfer =
    You cannot send <i><b>base</b></i> to yourself!!
    Please enter your friend's username or link again

share-base-error-user-not-found = User <b>@{ $username }</b> has not visited our store yet!!

share-base-error-user-has-premium =
    You cannot transfer <i><b>base</b></i>!!
    User <b>@{ $username }</b> has a status of { -books-base-premium } ⚜️

share-base-transfer =
    <b>2/2</b>
    How much <i><b>base</b></i> do you want to send to user <b>@{ $username }</b>??

    { base-balance }

share-base-error-insufficient-funds = You do not have enough <i><b>base</b></i> to send to @{ $username }!!

share-base-error-general =
    An error occurred while sending <i><b>base</b></i>!!
    The recipient may have blocked the bot

    Please try again later

share-base-success =
    You have successfully sent { $base_received } <i><b>base</b></i> 💎 to user <b>@{ $username }</b>!!

    { base-balance }

share-base-success-message-for-user =
    You have received { $base_received } <i><b>base</b></i> 💎 from user { $user_link }!!

    { base-balance }

share-base-success-message-for-admin =
    User { $user_link_sender } (<code>{ $id_user_sender }</code>) transferred { $base_received } <i><b>base</b></i> 💎 to user { $user_link_recipient } (<code>{ $id_user_recipient }</code>)

    Balance of { $user_link_sender }: <b>{ $sender_base_balance } <i>base</i></b> 💎
    Balance of { $user_link_recipient }: <b>{ $recipient_base_balance } <i>base</i></b> 💎

share-base-canceled = You have canceled the sending of base

share-base-unprocessed-messages = Choose the amount of <b><i>base</i></b> you want to send to the user, or cancel the action