def edit_ticket():
                edit_ticket_window = Toplevel(root)
                edit_ticket_window.title("แก้ไขตั๋ว")
                edit_ticket_window.geometry("1024x768+220+20")
                edit_ticket_window.resizable(False, False)
                background_image = tk.PhotoImage(file=r"c:\Users\noeyw\Downloads\edit.png")
                background_label = tk.Label( edit_ticket_window, image=background_image)
                background_label.place(x=0, y=0, relwidth=1, relheight=1)
                background_label.image = background_image
                tk.Label(edit_ticket_window, text="รหัสตั๋วที่ต้องการแก้ไข:",font=("Helvetica", 14)).place(x=350, y=100) 
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

                        conn = sqlite3.connect('New.db')
                        c = conn.cursor()
                        c.execute("SELECT * FROM regi WHERE id=?", (ticket_id,))
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

                                conn = sqlite3.connect('New.db')
                                c = conn.cursor()
                                c.execute("UPDATE regi SET fname=?, lname=?, phone=?, email=? WHERE id=?", 
                                        (new_fname, new_lname, new_phone, new_email, ticket_id))
                                conn.commit()
                                conn.close()

                                result_label.config(text="บันทึกการแก้ไขสำเร็จ",font=("Helvetica", 18))

                        save_button = tk.Button(edit_ticket_window, text="บันทึกการแก้ไข",font=("Helvetica",18), command=save_edited_ticket)
                        save_button.place(x=570, y=400)

                result_label = tk.Label(edit_ticket_window, text="")
                result_label.place(x=570, y=450) 

                retrieve_button = tk.Button(edit_ticket_window, text="ค้นหาตั๋ว",font=("Helvetica",12), command=retrieve_ticket_details)
                retrieve_button.place(x=600, y=150) 
                
                # สร้างปุ่ม "กลับหน้าหลัก" ในหน้าแก้ไขตั๋ว
                close_button = tk.Button(edit_ticket_window, text="ย้อนกลับ", command=lambda:(edit_ticket_window.destroy(),admin()))
                close_button.place(x=850,y=680)