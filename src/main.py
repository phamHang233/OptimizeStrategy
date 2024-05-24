from src.algorthisms.genetic_algorithms import GeneticAlgorithms

if __name__ == '__main__':
    ga = GeneticAlgorithms(pool='0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640', protocol='ethereum')
    ga.process()