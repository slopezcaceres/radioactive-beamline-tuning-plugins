from .optimizer import LLMBOOptimizer

def optimize(evaluate, params):
    return LLMBOOptimizer(evaluate, params)()
