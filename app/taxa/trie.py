from app import model


class SpeciesTrie:
    def __init__(self, species: list[model.Species]):
        self.species = species
        self.trie = self._trie_init(self.species)

    def search(self, word: str) -> list:
        search_results = []
        if not word:
            return search_results

        trie = self.trie
        word = word.lower()

        for w in word:
            if w in trie:
                trie = trie[w]
            else:
                return search_results

        tasks = [trie]
        while tasks:
            task = tasks.pop()
            for key, value in task.items():
                if key == "end":
                    search_results.extend(value)
                else:
                    tasks.append(value)
        return self._search_results_as_dict(search_results)

    def _search_results_as_dict(self, search_results: list[tuple[int, str]]):
        return [
            {"code": code, "chinese_common_name": name} for code, name in search_results
        ]

    def _trie_init(self, species: list[model.Species]) -> dict:
        trie = {}
        for sp in species:
            ans_name = (
                sp.chinese_common_name
                if sp.chinese_common_name
                else sp.english_common_name
            )
            taxon_name = sp.english_common_name.split(" ")[-1].lower()
            ans = (sp.taxon_order, ans_name)
            if sp.chinese_common_name:
                trie = self._insert_trie(trie, sp.chinese_common_name, ans)
            trie = self._insert_trie(trie, sp.english_common_name.lower(), ans)
            trie = self._insert_trie(trie, taxon_name, ans)
            for code in sp.codes:
                trie = self._insert_trie(trie, code.lower(), ans)
        return trie

    def _insert_trie(self, trie, word: str, ans):
        tmp_trie = trie
        for w in word:
            while w not in tmp_trie:
                tmp_trie[w] = {}
            tmp_trie = tmp_trie[w]
        if "end" in tmp_trie:
            tmp_trie["end"].append(ans)
        else:
            tmp_trie["end"] = [ans]
        return trie
