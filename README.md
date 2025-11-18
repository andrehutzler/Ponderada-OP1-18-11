# Máquina Enigma em Python

Autor: **Lucas de Luccas**

Projeto desenvolvido para a optativa de Criptografia e Computação Quântica.
## Visão Geral

- Implementação fiel de uma Enigma de 3 rotores, com suporte a:
  - Seleção de rotores históricos (`I` a `V`)
  - Ajuste de `ring settings` e posições iniciais
  - Plugboard configurável
  - Refletores `A`, `B` ou `C`
- Demonstração interativa em `enigma.py`
- Testes automatizados em `tests/test_enigma.py`

## Requisitos

- Python ≥ 3.10

## Estrutura

- `enigma.py`: implementação completa + função `demo()`
- `tests/test_enigma.py`: suíte de testes via `unittest`

## Uso Rápido

```bash
cd /Users/klubi/Desktop/Inteli/Aula-Criptografia
python enigma.py
```

A demonstração imprime texto plano e cifrado com uma configuração padrão (pode ser alterada diretamente na função `demo()`).

### Personalizando a Máquina

Use o método `EnigmaMachine.from_preset` para ajustar os parâmetros:

```python
machine = EnigmaMachine.from_preset(
    ("I", "II", "III"),
    ring_settings=(1, 1, 1),
    positions=("A", "A", "A"),
    reflector="B",
    plugboard_pairs=("AM", "FI", "NV", "PS", "TU"),
)
ciphertext = machine.encipher("PALMEIRAS PRIMEIRO CAMPEAO MUNDIAL")
```

- `rotor_names`: tupla com três rotores (da esquerda para a direita)
- `ring_settings`: deslocamento interno (1–26)
- `positions`: posição inicial (letras A–Z)
- `plugboard_pairs`: pares de letras conectadas

A cifra é simétrica: cifrar novamente com a **mesma configuração** decifra o texto.

## Testes

```bash
cd /Users/klubi/Desktop/Inteli/Aula-Criptografia
python -m unittest discover tests
```

Cobrem:

- Comparação com ciphertext conhecido
- Propriedade de ida e volta (cifrar e decifrar)

## Referências

- CrypTool Online — seção Enigma ([CrypTool Online](https://www.cryptool.org/en/cto/))

## Créditos

Projeto e documentação por **Lucas de Luccas**.

---

# Kamasutra — Documentação Secundária

Autor: **Andre Hutzler**

Projeto desenvolvido como ramificação didática do estudo sobre cifras históricas apresentado neste repositório.

## Visão Geral

- Reimplementação fiel da máquina Enigma de 3 rotores, adaptada ao contexto do projeto Kamasutra.
- Suporte a:
  - Seleção de rotores históricos (`I` … `V`)
  - Ajuste de *ring settings* e posições iniciais independentes
  - Plugboard totalmente configurável
  - Refletores `A`, `B` ou `C`
- Demonstração interativa disponível em `enigma.py`
- Testes automatizados concentrados em `tests/test_enigma.py`

## Requisitos de Ambiente

- Python 3.10 ou superior (recomendado CPython)

## Estrutura do Projeto

- `enigma.py`: contém a implementação completa da máquina e a função `demo()`
- `tests/test_enigma.py`: suíte de testes baseada em `unittest`

## Início Rápido

```bash
cd /Users/klubi/Desktop/Inteli/Aula-Criptografia
python enigma.py
```

A execução da `demo()` exibe texto plano e texto cifrado usando uma configuração padrão. Ajuste os parâmetros diretamente na função para experimentar novos cenários.

## Configuração Avançada

```python
from enigma import EnigmaMachine

machine = EnigmaMachine.from_preset(
    ("I", "II", "III"),
    ring_settings=(1, 1, 1),
    positions=("A", "A", "A"),
    reflector="B",
    plugboard_pairs=("AM", "FI", "NV", "PS", "TU"),
)
ciphertext = machine.encipher("PALMEIRAS PRIMEIRO CAMPEAO MUNDIAL")
```

- `rotor_names`: três rotores (esquerda → direita)
- `ring_settings`: deslocamento interno (1–26)
- `positions`: posição inicial (A–Z)
- `plugboard_pairs`: pares de letras conectadas

Lembre-se: cifrar novamente com a **mesma configuração** decifra a mensagem.

## Testes Automatizados

```bash
cd /Users/klubi/Desktop/Inteli/Aula-Criptografia
python -m unittest discover tests
```

Cobertura atual:

- Comparação com ciphertext conhecido
- Validação da propriedade ida/volta (cifrar e decifrar)

## Referências

- CrypTool Online — seção Enigma: <https://www.cryptool.org/en/cto/>

## Créditos

- Arquitetura original: Lucas de Luccas
- Adaptação e documentação Kamasutra: **Andre Hutzler**

