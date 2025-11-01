# phan mem quan ly sinh vien
# tao tai khoan va dang nhap
users = {
    "user": "admin",
    "password": "12345"
}


def tao_tai_khoan():
    username = input("Nhap ten tai khoan: \n")
    passnew = input("Nhap mat khau: \n")
    while True:
        confirm = input("Xac nhan mat khau: \n")
        if confirm == passnew:
            users[username] = passnew
            print("Tao tai khoan thanh cong!")
            break
        else:
            print("Mat khau khong khop, vui long thu lai.")



tao_tai_khoan()