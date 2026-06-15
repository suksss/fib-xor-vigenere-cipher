#!/usr/bin/env python3
"""
Module: fib_xor_cipher.py
Description: Implementation of the Fib-XOR Vigenère Cipher.
Coursework: CC5009NI: Cybersecurity in Computing (2025-26)
Author: Sukrish Shrestha
Student ID: 24046519 / NP01NT4A240015
"""

# =====================================================================
# SECTION 1: CONSTANTS & ALPHABET DEFINITION
# =====================================================================
# Custom 70-character alphabet ring (N = 70)
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,?%#!@ "
N = len(ALPHABET)


# =====================================================================
# SECTION 2: HELPER FUNCTIONS
# =====================================================================
def char_to_index(char):
    """Maps a character to its index in the custom alphabet ring."""
    if char not in ALPHABET:
        raise ValueError(f"Character '{char}' is not in the supported alphabet.")
    return ALPHABET.index(char)


def index_to_char(idx):
    """Maps an index to its corresponding character in the alphabet ring."""
    return ALPHABET[idx % N]


# =====================================================================
# SECTION 3: KEY EXPANSION ENGINE
# =====================================================================
def generate_fibonacci_sequence(length):
    """Generates a Fibonacci sequence modulo N of a given length."""
    if length <= 0:
        return []
    if length == 1:
        return [1]
    
    seq = [1, 1]
    while len(seq) < length:
        next_val = (seq[-1] + seq[-2]) % N
        seq.append(next_val)
    return seq


def expand_key(password, target_length):
    """
    Expands the user password to match the target length using 
    a modulo Fibonacci progression mechanism.
    """
    if not password:
        raise ValueError("Password key cannot be empty.")
        
    # Convert initial key to numeric indices
    key_indices = [char_to_index(c) for c in password]
    
    # Recursively expand key using Fibonacci logic if it's shorter than plaintext
    while len(key_indices) < target_length:
        next_key_val = (key_indices[-1] + key_indices[-2 if len(key_indices) > 1 else -1]) % N
        key_indices.append(next_key_val)
        
    return key_indices[:target_length]


# =====================================================================
# SECTION 4: SHIFT CALCULATION MATRIX
# =====================================================================
def calculate_dynamic_shifts(key_indices, fib_seq):
    """
    Computes the dynamic shift S_i for each character position.
    Formula: S_i = ((K_i XOR F_i) + (13 * i)) mod N
    """
    shifts = []
    for i in range(len(key_indices)):
        k_i = key_indices[i]
        f_i = fib_seq[i]
        
        # Bitwise XOR operation combined with position multiplier
        s_i = ((k_i ^ f_i) + (13 * i)) % N
        shifts.append(s_i)
    return shifts


# =====================================================================
# SECTION 5: CORE ENCRYPTION ENGINE
# =====================================================================
def encrypt(plaintext, password):
    """
    Encrypts plaintext using the Fib-XOR Vigenere Cipher protocol.
    Includes Affine Shift, Chaining Filter (AND), and Mixing Combinator.
    """
    length = len(plaintext)
    key_indices = expand_key(password, length)
    fib_seq = generate_fibonacci_sequence(length)
    shifts = calculate_dynamic_shifts(key_indices, fib_seq)
    
    ciphertext_indices = []
    c_prev = 0  # Initialization Vector (C_{-1} = 0)
    
    for i in range(length):
        p_i = char_to_index(plaintext[i])
        s_i = shifts[i]
        k_i = key_indices[i]
        
        # 1. Affine Shift Layer
        t_i = (p_i + s_i) % N
        
        # 2. Chaining Filter Layer (State dependency on previous ciphertext)
        a_i = k_i & c_prev
        
        # 3. Mixing Combinator Layer
        c_i = (t_i + a_i) % N
        
        ciphertext_indices.append(c_i)
        c_prev = c_i  # Update state history context for the next cycle
        
    # Map indices back to characters
    return "".join(index_to_char(idx) for idx in ciphertext_indices)


# =====================================================================
# SECTION 6: CORE DECRYPTION ENGINE
# =====================================================================
def decrypt(ciphertext, password):
    """
    Decrypts ciphertext by reversing the Fib-XOR Vigenere layers.
    """
    length = len(ciphertext)
    key_indices = expand_key(password, length)
    fib_seq = generate_fibonacci_sequence(length)
    shifts = calculate_dynamic_shifts(key_indices, fib_seq)
    
    plaintext_chars = []
    c_prev = 0  # Initialization Vector (C_{-1} = 0)
    
    for i in range(length):
        c_i = char_to_index(ciphertext[i])
        s_i = shifts[i]
        k_i = key_indices[i]
        
        # 1. Filter Reconstruction using historical ciphertext context
        a_i = k_i & c_prev
        
        # 2. Unmixing Line
        t_i = (c_i - a_i) % N
        
        # 3. Reverse Shift Mapping
        p_i = (t_i - s_i) % N
        
        plaintext_chars.append(index_to_char(p_i))
        c_prev = c_i  # Move state forward
        
    return "".join(plaintext_chars)


# =====================================================================
# SECTION 7: INTERACTIVE CLI DASHBOARD
# =====================================================================
def display_menu():
    print("\n" + "="*50)
    print("FIB-XOR VIGENÈRE CIPHER DASHBOARD")
    print("="*50)
    print("1. Encrypt Text")
    print("2. Decrypt Text")
    print("3. Exit System")
    print("-"*50)


def main():
    while True:
        display_menu()
        choice = input("Select Operation (1-3): ").strip()
        
        if choice == '1':
            print("\n--- Encryption Mode ---")
            plaintext = input("Enter message to encrypt:\n> ")
            key = input("Enter secret key:\n> ")
            
            try:
                ciphertext = encrypt(plaintext, key)
                print(f"\nResulting Ciphertext:\n{ciphertext}")
            except ValueError as e:
                print(f"\n[ERROR] Encryption Failed: {e}")
                
        elif choice == '2':
            print("\n--- Decryption Mode ---")
            ciphertext = input("Enter ciphertext to decrypt:\n> ")
            key = input("Enter secret key:\n> ")
            
            try:
                plaintext = decrypt(ciphertext, key)
                print(f"\nRecovered Plaintext:\n{plaintext}")
            except ValueError as e:
                print(f"\n[ERROR] Decryption Failed: {e}")
                
        elif choice == '3':
            print("\nExiting cryptographic portal. Secure data streams terminated.")
            break
        else:
            print("\n[INVALID SELECTION] Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
