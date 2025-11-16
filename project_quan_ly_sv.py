import os
import hashlib
import secrets


FILENAME = "users.txt"  # thu muc chua tai khoan dang nhap
DATA_DIR = "sv_data"    # thu muc luu danh sach sinh vien


# khoi tao file luu tk va thu muc sinh vien
def init_system():
    try:
        if not os.path.exists(FILENAME):
            open(FILENAME, "a").close()
    except Exception as e:
        print("Loi khi tao file", e)
    try:
        if not os.path.exists(DATA_DIR):
            os.mkdir(DATA_DIR)
    except Exception as e:
        print("Loi khi tao danh muc luu", e)


# ma hoa mat khau
def hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


# load danh dach user
def load_users(filename=FILENAME):
    users = {}
    if not os.path.exists(filename):
        open(filename, 'a').close()
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                username, salt, hashed = parts
                users[username] = (salt, hashed)
    return users


# luu danh dach user moi
def save_user(username, salt, hashed):
    with open(FILENAME, "a") as f:
        f.write(f"{username} {salt} {hashed}\n")


# tao tai khoan
def tao_tai_khoan(users):
    username = input("Nhap ten tai khoan: \n")
    if username in users:
        print("Ten tai khoan da ton tai, vui long nhap ten tai khoan khac.\n")
        return users
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
    return users


# dang nhap tai khoan
def dang_nhap(users):
    username = input("Nhap ten tai khoan: \n")
    password = input("Nhap mat khau: \n")
    if username not in users:
        print("Tai khoan khong ton tai.")
        return None
    salt, hashed = users[username]
    if hash_password(password, salt) == hashed:
        print("Dang nhap thanh cong.")
        return username
    else:
        print("Sai mat khau.")
        return None


# ham de nhap diem
def nhap_diem(mon):
    while True:
        try:
            diem = float(input(f"Nhap diem {mon}: "))
            if 0 <= diem <= 10:
                return diem
            print("Diem khong hop le! (0-10)")
        except ValueError:
            print("Vui long nhap diem hop le.")


# nhap danh sach sinh vien
def Nhap_sinhvien():
    ds_sinh_vien = []
    n = int(input("Nhap so luong hoc sinh: "))
    for i in range(n):
        ho_ten = input("Nhap ho va ten hoc sinh: ")
        toan = nhap_diem("Toan")
        van = nhap_diem("Van")
        anh = nhap_diem("Tieng Anh")
        sv = {
            "ho_ten": ho_ten,
            "diem_toan": toan,
            "diem_van": van,
            "diem_anh": anh
        }
        ds_sinh_vien.append(sv)
    return ds_sinh_vien


# ham luu danh sach sinh vien vao file
def save_students(username, ds_sinh_vien):
    filename = os.path.join(DATA_DIR, f"{username}.txt")
    with open(filename, "w") as f:
        for sv in ds_sinh_vien:
            ho_ten = sv["ho_ten"]
            toan = sv["diem_toan"]
            van = sv["diem_van"]
            anh = sv["diem_anh"]
            f.write(f"{ho_ten},{toan},{van},{anh}\n")


# doc danh sach sinh vien cua users
def load_students(username):
    filename = os.path.join(DATA_DIR, f"{username}.txt")
    ds = []
    if not os.path.exists(filename):
        return ds
    with open(filename, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 4:
                ho_ten, toan, van, anh = parts
                ds.append({
                    "ho_ten": ho_ten,
                    "diem_toan": float(toan),
                    "diem_van": float(van),
                    "diem_anh": float(anh)
                })
    return ds


# tinh diem trung binh cua sinh vien
def tinh_tb(toan, van, anh):
    diem_tb = (toan + van + anh)/3
    return round(diem_tb, 2)


# xep loai sinh vien theo diem trung binh
def xep_loai(diem_tb):
    if diem_tb >= 8.5:
        return "Gioi"
    elif diem_tb >= 7.0:
        return "Kha"
    elif diem_tb >= 5.0:
        return "Trung Binh"
    else:
        return "Yeu"


# hien thi danh sach sinh vien va thanh tich xep loai sinh vien
def hienthi_ds(ds_sinh_vien):
    for sv in ds_sinh_vien:
        diem_tb = tinh_tb(sv["diem_toan"], sv["diem_van"], sv["diem_anh"])
        loai = xep_loai(diem_tb)
        print(f"Ho va ten: {sv['ho_ten']}")
        print(f"Diem Toan: {sv['diem_toan']} | Diem Van: {sv['diem_van']}\
            | Diem Tieng Anh: {sv['diem_anh']}")
        print(f"Diem Trung Binh: {diem_tb} | Xep Loai: {loai}")


# ham menu tai khoan
def login_menu():
    print("\n--- LOGIN MENU ---")
    print("1. Dang nhap")
    print("2. Tao tai khoan moi")
    choice = input("Chon chuc nang: ")
    return choice


# ham menu chon
def menu():
    print("\n--- MENU ---")
    print("1. Nhap danh sach sinh vien")
    print("2. Hien thi danh sach sinh vien")
    print("3. Them sinh vien vao danh sach")
    print("4. Thoat")
    choiced = input("Chon chuc nang: ")
    return choiced


# chuong trinh chinh
def main():
    """
    Main entry point for the student management console application.

    This function orchestrates the program flow and user interaction. It
    performs
    initialization, handles user authentication (login or account creation),
    loads
    the authenticated user's student list, and runs the main menu loop until
    the user chooses to exit.
    Behavior and side effects:
    - Calls init_system() to perform any necessary startup initialization.
    - Loads existing user accounts via load_users().
    - Repeatedly prompts the user with login_menu() until a valid account is
        selected or created:
            - '1' attempts to authenticate via dang_nhap(users).
            - '2' creates a new account via tao_tai_khoan(users) and updates
            users.
            - Other inputs print an error and reprompt.
    - After authentication, calls load_students(username) to load that user's
        student records.
    - Enters the main command loop using menu() and responds to choices:
            - '1': prompts for student entry via Nhap_sinhvien(), saves with
                save_students(username, ds), and informs the user.
            - '2': displays the current student list via hienthi_ds(ds).
            - '3': prints an exit message and breaks the loop, ending the
            program.
            - Other inputs print an error and continue the
            loop.
    - Uses printing and persistent storage functions; side effects include
    console
        output and file or database operations performed by the helper
        functions.

    Parameters: None

    Returns: None

    Exceptions:
    - Propagates exceptions raised by helper functions (e.g., file I/O errors,
        data parsing errors). Caller or helpers should handle expected error
        cases.

    Example usage:
    - Call main() to start the interactive application from the program entry
    point.
    """
    init_system()
    users = load_users()
    username = None
    while not username:
        choice = login_menu()
        if choice == '1':
            username = dang_nhap(users)
        elif choice == '2':
            users = tao_tai_khoan(users)
        else:
            print("Lua chon khong hop le!")

    ds = load_students(username)
    while True:
        choiced = menu()
        if choiced == '1':
            ds = Nhap_sinhvien()
            save_students(username, ds)
            print("Da luu danh sach sinh vien thanh cong")
        elif choiced == '2':
            hienthi_ds(ds)
        elif choiced == '3':
            ds_new = Nhap_sinhvien()   # nhập mới
            ds.extend(ds_new)          # GỘP danh sách cũ + mới
            save_students(username, ds)  # lưu toàn bộ danh sách
        elif choice == '4':
            print("Ban da thoat!")
            break
        else:
            print("Lua chon khong hop le!")


# khoi dong chuonng trinh
if __name__ == "__main__":
    main()
