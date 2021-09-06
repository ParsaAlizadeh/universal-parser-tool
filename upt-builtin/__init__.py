from .atcoder import AtCoder
from .codeforces import Codeforces
from .quera import Quera
from .usaco import Usaco

def register():
    return {
        'cf': Codeforces,
        'codeforces': Codeforces,
        'atc': AtCoder,
        'atcoder': AtCoder,
        'quera': Quera,
        'us': Usaco,
        'usaco': Usaco
    }
