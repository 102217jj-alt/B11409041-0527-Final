import os
import json

class Library:
    def __init__(self, file_name="library_data.json"):
        self.file_name = file_name
        self.books = []
        self.load_data()

    def load_data(self):
        """從 JSON 檔案載入書籍資料"""
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, "r", encoding="utf-8") as f:
                    self.books = json.load(f)
            except json.JSONDecodeError:
                print("檔案格式錯誤，無法載入資料。")
                self.books = []
        else:
            self.books = []

    def save_data(self):
        """將書籍資料儲存到 JSON 檔案"""
        try:
            with open(self.file_name, "w", encoding="utf-8") as f:
                json.dump(self.books, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"儲存資料時發生錯誤：{e}")

    VALID_STATUSES = ["available", "borrowed"]  # 定義允許的狀態

    def add_book(self, title, isbn, status):
        """新增書籍"""
        if self.is_isbn_exist(isbn):
            print("ISBN 已存在，無法新增。")
            return
        if status not in self.VALID_STATUSES:
            print(f"狀態無效！允許的狀態為：{', '.join(self.VALID_STATUSES)}")
            return
        self.books.append({"title": title, "isbn": isbn, "status": status})
        print("書籍新增成功！")

    def is_isbn_exist(self, isbn):
        """檢查 ISBN 是否已存在"""
        return any(book["isbn"] == isbn for book in self.books)

    def show_books(self):
        """顯示所有書籍"""
        if not self.books:
            print("目前沒有任何書籍資料。")
            return
        for book in self.books:
            print(f"書名: {book['title']}, ISBN: {book['isbn']}, 狀態: {book['status']}")

    def borrow_book(self, isbn):
        """借閱書籍"""
        for book in self.books:
            if book["isbn"] == isbn:
                if book["status"] == "available":
                    book["status"] = "borrowed"
                    print("書籍已成功借出！")
                else:
                    print("書籍已被借出，無法再次借閱。")
                return
        print("找不到對應的 ISBN，無法借閱。")

    def exit_system(self):
        """儲存資料並退出系統"""
        self.save_data()
        print("系統資料已儲存，系統關閉。")

def main():
    library = Library()

    print("=== 圖書管理系統 v1.0 (Modern) ===")
    while True:
        op = input("> ").strip()
        
        if op == "exit":
            library.exit_system()
            break
        elif op.startswith("add "):
            try:
                _, raw = op.split(" ", 1)
                title, isbn, status = raw.split("/")
                library.add_book(title.strip(), isbn.strip(), status.strip())
            except ValueError:
                print("格式錯誤！正確格式為：add 書名/ISBN/狀態")
        elif op == "show":
            library.show_books()
        elif op.startswith("borrow "):
            try:
                _, isbn = op.split(" ", 1)
                library.borrow_book(isbn.strip())
            except ValueError:
                print("格式錯誤！正確格式為：borrow ISBN")
        else:
            print("未知指令，請重新輸入。")

if __name__ == "__main__":
    main()