from .add_book import AddBook
from .booking import Booking
from .cancel_booking import CancelBooking
from .delete_book import DeleteBook
from .edit_book import EditBook
from .send_files import SendFiles
from .share_base import ShareBase
from .support import Support

all_states = [
    AddBook,
    Booking,
    CancelBooking,
    DeleteBook,
    EditBook,
    SendFiles,
    ShareBase,
    Support,
    None,
]
