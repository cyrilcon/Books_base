import uuid
from dataclasses import dataclass
from aiomoney import YooMoney
from aiomoney.schemas import InvoiceSource
from config import config


@dataclass
class Payment:
    """Class to work with payments"""

    amount: int
    comment: str = None
    id: str = None

    def create(self):
        """A payment id is created"""

        self.id = str(uuid.uuid4())

    async def check_payment(self) -> bool:
        """Search for a transaction"""

        wallet = YooMoney(access_token=config.yoomoney_wallet.token)
        return await wallet.is_payment_successful(label=self.id)

    async def invoice(self) -> str:
        """Creates a product and a payment link"""

        wallet = YooMoney(access_token=config.yoomoney_wallet.token)
        payment_form = await wallet.create_invoice(
            amount_rub=self.amount,
            label=self.id,
            payment_source=InvoiceSource.YOOMONEY_WALLET,
            success_redirect_url=config.tg_bot.link,
        )
        return payment_form.url
