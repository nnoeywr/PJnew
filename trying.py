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



conn = sqlite3.connect('Vanbk.db')
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
        place VARCHAR(100) NOT NULL,
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
        place VARCHAR(100) NOT NULL,
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
        # background_image = tk.PhotoImage(file="")
        # background_label = tk.Label(Regitwindow, image=background_image)
        # background_label.pack()
        # background_label.image = background_image
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
                                                conn = sqlite3.connect('Vanbk.db')
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

        tk.Label(Regitwindow, text="ชื่อจริง:", font=("Helvetica", 16) ,bg='#196658', fg="white", highlightthickness=0, borderwidth=0,).place(x=120, y=110)
        fname_entry = tk.Entry(Regitwindow, bg="#98D6FC", highlightthickness=0, borderwidth=0, cursor='hand2', font=("Helvetica", 17))  
        fname_entry.place(x=225, y=115)

        tk.Label(Regitwindow, text="นามสกุล:",font=("Helvetica", 16) ,bg='#196658', fg="white", highlightthickness=0, borderwidth=0,).place(x=120, y=150)
        lname_entry = tk.Entry(Regitwindow, bg="#98D6FC", highlightthickness=0, borderwidth=0, cursor='hand2', font=("Helvetica", 17))
        lname_entry.place(x=225, y=155)

        tk.Label(Regitwindow, text="เบอร์โทรศัพท์:",font=("Helvetica", 16) ,bg='#196658', fg="white", highlightthickness=0, borderwidth=0,).place(x=115, y=190)
        phone_entry = tk.Entry(Regitwindow, bg="#98D6FC", highlightthickness=0, borderwidth=0, cursor='hand2', font=("Helvetica", 17))
        phone_entry.place(x=225, y=195)

        tk.Label(Regitwindow, text="อีเมล:",font=("Helvetica", 16) ,bg='#196658', fg="white", highlightthickness=0, borderwidth=0,).place(x=120, y=230)
        email_entry = tk.Entry(Regitwindow, bg="#98D6FC", highlightthickness=0, borderwidth=0, cursor='hand2', font=("Helvetica", 17))
        email_entry.place(x=225, y=235)

        tk.Label(Regitwindow, text="รหัสผ่าน:",font=("Helvetica", 16) ,bg='#196658', fg="white", highlightthickness=0, borderwidth=0,).place(x=125, y=270)
        password_entry = tk.Entry(Regitwindow, bg="#98D6FC", highlightthickness=0, borderwidth=0, cursor='hand2', font=("Helvetica", 17))
        password_entry.place(x=225, y=275)

        result_label = Label(Regitwindow, text="",bg='#fcdde2',fg='black',font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0)
        result_label.place(x=350,y=330)

        #ปุ่มสมัครสมาชิก 
        reg_But= Button(Regitwindow ,bg='#fcd9e2',text="สมัครสมาชิก" ,fg='black',command=Regemember,cursor="hand2", font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0,activebackground='#fcd9e2')
        reg_But.place(x=320,y=315) 

        #ปุ่มกลับหน้าหลัก
        back1_But= Button(Regitwindow ,bg='#fcd9e2',text="ย้อนกลับ", fg='black',command=lambda:(Regitwindow.destroy()),cursor="hand2", font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0,activebackground='#fcd9e2')
        back1_But.place(x=435,y=315)

