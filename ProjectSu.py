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
import re
import numpy as np
from io import BytesIO
from PIL import Image, ImageTk
from tkinter import simpledialog
import yagmail
from yagmail.error import YagConnectionClosed
from tkinter import messagebox
from datetime import datetime


conn = sqlite3.connect('Prebook.db')
c = conn.cursor()
try:
        #สมัครสมาชิก
        c.execute('''CREATE TABLE regi(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fname VARCHAR(30) NOT NULL,
        lname VARCHAR(30) NOT NULL,
        phone VARCHAR(30) NOT NULL,
        email VARCHAR(50) NOT NULL,
        Password VARCHAR(30) NOT NULL)''')
        #จองตั๋ว
        c.execute('''CREATE TABLE booking(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email VARCHAR(50) NOT NULL,
        location VARCHAR(100) NOT NULL,
        travel_date VARCHAR(10) NOT NULL,
        time_slot VARCHAR(30) NOT NULL,
        day VARCHAR(30) NOT NULL,
        month VARCHAR(30) NOT NULL,
        year VARCHAR(30) NOT NULL,
        status VARCHAR(30) NOT NULL)''')
        c.execute('''CREATE TABLE  Last (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fname VARCHAR(30) NOT NULL,
        lname VARCHAR(30) NOT NULL,
        travel_date VARCHAR(10) NOT NULL,
        time_slot VARCHAR(30) NOT NULL,
        location VARCHAR(100) NOT NULL,
        status VARCHAR(30) NOT NULL
        email VARCHAR(50) NOT NULL)''')
        conn.commit()
except:
        pass

def Register():
        Regitwindow = tk.Toplevel(root)
        Regitwindow.title("Rrgister")
        regi_cm =  False
        Regitwindow.geometry("1024x768+220+20")
        background_image = tk.PhotoImage(file=r"c:\Users\noeyw\Downloads\regit.png")
        background_label = tk.Label(Regitwindow, image=background_image)
        background_label.pack()
        background_label.image = background_image
        def Regemember():
                nonlocal regi_cm
                fname = fname_entry.get()
                lname = lname_entry.get()
                phone = phone_entry.get()
                email = email_entry.get()
                Password = password_entry.get()
                if not fname and not lname and not phone and not email and not Password:##เช็คว่ากรอกข้อมูลครบหรือไม่
                        result_label.config(text="กรุณากรอกข้อมูลให้ครบถ้วน")    
                else: 
                        if not phone.isdigit() or len(phone) != 10:##เช็คเบอร์
                                result_label.config(text="กรุณากรอกหมายเลขโทรศัพท์ให้ถูกต้อง")
                        else :
                                try:       
                                        if len(Password)>=6 and re.match(r'^[A-Z]', Password):##check password
                                                conn = sqlite3.connect('Prebook.db')
                                                c = conn.cursor()
                                                c.execute("SELECT email FROM regi WHERE email=?", (email,))
                                                check_email = c.fetchone()
                                                if check_email:##check email
                                                        result_label.config(text="มีอีเมลล์นี้อยู่แล้ว กรุณาใช้อีเมลล์อื่น")
                                                elif not re.match("^[a-zA-Z0-9 @ . .]+$", email)or not email.endswith('.com'):
                                                        result_label.config(text="กรุณาตรวจสอบอีเมลล์ให้ถูกต้อง")
                                                else:          
                                                        sql = '''INSERT INTO regi (fname, lname, phone, email, Password) VALUES (?, ?, ?, ?, ?)'''
                                                        data = (fname, lname, phone, email, Password)
                                                        c.execute(sql, data)
                                                        
                                                        conn.commit()
                                                        messagebox.showinfo("result", "ลงทะเบียนสำเร็จ:)")                                                        
                                                        regi_cm = True
                                                        delay_ms = 500
                                                        Regitwindow.after(delay_ms, Regitwindow.destroy())  
                                        else:
                                                result_label.config(text="รหัสผ่านควรขึ้นต้นด้วยตัวอักษรพิมพ์ใหญ่\nและต้องมีอย่างน้อย 6 ตัวขึ้นไป")
                                except:
                                        ()

        tk.Label(Regitwindow, text="ชื่อจริง:", font=("Helvetica", 20) ,bg='#446C9E', fg="white", highlightthickness=0, borderwidth=0,).place(x=260, y=130)
        fname_entry = tk.Entry(Regitwindow, bg="#CBCBCB", highlightthickness=0, borderwidth=0, cursor='hand2', font=("Helvetica", 17))  
        fname_entry.place(x=440, y=140)

        tk.Label(Regitwindow, text="นามสกุล:",font=("Helvetica",20) ,bg='#446C9E', fg="white", highlightthickness=0, borderwidth=0,).place(x=260, y=220)
        lname_entry = tk.Entry(Regitwindow, bg="#CBCBCB", highlightthickness=0, borderwidth=0, cursor='hand2', font=("Helvetica", 17))
        lname_entry.place(x=440, y=230)

        tk.Label(Regitwindow, text="เบอร์โทรศัพท์:",font=("Helvetica", 20) ,bg='#446C9E', fg="white", highlightthickness=0, borderwidth=0,).place(x=240, y=310)
        phone_entry = tk.Entry(Regitwindow, bg="#CBCBCB", highlightthickness=0, borderwidth=0, cursor='hand2', font=("Helvetica", 17))
        phone_entry.place(x=440, y=320)

        tk.Label(Regitwindow, text="อีเมล:",font=("Helvetica", 20) ,bg='#446C9E', fg="white", highlightthickness=0, borderwidth=0,).place(x=260, y=400)
        email_entry = tk.Entry(Regitwindow, bg="#CBCBCB", highlightthickness=0, borderwidth=0, cursor='hand2', font=("Helvetica", 17))
        email_entry.place(x=440, y=410)

        tk.Label(Regitwindow, text="รหัสผ่าน:",font=("Helvetica", 20) ,bg='#446C9E', fg="white", highlightthickness=0, borderwidth=0,).place(x=260, y=490)
        password_entry = tk.Entry(Regitwindow, bg="#CBCBCB", highlightthickness=0, borderwidth=0, cursor='hand2', font=("Helvetica", 17))
        password_entry.place(x=440, y=500)

        result_label = Label(Regitwindow, text="",bg='#ffffff',fg='black',font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0)
        result_label.place(x=520,y=550)

        #ปุ่มสมัครสมาชิก 
        reg_But= Button(Regitwindow ,bg='#D89B4A',text="สมัครสมาชิก" ,fg='black',command=Regemember,cursor="hand2", font=("DB Helvethaica X", 20),borderwidth=0, highlightthickness=0,activebackground='#D89B4A')
        reg_But.place(x=540,y=585) 

        #ปุ่มกลับหน้าหลัก
        back1_But= Button(Regitwindow ,bg='#ffffff',text="ย้อนกลับ", fg='black',command=lambda:(Regitwindow.destroy()),cursor="hand2", font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0,activebackground='#ffffff')
        back1_But.place(x=800,y=700)

