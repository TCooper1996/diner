from typing import Callable, TypeVar, Generic

Env = TypeVar("Env")
A = TypeVar("A")
B = TypeVar("B")

class Reader(Generic[Env, A]):
    def __init__(self, run: Callable[[Env], A]):
        self.run = run

    def map(self, f: Callable[[A], B]) -> 'Reader[Env, B]':
        return Reader(lambda env: f(self.run(env)))

    def flat_map(self, f: Callable[[A], 'Reader[Env, B]']) -> 'Reader[Env, B]':
        return Reader(lambda env: f(self.run(env)).run(env))

    def __call__(self, env: Env) -> A:
        return self.run(env)