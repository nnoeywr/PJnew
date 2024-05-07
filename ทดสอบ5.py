import sqlite3
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from tkinter import *
import tkinter.messagebox as msgbox
import datetime
from tkinter import PhotoImage
import time
import requests
import cv2
import numpy as np
from io import BytesIO
from PIL import Image, ImageTk
from tkinter import simpledialog
import yagmail
from yagmail.error import YagConnectionClosed

conn = sqlite3.connect('Booking_van.db')
c = conn.cursor()
try:
    #Databaseเก็บข้อมูลการจองตั๋ว
    c.execute('''CREATE TABLE tickets(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    phone_number VARCHAR(30) NOT NULL,
    email VARCHAR(30) NOT NULL,
    travel_date VARCHAR(10) NOT NULL,
    selected_price VARCHAR(30) NOT NULL,
    time_slot VARCHAR(30) NOT NULL,
    day VARCHAR(30) NOT NULL,  
    month VARCHAR(30) NOT NULL,
    year VARCHAR(30) NOT NULL)''')
    conn.commit()
except:
    pass

#หน้่าจองตั๋ว
def book_ticket():
    book_ticket_window = tk.Toplevel(root)
    book_ticket_window.title("Booking")
    book_ticket_window.geometry("1024x768+220+20")
    book_ticket_window.resizable(False, False)
    #backgroundหน้่าจองตั๋ว
    # background_image = tk.PhotoImage(file="/Users/suponb./Downloads/IMG_6270.PNG")
    # background_label = tk.Label(book_ticket_window, image=background_image)
    # background_label.pack()
    # background_label.image = background_image
    fname=''
    lname=''
    phone=''
    Email=''
    travel=''
    st=''
    sp=''
    


#นาฬิกา
    clock_label = tk.Label(book_ticket_window, text="", font=("Helvetica", 36) ,bg='#FFFFFF', fg="Black")
    clock_label.place(x=638, y=315)

# สร้างฟังก์ชันอัปเดตนาฬิกา
    def update_clock():
        current_time = time.strftime('%H:%M:%S')  # รูปแบบเวลา: ชั่วโมง:นาที:วินาที
        clock_label.config(text=current_time)
        book_ticket_window.after(1000, update_clock)  # อัปเดตทุก 1000 มิลลิวินาที (1 วินาที)