def loing():
        loingwindow=tk.Toplevel(root)
        loingwindow.title("Login Page")
        loingwindow.geometry("1024x768+220+20")
        loingwindow.resizable(False, False)
        background_image = tk.PhotoImage(file=r"c:\Users\noeyw\Downloads\Loi.png")
        background_label = tk.Label(loingwindow, image=background_image)
        background_label.pack()
        background_label.image = background_image
        logged_in_fname = ""
        logged_in_lname = ""
        show_phone="" 
        show_email=""
        fname=""
        lname=""
        phone=""
        e=""
        pw=""
        date=""
        def loingchecks():##เข้าสู่ระบบเช็ค
                nonlocal logged_in_fname #ใช้ประกาศตัวแปรให้ใช้ในฟังก์ชันอื่นภายนอกฟังก์ชันตัวเอง
                nonlocal logged_in_lname 
                nonlocal show_email 
                nonlocal show_phone
                email = email_entry.get()
                password = password_entry.get()
                show_email=email
                conn = sqlite3.connect('Prebook.db')
                c = conn.cursor()
                c.execute("SELECT * FROM regi WHERE email=? AND password=?", (email, password))
                log = c.fetchone()
                if log :
                        logged_in_fname = log[1]  # ชื่ออยู่ในตำแหน่งที่ 1 ของผลลัพธ์ที่คืนมา
                        logged_in_lname = log[2]
                        show_phone=log[3]
                        result_label.config(text=f'เข้าสู่ระบบสำเร็จ\nชื่อ: {logged_in_fname} {logged_in_lname}')
                        delay_ms = 500
                        loingwindow.after(delay_ms, booking())                          
                elif  email=='admin' and password=='1': 
                        admin()
                        loingwindow.destroy()                            
                else:
                        result_label.config(text='เข้าสู่ระบบไม่สำเร็จ\nโปรดตรวจสอบอีเมลล์และรหัสผ่านของคุณอีกครั้ง')

        Label(loingwindow, text="อีเมล:", font=("Helvetica", 25) ,bg='#446C9E', fg="white", highlightthickness=0, borderwidth=0,).place(x=260, y=250)
        email_entry =Entry(loingwindow, bg="#CBCBCB", highlightthickness=0, borderwidth=0, cursor='hand2', font=("Helvetica", 17))  
        email_entry.place(x=440, y=270)

        Label(loingwindow, text="รหัสผ่าน:", font=("Helvetica", 25) ,bg='#446C9E', fg="white", highlightthickness=0, borderwidth=0,).place(x=250, y=350)
        password_entry = Entry(loingwindow,show='*', bg="#CBCBCB", highlightthickness=0, borderwidth=0, cursor='hand2', font=("Helvetica", 17))  
        password_entry.place(x=440, y=370) 

        result_label = Label(loingwindow, text="",bg='#FFFFFF',fg='black',font=("DB Helvethaica X", 10))
        result_label.place(x=470,y=410)
      
        def repasword():##func รีเซ็ทรหัส
                loingwindow.destroy() 
                forgotpwwindow = Toplevel(root)
                forgotpwwindow.title("Forgot Password")
                forgotpwwindow.geometry("1024x768+220+20")
                forgotpwwindow.resizable(False,False)
                bg_image_forgot = Image.open(r"c:\Users\noeyw\Downloads\22.png")
                bg_photo_forgot = ImageTk.PhotoImage(bg_image_forgot)
                bg_label_forgot = Label(forgotpwwindow,image=bg_photo_forgot)
                bg_label_forgot.photo = bg_photo_forgot # เก็บ reference รูปภาพ
                bg_label_forgot.pack(fill="both", expand=True)
                def changePassword():
                        email = email_entry.get()
                        new_password = new_password_entry.get()
                        conn = sqlite3.connect('Prebook.db')
                        c=conn.cursor()
                        c.execute("SELECT * FROM regi WHERE email=?",(email,))
                        user=c.fetchone()
                        if user:
                                if len(new_password)>=6 and re.match(r'^[A-Z]', new_password):
                                        if new_password != user[5]:
                                                c.execute("UPDATE regi SET password=? WHERE email=?",(new_password,email))
                                                conn.commit()
                                                result_label.config(text='เปลี่ยนรหัสผ่านสำเร็จค่ะ (✯◡✯)',font=("DB Helvethaica X", 10))    
                                                delay_ms = 500
                                                forgotpwwindow.after(delay_ms,lambda:(forgotpwwindow.destroy(),loing()))   
                                        else :
                                                result_label.config(text='รหัสผ่านใหม่ต้องไม่ซ้ำกับรหัสผ่านเดิมค่ะ (πーπ)', font=("DB Helvethaica X", 10))
                                else:
                                        result_label.config(text='รหัสผ่านควรขึ้นต้นด้วยตัวอักษรพิมพ์ใหญ่\nและต้องมีอย่างน้อย 6 ตัวขึ้นไป (πーπ)', font=("DB Helvethaica X", 10))
                        else:
                                result_label.config(text='ไม่พบสมาชิก (πーπ)',font=("DB Helvethaica X", 10),)

                Label(forgotpwwindow, text="อีเมล:", font=("Helvetica", 20) ,bg='#446C9E', fg="white", highlightthickness=0, borderwidth=0,).place(x=250, y=260)
                email_entry = Entry(forgotpwwindow, bg="#CBCBCB", highlightthickness=0, borderwidth=0, cursor='hand2', font=("Helvetica", 17))
                email_entry.place(x=470, y=270)

                Label(forgotpwwindow, text="รหัสผ่านใหม่:", font=("Helvetica", 20) ,bg='#446C9E', fg="white", highlightthickness=0, borderwidth=0,).place(x=240, y=350)
                new_password_entry = Entry(forgotpwwindow, bg="#CBCBCB", highlightthickness=0, borderwidth=0, cursor='hand2', font=("Helvetica", 17))
                new_password_entry.place(x=470, y=360) 

                result_label = Label(forgotpwwindow, text="",bg='#ffffff',fg='black',font=("DB Helvethaica X", 10))
                result_label.place(x=470,y=420)

                resetpass_But= Button(forgotpwwindow,text="เปลี่ยนรหัสผ่าน:",bg='#D89B4A',fg='black',command=changePassword,cursor="hand2", font=("DB Helvethaica X", 20),borderwidth=0, highlightthickness=0,activebackground='#fcd9e2')
                resetpass_But.place(x=520,y=460)
                
                back2_But= Button(forgotpwwindow,text="ย้อนกลับ:",bg='#ffffff',fg='black',command=lambda:(forgotpwwindow.destroy(),loing()),cursor="hand2", font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0,activebackground='#ffffff')
                back2_But.place(x=850,y=680) 

            
        def booking ():
                bookingwindow=Toplevel(root)
                bookingwindow.title("จองตั๋ว")
                bookingwindow.geometry("1024x768+220+20") 
                background_image = tk.PhotoImage(file=r"c:\Users\noeyw\Downloads\Book11.png")
                background_label = tk.Label(bookingwindow, image=background_image)
                background_label.pack()
                background_label.image = background_image
                def bookticket ():
                        location = location_var.get()
                        time_slot = time_slot_var.get()
                        travel_date = cal.get_date()
                        year, month, day = map(int, travel_date.split('-'))
                        if not location or not time_slot or not travel_date:
                                result_label.config(text="กรุณากรอกข้อมูลให้ครบถ้วน")
                        else:
                                # ตรวจสอบว่าวันที่ที่ผู้ใช้เลือกไม่ซ้ำกับวันที่อื่นที่มีอยู่ในระบบ
                                conn = sqlite3.connect('Prebook.db')
                                c = conn.cursor()
                                c.execute("SELECT COUNT(*) FROM booking WHERE travel_date = ?", (travel_date,))
                                booking_count = c.fetchone()[0]  # ดึงจำนวนแถวที่มีวันที่ซ้ำกัน
                                conn.close()
                                if   travel_date < current_date:
                                        result_label.config(text="กรุณาเลือกวันที่ให้ถูกต้อง\nไม่สามารถจองวันในอดีตได้ค่ะ ")
                                elif booking_count > 7:
                                        result_label.config(text="วันที่นี้ถูกจองแล้ว")
                                else : 
                                    pay = tk.Toplevel(root)
                                    pay.title("Payment")
                                    pay.geometry("1024x768+220+20")
                                    pay.resizable(False, False)
                                    background_image = tk.PhotoImage(file=r"c:\Users\noeyw\Downloads\pay12.png")
                                    background_label = tk.Label(pay, image=background_image)
                                    background_label.place(x=0, y=0, relwidth=1, relheight=1)
                                    background_label.image = background_image
                                    def final():
                                            response = messagebox.askyesno("การจอง", "คุณชำระเงินเรียบร้อยใช่หรือไม่?")
                                            if response>0:
                                                    conn = sqlite3.connect('Prebook.db')
                                                    c = conn.cursor()
                                                    # sql1 = '''INSERT INTO booking (email,location, time_slot, travel_date ,day,month,year ,status) VALUES (?,?,?, ?,?,?,?, ?)'''
                                                    # booked = (show_email,prices_options, time_slot, travel_date,day,month,year,"รอดำเนินการ")
                                                    # c.execute(sql1, booked)
                                                    c.execute("INSERT INTO booking (email,location, time_slot, travel_date ,day,month,year ,status) VALUES (?,?,?, ?,?,?,?, ?)",(show_email,location, time_slot, travel_date,day,month,year,"รอดำเนินการ",))
                                                    conn.commit()
                                                    conn.close()
                                                    messagebox.showinfo("Result", "การจองสำเร็จ ")
                                                    email = show_email
                                                    try:
                                                            # กำหนดข้อมูลเข้าสู่ระบบของอีเมล์
                                                            email_sender = "premiumvanbooking@gmail.com"
                                                            app_password = "gcqt nwpn rwcr asay "  # กรอกรหัส 16 หลักจากการสร้าง App Password
                                                            # เริ่มต้นเซสชัน Yagmail
                                                            yag = yagmail.SMTP(email_sender, app_password)
                                                            # กำหนดผู้รับ
                                                            recipients = [email]
                                                            text = f"✅Booking ticket confirm\n ⚠️ให้ท่านนำตั๋วมาแสดงต่อเจ้าหน้าที่ก่อนขึ้นรถ\n"
                                                            text += "----------------------------------------------------\n"
                                                            text += f"ชื่อผู้จอง: {logged_in_fname}  {logged_in_lname}\n"
                                                            text += f"เดินทางวันที่: {travel_date}\n"
                                                            text += f"เวลา: {time_slot}\n"
                                                            text += f"จุดหมายปลายทาง: {location}\n"
                                                            text += f"หมายเลขติดต่อ: {show_phone}\n"
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
                                                            messagebox.showerror("Error", "Connection to email server failed. Please check your credentials and internet connection.")
                                                    except Exception as e:
                                                            messagebox.showerror("Error", f"An error occurred while sending the email: {str(e)}")
                                            else:
                                                    messagebox.showinfo("Result", "กรุณาทำรายการใหม่อีกครั้งค่ะ")
                                                    bookticket()
                                    info_label =Label(pay, text=f"{logged_in_fname} {logged_in_lname} ",bg='#294364',fg="#FFFFFF",font=("DB Helvethaica X", 15))
                                    info_label.place(x=260,y=237)
                                    info_label1 =Label(pay, text=f"{show_phone} ",bg='#294364',fg="#FFFFFF",font=("DB Helvethaica X", 15))
                                    info_label1.place(x=260,y=307)
                                    info_label2 =Label(pay, text=f"{location} ",bg='#294364',fg="#FFFFFF",font=("DB Helvethaica X", 15))
                                    info_label2.place(x=260,y=377)
                                    info_label2 =Label(pay, text=f"{time_slot} ",bg='#294364',fg="#FFFFFF",font=("DB Helvethaica X", 15))
                                    info_label2.place(x=260,y=447)
                                    info_label2 =Label(pay, text=f"{travel_date} ",bg='#294364',fg="#FFFFFF",font=("DB Helvethaica X", 15))
                                    info_label2.place(x=260,y=504)
                                    #หน้าจ่ายเงิน
                                    prices = {  "ท่ารถตู้ปรับอากาศขอนแก่น-เซ็นทรัลขอนแก่น": 16,
                                                "ท่ารถตู้ปรับอากาศขอนแก่น-แยกน้ำพอง": 92,
                                                "ท่ารถตู้ปรับอากาศขอนแก่น-เขาสวนกวาง": 134,
                                                "ท่ารถตู้ปรับอากาศขอนแก่น-แยกกุมภวาปี": 190,
                                                "ท่ารถตู้ปรับอากาศขอนแก่น-เซ็นทรัลอุดรธานี(บขส1)": 249,
                                                "เซ็นทรัลขอนแก่น-แยกน้ำพอง": 76,
                                                "เซ็นทรัลขอนแก่น-เขาสวนกวาง": 120,
                                                "เซ็นทรัลขอนแก่น-แยกน้ำพอง": 237,
                                                "แยกน้ำพอง-เขาสวนกวาง": 44,
                                                "แยกน้ำพอง-แยกกุมภวาปี": 98,
                                                "แยกน้ำพอง-เซ็นทรัลอุดรธานี(บขส1)": 160,
                                                "เขาสวนกวาง-แยกกุมภวาปี": 54,
                                                "เขาสวนกวาง-เซ็นทรัลอุดรธานี(บขส1)": 116,
                                                "แยกกุมภวาปี-เซ็นทรัลอุดรธานี(บขส1)": 62
                                                }
                                    

                                    total_price = prices.get(location, 0)
                                    price_url = f"https://promptpay.io/0973190292/{total_price}.png"
                                    price_url = price_url

                                    # Send a request to download the image
                                    response = requests.get(price_url)
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
                                            label.place(x = 670, y = 350)

                                            close_button = tk.Button(pay, text="ชำระเงินแล้ว", command=lambda:(final()))
                                            close_button.place(x=400,y=600)

                                            back_But= Button(pay, text="ย้อนกลับ",bg='#ffffff',command=lambda:(pay.destroy()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#fcdbe2')
                                            back_But.place(x=900, y=700)       

                                    else:
                                            print("Failed to download the image. HTTP status code:", response.status_code)
                                                
                Label(bookingwindow, text="สถานที่ขึ้น-ลง:", font=("Helvetica", 16), bg='#D89B4A', fg="white", highlightthickness=0, borderwidth=0).place(x=120, y=350)
                prices_options = [  "ท่ารถตู้ปรับอากาศขอนแก่น-เซ็นทรัลขอนแก่น",
                                    "ท่ารถตู้ปรับอากาศขอนแก่น-แยกน้ำพอง",
                                    "ท่ารถตู้ปรับอากาศขอนแก่น-เขาสวนกวาง",
                                    "ท่ารถตู้ปรับอากาศขอนแก่น-แยกกุมภวาปี", 
                                    "ท่ารถตู้ปรับอากาศขอนแก่น-เซ็นทรัลอุดรธานี(บขส1)", 
                                    "เซ็นทรัลขอนแก่น-แยกน้ำพอง", 
                                    "เซ็นทรัลขอนแก่น-เขาสวนกวาง", 
                                    "เซ็นทรัลขอนแก่น-แยกน้ำพอง", 
                                    "แยกน้ำพอง-เขาสวนกวาง", 
                                    "แยกน้ำพอง-แยกกุมภวาปี", 
                                    "แยกน้ำพอง-เซ็นทรัลอุดรธานี(บขส1)", 
                                    "เขาสวนกวาง-แยกกุมภวาปี", 
                                    "เขาสวนกวาง-เซ็นทรัลอุดรธานี(บขส1)", 
                                    "แยกกุมภวาปี-เซ็นทรัลอุดรธานี(บขส1)" ]
                        
                location_var = StringVar()
                location_var.set(prices_options[0])
                location_menu = OptionMenu(bookingwindow, location_var, *prices_options)
                location_menu.place(x=260, y=350)
                
                Label(bookingwindow, text="เวลาเดินทาง:",font=("Helvetica", 16) ,bg='#D89B4A', fg="white", highlightthickness=0, borderwidth=0,).place(x=120, y=410)
                time_slot_var = StringVar(bookingwindow)
                time_slots = {
                        1: "06:00-08:00",
                        2: "10:00-12:00",
                        3: "14:00-16:00",
                        4: "19:00-21:00"
                }
                time_slot_var.set(time_slots[1])  # Set the default time slot
                time_slot_menu = OptionMenu(bookingwindow, time_slot_var, *time_slots.values())
                time_slot_menu.place(x=260, y=410)
                
                Label(bookingwindow, text="วันเดินทาง:", font=("Helvetica", 16), bg='#D89B4A', fg="white", highlightthickness=0, borderwidth=0).place(x=120, y=150)
                current_date = datetime.now().strftime('%Y-%m-%d')
                cal = Calendar(bookingwindow, selectmode="day", year=2023, month=10, day=1, date_pattern="yyyy-mm-dd", date=current_date)
                cal.place(x=270, y=150)

                
                confirm_But= Button(bookingwindow,text="บันทึก",bg='#D89B4A',fg='#ffffff', font=("Helvetica", 20),command=lambda:(bookticket()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#fcdce2')
                confirm_But.place(x=280, y=600)

                back_But= Button(bookingwindow,text="ย้อนกลับ",bg='#ffffff',fg='black',command=lambda:(bookingwindow.destroy(),Place()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#fcdce2')
                back_But.place(x=900, y=700)

                result_label = Label(bookingwindow, text="",bg='#FFFFFF',font=("DB Helvethaica X", 10),fg='black')
                result_label.place(x=250,y=685)

        def admin():
                admin_window = Toplevel(root)
                admin_window.title("Admin")
                admin_window.geometry("1024x768+220+20") 
                admin_window.resizable(False,False)
                # background_image = tk.PhotoImage(file=r"c:\Users\noeyw\Downloads\admin.png")
                # background_label = tk.Label(admin_window, image=background_image)
                # background_label.pack()
                # background_label.image = background_image

                def on_vertical_scroll(*args):
                        tree.yview(*args)
                tree_label = tk.Label(admin_window, text="ข้อมูลทั้งหมด", font=("DB Helvethaica X", 14))
                tree_label.pack()
                frame = ttk.Frame(admin_window)
                frame.pack()
                tree = ttk.Treeview(frame,columns=("id","name","lastname","phone","email","Password"))
                tree.heading("id",text="id")
                tree.heading("name",text="ชื่อ")
                tree.heading("lastname",text="นามสกุล")
                tree.heading("phone",text="เบอร์")
                tree.heading("email",text="อีเมล")
                tree.heading("Password",text="รหัส")
                tree.column("id",anchor="center",width=60)
                tree.column("name",anchor="center",width=125)
                tree.column("lastname",anchor="center",width=125)
                tree.column("phone",anchor="center",width=110)
                tree.column("email",anchor="center",width=150)
                tree.column("Password",anchor="center",width=100)
                tree.column("#0",width=0,stretch=NO)
                style = ttk.Style()
                style.configure("Treeview.Heading",font = ("DB Helvethaica X",12))
                style.configure("Treeview", font=("DB Helvethaica X", 12))
                conn = sqlite3.connect("Prebook.db")
                c = conn.cursor()
                c.execute("SELECT * FROM regi ")
                result = c.fetchall()
                for x in result :
                        tree.insert("","end",values=x)
                vscrollbar = ttk.Scrollbar(frame, orient="vertical", command=on_vertical_scroll)
                vscrollbar.pack(side="right", fill="y")
                tree.config(yscrollcommand=vscrollbar.set)
                tree.pack(fill="both", expand=True)
                def on_vertical_scroll(*args):
                        tree.yview(*args) 
                tree_label = tk.Label(admin_window, text="ข้อมูลการจอง", font=("DB Helvethaica X", 14))
                tree_label.pack()
                frame1 = ttk.Frame(admin_window)
                frame1.pack()
                tree = ttk.Treeview(frame1,columns=("id","email","location","travel_date","time_slot","status"))
                tree.heading("id",text="")
                tree.heading("email",text="อีเมลล์")
                tree.heading("location",text="สถานที่ขึ้นลง")
                tree.heading("travel_date",text="วันที่จอง")
                tree.heading("time_slot",text="รอบรถ")
                tree.heading("status",text="สถานะ")
                tree.column("id",anchor="center",width=60)
                tree.column("email",anchor="center",width=150)
                tree.column("location",anchor="center",width=100)
                tree.column("travel_date",anchor="center",width=100)
                tree.column("time_slot",anchor="center",width=150)
                tree.column("status",anchor="center",width=130)
                tree.column("#0",width=0,stretch=NO)
                
                style = ttk.Style()
                style.configure("Treeview.Heading",font = ("DB Helvethaica X", 12))
                style.configure("Treeview", font=("DB Helvethaica X", 12))
                conn = sqlite3.connect("Prebook.db")
                c = conn.cursor()
                c.execute("SELECT * FROM booking ")
                result = c.fetchall()
                for x in result :
                        tree.insert("", "end", values=(x[0],x[1], x[2], x[3], x[7], x[8]))
                vscrollbar = ttk.Scrollbar(frame1, orient="vertical", command=on_vertical_scroll)
                vscrollbar.pack(side="right", fill="y")
                tree.config(yscrollcommand=vscrollbar.set)
                tree.pack(fill="both", expand=True)
                def delete_booking() :
                        conn = sqlite3.connect('Prebook.db')
                        c = conn.cursor()
                        c.execute("DELETE FROM data WHERE status = 'เสร็จสิ้น'")
                        conn.commit()
                        conn.close()

                edit_But= Button(admin_window,text="แก้ไขตั๋ว",bg='#ffffff',font=("Helvetica", 20),command=lambda:(edit_ticket(),admin_window.destroy()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#D89B4A')
                edit_But.place(x=230,y=550) 
                
                delete_but = Button(admin_window,text="ยกเลิกตั๋ว", bg='#ffffff',font=("Helvetica", 20),command=lambda: (delete_ticket()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#D89B4A')
                delete_but.place(x=420,y=550) 
        
                sum_But= Button(admin_window,text="รายได้รวมทั้งหมด",bg='#ffffff',font=("Helvetica", 18),command=lambda:(admin_window.destroy(),show_sum()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#D89B4A')
                sum_But.place(x=590, y=555)

                back_But= Button(admin_window,text="ย้อนกลับ",bg='#ffffff',command=lambda:(admin_window.destroy(),loing()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#D89B4A')
                back_But.place(x=850,y=690) 

        def edit_ticket():
                edit_ticket_window = Toplevel(root)
                edit_ticket_window.title("แก้ไขตั๋ว")
                edit_ticket_window.geometry("1024x768+220+20")
                edit_ticket_window.resizable(False, False)
                background_image = tk.PhotoImage(file=r"c:\Users\noeyw\Downloads\editfi.png")
                background_label = tk.Label( edit_ticket_window, image=background_image)
                background_label.place(x=0, y=0, relwidth=1, relheight=1)
                background_label.image = background_image
                def edit():
                        email = email_entry.get()    
                        conn = sqlite3.connect('Prebook.db')
                        c = conn.cursor() 
                        c.execute("SELECT fname FROM regi WHERE email=?", (email,))
                        booked = c.fetchall()
                        for x in booked :
                                nentry=Entry(edit_ticket_window,textvariable=fname,width = 13,borderwidth=0,bg="#FFB149",font=("DB Helvethaica X", 18))
                                nentry.insert(0,x)
                                nentry.place(x=240 ,y=230)
                        c.execute("SELECT lname FROM regi WHERE email=?", (email,))
                        booked = c.fetchall()
                        for x in booked :
                                lnameentry=Entry(edit_ticket_window,textvariable=lname,width = 13,borderwidth=0,bg="#FFB149",font=("DB Helvethaica X", 18))
                                lnameentry.insert(0,x)
                                lnameentry.place(x=660 ,y=230)
                        c.execute("SELECT phone FROM regi WHERE email=?", (email,))
                        booked = c.fetchall()
                        for x in booked :
                                telentry=Entry(edit_ticket_window,textvariable=phone,width = 13,borderwidth=0,bg="#FFB149",font=("DB Helvethaica X", 18))
                                telentry.insert(0,x)
                                telentry.place(x=660 ,y=295)
                        c.execute("SELECT email FROM regi WHERE email=?", (email,))
                        booked = c.fetchall()
                        for x in booked :
                                eentry=Entry(edit_ticket_window,textvariable=email,width = 25,borderwidth=0,bg="#FFB149",font=("DB Helvethaica X", 13))
                                eentry.insert(0,x)
                                eentry.place(x=230 ,y=310)
                        c.execute("SELECT password FROM regi WHERE email=?", (email,))
                        booked = c.fetchall()
                        for x in booked :
                                pwentry=Entry(edit_ticket_window,textvariable=pw,width = 13,borderwidth=0,bg="#FFB149",font=("DB Helvethaica X", 18))
                                pwentry.insert(0,x)
                                pwentry.place(x=240 ,y=370) 
                    
                        c.execute("SELECT status FROM booking WHERE email=?", (email,))
                        booked = c.fetchall()
                        status_var = StringVar()
                        status_options = ["การจองสำเร็จ", "เสร็จสิ้น"]
                        status_var.set("ระบุสถานะ")
                        status_menu = OptionMenu(edit_ticket_window, status_var, *status_options)
                        status_menu.place(x=400, y=525)

                        def saveedit():
                                n1 = nentry.get()
                                lname = lnameentry.get()
                                tel = telentry.get()
                                e = eentry.get()
                                pw = pwentry.get()
                                email = email_entry.get()
                                conn = sqlite3.connect('Prebook.db')
                                c = conn.cursor()
                                data=(n1,lname,tel,e,pw,email)
                                c.execute('''UPDATE regi SET fname=?,lname=?,phone=?,email=?,Password=?  WHERE email=?''',data)
                                conn.commit()
                                conn.close()
                        def statusup():
                                status=status_var.get()
                                conn = sqlite3.connect('Prebook.db')
                                c = conn.cursor()
                                c.execute('''UPDATE booking SET status=? WHERE email=?''', (status, email))
                                conn.commit()
                                conn.close()
                        def clear_booking():
                                conn = sqlite3.connect('Prebook.db')
                                c = conn.cursor()
                                c.execute("DELETE FROM booking WHERE email=? ",(email,))
                                conn.commit()
                                conn.close()

                        save_But= Button(edit_ticket_window,text="บันทึก", bg='#ED6B59',fg='black',font=("Helvetica", 18),command=lambda: (saveedit(),edit_ticket_window.destroy(),admin()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#ffffff')
                        save_But.place(x=670, y=380)

                        save_But= Button(edit_ticket_window,text='บันทึกสถานะ',bg='#ED6B59',fg='black',font=("Helvetica", 16),command=lambda: (statusup()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#ffffff')
                        save_But.place(x=670, y=525)
        

                email_entry = Entry(edit_ticket_window,width=25, font=("DB Helvethaica X", 16),bg="#FFB149",borderwidth=0, highlightthickness=0)
                email_entry.place(x=400, y=150)


                serch_But = Button(edit_ticket_window,text="ค้นหา", bg='#A73B24', command=edit, font=("DB Helvethaica X", 10),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#fcd3e2')
                serch_But.place(x=760, y=150)

                back_But= Button(edit_ticket_window, text="ย้อนกลับ",bg='#ffffff',command=lambda:(edit_ticket_window.destroy(),admin()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#fcdbe2')
                back_But.place(x=850,y=680)  

        def delete_ticket():
            delete_window = tk.Toplevel(root)
            delete_window.title("ยกเลิกตั๋ว")
            delete_window.geometry("1024x768+220+20")
            delete_window.resizable(False, False)
            background_image = tk.PhotoImage(file=r"c:\Users\noeyw\Downloads\del.png")
            background_label = tk.Label(delete_window, image=background_image)
            background_label.pack()
            background_label.image = background_image
            tk.Label(delete_window, text="รหัสตั๋วที่ต้องการยกเลิก:",font=("Helvetica", 16)).place(x=260, y=100) 
            ticket_id_entry = tk.Entry(delete_window ,highlightthickness=0,borderwidth=0,cursor='hand2')
            ticket_id_entry.place(x=510, y=108) 
            ticket_id_entry.config(bg="#3196FF",)
            # ลบการจองทั้งหมด
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
                conn = sqlite3.connect('Prebook.db')
                c = conn.cursor()

                # ตรวจสอบว่ามีตั๋วที่มีรหัสที่ให้ไว้หรือไม่
                c.execute("SELECT * FROM booking WHERE id=?", (ticket_id,))
                existing_ticket = c.fetchone()

                

                if existing_ticket:
                    # ใช้ msgbox เพื่อยืนยันการยกเลิก
                    confirmation = msgbox.askyesno("ยืนยันการยกเลิก", f"คุณต้องการยกเลิกตั๋วรหัส {ticket_id} ใช่หรือไม่? **หากคุณยกเลิกตั๋วแล้ว ทางบริษัทขอสงวนสิทธิ์คืนเงินทุกกรณี**")
                    
                    if confirmation:
                        # ดำเนินการลบ
                        c.execute("DELETE FROM booking WHERE id=?", (ticket_id,))
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

            delete_button = tk.Button(delete_window, text="ยกเลิกตั๋ว",font=("Helvetica", 16), command=perform_ticket_deletion)
            delete_button.place(x=560, y=150) 
            # ปุ่มกลับหน้าหลักหน้ายกเลิก
            close_button = tk.Button(delete_window, text="ย้อนกลับ", command=delete_window.destroy)
            close_button.place(x=850,y=680)


        def summary():
                conn = sqlite3.connect('Prebook.db')
                c = conn.cursor()
                c.execute("SELECT travel_date, location FROM booking")
                bookings = c.fetchall()
                amount = {} # สร้างพจนานุกรมเพื่อเก็บยอดเงินรายเดือน
                # นับยอดเงินในแต่ละเดือน
                for booking in bookings:
                        travel_date = booking[0]#ดึงวันที่จองจาก tuple ใน bookings
                        year, month, _ = map(int, travel_date.split('-'))
                        location = booking[1]
                        prices = { "ท่ารถตู้ปรับอากาศขอนแก่น-เซ็นทรัลขอนแก่น": 16,
                                        "ท่ารถตู้ปรับอากาศขอนแก่น-แยกน้ำพอง": 92,
                                        "ท่ารถตู้ปรับอากาศขอนแก่น-เขาสวนกวาง": 134,
                                        "ท่ารถตู้ปรับอากาศขอนแก่น-แยกกุมภวาปี": 190,
                                        "ท่ารถตู้ปรับอากาศขอนแก่น-เซ็นทรัลอุดรธานี(บขส1)": 249,
                                        "เซ็นทรัลขอนแก่น-แยกน้ำพอง": 76,
                                        "เซ็นทรัลขอนแก่น-เขาสวนกวาง": 120,
                                        "เซ็นทรัลขอนแก่น-แยกน้ำพอง": 237,
                                        "แยกน้ำพอง-เขาสวนกวาง": 44,
                                        "แยกน้ำพอง-แยกกุมภวาปี": 98,
                                        "แยกน้ำพอง-เซ็นทรัลอุดรธานี(บขส1)": 160,
                                        "เขาสวนกวาง-แยกกุมภวาปี": 54,
                                        "เขาสวนกวาง-เซ็นทรัลอุดรธานี(บขส1)": 116,
                                        "แยกกุมภวาปี-เซ็นทรัลอุดรธานี(บขส1)": 62
                                        }

                        income = prices.get(location)##ดึงราคาของแพ็คเกจที่ถูกจองและเก็บไว้ในตัวแปร 
                        # เพิ่มยอดเงินในแต่ละเดือน##ตรวจสอบว่าข้อมูลรายได้สำหรับเดือนและปีที่กำลังพิจารณาอยู่ในamount
                        if (year, month) in amount:
                                amount[(year, month)] += income
                        else:
                                amount[(year, month)] = income
                conn.close()
                return amount
        
        def show_sum():
            result_window = Toplevel(root)
            result_window.title("สรุปยอดเงินรายเดือน")
            result_window.geometry("1024x768+220+20")
            result_window.resizable(False,False)

            canvas = Canvas(result_window, width=1000, height=650)
            canvas.pack()
            bg_image = Image.open(r"c:\Users\noeyw\Downloads\last.png")
            bg_photo = ImageTk.PhotoImage(bg_image)
            canvas.create_image(0, 0, anchor=NW, image=bg_photo)
            canvas.image = bg_photo

            frame = Frame(canvas)  # Create a frame as a child of the canvas
            canvas.create_window((250,200), window=frame, anchor=NW)  # Place the frame on the canvas
            tree = ttk.Treeview(frame, columns=("location", "travel_date", "time_slot", "status"))
            tree.heading("location", text="สถานที่ขึ้น-ลง")
            tree.heading("travel_date", text="วันที่จอง")
            tree.heading("time_slot", text="รอบรถ")
            tree.heading("status", text="สถานะ")
            tree.column("location", anchor="center", width=100)
            tree.column("travel_date", anchor="center", width=100)
            tree.column("time_slot", anchor="center", width=150)
            tree.column("status", anchor="center", width=130)
            tree.column("#0", width=0, stretch=NO)
            style = ttk.Style()
            style.configure("Treeview.Heading", font=("DB Helvethaica X", 12))
            style.configure("Treeview", font=("DB Helvethaica X", 12))         
            tree.pack(pady=10)                                      
            def select_show():
                    selected_month = month_var.get()
                    selected_year = year_var.get()
                    if selected_month != "เดือน" and selected_year != "ปี":
                            selected_month = int(selected_month)
                            selected_year = int(selected_year)

                    if selected_month != "เดือน" and selected_year != "ปี":
                            month_total = summary()
                            result_label.config(text="สรุปยอดเงินรายเดือน")
                            
                            for item in tree.get_children():
                                    tree.delete(item)

                            conn = sqlite3.connect("Prebook.db")
                            c = conn.cursor()
                            c.execute("SELECT * FROM booking WHERE month=? AND year=?", (selected_month, selected_year))
                            result = c.fetchall()
                            
                            for x in result:
                                    tree.insert("", "end", values=(x[2], x[3], x[7], x[8]))

                            label_text = f"รวม : {month_total.get((selected_year, selected_month), 0)} บาท"
                            result_label.config(text=label_text)
                    else:
                            result_label.config(text="กรุณาเลือกเดือนและปี")

            month_var = StringVar()                        
            year_var = StringVar()
            month_options = ["01", "02","03","04","05","06","07","08","09","10","11","12"]
            month_var.set("ระบุเดือน")
            month_menu = OptionMenu(result_window, month_var, *month_options)
            month_menu.place(x=370,y=450)
            
            
            year_options = ["2023","2024","2025","2026","2027","2028","2029","2030","2031","2032","2033"]
            year_var.set("ระบุปี")
            year_menu = OptionMenu(result_window, year_var, *year_options)
            year_menu.place(x=520,y=450)
            
            show_But= Button(result_window,text="ดูการสรุปยอด", bg='#D89B4A',font=("Helvetica", 14),command=lambda:(select_show()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#D89B4A')
            show_But.place(x=420, y=495)  

            result_label = Label(result_window, text="", font=("DB Helvethaica X", 15),bg='#D89B4A',fg='black')
            result_label.place(x=420, y=550)
            
            back_But= Button(result_window, text="ย้อนกลับ",bg='#ffffff',command=lambda:(result_window.destroy(),admin()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#fcdbe2')
            back_But.place(x=850,y=680)  

        login_But = Button(loingwindow, text="เข้าสู่ระบบ",bg="#D89B4A", command=lambda:(loingchecks()),font=("Helvetica", 25),  compound="center", highlightthickness=0,borderwidth=0,cursor="hand2", fg="white")
        login_But.place(x=440,y=450)     

        Register_but = Button(loingwindow, text="สมัครสมาชิก",bg="#ffffff",command=Register,font=("Helvetica", 16),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#ffffff' )
        Register_but.place(x=550,y=560)

        forget_But = Button(loingwindow,text="ลืมรหัสผ่าน",bg="#ffffff",command=repasword,font=("Helvetica", 16),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#ffffff')
        forget_But.place(x=380,y=560)
        


def contact_us():
    contact_window = tk.Toplevel(root)
    contact_window.title("ติดต่อเรา")
    contact_window.geometry("1024x768+220+20")
    contact_window.resizable(False, False)
    
# แทรกรูปภาพหน้าติดต่อเรา
    background_image = tk.PhotoImage(file=r"c:\Users\noeyw\Downloads\GUI (1).png")
    background_label = tk.Label(contact_window, image=background_image)
    background_label.pack()
    background_label.image = background_image

#ปุ่มกลับหน้าหลักหน้าติดต่อเรา
    close_button = tk.Button(contact_window, text="กลับหน้าหลัก", command=contact_window.destroy)
    close_button.place(x=850,y=680)


                                                               
                                
root = Tk()
root.title("🚐Premium_Van_Booking")
root.geometry("1024x768+220+20")
# เพิ่มพื้นหลังหน้าแรก
root.resizable(False, False)
background_image = tk.PhotoImage(file=r"c:\Users\noeyw\Downloads\html.png")
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)
background_label.pack()

login_button = Button(root, text='เข้าสู่หน้าแรก', bg='#D89B4A',fg='white', font=45, command=loing,borderwidth=0, highlightthickness=0,cursor="hand2",activebackground='#D89B4A')
login_button.config(font=("DB Helvethaica X", 25,'bold'))
login_button.place(x=410, y=660)


root.mainloop()
