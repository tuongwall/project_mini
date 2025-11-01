import os
import hashlib
import secrets


FILENAME = "users.txt"


def init_file(filename=FILENAME):
    try:
        if not os.path.exists(filename):
            open(filename, "a").close()
    except Exception as e:
        print("Loi khi tao file", e)


def hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def load_users(filename=FILENAME):
    users = {}
    if not os.path.exists(FILENAME):
        open(FILENAME, 'a').close()
    with open(FILENAME, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                username, salt, hashed = parts
                users[username] = (salt, hashed)
    return users


def save_user(username, salt, hashed):
    with open(FILENAME, "a") as f:
        f.write(f"tk: {username}, mk: {salt} {hashed}\n")


users = load_users()


def tao_tai_khoan():
    username = input("Nhap ten tai khoan: \n")
    if username in users:
        print("Ten tai khoan da ton tai, vui long nhap ten tai khoan khac.\n")  
        return
    passnew = input("Nhap mat khau:\n")
    while True:
        confirm = input("Xac nhan mat khau: \n")
        if confirm == passnew:
            salt = secrets.token_hex(8)
            hashed = hash_password(passnew, salt)
            users[username] = (salt, hashed)
            save_user(username, salt, hashed)
            print("Tao tai khoan thanh cong")
            break
        else:
            print("Mat khau khong khop, vui long thu lai.\n")


def dang_nhap():
    username = input("Nhap ten tai khoan: \n")
    password = input("Nhap mat khau: \n")
    if username not in users:
        print("Tai khoan khong ton tai.")
        return False
    salt, hashed = users[username]
    if hash_password(password, salt) == hashed:
        print("Dang nhap thanh cong.")
        return True
    else:
        print("Sai mat khau.")
        return False


def Nhap_sinhvien():
    ds_sinh_vien = []
    n = int(input("Nhap so luong hoc sinh: "))
    for i in range(n):
        ho_ten = input("Nhap ho va ten hoc sinh: ")

        def nhap_diem(diem):
            while True:
                if diem < 0 or diem > 10:
                    print("Diem khong hop le! Vui long nhap lai (0 - 10).")
                    diem = float(input(f"Nhap diem {diem}: "))
                else:
                    return diem

        toan = nhap_diem(float(input("Nhap diem Toan: ")))
        ly = nhap_diem(float(input("Nhap diem Ly: ")))
        hoa = nhap_diem(float(input("Nhap diem Hoa: ")))
        sv = {
            "ho_ten": ho_ten,
            "diem_toan": toan,
            "diem_ly": ly,
            "diem_hoa": hoa
        }
        ds_sinh_vien.append(sv)
    return ds_sinh_vien


def tinh_tb(toan, ly, hoa):
    diem_tb = (toan + ly + hoa)/3
    return round(diem_tb, 2)


def xep_loai(diem_tb):
    if diem_tb >= 8.5:
        return "Gioi"
    elif diem_tb >= 7.0:
        return "Kha"
    elif diem_tb >= 5.0:
        return "Trung Binh"
    else:
        return "Yeu"


def hienthi_ds(ds_sinh_vien):
    for sv in ds_sinh_vien:
        diem_tb = tinh_tb(sv["diem_toan"], sv["diem_ly"], sv["diem_hoa"])
        loai = xep_loai(diem_tb)
        print(f"Ho va ten: {sv['ho_ten']}")
        print(f"Diem Toan: {sv['diem_toan']} | Diem Ly: {sv['diem_ly']}| Diem \
            Hoa: {sv['diem_hoa']}")
        print(f"Diem Trung Binh: {diem_tb} | Xep Loai: {loai}")


def login_menu():
    print("\n--- LOGIN MENU ---")
    print("1. Dang nhap")
    print("2. Tao tai khoan moi")
    choice = input("Chon chuc nang: ")
    return choice


def menu():
    print("\n--- MENU ---")
    print("1. Nhap danh sach sinh vien")
    print("2. Hien thi danh sach sinh vien")
    print("3. Thoat")
    choiced = input("Chon chuc nang: ")
    return choiced


while True:
    choice = login_menu()
    if choice == '1':
        if dang_nhap():
            break
    elif choice == '2':
        tao_tai_khoan()
    else:
        print("Lua chon khong hop le! Vui long chon lai.")

ds = []
while True:
    choice = menu()
    if choice == '1':
        ds = Nhap_sinhvien()
    elif choice == '2':
        if ds:
            hienthi_ds(ds)
        else:
            print("Danh sach sinh vien trong!")
    elif choice == '3':
        print("Thoat chuong trinh.")
        break
    else:
        print("Lua chon khong hop le! Vui long chon lai.")