# เรียกใช้ฟังก์ชันเพื่อเริ่มการอัปเดตนาฬิกา
    update_clock()

    def confirm_booking():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        phone_number = phone_number_entry.get()
        email = email_entry.get()
        travel_date = cal.get_date()
        selected_time_slot = time_slot_var.get()
        selected_price = prices_var.get()
        day,month,year = map(int,travel_date.split('/'))
        nonlocal fname
        nonlocal lname
        nonlocal phone
        nonlocal Email
        nonlocal travel
        nonlocal st
        nonlocal sp
        fname=first_name
        lname=last_name
        phone=phone_number
        Email=email
        travel=travel_date
        st=selected_time_slot
        sp=selected_price

        if not first_name or not last_name or not phone_number or not email or not travel_date:
            result_label.config(text="ข้อมูลไม่ครบ โปรดกรอกข้อมูลทุกช่อง")
            return
        else:
            if len(phone_number) != 10:
                result_label.config(text="กรุณากรอกหมายเลขโทรศัพท์ให้ถูกต้อง")
                return
        
        '''
        conn = sqlite3.connect('Booking_van.db')
        c = conn.cursor()
        c.excute("SELECT email FROM ussers WHERE email=?",(email,))
        check_email = c.fetchall()
        if check_email:
                result_label.config(text="อีเมลนี้มีอยู่แล้ว, โปรดใช้อีเมลอื่น")
        elif not re.match("^[a-z]")
        '''


        conn = sqlite3.connect('Booking_van.db')
        c = conn.cursor()
        c.execute("SELECT * FROM tickets WHERE phone_number=?", (phone_number,))
        existing_ticket = c.fetchone()
        conn.close()

        if existing_ticket:
            result_label.config(text="หมายเลขโทรศัพท์นี้ถูกใช้แล้ว โปรดใช้หมายเลขโทรศัพท์อื่น")
            return
        
        # ดึงราคาจากรายการราคาและอัตราค่าโดยสารที่เลือก
        #selected_price = prices_var.get()
        #selected_price_value = [item[1] for item in prices_options if item[0] == selected_price][0]
        def send():
            pay = tk.Toplevel(root)
            pay.title("Payment")
            pay.geometry("1024x768+220+20")
            pay.resizable(False, False)
            Email=email
            try:
                # กำหนดข้อมูลเข้าสู่ระบบของอีเมล์
                email_sender = "premiumvanbooking@gmail.com"
                app_password = "gcqt nwpn rwcr asay "  # กรอกรหัส 16 หลักจากการสร้าง App Password
                # เริ่มต้นเซสชัน Yagmail
                yag = yagmail.SMTP(email_sender, app_password)
                # กำหนดผู้รับ
                recipients = [Email]
                text = f"✅Booking ticket confirm\n ⚠️ให้ท่านนำตั๋วมาแสดงต่อเจ้าหน้าที่ก่อนขึ้นรถ\n"
                text += "----------------------------------------------------\n"
                text += f"ชื่อผู้จอง: {first_name}  {last_name}\n"
                text += f"เดินทางวันที่: {travel}\n"
                text += f"เวลา: {st}\n"
                text += f"จุดหมายปลายทาง: {sp}\n"
                text += f"หมายเลขติดต่อ: {phone}\n"
                text += "----------------------------------------------------\n"
                text += "**ขอบคุณที่ใช้บริการ premium van booking**"
                text += " email ฉบับนี้เป็นการส่งโดยระบบอัตโนมัติ \nกรุณาอย่าตอบกลับ หากต้องการสอบถามข้อมูลเพิ่มเติม\n สามารดูช่องทางการติดต่อได้ผ่านเว็บไซต์ของpremium van booking  และเลือกเมนูติดต่อเรา"
                        
            
                # เริ่มต้นเซสชัน Yagmail
                yag = yagmail.SMTP(email_sender, app_password)

                # ส่งอีเมล์
                yag.send(         
                    to=recipients,
                    subject="recipe",
                    contents=text 
                )
                msgbox.showinfo("Success", "Email sent successfully! ระบบได้ส่งตั๋วไปยังEmail ของคุณแล้ว")
                # Close the Yagmail session
                yag.close()
            except YagConnectionClosed:
                msgbox.showerror("Error", "Connection to email server failed. Please check your credentials and internet connection.")
            except Exception as e:
                msgbox.showerror("Error", f"An error occurred while sending the email: {str(e)}")
            pay.destroy()
                
        # แสดงหน้าต่างยืนยันการจอง
        confirmation_message = f"ยืนยันการจองด้วยข้อมูลดังนี้:\nชื่อ: {first_name} \nนามสกุล: {last_name}\nเบอร์โทร: {phone}\nอีเมล: {email}\nวันเดินทาง: {travel}\nสถานที่ขึ้น-ลง: {sp}\nเวลาเดินทาง:{st}\nราคา: {selected_price_value} บาท"
        confirmation = msgbox.askyesno("ยืนยันการจอง",confirmation_message)

        if confirmation>0:
            #หน้าจ่ายเงิน
            pay = tk.Toplevel(root)
            pay.title("Payment")
            pay.geometry("1024x768+220+20")
            pay.resizable(False, False)
            # background_image = tk.PhotoImage(file="/Users/suponb./Downloads/IMG_6314.PNG")
            # background_label = tk.Label(pay, image=background_image)
            # background_label.place(x=0, y=0, relwidth=1, relheight=1)
            # background_label.image = background_image
            prices={"ท่ารถตู้ปรับอากาศขอนแก่น-เซ็นทรัลขอนแก่น": 16,
                    "ท่ารถตู้ปรับอากาศขอนแก่น-แยกน้ำพอง": 92,
                    "ท่ารถตู้ปรับอากาศขอนแก่น-เขาสวนกวาง": 134,
                    "ท่ารถตู้ปรับอากาศขอนแก่น-แยกกุมภวาปี":190,
                    "ท่ารถตู้ปรับอากาศขอนแก่น-เซ็นทรัลอุดรธานี(บขส1)": 249,
                    "เซ็นทรัลขอนแก่น-แยกน้ำพอง":76,
                    "เซ็นทรัลขอนแก่น-เขาสวนกวาง": 120,
                    "เซ็นทรัลขอนแก่น-แยกน้ำพอง": 237,
                    "แยกน้ำพอง-เขาสวนกวาง":44,
                    "แยกน้ำพอง-แยกกุมภวาปี":98,
                    "แยกน้ำพอง-เซ็นทรัลอุดรธานี(บขส1)":160,
                    "เขาสวนกวาง-แยกกุมภวาปี": 54,
                    "เขาสวนกวาง-เซ็นทรัลอุดรธานี(บขส1)": 116,
                    "แยกกุมภวาปี-เซ็นทรัลอุดรธานี(บขส1)": 62}
            
           #หน้าจ่ายเงิน
            price=prices.get(selected_price,0)
            image_url = f"https://promptpay.io/0960941078/{price}.png"
            image_url = image_url

            # Send a request to download the image
            response = requests.get(image_url)

            # Check if the request was successful (HTTP status code 200)
            if response.status_code == 200:
                # Open the image using PIL
                image = Image.open(BytesIO(response.content))
                
                # Convert the image to grayscale if it's not already
                if image.mode != 'L':
                    image = image.convert('L')
                
                # Convert the PIL image to a NumPy array
                img_np = np.array(image)

                # Initialize the QRCode detector
                qr_decoder = cv2.QRCodeDetector()

                # Detect and decode the QR code
                val, pts, qr_code = qr_decoder.detectAndDecode(img_np)

                # Print the decoded value from the QR code
                print("Decoded value from the QR code:", val)

                # Display the image in a Tkinter window
                image = image.resize((int(image.width * 0.75), int(image.height * 0.75)))
                img_tk = ImageTk.PhotoImage(image)
                label = Label(pay, image=img_tk)
                label.image = img_tk  # Keep a reference to avoid garbage collection
                label.place(x = 500, y = 250)

                close_button = tk.Button(pay, text="ชำระเงินแล้ว", command=lambda:(send(),pay.destroy()))
                close_button.place(x=590,y=600)
            
            
            else:
                print("Failed to download the image. HTTP status code:", response.status_code)

            close_button = tk.Button(book_ticket_window, text="กลับหน้าหลัก", command=book_ticket_window.destroy)
            close_button.place(x=850,y=680)
            
        if confirmation:
            conn = sqlite3.connect('Booking_van.db')
            c = conn.cursor()

            c.execute("INSERT INTO tickets (first_name, last_name, phone_number, email, travel_date, selected_price, time_slot,day,month,year) VALUES (?, ?, ?, ?, ?, ?, ?,?,?,?)",
                    (first_name, last_name, phone_number, email, travel_date, selected_price, selected_time_slot,day,month,year))
            conn.commit()

        result_label.config(text="การจองสำเร็จ")
        book_ticket_window.destroy()


        c.execute("SELECT COUNT(*) FROM tickets WHERE travel_date = ? AND time_slot = ?",
                       (travel_date, selected_time_slot))
        conn.commit()
        bookings_count = c.fetchone()[0]

        if bookings_count >= 7:
            msgbox.showerror("เวลาเต็ม", "เวลาที่ท่านเลือกถูกจองเต็มแล้วค่ะ")
            return
    
    result_label = tk.Label(book_ticket_window, text="สถานะการจองจะแสดงที่นี้", font=("Helvetica", 16) ,fg="white", bg="#3196FF", highlightthickness=0, borderwidth=0,)
    result_label.place(x=250, y=558)
    
    #เอาไว้แสดงราคา
    def update_selected_price(event):
        # ดึงราคาจากรายการราคาและอัตราค่าโดยสารที่เลือก
        selected_price = prices_var.get()
        selected_price_value = [item[1] for item in prices_options if item[0] == selected_price][0]
        
        # อัปเดต StringVar ที่ใช้แสดงราคา
        selected_price_var.set(f"{selected_price_value} บาท")
        selected_price_label = tk.Label(book_ticket_window, textvariable=selected_price_var, font=("Helvetica", 16), bg="#446C9E" ,fg='white')
        selected_price_label.place(x=230, y=485) 
        
    tk.Label(book_ticket_window, text="กรุณากรอกข้อมูลผู้โดยสาร", font=("Helvetica", 20),bg='#196658', fg="white", highlightthickness=0, borderwidth=0,).place(x=217, y=60)
    
    tk.Label(book_ticket_window, text="ชื่อจริง:", font=("Helvetica", 16) ,bg='#196658', fg="white", highlightthickness=0, borderwidth=0,).place(x=120, y=110)
    first_name_entry = tk.Entry(book_ticket_window, bg="#98D6FC", highlightthickness=0, borderwidth=0, cursor='hand2', font=("Helvetica", 17))  
    first_name_entry.place(x=225, y=115)


    tk.Label(book_ticket_window, text="นามสกุล:",font=("Helvetica", 16) ,bg='#196658', fg="white", highlightthickness=0, borderwidth=0,).place(x=120, y=150)
    last_name_entry = tk.Entry(book_ticket_window, bg="#98D6FC", highlightthickness=0, borderwidth=0, cursor='hand2', font=("Helvetica", 17))
    last_name_entry.place(x=225, y=155)

    tk.Label(book_ticket_window, text="เบอร์โทรศัพท์:",font=("Helvetica", 16) ,bg='#196658', fg="white", highlightthickness=0, borderwidth=0,).place(x=115, y=190)
    phone_number_entry = tk.Entry(book_ticket_window, bg="#98D6FC", highlightthickness=0, borderwidth=0, cursor='hand2', font=("Helvetica", 17))
    phone_number_entry.place(x=225, y=195)

    tk.Label(book_ticket_window, text="อีเมล:",font=("Helvetica", 16) ,bg='#196658', fg="white", highlightthickness=0, borderwidth=0,).place(x=120, y=230)
    email_entry = tk.Entry(book_ticket_window, bg="#98D6FC", highlightthickness=0, borderwidth=0, cursor='hand2', font=("Helvetica", 17))
    email_entry.place(x=225, y=235)

    tk.Label(book_ticket_window, text="วันเดินทาง:",font=("Helvetica", 16) ,bg='#196658', fg="white", highlightthickness=0, borderwidth=0,).place(x=120, y=270)
    #ปฏิทิน
    cal = Calendar(
    book_ticket_window,
    selectmode="day",
    year=2023,
    month=10,
    day=1,
    date_pattern="dd/mm/yyyy", 
)
    cal.place(x=225, y=270)


    tk.Label(book_ticket_window, text="เวลาเดินทาง:",font=("Helvetica", 16) ,bg='#196658', fg="white", highlightthickness=0, borderwidth=0,).place(x=120, y=520)
    time_slot_var = tk.StringVar(book_ticket_window)
    time_slots = {
        1: "06:00-08:00",
        2: "10:00-12:00",
        3: "14:00-16:00",
        4: "19:00-21:00"
    }
    time_slot_var.set(time_slots[1])  # Set the default time slot
    time_slot_menu = tk.OptionMenu(book_ticket_window, time_slot_var, *time_slots.values())
    time_slot_menu.place(x=230, y=520)

    # สร้าง Label สำหรับราคาและเมนู dropdown
    tk.Label(book_ticket_window, text="สถานที่ขึ้น-ลง:",font=("Helvetica", 16) ,bg='#196658', fg="white", highlightthickness=0, borderwidth=0,).place(x=120, y=450)

    # สร้างรายการราคาและอัตราค่าโดยสารในรูปแบบคู่ (ชื่อสถานที่, ราคา)
    prices_options = [
        ("ท่ารถตู้ปรับอากาศขอนแก่น-เซ็นทรัลขอนแก่น", 16),
        ("ท่ารถตู้ปรับอากาศขอนแก่น-แยกน้ำพอง", 92),
        ("ท่ารถตู้ปรับอากาศขอนแก่น-เขาสวนกวาง", 134),
        ("ท่ารถตู้ปรับอากาศขอนแก่น-แยกกุมภวาปี", 190),
        ("ท่ารถตู้ปรับอากาศขอนแก่น-เซ็นทรัลอุดรธานี(บขส1)", 249),
        ("เซ็นทรัลขอนแก่น-แยกน้ำพอง", 76),
        ("เซ็นทรัลขอนแก่น-เขาสวนกวาง", 120),
        ("เซ็นทรัลขอนแก่น-แยกน้ำพอง", 237),
        ("แยกน้ำพอง-เขาสวนกวาง", 44),
        ("แยกน้ำพอง-แยกกุมภวาปี", 98),
        ("แยกน้ำพอง-เซ็นทรัลอุดรธานี(บขส1)", 160),
        ("เขาสวนกวาง-แยกกุมภวาปี", 54),
        ("เขาสวนกวาง-เซ็นทรัลอุดรธานี(บขส1)", 116),
        ("แยกกุมภวาปี-เซ็นทรัลอุดรธานี(บขส1)", 62)
    ]

    # สร้าง StringVar สำหรับเลือกค่า
    prices_var = tk.StringVar(book_ticket_window)

    # กำหนดค่าเริ่มต้นให้เป็นรายการแรกในรายการราคาและอัตราค่าโดยสาร
    prices_var.set(prices_options[0][0])

    # สร้าง OptionMenu โดยใช้ List comprehension เพื่อดึงชื่อสถานที่จากรายการราคาและอัตราค่าโดยสาร
    selected_price = tk.OptionMenu(book_ticket_window, prices_var, *([item[0] for item in prices_options]))
    selected_price.place(x=230, y=450)

    confirm_button = ttk.Button(book_ticket_window, text="ยืนยันการจอง", command=lambda:(confirm_booking()))
    confirm_button.place(x=270, y=680)

                
    
    price_label = tk.Label(book_ticket_window, text="ราคา:", font=("Helvetica", 16), fg="#446C9E")
    price_label.place(x=230, y=485)

    # สร้าง StringVar สำหรับแสดงราคาที่ถูกเลือก
    selected_price_var = tk.StringVar(book_ticket_window)

    # กำหนดค่าเริ่มต้นให้เป็นราคาแรกในรายการราคาและอัตราค่าโดยสาร
    selected_price_var.set(f"{prices_options[0][1]} บาท")
    selected_price_label = tk.Label(book_ticket_window, textvariable=selected_price_var, font=("Helvetica", 16), bg="#446C9E")
    selected_price_label.place(x=230, y=485) 

    # สร้าง Label สำหรับแสดงราคาที่ถูกเลือก
    selected_price_label = tk.Label(book_ticket_window, textvariable=selected_price_var, font=("Helvetica", 16), bg="#446C9E" ,fg="white")
    selected_price_label.place(x=230, y=485)

    # สร้าง OptionMenu โดยใช้ List comprehension เพื่อดึงชื่อสถานที่จากรายการราคาและอัตราค่าโดยสาร
    selected_price_optionmenu = tk.OptionMenu(book_ticket_window, prices_var, *([item[0] for item in prices_options]), command=update_selected_price)
    selected_price_optionmenu.place(x=230, y=450)


        
    #ปุ่มกลับหน้าจองตั๋ว
    close_button = tk.Button(book_ticket_window, text="กลับหน้าหลัก", command=book_ticket_window.destroy)
    close_button.place(x=850,y=680)
 
