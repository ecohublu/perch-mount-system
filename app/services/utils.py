class SearchStr(str):

    def __init__(self, string: str) -> None:
        super().__init__()
        self.string = string

    @property
    def search_phrase(self) -> str:
        return f"%{self.string}%"

    @property
    def search_phrase_from_start(self) -> str:
        return f"{self.string}%"

    @property
    def search_phrase_from_end(self) -> str:
        return f"%{self.string}"
