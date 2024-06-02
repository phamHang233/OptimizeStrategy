import time
from multiprocessing import Pool
import random

import numpy as np

from src.crawlers.uni_pool_data import pool_by_id, get_high_low_day_price_datas, get_pool_hour_data
from src.services.fee_from_strategy import uniswap_strategy_algorithm


class GeneticAlgorithms:
    '''
    Class representing individual in population
    '''

    def __init__(self, pool, protocol, start_timestamp, end_timestamp):
        self.max_price = 0
        self.min_price = 0
        self.pool = pool
        self.protocol = protocol
        self.generations = 10  # Số thế hệ
        self.crossover_rate = 0.8  # Tỷ lệ giao phối
        self.mutation_rate = 0.2  # Tỷ lệ đột biến
        # Tạo quần thể ban đầu
        self.pool_data = pool_by_id(pool, protocol)
        self.population_size = 200
        self.end_timestamp = end_timestamp
        self.start_timestamp = start_timestamp
        self.pool_hour_data = get_pool_hour_data(pool, start_timestamp, end_timestamp, protocol)[::-1]

    def selection(self, population, fitnesses):
        # Chọn số lượng cha mẹ cần thiết
        num_parents = 60  # Điều chỉnh số lượng cha mẹ theo nhu cầu
        positive_fitnesses, negative_fitness= [], []
        positive_population, negative_population = [], []
        # Tính tổng độ phù hợp
        for id, fit in enumerate(fitnesses):
            if fit > 0:
                positive_fitnesses.append(fit)
                positive_population.append(population[id])
            else:
                negative_fitness.append(fit)
                negative_population.append(population[id])

        total_fitness = sum(positive_fitnesses)
        # Tính xác suất chọn của mỗi cá thể
        selection_probs = [fitness / total_fitness for fitness in positive_fitnesses]

        positive_number = len(positive_fitnesses)
        if positive_number < num_parents:
            parents = positive_population

            abs_negative_fitness = [abs(fit) for fit in negative_fitness]
            total_negative_fitness = sum(abs_negative_fitness)
            neg_selection_probs = [1 - (fitness / total_negative_fitness) for fitness in abs_negative_fitness]
            selected_index = np.random.choice(len(negative_fitness), p=neg_selection_probs, size=num_parents-positive_number, replace=False)
            parents.append([negative_population[id] for id in selected_index])
        else:
            # Chọn ngẫu nhiên các cá thể dựa trên xác suất
            selected_index = np.random.choice(len(positive_fitnesses), p=selection_probs, size=num_parents,
                                              replace=False)
            parents = [positive_population[id] for id in selected_index]
        return parents

    def crossover(self, parents):
        offspring = []

        # Chọn ngẫu nhiên hai cặp cha mẹ
        selected_parents = random.sample(parents, 2)

        # Lai hai cặp cha mẹ đã chọn
        parent1 = selected_parents[0]
        parent2 = selected_parents[1]

        # Lai tuyến tính cho mỗi gen
        alpha = random.random()
        new_min_value = (parent1[0] * (1 - alpha) + alpha * parent2[0])
        new_max_value = (parent1[1] * (1 - alpha) + alpha * parent2[1])
        offspring.append([new_min_value, new_max_value])

        return offspring

    def generate_offspring(self, parents):
        offspring = []

        # Lặp lại quy trình lai tạo cho đến khi tạo ra đủ số lượng cá thể con
        while len(offspring) < self.population_size:
            new_offspring = self.crossover(parents)
            offspring.extend(new_offspring)

        return offspring

    # Hàm đột biến (Bit flip mutation)
    def mutation(self, offspring):
        for chromosome in offspring:
            if random.random() < self.mutation_rate:
                maximum_price_change = min(chromosome[1] - chromosome[0], chromosome[0] - self.min_price)
                delta = random.uniform(-maximum_price_change, maximum_price_change) * 0.5

                # Đột biến min price
                new_value = chromosome[0] + delta

                if new_value < self.min_price:
                    print("MUTATION ERROR!!")
                else:
                    # Giữ giá trị  nếu hợp lệ
                    chromosome[0] = new_value

            if random.random() < self.mutation_rate:
                maximun_price_change = min(chromosome[1] - chromosome[0], self.max_price - chromosome[1])
                delta = random.uniform(-maximun_price_change, maximun_price_change) * 0.5
                # Đột biến max price
                new_value = chromosome[1] + delta
                if new_value > self.max_price:
                    print("MUTATION ERROR!!")
                else:
                    # Giữ giá trị  nếu hợp lệ
                    chromosome[1] = new_value
            if chromosome[0] > chromosome[1]:
                chromosome = chromosome[::-1]

        return offspring

    def fitness_worker(self, data):
        """Hàm thực thi trong mỗi luồng."""
        min_range = data[0]
        max_range = data[1]
        if min_range > max_range:
            print("ERROR: MIN > MAX")
        data = uniswap_strategy_algorithm(
            pool_data=self.pool_data, backtest_data=self.pool_hour_data, investment_amount=1000,
            min_range=min_range, max_range=max_range)
        apr = data['apr']
        return apr

    def process(self):
        pool_info = get_high_low_day_price_datas(self.pool, self.protocol, from_date=self.start_timestamp,
                                                 to_date=self.end_timestamp)
        population = []

        self.min_price = min([float(pool_info[i]['low']) for i in range(len(pool_info))])
        self.max_price = max([float(pool_info[i]['high']) for i in range(len(pool_info))])
        for _ in range(self.population_size):
            min_range = random.uniform(self.min_price, self.max_price)
            max_range = random.uniform(min_range, self.max_price)  # Giữ max_range lớn hơn min_range
            population.append([min_range, max_range])

        # Lặp lại qua các thế hệ
        for generation in range(self.generations):
            print(f'generation {generation}')
            with Pool() as pool:
                # Gửi yêu cầu tính toán fitness cho các luồng
                fitnesses = pool.map(self.fitness_worker, population)

            print('finish cal fitness')
            best_index = fitnesses.index(max(fitnesses))
            best_chromone = population[best_index]
            data = uniswap_strategy_algorithm(
                pool_data=self.pool_data, backtest_data=self.pool_hour_data, investment_amount=1000,
                min_range=best_chromone[0], max_range=best_chromone[1])

            print(
                f'the best apr in generation {generation}st: {data.get("apr")} - {data["timeInRange"]}')
            print(f'the best range in generation {generation}st: {best_chromone}')
            print(len([i for i in fitnesses if i > 0]))

            parents = self.selection(population, fitnesses)

            # Giao phối và tạo ra con cái
            offspring = self.generate_offspring(parents)

            # Đột biến
            offspring = self.mutation(offspring)

            # Tạo quần thể mới
            population = offspring + parents

# def convert_tick_to_price(tick, decimals0, decimals1):
#     return 1 / (1.0001 ** tick / 10 ** (decimals1 - decimals0))
#
#
# def convert_price_to_tick(price, decimals0, decimals1):
#     return int(math.log(1 / price * 10 ** (decimals1 - decimals0), 1.0001))