#หน้าเช็คตั๋ว
def check_ticket():
    check_ticket_window = tk.Toplevel(root)
    check_ticket_window.title("Check Ticket")
    check_ticket_window.geometry("1024x768+220+20")
    check_ticket_window.resizable(False, False)
#พื้นหลังหน้สเช็คตั๋ว
    # background_image = tk.PhotoImage(file="/Users/suponb./Downloads/กะเทยตายแน่.001 6.png")
    # background_label = tk.Label(check_ticket_window, image=background_image)
    # background_label.pack()
    # background_label.image = background_image

    #ปุ่มกลับหน้าเช็คตั๋ว
    close_button = tk.Button(check_ticket_window, text="กลับหน้าหลัก", bg="green", fg="Black", command=check_ticket_window.destroy)
    close_button.place(x=850, y=680)


    # สร้าง Label และ Entry สำหรับป้อนหมายเลขโทรศัพท์
    #tk.Label(check_ticket_window, text="กรุณาป้อนหมายโทรศัพท์ของท่านเพื่อค้นหาตั๋ว", font=("Helvetica", 20)).place(x=600, y=65)
    # Create a label and an entry field for phone number
    tk.Label(check_ticket_window, text="เบอร์โทร:", font=("Helvetica", 20)).place(x=380, y=140)
    check_phone_number_entry = tk.Entry(check_ticket_window, highlightthickness=0, borderwidth=0, cursor='hand2', font=("Helvetica", 18))
    check_phone_number_entry.place(x=480, y=145)
    check_phone_number_entry.config(bg="#ACEE94")

    



    # สร้าง Label สำหรับแสดงผลลัพธ์การค้นหา
    check_result_label = tk.Label(check_ticket_window, text="ข้อมูลของท่านจะแสดงตรงนี้", font=("Helvetica", 16), bg="#00B796")
    check_result_label.place(x=478, y=276)

    

    #ช่องข้อมูลโดยสาร
    ticket_frame = tk.Frame(check_ticket_window)
    ticket_frame.place(x=390, y=350)

    def check_phone_number():
        phone_number = check_phone_number_entry.get()
        
        conn = sqlite3.connect('Booking_van.db')
        c = conn.cursor()

        c.execute("SELECT * FROM tickets WHERE phone_number = ?", (phone_number,))
        tickets = c.fetchall()

        if tickets:
            check_result_label.config(text=f"ท่านได้จองตั๋วแล้ว {phone_number}")

            for widget in ticket_frame.winfo_children():
                widget.destroy()

            for ticket in tickets:
                ticket_info = f"ชื่อ: {ticket[1]}, นามสกุล: {ticket[2]}\nเบอร์โทร: {ticket[3]}\nสถานที่ขึ้น-ลง: {ticket[6]}\nเวลา: {ticket[7]}\nวันที่: {ticket[5]}\nรหัสหากต้องการแก้ไข/ยกเลิกตั๋ว: {ticket[0]}"
                label = tk.Label(ticket_frame, text=ticket_info, font=("Helvetica", 14), bg="#446C9E")
                label.pack()

        else:
            check_result_label.config(text=f"ไม่พบตั๋วสำหรับเบอร์โทร {phone_number}")
        conn.close()

    check_button = ttk.Button(check_ticket_window, text="เช็คตั๋ว", command=check_phone_number)
    check_button.place(x=530, y=200)

        

        
