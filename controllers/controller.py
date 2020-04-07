import operator

from scrapper.web_scrapper import WebScrapper
from text_analyzer.analyzer import TextAnalyzer, WordFrequency


class Comparison:
    def perform_compare(self, text: str, keywords: list) -> float:
        text_analyzer = TextAnalyzer()
        word_sim = WordFrequency()
        text1 = text_analyzer.tokenize_words(text, "spanish")
        text2 = text_analyzer.tokenize_words(' '.join(keywords), "spanish")
        sim = word_sim.get_data(text1, text2)
        return sim


class Validator:
    def validate_request(self, keywords: list) -> bool:
        if not isinstance(keywords, list):
            return False
        for string in keywords:
            if not isinstance(string, str):
                return False
        return True


class RankingData:
    def rank_data(self, data: list, keywords: list) -> list:
        comp = Comparison()
        for item in data:
            rating = comp.perform_compare(item['content'], keywords)
            item['rating'] = rating
        sorted_data = sorted(data, key=lambda k: k['rating'])
        return sorted_data[-1:]


class PerformSearch:
    def perform_search(self, keywords: list) -> list:
        rank = RankingData()
        excelsior_scrapper = WebScrapper('excelsior')
        excelsior_data = excelsior_scrapper.get_final_data()
        ranked_excelsior_data = rank.rank_data(excelsior_data, keywords)
        milenio_scrapper = WebScrapper('milenio')
        milenio_data = milenio_scrapper.get_final_data()
        ranked_milenio_data = rank.rank_data(milenio_data, keywords)
        minutos_scrapper = WebScrapper('20minutos')
        minutos_data = minutos_scrapper.get_final_data()
        ranked_minutos_data = rank.rank_data(minutos_data, keywords)
        data = ranked_excelsior_data + ranked_milenio_data + ranked_minutos_data
        return data
