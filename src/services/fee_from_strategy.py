
from src.services.strategy_backtest import tokens_for_strategy, liquidity_for_strategy, calc_fees, pivot_fee_data
from src.crawlers.uni_pool_data import pool_by_id, get_pool_hour_data


def uniswap_strategy_backtest(pool, investment_amount, min_range, max_range, protocol, start_timestamp, end_timestamp):
    if min_range == max_range:
        return 0,0,0
    pool_data = pool_by_id(pool, protocol)
    hourly_price_data = get_pool_hour_data(pool, start_timestamp, end_timestamp, protocol)
    if pool_data and hourly_price_data and len(hourly_price_data) > 0:
        backtest_data = hourly_price_data[::-1]  ## thời gian từ quá khứ đến hiện tại
        # print(min_range, max_range)
        entry_price = backtest_data[0]['close']
        decimals0 = int(pool_data['token0']['decimals'])
        decimals1 = int(pool_data['token1']['decimals'])
        amount0, amount1 = tokens_for_strategy(min_range, max_range, investment_amount, float(entry_price),
                                               decimals1 - decimals0)
        liquidity = liquidity_for_strategy(float(entry_price), min_range, max_range, amount0, amount1,
                                           decimals0, decimals1)
        # unbound_liquidity = liquidity_for_strategy(float(entry_price), 1.0001 ** -887220, 1.0001 ** 887220, amount0,
        #                                            amount1, decimals0, decimals1)
        hourly_backtest = calc_fees(backtest_data, pool_data, liquidity,
                                    min_range, max_range)
        return pivot_fee_data(hourly_backtest)

def uniswap_strategy_algorithm(backtest_data, pool_data, investment_amount, min_range, max_range):
    entry_price = backtest_data[0]['close']
    decimals0 = int(pool_data['token0']['decimals'])
    decimals1 = int(pool_data['token1']['decimals'])
    amount0, amount1 = tokens_for_strategy(min_range, max_range, investment_amount, float(entry_price),
                                           decimals1 - decimals0)
    liquidity = liquidity_for_strategy(float(entry_price), min_range, max_range, amount0, amount1,
                                       decimals0, decimals1)
    # unbound_liquidity = liquidity_for_strategy(float(entry_price), 1.0001 ** -887220, 1.0001 ** 887220, amount0,
    #                                            amount1, decimals0, decimals1)
    hourly_backtest = calc_fees(backtest_data, pool_data, liquidity,
                                min_range, max_range)
    return pivot_fee_data(hourly_backtest)
# res, pivot = uniswap_strategy_backtest(pool = "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640",investment_amount= 1000, min_range=3242.17, max_range= 3721.91,
#                                             protocol='ethereum')
# print(res, pivot)