#หน้าเช็ครอบรถ
def show_available_seats():
    show_available_seats_window = tk.Toplevel(root)
    show_available_seats_window.title("Check Seat Availability")
    show_available_seats_window.geometry("1024x768+220+20")
    show_available_seats_window.resizable(False, False)
    conn = sqlite3.connect("Booking_van.db")
    cursor = conn.cursor()

    # Load and display the background image
    # background_image = tk.PhotoImage(file="/Users/suponb./Downloads/IMG_6264.PNG")
    # background_label = tk.Label(show_available_seats_window, image=background_image)
    # background_label.place(x=0, y=0, relwidth=1, relheight=1)
    # background_label.image = background_image

#นาฬิกา
    clock_label = tk.Label(show_available_seats_window, text="", font=("Helvetica", 36) ,bg='#FFFFFF', fg="Black")
    clock_label.place(x=605, y=285)

# สร้างฟังก์ชันอัปเดตนาฬิกา
    def update_clock():
        current_time = time.strftime('%H:%M:%S')  # รูปแบบเวลา: ชั่วโมง:นาที:วินาที
        clock_label.config(text=current_time)
        show_available_seats_window.after(1000, update_clock)  # อัปเดตทุก 1000 มิลลิวินาที (1 วินาที)

# เรียกใช้ฟังก์ชันเพื่อเริ่มการอัปเดตนาฬิกา
    update_clock()
    # Close button to return to the main window
    close_button = tk.Button(show_available_seats_window, text="กลับหน้าหลัก", command=show_available_seats_window.destroy, bg="yellow", fg="red")
    close_button.place(x=850, y=680)


    def calculate_available_seats():
        today = datetime.date.today()
        window = show_available_seats_window 
        result_label = tk.Label(show_available_seats_window, text="รายละเอียดจะแสดงที่นี่",font=("Helvetica", 20),bg='#A2D16E')
        result_label.place(x=340, y=530)

        def update_result():
            choice_date = date_choice_var.get()
            choice_round = round_choice_var.get()

            if choice_date < 1 or choice_date > 7 or choice_round < 1 or choice_round > 4:
                result_label.config(text="กรุณาเลือกวันที่และรอบรถให้ถูกต้อง")
                return

            travel_date = today + datetime.timedelta(days=choice_date)
            round_trip = round_trip_mapping[choice_round]

            cursor.execute("SELECT COUNT(*) FROM tickets WHERE travel_date = ? AND time_slot = ?", (travel_date, round_trip))

            booked_seats = cursor.fetchone()[0]
            total_seats = 7   #จำนวนที่นั่งทั้งหมดในแต่ละช่วงเวลา
            available_seats = total_seats - booked_seats
            result_label.config(text=f"รอบรถ: {round_trip} วันที่: {travel_date} จำนวนที่ว่าง: {available_seats}")
            

        date_choice_var = tk.IntVar()
        date_choice_var.set(1)
        date_label = tk.Label(window, text="เลือกวันที่เดินทาง:",font=("Helvetica", 18),bg="#ED6B59")
        date_label.place(x=178, y=100) 
        for i in range(1, 8):
            travel_date = today + datetime.timedelta(days=i)
            date_option = tk.Radiobutton(window, text=travel_date.strftime('%Y-%m-%d'), variable=date_choice_var, value=i,bg="#F09285")
            date_option.place(x=350, y=70 + i * 30)

        round_choice_var = tk.IntVar()
        round_choice_var.set(1)
        round_label = tk.Label(window, text="เลือกรอบรถ:",font=("Helvetica", 17),bg="#D44A7A")
        round_label.place(x=570, y=100) 
        for i, round_trip in round_trip_mapping.items():
            round_option = tk.Radiobutton(window, text=round_trip, variable=round_choice_var, value=i,bg="#DD799D")
            round_option.place(x=690, y=70 + i * 30)

        check_button = tk.Button(window, text="เช็คที่ว่าง", font=("Helvetica", 25), bg="white", fg="black", relief="flat", command=update_result)
        check_button.place(x=480, y=415)


    round_trip_mapping = {
        1: "06:00-08:00",
        2: "10:00-12:00",
        3: "14:00-16:00",
        4: "19:00-21:00"
    }
    calculate_available_seats()

    show_available_seats_window.mainloop()

    
