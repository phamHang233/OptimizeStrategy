import time

from src.databases.mongodb_klg import MongoDB

max_return = 0
max_nft = None

def backtest(pool_address, chain_id):
    klg = MongoDB()
    now = time.time()
    cursor = klg.get_nfts_by_pool(chain_id, pool_address)
    for doc in cursor:
        token_id = doc['tokenId']
        liquidity_change_logs = doc['liquidityChangeLogs']
        for timestamp, amount in liquidity_change_logs.items():
            if timestamp > now - 24 * 30 * 3600:
                continue
        collected_fee = doc['collectedFee']
        liquidity = doc['liquidity']
        if


