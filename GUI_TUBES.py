import tkinter as tk
from tkinter import messagebox
import time
from tkinter import ttk

# Fungsi Insertion Sort Iteratif
def insertion_sort_iterative(arr, data):
    start_time = time.time_ns()
    for i in range(1, len(arr)):
        key = arr[i]
        key_id = data[i][0]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            data[j + 1] = data[j]
            j -= 1
        arr[j + 1] = key
        data[j + 1] = (key_id, key)
    end_time = time.time_ns()
    running_time = end_time - start_time
    return data, running_time

# Fungsi Insertion Sort Rekursif
def insertion_sort_recursive(arr, data, n=None):
    start_time = time.time_ns()
    if n is None:
        n = len(arr)
    if n <= 1:
        return data, 0
    
    data, prev_time = insertion_sort_recursive(arr, data, n - 1)
    
    key = arr[n - 1]
    key_id = data[n - 1][0]
    j = n - 2
    
    while j >= 0 and key < arr[j]:
        arr[j + 1] = arr[j]
        data[j + 1] = data[j]
        j -= 1
    
    arr[j + 1] = key
    data[j + 1] = (key_id, key)
    
    end_time = time.time_ns()
    running_time = end_time - start_time + prev_time
    return data, running_time

# Fungsi Selection Sort Iteratif
def selection_sort_iterative(arr, data):
    start_time = time.time_ns()
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        data[i], data[min_idx] = data[min_idx], data[i]
    end_time = time.time_ns()
    running_time = end_time - start_time
    return data, running_time

# Fungsi untuk mencari indeks minimum
def find_min_index(arr, start, end):
    if start == end:
        return start
    
    min_idx = find_min_index(arr, start + 1, end)
    
    if arr[start] < arr[min_idx]:
        return start
    else:
        return min_idx

# Fungsi Selection Sort Rekursif
def selection_sort_recursive(arr, data, n=None, start=0):
    start_time = time.time_ns()
    
    if n is None:
        n = len(arr)
    
    if start >= n - 1:
        return data, 0
    
    min_idx = find_min_index(arr, start, n-1)
    
    if min_idx != start:
        arr[start], arr[min_idx] = arr[min_idx], arr[start]
        data[start], data[min_idx] = data[min_idx], data[start]
    
    data, prev_time = selection_sort_recursive(arr, data, n, start + 1)
    
    end_time = time.time_ns()
    running_time = end_time - start_time + prev_time
    
    return data, running_time

def string_to_list(input_string):
    try:
        data = []
        for item in input_string.replace(",", " ").split():
            parts = item.split(":")
            if len(parts) == 2:
                id_customer = parts[0].strip()
                nominal_refund = float(parts[1].strip())
                data.append((id_customer, nominal_refund))
        return data
    except ValueError:
        messagebox.showerror("Input Error", "Input harus berupa pasangan IDCustomer:nominal refund.")
        return []

def proses_sort():
    input_data = input_text.get("1.0", "end-1c")
    data = string_to_list(input_data)
    
    if not data:
        return
    
    # Clear existing data
    for row in result_tree.get_children():
        result_tree.delete(row)
        
    # Clear existing runtime data
    for row in runtime_tree.get_children():
        runtime_tree.delete(row)
    
    # Membuat copy data untuk setiap algoritma
    data_insertion_iter = data.copy()
    data_insertion_rec = data.copy()
    data_selection_iter = data.copy()
    data_selection_rec = data.copy()
    
    nominal_data = [nominal for _, nominal in data]
    
    # Menjalankan semua algoritma
    results = {
        "Insertion Sort (Iteratif)": insertion_sort_iterative(nominal_data.copy(), data_insertion_iter.copy()),
        "Insertion Sort (Rekursif)": insertion_sort_recursive(nominal_data.copy(), data_insertion_rec.copy()),
        "Selection Sort (Iteratif)": selection_sort_iterative(nominal_data.copy(), data_selection_iter.copy()),
        "Selection Sort (Rekursif)": selection_sort_recursive(nominal_data.copy(), data_selection_rec.copy())
    }
    
    # Menggunakan hasil Insertion Sort Iteratif sebagai default untuk ditampilkan
    sorted_data = results["Insertion Sort (Iteratif)"][0]
    
    # Menampilkan data terurut
    for customer_id, nominal in sorted_data:
        result_tree.insert("", tk.END, values=(customer_id, f"{nominal:,.2f}"))
    
    # Menampilkan semua runtime
    for algo_name, (_, runtime) in results.items():
        runtime_tree.insert("", tk.END, values=(algo_name, f"{runtime:,.2f}"))

def reset():
    input_text.delete("1.0", "end")
    for row in result_tree.get_children():
        result_tree.delete(row)
    for row in runtime_tree.get_children():
        runtime_tree.delete(row)

# GUI Setup
root = tk.Tk()
root.title("Pengelolaan Data Refund Customer")
root.geometry("800x900")
root.configure(bg="#f4f4f9")

# Title
title_label = tk.Label(root, text="Pengelolaan Data Refund Customer", font=("Arial", 16, "bold"), bg="#4caf50", fg="white", pady=10)
title_label.pack(fill=tk.X)

# Input section
instruksi_label = tk.Label(root, text="Masukkan IDCustomer dan nominal refund dalam .000(format-> IDCustomer:nominal):", font=("Arial", 12), bg="#f4f4f9")
instruksi_label.pack(pady=10)

input_text = tk.Text(root, height=5, width=60, font=("Arial", 12), bd=2, relief="solid")
input_text.pack(pady=10)

# Buttons
proses_button = tk.Button(root, text="Proses Pengurutan", command=proses_sort, font=("Arial", 12, "bold"), bg="#2196f3", fg="white", relief="raised", padx=10, pady=5)
proses_button.pack(pady=10)

reset_button = tk.Button(root, text="Reset", command=reset, font=("Arial", 12, "bold"), bg="#f44336", fg="white", relief="raised", padx=10, pady=5)
reset_button.pack(pady=10)

# Results section
result_label = tk.Label(root, text="Hasil Pengurutan:", font=("Arial", 12, "bold"), bg="#f4f4f9")
result_label.pack(pady=5)

# Treeview untuk hasil pengurutan
columns = ("IDCustomer", "Nominal Refund")
result_tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
result_tree.pack(pady=10, padx=20)

result_tree.heading("IDCustomer", text="IDCustomer")
result_tree.heading("Nominal Refund", text="Nominal Refund")

# Runtime comparison section
runtime_label = tk.Label(root, text="Perbandingan Running Time:", font=("Arial", 12, "bold"), bg="#f4f4f9")
runtime_label.pack(pady=5)

# Treeview untuk running time
runtime_columns = ("Algorithm", "Running Time (ns)")
runtime_tree = ttk.Treeview(root, columns=runtime_columns, show="headings", height=4)
runtime_tree.pack(pady=10, padx=20)

runtime_tree.heading("Algorithm", text="Algorithm")
runtime_tree.heading("Running Time (ns)", text="Running Time (ns)")

root.mainloop()