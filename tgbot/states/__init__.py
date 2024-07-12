from .add_admin import AddAdmin
from .add_blacklist import AddBlacklist
from .add_book import AddBook
from .booking import Booking
from .cancel_booking import CancelBooking
from .delete_book import DeleteBook
from .edit_book import EditBook
from .remove_admin import RemoveAdmin
from .remove_blacklist import RemoveBlacklist
from .send_files import SendFiles
from .send_message import SendMessage
from .share_base import ShareBase
from .support import Support

all_states = [
    AddAdmin,
    AddBlacklist,
    AddBook,
    Booking,
    CancelBooking,
    DeleteBook,
    EditBook,
    RemoveAdmin,
    RemoveBlacklist,
    SendFiles,
    SendMessage,
    ShareBase,
    Support,
    None,
]
