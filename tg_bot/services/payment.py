import uuid
from dataclasses import dataclass

from yoomoney import Quickpay, Client

from tg_bot.config import config


@dataclass
class Payment:
    """Class to work with payments"""

    amount: float
    comment: str = None
    id: str = None

    def create(self):
        """A payment id is created"""

        self.id = str(uuid.uuid4())

    def check_payment(self):
        """Search for a transaction"""

        client = Client(config.yoomoney_wallet.token)
        history = client.operation_history(label=self.id)
        for operation in history.operations:
            if str(self.id) == operation.label:
                return True

    @property
    def invoice(self):
        """Creates a product and a payment link"""

        quick_pay = Quickpay(
            receiver=config.yoomoney_wallet.number,
            quickpay_form="shop",
            targets=f"Books_base",
            paymentType="SB",
            sum=self.amount,
            label=f"{self.id}",
            comment=self.comment,
            successURL=config.channel.link,
        )
        link = quick_pay.base_url

        return link
