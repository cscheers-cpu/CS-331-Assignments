#store a word with missing plaintext letters along with:
# 1) its associated cipherword
# 2) the plaintext word formatted with regex range
# 3) indices of '_' in original plaintext
# 4) indices of '_' in formatted text
# 5) list of dictionary words that match formatted word
class wordMatch:
    def __init__(self,
            cipherword: str, 
            plainword: str,  
            formatword: str, 
            plainindices: list[int],  
            formatindices: list[int], 
            wordMatch: list[str] | None = None):
        
        self.cipherword = cipherword
        self.plainword = plainword
        self.formatword = formatword
        self.formatindices = formatindices
        self.plainindices = plainindices
        self.wordMatch = wordMatch if wordMatch is not None else []

    def __repr__(self) -> str:
        return f"Cipherword: {self.cipherword}  plainword: {self.plainword} wordMatch: {self.wordMatch}"
        
    def get_cipherword(self):
        return self.cipherword
    
    def get_plainword(self):
        return self.plainword

    def get_formatword(self):
        return self.formatword
    
    def get_plainindices(self):
        return self.plainindices

    def get_formatindices(self):
        return self.formatindices

    def get_wordMatch(self):
        return self.wordMatch

    def set_wordMatch(self, wordMatch: list[str]):
        self.wordMatch = wordMatch

    def len_wordMatch(self) -> int:
        return len(self.wordMatch)

    def len_indices(self) -> int:
        return len(self.plainindices)