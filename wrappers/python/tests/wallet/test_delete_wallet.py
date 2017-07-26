from indy import IndyError
from indy import wallet
from indy.error import ErrorCode

from ..utils import storage

import pytest
import logging

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.asyncio
async def test_delete_wallet_works(cleanup_storage):
    wallet_name = 'wallet1'
    await wallet.create_wallet('pool1', wallet_name, None, None, None)
    await wallet.delete_wallet(wallet_name, None)
    await wallet.create_wallet('pool1', wallet_name, None, None, None)


@pytest.mark.asyncio
async def test_delete_wallet_works_for_closed(cleanup_storage):
    wallet_name = 'wallet2'
    await wallet.create_wallet('pool1', wallet_name, None, None, None)
    wallet_handle = await wallet.open_wallet(wallet_name, None, None)
    await wallet.close_wallet(wallet_handle)
    await wallet.delete_wallet(wallet_name, None)
    await wallet.create_wallet('pool1', wallet_name, None, None, None)


@pytest.mark.skip(reason="There is BUG in indy-sdk")
async def test_delete_wallet_works_for_opened(cleanup_storage):
    with pytest.raises(IndyError) as e:
        wallet_name = 'wallet_for_opened'
        await wallet.create_wallet('pool1', wallet_name, None, None, None)
        await wallet.open_wallet(wallet_name, None, None)
        await wallet.delete_wallet(wallet_name, None)
    assert ErrorCode.CommonIOError == e.value.error_code


@pytest.mark.asyncio
async def test_delete_wallet_works_for_twice(cleanup_storage):
    with pytest.raises(IndyError) as e:
        wallet_name = 'wallet_for_twice'
        await wallet.create_wallet('pool1', wallet_name, None, None, None)
        await wallet.delete_wallet(wallet_name, None)
        await wallet.delete_wallet(wallet_name, None)
    assert ErrorCode.CommonIOError == e.value.error_code


@pytest.mark.asyncio
async def test_delete_wallet_works_for_not_created(cleanup_storage):
    with pytest.raises(IndyError) as e:
        wallet_name = 'wallet_not_created'
        await wallet.delete_wallet(wallet_name, None)
    assert ErrorCode.CommonIOError == e.value.error_code