import sys

def prepare_key_matrix(key):
    """
    Genereaza tabla Playfair 5x5 pe baza cheii date.
    Reguli: J -> I, duplicate eliminate, completare cu restul alfabetului.
    """
    key = key.upper().replace("J", "I")
    matrix = []
    used_chars = set()
    
    # Construire lista liniara de caractere unice
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ" # Fara J
    processed_key = ""
    
    # Adaugare caractere din cheie
    for char in key:
        if char.isalpha() and char not in used_chars:
            used_chars.add(char)
            processed_key += char
            
    # Completare cu restul alfabetului
    for char in alphabet:
        if char not in used_chars:
            used_chars.add(char)
            processed_key += char
            
    # Transformare in matrice 5x5
    for i in range(0, 25, 5):
        matrix.append(list(processed_key[i:i+5]))
        
    return matrix

def find_position(matrix, char):
    """Returneaza randul si coloana (r, c) pentru un caracter dat."""
    for r, row in enumerate(matrix):
        if char in row:
            return r, row.index(char)
    return None

def preprocess_text(text):
    """
    Preproceseaza textul pentru criptare conform regulilor Playfair.
    """
    text = text.upper().replace("J", "I")
    clean_text = "".join([c for c in text if c.isalpha()])
    
    final_text = ""
    i = 0
    while i < len(clean_text):
        char1 = clean_text[i]
        final_text += char1
        
        if i + 1 < len(clean_text):
            char2 = clean_text[i+1]
            
            # Regulile pentru litere duble
            if char1 == char2:
                # Daca literele sunt identice, inseram X (sau Z daca e XX)
                if char1 == 'X':
                    final_text += 'Z'
                else:
                    final_text += 'X'
                # Nu incrementam i cu 2, pentru ca al doilea caracter 
                # va face parte din urmatoarea diagrama
                i += 1
            else:
                final_text += char2
                i += 2
        else:
            i += 1
            
    # Tratare lungime impara la final
    if len(final_text) % 2 != 0:
        if final_text[-1] == 'X':
            final_text += 'Z'
        else:
            final_text += 'X'
            
    return final_text

def process_playfair(text, matrix, mode='encrypt'):
    """
    Aplica algoritmul Playfair (criptare sau decriptare).
    mode: 'encrypt' sau 'decrypt'
    """
    result = ""
    shift = 1 if mode == 'encrypt' else -1
    
    # Procesare in digrame (perechi de 2)
    for i in range(0, len(text), 2):
        char1 = text[i]
        char2 = text[i+1]
        
        r1, c1 = find_position(matrix, char1)
        r2, c2 = find_position(matrix, char2)
        
        if r1 == r2: # Aceeasi linie
            result += matrix[r1][(c1 + shift) % 5]
            result += matrix[r2][(c2 + shift) % 5]
        elif c1 == c2: # Aceeasi coloana
            result += matrix[(r1 + shift) % 5][c1]
            result += matrix[(r2 + shift) % 5][c2]
        else: # Dreptunghi
            result += matrix[r1][c2]
            result += matrix[r2][c1]
            
    return result

def print_matrix(matrix):
    print("Tabla Playfair:")
    for row in matrix:
        print(" ".join(row))
    print()

# Functia principala pentru demonstratie
def main():
    print("--- DEMO PLAYFAIR ---")
    
    # Citire date (hardcodat pentru exemplu, poate fi input())
    key = input("Introduceți cheia: ")
    mode = input("Mod (encrypt/decrypt): ").lower()
    message = input("Introduceți mesajul: ")
    
    # 1. Generare Matrice
    matrix = prepare_key_matrix(key)
    print_matrix(matrix)
    
    # 2. Procesare
    if mode == 'encrypt':
        processed_msg = preprocess_text(message)
        print(f"Text preprocesat (digrame): {processed_msg}")
        # Afisare digrame separate pentru claritate
        digrams = [processed_msg[i:i+2] for i in range(0, len(processed_msg), 2)]
        print(f"Digrame: {' '.join(digrams)}")
        
        result = process_playfair(processed_msg, matrix, 'encrypt')
        print(f"Text CRIPTAT: {result}")
        
    elif mode == 'decrypt':
        # La decriptare presupunem ca textul e deja valid
        clean_msg = message.upper().replace("J", "I").replace(" ", "")
        result = process_playfair(clean_msg, matrix, 'decrypt')
        print(f"Text DECRIPTAT: {result}")

if __name__ == "__main__":
    main()
