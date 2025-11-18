from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _letter_to_index(letter: str) -> int:
    return ALPHABET.index(letter)


def _index_to_letter(index: int) -> str:
    return ALPHABET[index % 26]


@dataclass(frozen=True)
class RotorSpec:
    wiring: str
    notch: str


ROTOR_SPECS: Dict[str, RotorSpec] = {
    "I": RotorSpec("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),
    "II": RotorSpec("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),
    "III": RotorSpec("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),
    "IV": RotorSpec("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"),
    "V": RotorSpec("VZBRGITYUPSDNHLXAWMJQOFECK", "Z"),
}

REFLECTORS: Dict[str, str] = {
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL",
}


class Plugboard:
    def __init__(self, pairs: Iterable[str] | None = None):
        self.mapping: Dict[str, str] = {letter: letter for letter in ALPHABET}
        if not pairs:
            return

        for pair in pairs:
            cleaned = pair.strip().upper()
            if len(cleaned) != 2 or cleaned[0] == cleaned[1]:
                raise ValueError(f"Par inválido para o plugboard: {pair}")
            a, b = cleaned
            if self.mapping[a] != a or self.mapping[b] != b:
                raise ValueError(
                    f"Letra já conectada no plugboard: {pair} (conflito com {a}-{self.mapping[a]} / {b}-{self.mapping[b]})"
                )
            self.mapping[a] = b
            self.mapping[b] = a

    def swap_letter(self, letter: str) -> str:
        return self.mapping.get(letter, letter)

    def swap_index(self, index: int) -> int:
        return _letter_to_index(self.swap_letter(_index_to_letter(index)))


class Rotor:
    def __init__(self, wiring: str, notch: str, ring_setting: int = 1, position: str = "A"):
        if len(wiring) != 26 or any(ch not in ALPHABET for ch in wiring):
            raise ValueError("A fiação do rotor deve ser uma permutação de 26 letras.")
        self.wiring = wiring
        self.notch = notch.upper()
        self.ring_offset = (ring_setting - 1) % 26
        self.position = _letter_to_index(position.upper())
        self.forward_mapping = [_letter_to_index(ch) for ch in wiring]
        self.backward_mapping = [0] * 26
        for idx, target in enumerate(self.forward_mapping):
            self.backward_mapping[target] = idx

    @classmethod
    def from_name(
        cls, name: str, *, ring_setting: int = 1, position: str = "A"
    ) -> "Rotor":
        try:
            spec = ROTOR_SPECS[name.upper()]
        except KeyError as exc:
            raise ValueError(f"Rotor desconhecido: {name}") from exc
        return cls(spec.wiring, spec.notch, ring_setting=ring_setting, position=position)

    def step(self) -> None:
        self.position = (self.position + 1) % 26

    def at_notch(self) -> bool:
        return _index_to_letter(self.position) == self.notch

    def encode_forward(self, index: int) -> int:
        shifted = (index + self.position - self.ring_offset) % 26
        encoded = self.forward_mapping[shifted]
        return (encoded - self.position + self.ring_offset) % 26

    def encode_backward(self, index: int) -> int:
        shifted = (index + self.position - self.ring_offset) % 26
        encoded = self.backward_mapping[shifted]
        return (encoded - self.position + self.ring_offset) % 26

    def set_position(self, letter: str) -> None:
        self.position = _letter_to_index(letter.upper())


class Reflector:
    def __init__(self, wiring: str):
        if len(wiring) != 26:
            raise ValueError("O refletor deve possuir 26 letras.")
        self.mapping = [_letter_to_index(ch) for ch in wiring]

    @classmethod
    def from_name(cls, name: str) -> "Reflector":
        try:
            wiring = REFLECTORS[name.upper()]
        except KeyError as exc:
            raise ValueError(f"Refletor desconhecido: {name}") from exc
        return cls(wiring)

    def reflect(self, index: int) -> int:
        return self.mapping[index]


class EnigmaMachine:
    def __init__(
        self,
        rotors: Sequence[Rotor],
        reflector: Reflector,
        plugboard: Plugboard | None = None,
    ):
        if len(rotors) != 3:
            raise ValueError("Esta implementação suporta exatamente 3 rotores.")
        self.rotors = list(rotors)
        self.reflector = reflector
        self.plugboard = plugboard or Plugboard()

    @classmethod
    def from_preset(
        cls,
        rotor_names: Sequence[str],
        *,
        ring_settings: Sequence[int] = (1, 1, 1),
        positions: Sequence[str] = ("A", "A", "A"),
        reflector: str = "B",
        plugboard_pairs: Iterable[str] | None = None,
    ) -> "EnigmaMachine":
        if len(rotor_names) != 3:
            raise ValueError("É necessário informar exatamente três rotores.")
        ring_settings = list(ring_settings)
        if len(ring_settings) != 3:
            raise ValueError("Os ring settings precisam de três valores.")
        positions = list(positions)
        if len(positions) != 3:
            raise ValueError("As posições iniciais precisam de três letras.")
        rotors = [
            Rotor.from_name(
                name,
                ring_setting=ring,
                position=pos,
            )
            for name, ring, pos in zip(rotor_names, ring_settings, positions)
        ]
        return cls(rotors, Reflector.from_name(reflector), Plugboard(plugboard_pairs))

    def _step_rotors(self) -> None:
        left, middle, right = self.rotors
        if middle.at_notch():
            left.step()
            middle.step()
        elif right.at_notch():
            middle.step()
        right.step()

    def encipher_character(self, char: str) -> str:
        upper_char = char.upper()
        if upper_char not in ALPHABET:
            return char

        self._step_rotors()

        index = _letter_to_index(upper_char)
        index = self.plugboard.swap_index(index)

        for rotor in reversed(self.rotors):
            index = rotor.encode_forward(index)

        index = self.reflector.reflect(index)

        for rotor in self.rotors:
            index = rotor.encode_backward(index)

        index = self.plugboard.swap_index(index)
        return _index_to_letter(index)

    def encipher(self, text: str) -> str:
        return "".join(self.encipher_character(ch) for ch in text)


def demo() -> None:
    machine = EnigmaMachine.from_preset(
        ("I", "II", "III"),
        ring_settings=(1, 1, 1),
        positions=("A", "A", "A"),
        reflector="B",
        plugboard_pairs=("AM", "FI", "NV", "PS", "TU"),
    )
    plaintext = "Palmeiras Primeiro campeao mundial"
    ciphertext = machine.encipher(plaintext)
    print(f"Texto Plano : {plaintext}")
    print(f"Texto Cifrado: {ciphertext}")


if __name__ == "__main__":
    demo()

