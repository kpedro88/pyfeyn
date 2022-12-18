from dataclasses import dataclass


@dataclass
class Test:
    _name: str = "schbell"

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, v: str):
        self._name = v
        return self


t = Test()
print(t.name)  # schbell
t.name = "flirp"
print(t.name)  # flirp
print(t)  # Test(_name='flirp')
