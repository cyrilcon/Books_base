from __future__ import annotations

import asyncio
import logging
import ssl
from typing import TYPE_CHECKING, Any, Union, List
from typing import Type, TypeVar, Generic, Optional

import backoff
from aiohttp import ClientError, ClientSession, TCPConnector, FormData
from pydantic import BaseModel, TypeAdapter
from ujson import dumps, loads

if TYPE_CHECKING:
    from collections.abc import Mapping

    from yarl import URL

ACCEPTABLE_STATUS_CODES = {200, 201, 204, 404, 409}


# Taken from here: https://github.com/Olegt0rr/WebServiceTemplate/blob/main/app/core/base_client.py
class BaseClient:
    """Represents base API client."""

    def __init__(self, base_url: str | URL) -> None:
        self._base_url = base_url
        self._session: ClientSession | None = None
        self.log = logging.getLogger(self.__class__.__name__)

    async def _get_session(self) -> ClientSession:
        """Get aiohttp session with cache."""
        if self._session is None:
            ssl_context = ssl.SSLContext()
            connector = TCPConnector(ssl_context=ssl_context)
            self._session = ClientSession(
                base_url=self._base_url,
                connector=connector,
                json_serialize=dumps,
            )

        return self._session

    @backoff.on_exception(
        backoff.expo,
        ClientError,
        max_time=10,
    )
    async def make_request(
        self,
        method: str,
        url: str | URL,
        params: Mapping[str, Union[str, int]] | None = None,
        json: Mapping[str, Union[str, int]] | None = None,
        headers: Mapping[str, Union[str, int]] | None = None,
        data: FormData | None = None,
    ) -> tuple[int, dict[str, Any]]:
        """Make request and return decoded json response."""
        session = await self._get_session()

        self.log.debug(
            "Making request %r %r with json %r and params %r",
            method,
            url,
            json,
            params,
        )
        async with session.request(
            method, url, params=params, json=json, headers=headers, data=data
        ) as response:
            status = response.status
            if status not in ACCEPTABLE_STATUS_CODES:
                s = await response.text()
                raise ClientError(f"Got status {status} for {method} {url}: {s}")
            try:
                result = await response.json(loads=loads)
            except Exception as e:
                self.log.exception(e)
                self.log.info(f"{await response.text()}")
                result = {}

        self.log.debug(
            "Got response %r %r with status %r and json %r",
            method,
            url,
            status,
            result,
        )
        return status, result

    async def close(self) -> None:
        """Graceful session close."""
        if not self._session:
            self.log.debug("There's not session to close.")
            return

        if self._session.closed:
            self.log.debug("Session already closed.")
            return

        await self._session.close()
        self.log.debug("Session successfully closed.")

        # Wait 250 ms for the underlying SSL connections to close
        # https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
        await asyncio.sleep(0.25)


T = TypeVar("T", bound=BaseModel)


class ApiResponse(Generic[T]):
    def __init__(self, status: int, result: Any, model: Optional[Type[T]] = None):
        self.status = status
        self._result = result
        self._model = model
        self._parsed_result = None

    @property
    def result(self) -> Any:
        """Returns the raw data received from the API."""

        return self._result

    def get_model(self) -> Union[T, List[T]]:
        """Returns the result as a Pydantic model, if a model was specified."""

        if self._parsed_result is not None:
            return self._parsed_result

        if self._model:
            if isinstance(self._result, list):
                adapter = TypeAdapter(List[self._model])
                self._parsed_result = adapter.validate_python(self._result)
            else:
                adapter = TypeAdapter(self._model)
                self._parsed_result = adapter.validate_python(self._result)
            return self._parsed_result

        raise TypeError("Model not provided, or result is not a list or dict!!")