#หน้าแก้ไขตั๋ว
def edit_ticket():
    edit_ticket_window = tk.Toplevel(root)
    edit_ticket_window.title("แก้ไขตั๋ว")
    edit_ticket_window.geometry("1024x768+220+20")
    edit_ticket_window.resizable(False, False)

     # Load and display the background image
    # background_image = tk.PhotoImage(file="/Users/suponb./Downloads/IMG_6251.PNG")
    # background_label = tk.Label( edit_ticket_window, image=background_image)
    # background_label.place(x=0, y=0, relwidth=1, relheight=1)
    # background_label.image = background_image
   
    tk.Label(edit_ticket_window, text="รหัสตั๋วที่ต้องการแก้ไข:",font=("Helvetica", 18)).place(x=350, y=100) 
    ticket_id_entry = tk.Entry(edit_ticket_window,highlightthickness=0,borderwidth=0,cursor='hand2',font=("Helvetica", 17))
    ticket_id_entry.place(x=550, y=106) 
    ticket_id_entry.config(bg="#D89B4A",)
        
    def retrieve_ticket_details():
        ticket_id = ticket_id_entry.get()
        
        try:
            ticket_id = int(ticket_id)
        except ValueError:
            msgbox.showerror("ข้อผิดพลาด", "รหัสตั๋วต้องเป็นตัวเลข")
            return

        if ticket_id <= 0:
            msgbox.showerror("ข้อผิดพลาด", "รหัสตั๋วไม่ถูกต้อง กรุณาดูที่หน้าเช็คตั๋ว")
            return

        conn = sqlite3.connect('Booking_van.db')
        c = conn.cursor()
        c.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,))
        ticket_data = c.fetchone()

        if not ticket_data:
            msgbox.showerror(title="Error", message="ไม่พบตั๋วที่ต้องการแก้ไข")
            return
            

        # Create and populate entry fields
        tk.Label(edit_ticket_window, text="ชื่อ:",font=("Helvetica", 18)).place(x=350, y=200) 
        first_name_entry = tk.Entry(edit_ticket_window,highlightthickness=0,borderwidth=0,cursor='hand2',font=("Helvetica", 17))
        first_name_entry.place(x=550, y=208) 
        first_name_entry.insert(0, ticket_data[1])
        first_name_entry.config(bg="#D89B4A",)

        tk.Label(edit_ticket_window, text="นามสกุล:",font=("Helvetica", 18)).place(x=350, y=250) 
        last_name_entry = tk.Entry(edit_ticket_window,highlightthickness=0,borderwidth=0,cursor='hand2',font=("Helvetica", 17))
        last_name_entry.place(x=550, y=257)
        last_name_entry.insert(0, ticket_data[2])
        last_name_entry.config(bg="#D89B4A",)

        tk.Label(edit_ticket_window, text="เบอร์โทรศัพท์:",font=("Helvetica", 18)).place(x=350, y=300) 
        phone_number_entry = tk.Entry(edit_ticket_window,highlightthickness=0,borderwidth=0,cursor='hand2',font=("Helvetica", 17))
        phone_number_entry.place(x=550, y=307)
        phone_number_entry.insert(0, ticket_data[3])
        phone_number_entry.config(bg="#D89B4A",)

        tk.Label(edit_ticket_window, text="อีเมล:",font=("Helvetica", 18)).place(x=350, y=350) 
        email_entry = tk.Entry(edit_ticket_window,highlightthickness=0,borderwidth=0,cursor='hand2',font=("Helvetica", 17))
        email_entry.place(x=550, y=350)
        email_entry.insert(0, ticket_data[4])
        email_entry.config(bg="#D89B4A",)

        def save_edited_ticket():
            new_first_name = first_name_entry.get()
            new_last_name = last_name_entry.get()
            new_phone_number = phone_number_entry.get()
            new_email = email_entry.get()
            if len(new_phone_number) != 10:
                    result_label.config(text="กรุณากรอกหมายเลขโทรศัพท์ให้ถูกต้อง")
                    return

            conn = sqlite3.connect('Booking_van.db')
            c = conn.cursor()
            c.execute("UPDATE tickets SET first_name=?, last_name=?, phone_number=?, email=? WHERE id=?", 
                    (new_first_name, new_last_name, new_phone_number, new_email, ticket_id))
            conn.commit()
            conn.close()

            result_label.config(text="บันทึกการแก้ไขสำเร็จ",font=("Helvetica", 18))


        save_button = tk.Button(edit_ticket_window, text="บันทึกการแก้ไข",font=("Helvetica",18), command=save_edited_ticket)
        save_button.place(x=570, y=400)

    result_label = tk.Label(edit_ticket_window, text="")
    result_label.place(x=570, y=450) 

    retrieve_button = tk.Button(edit_ticket_window, text="ค้นหาตั๋ว",font=("Helvetica",18), command=retrieve_ticket_details)
    retrieve_button.place(x=600, y=150) 
 
    # สร้างปุ่ม "กลับหน้าหลัก" ในหน้าแก้ไขตั๋ว
    close_button = tk.Button(edit_ticket_window, text="กลับหน้าหลัก", command=edit_ticket_window.destroy)
    close_button.place(x=850,y=680)

                
