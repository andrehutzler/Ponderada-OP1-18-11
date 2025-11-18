import unittest

from enigma import EnigmaMachine


class EnigmaMachineTest(unittest.TestCase):
    def setUp(self):
        self.config = dict(
            rotor_names=("I", "II", "III"),
            ring_settings=(1, 1, 1),
            positions=("A", "A", "A"),
            reflector="B",
            plugboard_pairs=("AM", "FI", "NV", "PS", "TU"),
        )

    def test_known_ciphertext(self):
        machine = EnigmaMachine.from_preset(**self.config)
        ciphertext = machine.encipher("HELLOWORLD")
        self.assertEqual(ciphertext, "FLBDMMAUMZ")

    def test_roundtrip(self):
        machine = EnigmaMachine.from_preset(**self.config)
        plaintext = "CRYPTOGRAPHY"
        ciphertext = machine.encipher(plaintext)

        machine_reset = EnigmaMachine.from_preset(**self.config)
        decoded = machine_reset.encipher(ciphertext)
        self.assertEqual(decoded, plaintext)


if __name__ == "__main__":
    unittest.main()