def loing():
        loingwindow=tk.Toplevel(root)
        loingwindow.title("Login Page")
        loingwindow.geometry("1024x768+220+20")
        loingwindow.resizable(False, False)
        # background_image = tk.PhotoImage(file="")
        # background_label = tk.Label(loingwindow, image=background_image)
        # background_label.pack()
        # background_label.image = background_image
        logged_in_fname = ""
        logged_in_lname = ""
        show_phone="" 
        show_email=""
        def loingchecks():##เข้าสู่ระบบเช็ค
                nonlocal logged_in_fname #ใช้ประกาศตัวแปรให้ใช้ในฟังก์ชันอื่นภายนอกฟังก์ชันตัวเอง
                nonlocal logged_in_lname 
                nonlocal show_email 
                nonlocal show_phone
                email = email_entry.get()
                password = password_entry.get()
                show_email=email
                conn = sqlite3.connect('Vanbk.db')
                c = conn.cursor()
                c.execute("SELECT * FROM regi WHERE email=? AND password=?", (email, password))
                log = c.fetchone()
                if log :
                        logged_in_name = log[1]  # ชื่ออยู่ในตำแหน่งที่ 1 ของผลลัพธ์ที่คืนมา
                        logged_in_lastname = log[2]
                        show_tel=log[3]
                        result_label.config(text=f'เข้าสู่ระบบสำเร็จ\nชื่อ: {logged_in_name} {logged_in_lastname}')
                        delay_ms = 500
                        loingwindow.after(delay_ms, Place(), loingwindow.destroy())                           
                elif  email=='admin' and password=='123456': 
                        admin()
                        loingwindow.destroy()                            
                else:
                        result_label.config(text='เข้าสู่ระบบไม่สำเร็จ\nโปรดตรวจสอบอีเมลล์และรหัสผ่านของคุณอีกครั้ง')

        tk.Label(loingwindow, text="อีเมล:", font=("Helvetica", 16) ,bg='#196658', fg="white", highlightthickness=0, borderwidth=0,).place(x=120, y=110)
        email_entry = tk.Entry(loingwindow, bg="#98D6FC", highlightthickness=0, borderwidth=0, cursor='hand2', font=("Helvetica", 17))  
        email_entry.place(x=225, y=115)

        tk.Label(loingwindow, text="รหัสผ่าน:", font=("Helvetica", 16) ,bg='#196658', fg="white", highlightthickness=0, borderwidth=0,).place(x=120, y=140)
        password_entry = tk.Entry(loingwindow, bg="#98D6FC", highlightthickness=0, borderwidth=0, cursor='hand2', font=("Helvetica", 17))  
        password_entry.place(x=225, y=150) 

        result_label = Label(loingwindow, text="",bg='#fcdbe2',fg='black',font=("DB Helvethaica X", 10))
        result_label.place(x=195,y=202)
      
        def repasword():##func รีเซ็ทรหัส
                loingwindow.destroy() 
                forgotpwwindow = Toplevel(root)
                forgotpwwindow.title("Forgot Password")
                forgotpwwindow.geometry("1024x768+220+20")
                forgotpwwindow.resizable(False,False)
                # bg_image_forgot = Image.open(r"D:\python\repassword_bg.png")
                # bg_photo_forgot = ImageTk.PhotoImage(bg_image_forgot)
                # bg_label_forgot = Label(forgotpwwindow,image=bg_photo_forgot)
                # bg_label_forgot.photo = bg_photo_forgot # เก็บ reference รูปภาพ
                # bg_label_forgot.pack(fill="both", expand=True)
                def changePassword():
                        email = email_entry.get()
                        new_password = password_entry.get()
                        conn = sqlite3.connect('Vanbk.db')
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
                                                forgotpwwindow.after(delay_ms,lambda:(forgotpwwindow.destroy(),login()))   
                                        else :
                                                result_label.config(text='รหัสผ่านใหม่ต้องไม่ซ้ำกับรหัสผ่านเดิมค่ะ (πーπ)', font=("DB Helvethaica X", 10))
                                else:
                                        result_label.config(text='รหัสผ่านควรขึ้นต้นด้วยตัวอักษรพิมพ์ใหญ่\nและต้องมีอย่างน้อย 6 ตัวขึ้นไป (πーπ)', font=("DB Helvethaica X", 10))
                        else:
                                result_label.config(text='Not found (πーπ)',font=("DB Helvethaica X", 10),)

                email_entry = Entry(forgotpwwindow,width=25,font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0,cursor="hand2")
                email_entry.place(x=175,y=70)
                password_entry = Entry(forgotpwwindow,show='*',width=25,font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0,cursor="hand2")
                password_entry.place(x=175,y=170)
                result_label = Label(forgotpwwindow, text="",bg='#fcdbe2',fg='black',font=("DB Helvethaica X", 10))
                result_label.place(x=195,y=202)

                resetpass_But= Button(forgotpwwindow,bg='#fcd9e2',fg='black',command=changePassword,cursor="hand2", font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0,activebackground='#fcd9e2')
                resetpass_But.place(x=150,y=240)
                
                back2_But= Button(forgotpwwindow,bg='#fcd9e2',fg='black',command=lambda:(forgotpwwindow.destroy(),loing()),cursor="hand2", font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0,activebackground='#fcd9e2')
                back2_But.place(x=280,y=240) 

                
        def booking ():
                bookingwindow=Toplevel(root)
                bookingwindow.title("จองตั๋ว")
                bookingwindow.geometry("1024x768+220+20") 
                def bookticket ():
                        place = place_var.get()
                        time_slot = time_slot_var.get()
                        selected_date = cal.get_date()
                        year, month, day = map(int, selected_date.split('-'))
                        if not place or not time_slot or not selected_date:
                                result_label.config(text="กรุณากรอกข้อมูลให้ครบถ้วน")
                        else:
                                # ตรวจสอบว่าวันที่ที่ผู้ใช้เลือกไม่ซ้ำกับวันที่อื่นที่มีอยู่ในระบบ
                                conn = sqlite3.connect('Vanbk.db')
                                c = conn.cursor()
                                c.execute("SELECT COUNT(*) FROM booking WHERE booking_date = ?", (selected_date,))
                                booking_count = c.fetchone()[0]  # ดึงจำนวนแถวที่มีวันที่ซ้ำกัน
                                conn.close()
                                if   selected_date < current_date:
                                        result_label.config(text="กรุณาเลือกวันที่ให้ถูกต้อง\nไม่สามารถจองวันในอดีตได้ค่ะ ")
                                elif booking_count > 0:
                                        result_label.config(text="วันที่นี้ถูกจองแล้ว")
                                else : 
                                        pay = tk.Toplevel(root)
                                        pay.title("Payment")
                                        pay.geometry("1024x768+220+20")
                                        pay.resizable(False, False)
                                        # background_image = tk.PhotoImage(file="/Users/suponb./Downloads/IMG_6314.PNG")
                                        # background_label = tk.Label(pay, image=background_image)
                                        # background_label.place(x=0, y=0, relwidth=1, relheight=1)
                                        # background_label.image = background_image
                                        
                                        def final():
                                                response = messagebox.askyesno("การจอง", "คุณชำระเงินเรียบร้อยใช่หรือไม่?")
                                                if response>0:
                                                        conn = sqlite3.connect('Vanbk.db')
                                                        c = conn.cursor()
                                                        sql1 = '''INSERT INTO booking (email,place, travel_date ,day,month,year, time_sloi ,status) VALUES (?,?,?, ?,?,?,?, ?)'''
                                                        booked = (show_email,prices_options, selected_date,day,month,year, time_slot,"รอดำเนินการ")
                                                        c.execute(sql1, booked)
                                                        c.execute("INSERT INTO data (name, travel_date, time_slot,status,email) VALUES (?,?, ?, ?,?)",(logged_in_fname +" "+ logged_in_lname,  selected_date, time_slot,"รอดำเนินการ",show_email))
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
                                                                text += f"เดินทางวันที่: {selected_date}\n"
                                                                text += f"เวลา: {time_slot}\n"
                                                                text += f"จุดหมายปลายทาง: {place}\n"
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
                                        info_label =Label(pay, text=f"{logged_in_fname} {logged_in_lname} ",bg='#ffffff',font=("DB Helvethaica X", 15))
                                        info_label.place(x=160,y=110)
                                        info_label1 =Label(pay, text=f"{show_phone} ",bg='#ffffff',font=("DB Helvethaica X", 15))
                                        info_label1.place(x=270,y=185)
                                        info_label2 =Label(pay, text=f"{place_optionmenu} ",bg='#ffffff',font=("DB Helvethaica X", 15))
                                        info_label2.place(x=217,y=255)
                                        info_label2 =Label(pay, text=f"{time_slot} ",bg='#ffffff',font=("DB Helvethaica X", 15))
                                        info_label2.place(x=270,y=325)
                                        info_label2 =Label(pay, text=f"{selected_date} ",bg='#ffffff',font=("DB Helvethaica X", 15))
                                        info_label2.place(x=220,y=397)
                                        #หน้าจ่ายเงิน
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
                # confirm_image = Image.open(r"D:\python\save_1_bt.png")
                # confirm_image = confirm_image.resize((100, 60))  # ปรับขนาดปุ่ม
                # confirm_photo = ImageTk.PhotoImage(confirm_image)
                confirm_But= Button(bookingwindow,bg='#fcdce2',fg='black',command=lambda:(bookticket()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#fcdce2')
                # confirm_But.photo = confirm_photo
                confirm_But.place(x=600, y=400)

                # back_image = Image.open(r"D:\python\back01_bt.png")
                # back_image = back_image.resize((100, 60))  # ปรับขนาดปุ่ม
                # back_photo = ImageTk.PhotoImage(back_image)
                back_But= Button(bookingwindow,bg='#fcdce2',fg='black',command=lambda:(bookingwindow.destroy(),place()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#fcdce2')
                # back_But.photo = back_photo
                back_But.place(x=510, y=400)

                def update_selected_price(event):
                # ดึงราคาจากรายการราคาและอัตราค่าโดยสารที่เลือก
                        place = place_var.get()
                        place_value = [item[1] for item in prices_options if item[0] == place][0]
                
                        # อัปเดต StringVar ที่ใช้แสดงราคา
                        place_var.set(f"{place_value} บาท")
                        place_label = tk.Label(bookingwindow, textvariable=place_var, font=("Helvetica", 16), bg="#446C9E" ,fg='white')
                        place_label.place(x=230, y=485) 

                # สร้าง Label สำหรับราคาและเมนู dropdown
                tk.Label(bookingwindow, text="สถานที่ขึ้น-ลง:", font=("Helvetica", 16), bg='#196658', fg="white", highlightthickness=0, borderwidth=0).place(x=120, y=450)

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
                place_var = tk.StringVar(bookingwindow)

                # กำหนดค่าเริ่มต้นให้เป็นรายการแรกในรายการราคาและอัตราค่าโดยสาร
                place_var.set(prices_options[0][0])

                # สร้าง OptionMenu โดยใช้ List comprehension เพื่อดึงชื่อสถานที่จากรายการราคาและอัตราค่าโดยสาร
                place_optionmenu = tk.OptionMenu(bookingwindow, place_var, *([item[0] for item in prices_options]), command=update_selected_price)
                place_optionmenu.place(x=230, y=450)

                # สร้าง Label สำหรับแสดงราคาที่ถูกเลือก
                place_label = tk.Label(bookingwindow, textvariable=place_var, font=("Helvetica", 16), bg="#446C9E", fg="white")
                place_label.place(x=230, y=485)

                tk.Label(bookingwindow, text="เวลาเดินทาง:",font=("Helvetica", 16) ,bg='#196658', fg="white", highlightthickness=0, borderwidth=0,).place(x=120, y=520)
                time_slot_var = tk.StringVar(bookingwindow)
                time_slots = {
                        1: "06:00-08:00",
                        2: "10:00-12:00",
                        3: "14:00-16:00",
                        4: "19:00-21:00"
                }
                time_slot_var.set(time_slots[1])  # Set the default time slot
                time_slot_menu = tk.OptionMenu(bookingwindow, time_slot_var, *time_slots.values())
                time_slot_menu.place(x=230, y=520)
                
                tk.Label(bookingwindow, text="วันเดินทาง:", font=("Helvetica", 16), bg='#196658', fg="white", highlightthickness=0, borderwidth=0).place(x=120, y=270)
                current_date = datetime.now().strftime('%Y-%m-%d')
                cal = Calendar(bookingwindow, selectmode="day", year=2023, month=10, day=1, date_pattern="dd/mm/yyyy", date=current_date)
                cal.place(x=225, y=270)

                #ปุ่มยืนยัน
                confirm_But= Button(bookingwindow,bg='#fcdce2',fg='black',command=lambda:(bookticket()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#fcdce2')
                confirm_But.place(x=600, y=400)

                back_But= Button(bookingwindow,bg='#fcdce2',fg='black',command=lambda:(bookingwindow.destroy(),Place()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#fcdce2')
                back_But.place(x=510, y=400)

                #text
                result_label = Label(bookingwindow, text="",bg='#e171ac',font=("DB Helvethaica X", 10),fg='white')
                result_label.place(x=520,y=460)

        def admin():
                admin_window = Toplevel(root)
                admin_window.title("Admin")
                admin_window.geometry("1024x768+220+20") 
                admin_window.resizable(False,False)

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
                conn = sqlite3.connect("Vanbk.db")
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
                tree = ttk.Treeview(frame1,columns=("id","email","place","selected_date","time_slot","status"))
                tree.heading("id",text="")
                tree.heading("email",text="อีเมลล์")
                tree.heading("place",text="สถานที่ขึ้นลง")
                tree.heading("selected_date",text="วันที่จอง")
                tree.heading("time_slot",text="รอบรถ")
                tree.heading("status",text="สถานะ")
                tree.column("id",anchor="center",width=60)
                tree.column("email",anchor="center",width=150)
                tree.column("place",anchor="center",width=100)
                tree.column("selected_date",anchor="center",width=100)
                tree.column("time_slot",anchor="center",width=150)
                tree.column("status",anchor="center",width=130)
                tree.column("#0",width=0,stretch=NO)
                
                style = ttk.Style()
                style.configure("Treeview.Heading",font = ("DB Helvethaica X", 12))
                style.configure("Treeview", font=("DB Helvethaica X", 12))
                conn = sqlite3.connect("Vanbk.db")
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
                        conn = sqlite3.connect('Vanbk.db')
                        c = conn.cursor()
                        c.execute("DELETE FROM data WHERE status = 'เสร็จสิ้น'")
                        conn.commit()
                        conn.close()

        def edit_ticket():
                edit_ticket_window = tk.Toplevel(root)
                edit_ticket_window.title("แก้ไขตั๋ว")
                edit_ticket_window.geometry("1024x768+220+20")
                edit_ticket_window.resizable(False, False)
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
                        fname_entry = tk.Entry(edit_ticket_window,highlightthickness=0,borderwidth=0,cursor='hand2',font=("Helvetica", 17))
                        fname_entry.place(x=550, y=208) 
                        fname_entry.insert(0, ticket_data[1])
                        fname_entry.config(bg="#D89B4A",)

                        tk.Label(edit_ticket_window, text="นามสกุล:",font=("Helvetica", 18)).place(x=350, y=250) 
                        lname_entry = tk.Entry(edit_ticket_window,highlightthickness=0,borderwidth=0,cursor='hand2',font=("Helvetica", 17))
                        lname_entry.place(x=550, y=257)
                        lname_entry.insert(0, ticket_data[2])
                        lname_entry.config(bg="#D89B4A",)

                        tk.Label(edit_ticket_window, text="เบอร์โทรศัพท์:",font=("Helvetica", 18)).place(x=350, y=300) 
                        phone_entry = tk.Entry(edit_ticket_window,highlightthickness=0,borderwidth=0,cursor='hand2',font=("Helvetica", 17))
                        phone_entry.place(x=550, y=307)
                        phone_entry.insert(0, ticket_data[3])
                        phone_entry.config(bg="#D89B4A",)

                        tk.Label(edit_ticket_window, text="อีเมล:",font=("Helvetica", 18)).place(x=350, y=350) 
                        email_entry = tk.Entry(edit_ticket_window,highlightthickness=0,borderwidth=0,cursor='hand2',font=("Helvetica", 17))
                        email_entry.place(x=550, y=350)
                        email_entry.insert(0, ticket_data[4])
                        email_entry.config(bg="#D89B4A",)

                        def save_edited_ticket():
                                new_fname = fname_entry.get()
                                new_lname = lname_entry.get()
                                new_phone = phone_entry.get()
                                new_email = email_entry.get()
                                if len(new_phone) != 10:
                                        result_label.config(text="กรุณากรอกหมายเลขโทรศัพท์ให้ถูกต้อง")
                                        return

                                conn = sqlite3.connect('Vanbk.db')
                                c = conn.cursor()
                                c.execute("UPDATE tickets SET fname=?, lname=?, phone=?, email=? WHERE id=?", 
                                        (new_fname, new_lname, new_phone, new_email, ticket_id))
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
                        conn = sqlite3.connect('Vanbk.db')
                        c = conn.cursor()

                        # ตรวจสอบว่ามีตั๋วที่มีรหัสที่ให้ไว้หรือไม่
                        c.execute("SELECT * FROM regi WHERE id=?", (ticket_id,))
                        existing_ticket = c.fetchone()

                        if existing_ticket:
                        # ใช้ msgbox เพื่อยืนยันการยกเลิก
                                confirmation = msgbox.askyesno("ยืนยันการยกเลิก", f"คุณต้องการยกเลิกตั๋วรหัส {ticket_id} ใช่หรือไม่? **หากคุณยกเลิกตั๋วแล้ว ทางบริษัทขอสงวนสิทธิ์คืนเงินทุกกรณี**")
                        
                        if confirmation:
                                # ดำเนินการลบ
                                c.execute("DELETE FROM regi WHERE id=?", (ticket_id,))
                                conn.commit()
                                conn.close()
                                result_label.config(text=f"ตั๋วรหัส {ticket_id} ถูกยกเลิกสำเร็จ")
                        else:
                                result_label.config(text="ยกเลิกการยกเลิกตั๋ว")
                        # else:
                        # result_label.config(text="ไม่พบตั๋วที่ต้องการยกเลิก")
                
                result_label = tk.Label(delete_window, text="",font=("Helvetica", 18),)
                result_label.place(x=530, y=220)
                result_label.config(bg="#00B796", highlightbackground="#00B796")

                delete_button = tk.Button(delete_window, text="ยกเลิกตั๋ว",font=("Helvetica", 18), command=perform_ticket_deletion)
                delete_button.place(x=560, y=150) 
                # ปุ่มกลับหน้าหลักหน้ายกเลิก
                close_button = tk.Button(delete_window, text="กลับหน้าหลัก", command=delete_window.destroy)
                close_button.place(x=850,y=680)
        def summary():
                conn = sqlite3.connect('Vanbk.db')
                c = conn.cursor()
                c.execute("SELECT selected_date, place FROM booking")
                bookings = c.fetchall()
                amount = {} # สร้างพจนานุกรมเพื่อเก็บยอดเงินรายเดือน
                # นับยอดเงินในแต่ละเดือน
                for booking in bookings:
                        selected_date = booking[0]#ดึงวันที่จองจาก tuple ใน bookings
                        year, month, _ = map(int, selected_date.split('-'))
                        Place = booking[1]
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
                        ("แยกกุมภวาปี-เซ็นทรัลอุดรธานี(บขส1)", 62) ]

                        income = prices_options.get(Place)##ดึงราคาของแพ็คเกจที่ถูกจองและเก็บไว้ในตัวแปร 
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
                result_window.geometry('1000x650+275+60')
                result_window.resizable(False,False)

                canvas = Canvas(result_window, width=1000, height=650)
                canvas.pack()
                # bg_image = Image.open(r"D:\python\Sarub_bg (1).png")
                # bg_photo = ImageTk.PhotoImage(bg_image)
                # canvas.create_image(0, 0, anchor=NW, image=bg_photo)
                # canvas.image = bg_photo

                frame = Frame(canvas)  # Create a frame as a child of the canvas
                canvas.create_window((200,170), window=frame, anchor=NW)  # Place the frame on the canvas
                tree = ttk.Treeview(frame, columns=("place", "selected_date", "time_slot", "status"))
                tree.heading("place", text="แพ็คเกต")
                tree.heading("selected_date", text="วันที่จอง")
                tree.heading("time_slot", text="รอบรถ")
                tree.heading("status", text="สถานะ")
                tree.column("place", anchor="center", width=100)
                tree.column("selected_date", anchor="center", width=100)
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

                                conn = sqlite3.connect("vanbk.db")
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
                month_menu.place(x=750,y=180)
               
                
                year_options = ["2023","2024","2025","2026","2027","2028","2029","2030","2031","2032","2033"]
                year_var.set("ระบุปี")
                year_menu = OptionMenu(result_window, year_var, *year_options)
                year_menu.place(x=750,y=210)

                # เพิ่มปุ่ม "ดูรายการสรุปยอด"
                # show_image = Image.open(r"D:\python\Total-summary_bt.png")
                # show_image = show_image.resize((120, 60))  # ปรับขนาดปุ่ม
                # show_photo = ImageTk.PhotoImage(show_image)
                show_But= Button(result_window, bg='#fcdbe2',command=lambda:(select_show()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#fcdbe2')
                # show_But.photo = show_photo
                show_But.place(x=750, y=260)  

                result_label = Label(result_window, text="", font=("DB Helvethaica X", 15),bg='#fcdbe2',fg='black')
                result_label.place(x=750, y=390)
                
                # back_image = Image.open(r"D:\python\back01_bt.png")
                # back_image = back_image.resize((110, 60))  # ปรับขนาดปุ่ม
                # back_photo = ImageTk.PhotoImage(back_image)
                back_But= Button(result_window, text="ย้อนกลับ",bg='#fcdbe2',command=lambda:(result_window.destroy(),admin()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#fcdbe2')
                # back_But.photo = back_photo
                back_But.place(x=750, y=310)  

        login_But = Button(loingwindow, text="เข้าสู่ระบบ",bg="#ffffff", command=booking,cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#ffffff')
        login_But.place(x=350, y=250)     

        forget_But = Button(loingwindow,text="ลืมรหัสผ่าน",bg="#ffffff",command=repasword,cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#ffffff')
        forget_But.place(x=460,y=250)

        


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


                                                               
                                
root = tk.Tk()
root.title("🚐Premium_Van_Booking")
root.geometry("1024x768+220+20")
# เพิ่มพื้นหลังหน้าแรก
root.resizable(False, False)
background_image = tk.PhotoImage(file=r"c:\Users\noeyw\Downloads\GUI.png")
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)
background_label.pack()

Register_button = tk.Label(root, text='Sign Up',font=("Helvetica", 30),  compound="center", highlightthickness=0,borderwidth=0,cursor="hand2", fg="white")
Register_button.place(x=515, y=370, anchor="center",)
Register_button.bind("<Button-1>", lambda event: Register())
Register_button.config(bg="#FFB149",)

login_button = tk.Label(root, text='Login',font=("Helvetica", 30),  compound="center", highlightthickness=0,borderwidth=0,cursor="hand2", fg="white")
login_button.place(x=515, y=270, anchor="center",)
login_button.bind("<Button-1>", lambda event: loing())
login_button.config(bg="#FFB149",)

contact_us_button = tk.Label(root, text='Contact',font=("Helvetica", 30),  compound="center", highlightthickness=0,borderwidth=0,cursor="hand2", fg="white")
contact_us_button.place(x=515, y=550, anchor="center",)
contact_us_button.bind("<Button-1>", lambda event: contact_us())
contact_us_button.config(bg="#FFB149",)

root.mainloop()