#หน้ายกเลิกตั๋ว
def delete_ticket():
    delete_window = tk.Toplevel(root)
    delete_window.title("ยกเลิกตั๋ว")
    delete_window.geometry("1024x768+220+20")
    delete_window.resizable(False, False)

     #backgroundหน้่ายกเลิกตั๋ว
    # background_image = tk.PhotoImage(file="/Users/suponb./Downloads/กะเทยตายแน่.001 4.png")
    # background_label = tk.Label(delete_window, image=background_image)
    # background_label.pack()
    # background_label.image = background_image
    tk.Label(delete_window, text="รหัสตั๋วที่ต้องการยกเลิก:",font=("Helvetica", 18)).place(x=300, y=100) 
    ticket_id_entry = tk.Entry(delete_window ,highlightthickness=0,borderwidth=0,cursor='hand2')
    ticket_id_entry.place(x=510, y=108) 
    ticket_id_entry.config(bg="#3196FF",)
    # ลบการจองทั้งหม
    def perform_ticket_deletion():
        ticket_id = ticket_id_entry.get()

        try:
            ticket_id = int(ticket_id)  
        except ValueError:
            result_label.config(text="รหัสตั๋วต้องเป็นตัวเลข")
            return

        if ticket_id <= 0:
            result_label.config(text="รหัสตั๋วต้องเป็นค่าบวก")
            return

        # ดำเนินการลบตั๋วจากฐานข้อมูล
        conn = sqlite3.connect('Booking_van.db')
        c = conn.cursor()

        # ตรวจสอบว่ามีตั๋วที่มีรหัสที่ให้ไว้หรือไม่
        c.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,))
        existing_ticket = c.fetchone()

        if existing_ticket:
            # ใช้ msgbox เพื่อยืนยันการยกเลิก
            confirmation = msgbox.askyesno("ยืนยันการยกเลิก", f"คุณต้องการยกเลิกตั๋วรหัส {ticket_id} ใช่หรือไม่? **หากคุณยกเลิกตั๋วแล้ว ทางบริษัทขอสงวนสิทธิ์คืนเงินทุกกรณี**")
            
            if confirmation:
                # ดำเนินการลบ
                c.execute("DELETE FROM tickets WHERE id=?", (ticket_id,))
                conn.commit()
                conn.close()
                result_label.config(text=f"ตั๋วรหัส {ticket_id} ถูกยกเลิกสำเร็จ")
            else:
                result_label.config(text="ยกเลิกการยกเลิกตั๋ว")
        else:
            result_label.config(text=f"ไม่พบตั๋วที่ต้องการยกเลิก")
    
    result_label = tk.Label(delete_window, text="",font=("Helvetica", 18),)
    result_label.place(x=530, y=220)
    result_label.config(bg="#00B796", highlightbackground="#00B796")

    delete_button = tk.Button(delete_window, text="ยกเลิกตั๋ว",font=("Helvetica", 18), command=perform_ticket_deletion)
    delete_button.place(x=560, y=150) 
    # ปุ่มกลับหน้าหลักหน้ายกเลิก
    close_button = tk.Button(delete_window, text="กลับหน้าหลัก", command=delete_window.destroy)
    close_button.place(x=850,y=680)


