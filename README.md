# TURNAM Restaurant Management System

TURNAM is a desktop-based restaurant automation system developed using **Python**, **PyQt5**, and **SQLite**. It is designed to assist small to medium-sized food businesses in managing their menus, orders, employee data, and dynamically generating reports — all within a user-friendly interface.

---

## 🔑 Features

* ✅ **User Authentication**

  * Login system with username and password validation.
  * Input hints and masked password fields for a smooth and secure experience.

* 🍽️ **Menu Management**

  * Add, update, or delete products from the menu.
  * Each product includes name, price, and stock quantity.
  * Real-time table updates reflecting any change made.

* 🧾 **Order Management**

  * Dynamic order handling system.
  * Orders include product name, quantity, and price.
  * Automatically updates the stock quantity.

* 📊 **Reports Tab**

  * Retrieves data **dynamically from the Orders table**.
  * Displays total items sold and revenue generated — no static report table used.

* 👤 **Employee Management**

  * Add, update, or remove employee records.
  * Fields include: name, username, password, department, and phone number.

* 🚪 **Safe Exit Confirmation**

  * Displays a confirmation dialog before closing the application.

---

## 🖼️ Screenshots

### 🔐 Login Page

![Login Page]([./1d186411-0d36-4e56-81e9-b26b1f8a3a96.png](https://github.com/ayseatmaca/restoran-otomasyonu/blob/main/Yemek/images/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202025-05-26%20005605.png))

### 📋 Menu Management Page

![Menu Page](./0ffc8c0a-c5db-49f4-b3ef-95e30d6a4010.png)

---

## 📁 Folder Structure

```
TURNAM-Restaurant-System/
├── main.py
├── login.py
├── database.db
├── README.md
├── /ui/
│   ├── mainwindow.ui
│   └── login.ui
└── /assets/
    └── turnam_logo.png
```

---

## ⚙️ Technologies Used

* **Language:** Python 3.x
* **GUI Library:** PyQt5
* **Database:** SQLite
* **IDE:** Visual Studio Code

---

## 🛠️ Installation & Setup

To run this application locally, follow the steps below:

```bash
# 1. Clone the repository
git clone https://github.com/your-username/turnam-restaurant-system.git
cd turnam-restaurant-system

# 2. Install required libraries
pip install PyQt5

# 3. Run the application
python main.py
```

---

## 🧠 Project Purpose

This project was developed as a hands-on learning experience in:

* Python GUI development
* SQLite database integration
* Modular and scalable software design

It simulates a real-world restaurant workflow and can be extended with advanced features such as:

* Receipt printing
* Role-based permissions
* Visual reports (charts, graphs)
* Online system integration

---

## 📌 Notes

* The Reports tab is dynamically generated from the **Orders table**, ensuring real-time sales and inventory data.
* Password fields are masked for security.
* Data integrity is maintained across all operations (menu updates, deletions, etc.).

---

## 🤝 Contributing

This project is currently developed by a single contributor. However, suggestions, issues, and improvements are welcome! Feel free to fork the project and explore.

---

## 📄 License

This project is provided for educational and personal use only. **No commercial license is granted.**

---

## 🙋‍♀️ Developed by

**Ayşe Atmaca**
Aerospace Engineering & Software Engineering Double Major
[GitHub Profile](https://github.com/ayseatmaca)

---
