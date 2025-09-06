import numpy as np
import re

# Muhammad Arrafi Reva Razqana Arassy
# 241524017
# Fungsi Operasi (tambah, kurang, kali)
def tambah(X, Y):
    if isinstance(X, np.ndarray) and isinstance(Y, np.ndarray):
        if X.shape == Y.shape:
            return X + Y
        else:
            raise ValueError("Ordo matriks tidak sama untuk penjumlahan")
    elif isinstance(X, np.ndarray) and isinstance(Y, (int, float)):
        return X + Y
    elif isinstance(X, (int, float)) and isinstance(Y, np.ndarray):
        return X + Y
    else:
        return X + Y  # keduanya skalar

def kurang(X, Y):
    if isinstance(X, np.ndarray) and isinstance(Y, np.ndarray):
        if X.shape == Y.shape:
            return X - Y
        else:
            raise ValueError("Ordo matriks tidak sama untuk pengurangan")
    elif isinstance(X, np.ndarray) and isinstance(Y, (int, float)):
        return X - Y
    elif isinstance(X, (int, float)) and isinstance(Y, np.ndarray):
        return X - Y
    else:
        return X - Y  # keduanya skalar

def kali(X, Y):
    if isinstance(X, np.ndarray) and isinstance(Y, np.ndarray):
        if X.shape[1] == Y.shape[0]:
            return np.dot(X, Y)
        else:
            raise ValueError("Jumlah kolom matriks kiri harus sama dengan jumlah baris matriks kanan")
    elif isinstance(X, np.ndarray) and isinstance(Y, (int, float)):
        return X * Y
    elif isinstance(X, (int, float)) and isinstance(Y, np.ndarray):
        return X * Y
    else:
        return X * Y  # keduanya skalar

# Input Data
def input_data():
    data = {}
    ada_matriks = False

    while True:
        try:
            n = int(input("Masukkan jumlah matriks/skalar: "))
            if n > 0: break
            else: print(" Jumlah harus lebih dari 0.")
        except ValueError:
            print(" Input tidak valid. Harus angka.")

    for i in range(n):
        print(f"\n--- Mengisi Input ke-{i+1} ---")
        while True:
            jenis = input(f"Apakah input ke-{i+1} adalah Matriks (M) atau Skalar (S)? ").strip().upper()
            if jenis in ["M", "S"]: break
            else: print(" Input tidak valid! Masukkan 'M' atau 'S'.")

        while True:
            nama = input(f"Masukkan nama {'matriks' if jenis=='M' else 'skalar'} (satu huruf): ").strip().upper()
            if len(nama) == 1 and nama.isalpha():
                if nama not in data: break
                else: print(f" Nama {nama} sudah digunakan.")
            else: print(" Nama harus 1 huruf alfabet.")

        if jenis == "M":
            while True:
                try:
                    m, ncols = map(int, input("Masukkan jumlah baris dan kolom (dipisah spasi): ").split())
                    if m > 0 and ncols > 0: break
                    else: print(" Baris dan kolom harus > 0.")
                except (ValueError, IndexError):
                    print(" Input tidak valid. Masukkan dua angka dipisah spasi.")
            
            matriks = []
            print(f"Masukkan elemen matriks {nama} ({m}x{ncols}) (dipisah spasi):")
            for r in range(m):
                while True:
                    row_str = input(f"  Baris ke-{r+1}: ").split()
                    if len(row_str) != ncols:
                        print(f" Jumlah elemen harus {ncols}. Ulangi input.")
                        continue
                    try:
                        row = list(map(float, row_str))
                        matriks.append(row)
                        break
                    except ValueError:
                        print(" Semua elemen harus angka. Ulangi baris ini.")
            data[nama] = np.array(matriks)
            ada_matriks = True
        else:  # Skalar
            while True:
                try:
                    skalar = float(input(f"Masukkan nilai skalar {nama}: "))
                    data[nama] = skalar
                    break
                except ValueError:
                    print(" Input skalar harus angka.")

    if not ada_matriks:
        print("\n Harus ada minimal 1 matriks. Ulangi input.")
        return input_data()

    return data

# Evaluasi Ekspresi
# Fungsi bantuan untuk menentukan prioritas operator
def precedence(op):
    if op == '+' or op == '-':
        return 1
    if op == '*':
        return 2
    return 0

# Fungsi bantuan untuk melakukan satu operasi
def apply_op(operators, values):
    try:
        op = operators.pop()
        right = values.pop()
        left = values.pop()

        if op == '+':
            values.append(tambah(left, right))
        elif op == '-':
            values.append(kurang(left, right))
        elif op == '*':
            values.append(kali(left, right))
    except IndexError:
        raise ValueError("Ekspresi tidak valid atau tidak seimbang")


def evaluasi(ekspresi, data):
    # Regex baru untuk memisahkan variabel, operator, dan kurung
    tokens = re.findall(r'[A-Z]+|[+\-*/()]', ekspresi.replace(" ", ""))
    
    values = []  # Stack untuk nilai (matriks/skalar)
    ops = []     # Stack untuk operator

    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        if token.isalpha(): # Jika token adalah variabel
            if token in data:
                values.append(data[token])
            else:
                raise ValueError(f"Variabel '{token}' tidak ditemukan")
        
        elif token == '(': # Jika kurung buka
            ops.append(token)
            
        elif token == ')': # Jika kurung tutup
            # Selesaikan semua operasi di dalam kurung
            while ops and ops[-1] != '(':
                apply_op(ops, values)
            
            if not ops or ops[-1] != '(':
                raise ValueError("Kurung tutup ')' tidak cocok dengan kurung buka '('")
            ops.pop() # Hapus kurung buka dari stack

        else: # Jika token adalah operator
            # Selama operator di puncak stack punya prioritas lebih tinggi, lakukan operasi
            while (ops and ops[-1] != '(' and precedence(ops[-1]) >= precedence(token)):
                apply_op(ops, values)
            ops.append(token)
        
        i += 1
        
    # Lakukan semua sisa operasi yang ada di stack
    while ops:
        if ops[-1] == '(':
             raise ValueError("Kurung buka '(' tidak memiliki pasangan kurung tutup ')'")
        apply_op(ops, values)
        
    if len(values) != 1:
        raise ValueError("Ekspresi tidak valid")
        
    return values[0]

# Main
if __name__ == "__main__":
    try:
        data_input = input_data()

        print("\n" + "="*40)
        print(" Variabel yang Telah Definisikan:")
        print("="*40)
        for nama, nilai in data_input.items():
            print(f"-> Variabel '{nama}':")
            print(nilai, "\n")

        ekspresi_input = input("Masukkan operator operasi (contoh: A * B + C): ").strip().upper()
        if not ekspresi_input:
            print("Operator tidak boleh kosong.")
        else:
            hasil_akhir = evaluasi(ekspresi_input, data_input)
            print("\n" + "="*40)
            print(" HASIL AKHIR")
            print("="*40)
            print(f"Operator: {ekspresi_input}")
            print("Hasil:")
            print(hasil_akhir)

    except Exception as e:
        print(f"\n Terjadi Error: {e}")