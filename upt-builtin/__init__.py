from .atcoder import AtCoder
from .codeforces import Codeforces
from .quera import Quera
from .usaco import Usaco

def register():
    return [Codeforces, AtCoder, Quera, Usaco]
