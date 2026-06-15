# Fib-XOR Vigenère Cipher


An enhanced symmetric polyalphabetic cryptosystem built to address the structural vulnerabilities of the classical Vigenère cipher. Developed as part of the coursework for **Cybersecurity in Computing** (2025-26 Autumn Semester) at London Metropolitan University / Islington College.

> ⚠️ **Educational Disclaimer:** This repository features a conceptual cryptographic design created purely for pedagogical purposes to demonstrate principles of confusion and diffusion. It is **not** intended or vetted for securing production systems or sensitive real-world enterprise data.

---

## 📖 Overview & Background

The classical Vigenère cipher relies on a static, cyclical keyword repetition structure that leaves it highly vulnerable to **Kasiski Examination** (periodicity analysis) and subsequent **Frequency Analysis**. 

The **Fib-XOR Vigenère Cipher** implements a layered mathematical and state-dependent methodology to inject non-linearity, disrupt linguistic patterns, and introduce state memory. It changes the operational standard from a basic static alphabet table loop to a hybrid stream/block operational style.

### Key Conceptual Upgrades
*   **Expanded Alphabet Ring ($N=70$):** Extends standard upper/lowercase boundaries to explicitly index numerical data, common symbols, and spaces (`ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,?%#!@ `).
*   **Fibonacci-Based Key Expansion:** Replaces cyclical repetition with dynamic modulo-based sequence generation, producing a non-periodic stream that defeats standard key-length calculations.
*   **Bitwise XOR & AND Mask Chaining:** Injects state dependency into the processing line. The current character's output is directly dependent on the historical state of the previous ciphertext character, successfully establishing an **Avalanche Effect** (diffusion).

---

## 📐 Algorithmic Mechanics

The algorithm functions over a finite modulo ring of $N=70$.

### 1. Key & Shift Architecture
The password provided is converted to numerical indices and filled recursively to match the plaintext length $L$ using a modulo Fibonacci progression:
$$K_{\text{new}} = (K_{\text{last}} + K_{\text{second\_last}}) \pmod N$$

A dynamic shift parameter ($S_i$) is then generated for each element position $i$:
$$S_i = ((K_i \oplus F_i) + (13 \times i)) \pmod N$$
Where $\oplus$ denotes a bitwise Exclusive-OR and $F_i$ represents the local Fibonacci stream variable.

### 2. Layered Encryption Steps
For every character index $i$ tracking a plaintext character $P_i$ and assuming an Initialization Vector state of $C_{-1} = 0$:

1.  **Affine Shift Layer:** Move character position by calculated shift matrix.
    $$T_i = (P_i + S_i) \pmod N$$
2.  **Chaining Filter Layer:** Generate a directional state bitwise constraint filter ($A_i$) using logical AND ($\wedge$) bound against historical cipher text.
    $$A_i = K_i \wedge C_{i-1}$$
3.  **Mixing Combinator Layer:** 
    $$C_i = (T_i + A_i) \pmod N$$

### 3. Layered Decryption Steps
Because the receiver tracks the matching key stream parameters and holds historical context records ($C_{i-1}$), the process safely unwinds by recomputing $A_i$ directly without needing to compute an inverse logical AND:
1.  **Filter Reconstruction:** $A_i = K_i \wedge C_{i-1}$
2.  **Unmixing Line:** $T_i = (C_i - A_i) \pmod N$
3.  **Reverse Shift Mapping:** $P_i = (T_i - S_i) \pmod N$

---

## 🛠️ Project Structure & Architecture

```text
├── README.md               # Project documentation and specifications
└── fib-xor-vigenere-cipher.py       # Python source code containing implementation and CLI menu