root = tk.Tk()
root.title("🚐Premium_Van_Booking")
root.geometry("1024x768+220+20")
# เพิ่มพื้นหลังหน้าแรก
root.resizable(False, False)
# background_image = tk.PhotoImage(file="/Users/suponb./Downloads/IMG_6257 2.PNG")
# background_label = tk.Label(root, image=background_image)
# background_label.place(relwidth=1, relheight=1)
# background_label.pack()

# ฟังก์ชันสำหรับติดต่อเรา
def contact_us():
    contact_window = tk.Toplevel(root)
    contact_window.title("ติดต่อเรา")
    contact_window.geometry("1024x768+220+20")
    contact_window.resizable(False, False)
    
# แทรกรูปภาพหน้าติดต่อเรา
    background_image = tk.PhotoImage(file="/Users/suponb./Downloads/IMG_6359.PNG")
    background_label = tk.Label(contact_window, image=background_image)
    background_label.pack()
    background_label.image = background_image

#ปุ่มกลับหน้าหลักหน้าติดต่อเรา
    close_button = tk.Button(contact_window, text="🏠กลับหน้าหลัก", command=contact_window.destroy)
    close_button.place(x=850,y=680)

# Create the button with the image as background
book_ticket_button = tk.Label(root, text="🎟️จองตั๋ว",font=("Helvetica", 30),  compound="center", highlightthickness=0,borderwidth=0,cursor="hand2", fg="white")
book_ticket_button.place(x=280, y=540, anchor="center",)
book_ticket_button.bind("<Button-1>", lambda event: book_ticket())
book_ticket_button.config(bg="#FFB149",)

