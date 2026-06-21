import csv
import os
from datetime import datetime

CSV_FILE = "data_parkir.csv"

class ParkingQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, plat_nomor):
        self.queue.append(plat_nomor)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        return None

    def is_empty(self):
        return len(self.queue) == 0

    def view_queue(self):
        return self.queue


parking_lot = {}
antrean_masuk = ParkingQueue()

def load_from_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Plat_Nomor", "Jenis_Kendaraan", "Waktu_Masuk", "Slot_Parkir"])
        return

    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            parking_lot[row["Plat_Nomor"]] = {
                "Jenis_Kendaraan": row["Jenis_Kendaraan"],
                "Waktu_Masuk": row["Waktu_Masuk"],
                "Slot_Parkir": row["Slot_Parkir"]
            }

def save_to_csv():
    with open(CSV_FILE, mode='w', newline='') as file:
        fieldnames = ["Plat_Nomor", "Jenis_Kendaraan", "Waktu_Masuk", "Slot_Parkir"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for plat, info in parking_lot.items():
            writer.writerow({
                "Plat_Nomor": plat,
                "Jenis_Kendaraan": info["Jenis_Kendaraan"],
                "Waktu_Masuk": info["Waktu_Masuk"],
                "Slot_Parkir": info["Slot_Parkir"]
            })


def bubble_sort_by_time(data_list):
    n = len(data_list)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data_list[j][1]["Waktu_Masuk"] > data_list[j+1][1]["Waktu_Masuk"]:
                data_list[j], data_list[j+1] = data_list[j+1], data_list[j]
    return data_list

def search_kendaraan(plat_nomor):
    return parking_lot.get(plat_nomor, None)


def kendaran_masuk():
    print("\n--- KENDARAAN MASUK (CREATE) ---")
    plat = input("Masukkan Plat Nomor (ex: B1234XYZ): ").upper().strip()
    
    if search_kendaraan(plat):
        print("⚠️ Kendaraan dengan plat tersebut sudah ada di dalam parkiran!")
        return

    jenis = input("Jenis Kendaraan (Mobil/Motor): ").capitalize().strip()
    slot = input("Masukkan Kode Slot Parkir (ex: A01): ").upper().strip()
    waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    antrean_masuk.enqueue(plat)
    print(f"[Queue] Kendaraan {plat} dimasukkan ke antrean gerbang...")

    plat_proses = antrean_masuk.dequeue()
    parking_lot[plat_proses] = {
        "Jenis_Kendaraan": jenis,
        "Waktu_Masuk": waktu_sekarang,
        "Slot_Parkir": slot
    }
    
    save_to_csv()
    print(f"✅ Sukses! Kendaraan {plat_proses} berhasil parkir di slot {slot}.")

def tampilkan_parkiran():
    print("\n--- DAFTAR KENDARAAN PARKIR (READ & SORT) ---")
    if not parking_lot:
        print("Parkiran Kosong.")
        return

    data_list = list(parking_lot.items())
    sorted_data = bubble_sort_by_time(data_list)

    print(f"{'No':<4} | {'Plat Nomor':<12} | {'Jenis':<8} | {'Waktu Masuk':<20} | {'Slot':<6}")
    print("-" * 60)
    for idx, (plat, info) in enumerate(sorted_data, 1):
        print(f"{idx::<4} | {plat:<12} | {info['Jenis_Kendaraan']:<8} | {info['Waktu_Masuk']:<20} | {info['Slot_Parkir']:<6}")

def update_kendaraan():
    print("\n--- UPDATE DATA KENDARAAN ---")
    plat = input("Masukkan Plat Nomor yang ingin diubah: ").upper().strip()
    kendaraan = search_kendaraan(plat)

    if kendaraan:
        print(f"Data ditemukan: {kendaraan}")
        jenis_baru = input("Jenis Kendaraan Baru (Kosongkan jika tidak diubah): ").capitalize().strip()
        slot_baru = input("Slot Parkir Baru (Kosongkan jika tidak diubah): ").upper().strip()

        if jenis_baru:
            kendaraan["Jenis_Kendaraan"] = jenis_baru
        if slot_baru:
            kendaraan["Slot_Parkir"] = slot_baru

        save_to_csv()
        print("✅ Data kendaraan berhasil diperbarui!")
    else:
        print("❌ Kendaraan tidak ditemukan.")

def kendaraan_keluar():
    print("\n--- KENDARAAN KELUAR (DELETE) ---")
    plat = input("Masukkan Plat Nomor Kendaraan Keluar: ").upper().strip()
    kendaraan = search_kendaraan(plat)

    if kendaraan:

        waktu_masuk = datetime.strptime(kendaraan["Waktu_Masuk"], "%Y-%m-%d %H:%M:%S")
        durasi = datetime.now() - waktu_masuk
        menit = max(1, int(durasi.total_seconds() / 60)) # minimal 1 menit untuk simulasi
        biaya = menit * 2000 if kendaraan["Jenis_Kendaraan"] == "Mobil" else menit * 1000

        print(f"\nRingkasan Parkir {plat}:")
        print(f"  - Jenis       : {kendaraan['Jenis_Kendaraan']}")
        print(f"  - Slot        : {kendaraan['Slot_Parkir']}")
        print(f"  - Durasi      : {menit} Menit (Simulasi)")
        print(f"  - Total Biaya : Rp {biaya:,}")


        del parking_lot[plat]
        save_to_csv()
        print(f"✅ Kendaraan {plat} telah keluar. Data dihapus dari sistem.")
    else:
        print("❌ Plat nomor tidak ditemukan di dalam sistem parkir.")


def main():
    load_from_csv()
    while True:
        print("\n=====================================")
        print("      SISTEM SMART PARKING CLI       ")
        print("=====================================")
        print("1. Kendaraan Masuk (Create)")
        print("2. Tampilkan Semua Kendaraan (Read)")
        print("3. Cari Kendaraan (Search)")
        print("4. Update Data Kendaraan (Update)")
        print("5. Kendaraan Keluar (Delete)")
        print("6. Keluar Aplikasi")
        print("=====================================")
        
        pilihan = input("Pilih Menu (1-6): ").strip()

        if pilihan == "1":
            kendaran_masuk()
        elif pilihan == "2":
            tampilkan_parkiran()
        elif pilihan == "3":
            print("\n--- CARI KENDARAAN (SEARCHING) ---")
            plat = input("Masukkan Plat Nomor: ").upper().strip()
            hasil = search_kendaraan(plat)
            if hasil:
                print(f"🔎 Ditemukan! -> Jenis: {hasil['Jenis_Kendaraan']}, Slot: {hasil['Slot_Parkir']}, Masuk: {hasil['Waktu_Masuk']}")
            else:
                print("❌ Kendaraan tidak terdaftar.")
        elif pilihan == "4":
            update_kendaraan()
        elif pilihan == "5":
            kendaraan_keluar()
        elif pilihan == "6":
            print("Terima kasih telah menggunakan Sistem Parkir Pintar!")
            break
        else:
            print("⚠️ Pilihan tidak valid. Silakan masukkan angka 1-6.")

if __name__ == "__main__":
    main()