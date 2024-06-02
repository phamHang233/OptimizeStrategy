import time

from src.algorthisms.genetic_algorithms import GeneticAlgorithms
# from src.algorthisms.genetic_algorithms import GeneticAlgorithms
from src.algorthisms.simulated_anneal import SimulatedAnneal
from src.crawlers.uni_pool_data import get_high_low_day_price_datas

if __name__ == '__main__':
    pool = '0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640'
    protocol = 'ethereum'
    end_timestamp = int(time.time())
    start_timestamp = end_timestamp - 31 * 24 * 3600
    ga = GeneticAlgorithms(pool=pool, protocol=protocol, start_timestamp=start_timestamp,
                           end_timestamp=end_timestamp)
    ga.process()

    # pool_info = get_high_low_day_price_datas(pool, protocol, from_date=start_timestamp,
    #                                          to_date=end_timestamp)
    #
    # lowest_price = min([float(pool_info[i]['low']) for i in range(len(pool_info))])
    # highest_price = max([float(pool_info[i]['high']) for i in range(len(pool_info))])
    #
    # sa = SimulatedAnneal(pool=pool,protocol=protocol, min_price_bounds=(lowest_price, highest_price),
    #                      max_price_bounds=(lowest_price, highest_price), iterations=100,  cooling_rate=0.95)
    # best_min_price, best_max_price, best_apr = sa.simulated_annealing()
    # # In ra kết quả
    # print(f"Giá trị tối ưu: min_price = {best_min_price:.2f}, max_price = {best_max_price:.2f}, APR = {best_apr:.4f}")