# สร้างปุ่ม "เช็คตั๋ว"
check_ticket_button = tk.Label(root, text="🎫เช็คตั๋ว",font=("Helvetica", 30),  compound="center", highlightthickness=0,borderwidth=0,cursor="hand2", fg="white",)
check_ticket_button.place(x=515, y=540, anchor="center")
check_ticket_button.bind("<Button-1>", lambda event: check_ticket())
check_ticket_button.config(bg="#FFB149",)

# สร้างปุ่ม "ดูรอบรถ"
show_available_seats_button = tk.Label(root, text="⏰ดูรอบรถ",font=("Helvetica", 30),  compound="center", highlightthickness=0,borderwidth=0,cursor="hand2", fg="white",)
show_available_seats_button.place(x=730, y=540, anchor="center")
show_available_seats_button.bind("<Button-1>", lambda event: show_available_seats())
show_available_seats_button.config(bg="#FFB149",)

# สร้างปุ่ม "แก้ไขตั๋ว"
edit_button =  tk.Label(root, text="✍🏻แก้ไขตั๋ว",font=("Helvetica", 30),  compound="center", highlightthickness=0,borderwidth=0,cursor="hand2", fg="white",)
edit_button.place(x=280, y=625, anchor="center")
edit_button.bind("<Button-1>", lambda event:edit_ticket())
edit_button.config(bg="#FFB149",)
# สร้างปุ่ม "ยกเลิกตั๋ว"
cancel_button = tk.Label(root, text="🚮ยกเลิกตั๋ว",font=("Helvetica", 30),  compound="center", highlightthickness=0,borderwidth=0,cursor="hand2", fg="white",)
cancel_button.place(x=515, y=625, anchor="center")
cancel_button.bind("<Button-1>", lambda event:delete_ticket())
cancel_button.config(bg="#FFB149",)


# สร้างปุ่ม "ติดต่อเรา"
contact_button = tk.Label(root, text="📩ติดต่อเรา", font=("Helvetica", 30),  compound="center", highlightthickness=0,borderwidth=0,cursor="hand2", fg="white",)
contact_button.place(x=735, y=620, anchor="center")
contact_button.bind("<Button-1>", lambda event: contact_us())
contact_button.config(bg="#FFB149",)


# Create a function to close the application
def close_program():
    root.destroy()

# Create a button to close the program
close_button = ttk.Button(root, text="❌ปิดโปรแกรม", command=close_program)
close_button.place(x=850,y=680)

root.mainloop()
