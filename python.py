from ast import Num, Return
from genericpath import exists
from importlib.resources import contents
from itertools import count
from sqlite3 import Cursor, connect
from tabnanny import check
from flask import Flask, render_template, request, flash, abort, current_app, make_response
from sqlalchemy import false, true
from werkzeug.utils import secure_filename
from gtts import gTTS
from flask import jsonify
import os
from playsound import playsound
import time
from os import path
import playsound
import webbrowser
import speech_recognition as sr
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
import mysql.connector
connection = pymysql.connect(
    host="localhost", user="root", password="123456", database="mydb")


cursor = connection.cursor()
connection.autocommit(True)


def speak(text):
    tts = gTTS(text=text, lang='ar', slow=False)
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove('voice.mp3')


app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/help")
def help():
    return render_template("help.html")


@app.route("/ereg", methods=['POST'])
def ereg():
    std_id = request.form.get('x')
    return render_template("ereg.html", std_id=std_id)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/loginforstudent", methods=['POST'])
def loginforstudent():

    id = request.form.get("number")
    # print(id)
    password = request.form.get("password")


    value = request.form.getlist('check')
    b = int(id)
    if(value[0] == "notadmin"):
       q = "select count(*) from std_info where std_info.std_id = (%s)"
       v = (id)
       cursor.execute(q, v)
       connection.commit()
       dd = cursor.fetchone()[0]
       if(dd!=0): 
         q1 = "select std_info.password from std_info where std_info.std_id = (%s)"
         v1 = (id)
         cursor.execute(q1, v1)
         connection.commit()
         dd = cursor.fetchone()[0]
         result = check_password_hash(dd, password)
         if (result):
            q = ("SELECT * FROM  std_info WHERE std_id=(%s)")
            v = (b)
            cursor.execute(q, v)
            data = cursor.fetchall()
            return render_template("afterlogin.html", value=data)
         else:
            return render_template("login.html")
       else:
         return render_template("login.html")

    elif(value[0] == "admin"):
        q = ("SELECT count(*) FROM  admin WHERE id=(%s)")
        v = (b)
        cursor.execute(q, v)
        value3 = cursor.fetchone()[0]
        if (value3 == 0):
            return render_template("login.html")
        else:
            q2 = "select admin.pass from admin where id = (%s)"
            v2 = (id)
            cursor.execute(q2, v2)
            print("gggggggggggggggggggggggggggggggg")
            dd2 = cursor.fetchone()[0]
            result2 = check_password_hash(dd2, password)
            if (result2):

                return render_template("admin.html")
            else:
                return render_template("login.html")
         
    


@app.route("/StudentSchedule", methods=['POST'])
def StudentSchedule():
    std_id = request.form.get("y")
    q = (
        "select concat (section.full_building_name,' (',section.building,')'), CONCAT (section.building,'-' ,section.room_id) AS 'class_room',CONCAT( instructor_info.f_name ,' ', instructor_info.l_name  ) AS 'inst_name' , CONCAT ('[',section_time.start_time,' - ' ,section_time.end_time,'] ',section_time.day) AS 'time' , section.section_id,course.noOfHours,course.course_name,section.course_id from section join course on course.course_id = section.course_id join instructor_info on instructor_info.inst_id = section.inst_id join section_time on section_time.sec_time_id = section.section_time join registered_courses on (registered_courses.course_id=section.course_id and registered_courses.sec_id= section.section_id) where registered_courses.std_id=(%s)")
    v = (std_id)
    cursor.execute(q, v)
    data = cursor.fetchall()

    return render_template("StudentSchedule.html", value=data, v2=std_id)


@app.route("/chgpass", methods=['POST'])
def chgpass():
    std_id = request.form.get("x")
    return render_template("chgpass.html", v=std_id)


@app.route("/StudentInfo", methods=['POST'])
def StudentInfo():
    std_id = request.form.get("y")
    print(std_id)
    q = ("SELECT std_info.std_id ,CONCAT(std_info.f_name,' ',std_info.l_name)as name,std_info.gender,std_info.dept_name,std_info.phone_number,std_info.email from std_info where std_info.std_id=(%s)")
    v = (std_id)
    cursor.execute(q, v)
    data = cursor.fetchall()
    return render_template("StudentInfo.html", value=data, v2=std_id)


@app.route("/StudentRegistration", methods=['POST'])
def StudentRegistration():
    name = request.form.get("y")
    std_id = request.form.get("x")
    q = ("SELECT course.course_id,course.course_name,course.noOfHours,plan.req_type FROM  course JOIN plan  on course.course_id=plan.course_id and dept_name=(%s)")
    v = (name)
    cursor.execute(q, v)
    data2 = cursor.fetchall()
    return render_template("StudentRegistration.html", value=data2, v=name, v2=std_id)


@app.route("/speak_ajax", methods=['POST'])
def speak_ajax():
    text = request.form['name']
    print(text)
    speak(text)
    return "ok"


@app.route("/timer", methods=['POST'])
def timer():
  return render_template("timer.html")

@app.route("/time_ajax", methods=['POST'])
def time_ajax():
   h = request.form['h']
   m = request.form['m']
   s = request.form['s']

   q=("update  timer set houre=(%s),min=(%s),sec=(%s) where id=1")
   v=(h,m,s)
   cursor.execute(q,v)

   return jsonify("ok")

@app.route("/confirm_ajax", methods=['POST'])
def confirm_ajax():
    std_id = request.form['std_id']
    time.strftime("%H:%M:%S")
    currenttime = str(time.strftime("%H:%M:%S"))
    print(currenttime)
# Actual Start Time
    # timetogo = "19:00:00"
    q="select houre,min,sec from timer where id=1"
    cursor.execute(q)
    data=cursor.fetchall()
    h=data[0][0]
    m=data[0][1]
    s=data[0][2]
    timetogo=h+':'+m+':'+s
    print("sssssssssssssssssssssssss")
    print(timetogo)
# Time for testing (uncomment)
#timetogo = "18:00:00"

    while True:
        # print("start")
        currenttime = str(time.strftime("%H:%M:%S"))
        if currenttime == timetogo:
            print("helloooooooooooooooooooooooooooooooooooooooo")
            q = "select * from temp_registered_courses where temp_registered_courses.std_id = (%s)"
            v = (std_id)
            cursor.execute(q, v)
            section = cursor.fetchall()
            # print(section)

            for x in section:
                c = x[2]
                s = x[1]
                print(c)
                print(s)
                # q = "select classroom.room_capacity from classroom join section on (section.room_id = classroom.room_id and classroom.building = section.building) where  section.section_id =(%s) and section.course_id = (%s)"
                
                qqq=("select  count(*) from  registered_courses where course_id=(%s) and sec_id=(%s)")
                vvv=(c,s)
                cursor.execute(qqq,vvv)
                ddaata = cursor.fetchone()[0]

     
                qqq2=("select  classroom.room_capacity from  section join classroom on section.room_id=classroom.room_id and section.full_building_name=classroom.full_building_name where section.course_id=(%s) and section.section_id=(%s)")
                vvv2=(c,s)
                cursor.execute(qqq2,vvv2)
                ddaata2 = cursor.fetchone()[0]
          
    
                res=""
                if(ddaata==ddaata2):
                  res="مغلقه"
                else:
                  res="مفتوحه"
                
                 
                 
                if res == "مغلقه":
                    return jsonify("الشعبة مغلقة")
                else:
                    q = "select std_info.financial_record from std_info where std_info.std_id = (%s)"
                    v = (std_id)
                    cursor.execute(q, v)
                    fr = cursor.fetchone()[0]
                    fr1 = fr

                    q = "select course.noOfHours from course where course.course_id = (%s)"
                    v = (c)
                    cursor.execute(q, v)

                    cp = cursor.fetchone()[0]

                    price = cp*24

                    fr1 = fr1-price

                    if (fr1 < 0):
                        return ("السجل المالي غير كافي")
                    else:
                        # q = ("UPDATE std_info SET phone_number=(%s),email=(%s) where std_id=(%s)")
                        # print(capacity)
                        # capacity = capacity-1

                        # q = "update classroom join  section on classroom.room_id = section.room_id set classroom.room_capacity = (%s) where  section.section_id =(%s) and section.course_id = (%s) "
                        # v = (capacity, s, c)
                        # cursor.execute(q, v)

                        #                     INSERT INTO table_name (column1, column2, column3, ...)
                # VALUES (value1, value2, value3, ...);

                        q11 = "insert into registered_courses (std_id , course_id , sec_id) values (%s,%s,%s)"
                        v11 = (std_id, c, s)
                        cursor.execute(q11, v11)

                        q1 = "select std_info.hours from std_info where std_info.std_id=(%s) "
                        v1 = (std_id)
                        cursor.execute(q1, v1)
                        sh = cursor.fetchone()[0]
                        sh = sh + cp

                        q9 = (
                            "UPDATE std_info SET std_info.hours = (%s) WHERE std_info.std_id = (%s)")
                        v9 = (sh, std_id)
                        cursor.execute(q9, v9)

                        q10 = (
                            "UPDATE std_info SET std_info.financial_record = (%s) WHERE std_info.std_id = (%s)")
                        v10 = (fr1, std_id)
                        cursor.execute(q10, v10)

            return "ok"





@app.route("/d_ajax", methods=['POST'])
def d_ajax():

    std_id = request.form['std_id']
    c = request.form['cl']
    s = request.form['sl']


    q=("delete from  temp_registered_courses  where std_id=(%s) and sec_id=(%s) and course_id=(%s)")
    v=(std_id,s,c)
    cursor.execute(q,v)


    
        
    return jsonify("تم حذفه")





@app.route("/temp_ajax", methods=['POST'])
def temp_ajax():
    std_id = request.form['std_id']
    course_id = request.form['course_id']
    s_id = request.form['s_id']

   

    q = "select count(*) from section where section.course_id = (%s) and section.section_id = (%s)"
    v = (course_id, s_id)
    cursor.execute(q, v)
    value = cursor.fetchone()[0]
    if (value == 0):
        print("ggggggggggg")
        q = "select count(*) from course where course.course_id = (%s)"
        v = (course_id)
        cursor.execute(q, v)
        value2 = cursor.fetchone()[0]
        if (value2 == 0):
            print("hhhhhhhhhhhhhhhh")
            return jsonify("h","رقم المساق غير صحيح")
        else:
            return jsonify("h","رقم الشعبة غير صحيح")
    else:
          name=""
          q=("select course.course_name from course where course_id=(%s)")
          v=(course_id)
          cursor.execute(q,v)
          name= cursor.fetchone()[0]
        

        
          q = ("SELECT section.section_time from section where section.course_id=(%s) and section.section_id=(%s)")
          v = (course_id, s_id)
          cursor.execute(q, v)
          # section time id for course id
          curr_sec_time_id = cursor.fetchone()[0]
          # وقت الشعبة

# اذاا الطالب مسجل هاي المادة من قبل او لا
          q1 = ("select count(*) from temp_registered_courses where temp_registered_courses.course_id=(%s)  and temp_registered_courses.std_id=(%s)")
          v1 = (course_id,  std_id)
          cursor.execute(q1, v1)
          data2 = cursor.fetchone()[0]

          q3 = ("select section_time.sec_time_id from  section_time join section on section.section_time = section_time.sec_time_id join temp_registered_courses on section.section_id=temp_registered_courses.sec_id and section.course_id=temp_registered_courses.course_id where temp_registered_courses.std_id=(%s)")
          v3 = (std_id)
          cursor.execute(q3, v3)
          flag = true
# اذا الطالب مش مسجل ولا شعبة من هاي المادة بفوت ع هاي الاف
          if (data2 == 0):
            # جدول التعارض
             for row in cursor:
                if row[0] == curr_sec_time_id:
                    flag = false
                    break
                elif curr_sec_time_id == 1 or curr_sec_time_id == 2:
                    if(row[0] == 5 or row[0] == 10 or row[0] == 12):

                        flag = false
                        break

                elif curr_sec_time_id == 3 or curr_sec_time_id == 4:
                    if(row[0] == 6 or row[0] == 11 or row[0] == 13):

                        flag = false
                        break

                elif curr_sec_time_id == 7 or curr_sec_time_id == 8:
                    if(row[0] == 9 or row[0] == 14):

                        flag = false
                        break

                elif curr_sec_time_id == 5 or curr_sec_time_id == 10 or curr_sec_time_id == 12:
                    if(row[0] == 1 or row[0] == 2):

                        flag = false
                        break

                elif (curr_sec_time_id == 6 or curr_sec_time_id == 11 or curr_sec_time_id == 13):
                    if(row[0] == 3 or row[0] == 4):

                        flag = false
                        break

                elif curr_sec_time_id == 9 or curr_sec_time_id == 14:
                    if(row[0] == 7 or row[0] == 8):

                        flag = false
                        break

                # else:

                continue

                # الفلاج ترو يعني ما في تعارض
             if flag == true:

                # كل الامور تمام

                #                     INSERT INTO table_name (column1, column2, column3, ...)
                # VALUES (value1, value2, value3, ...);

                  q7 = (
                    "insert into mydb.temp_registered_courses (std_id,course_id,sec_id) values (%s,%s,%s)")
                  v7 = (std_id, course_id, s_id)
                  cursor.execute(q7, v7)
                  connection.commit()
                  
                 


                  return jsonify(name,"اكتملت العملية بنجاح")
             else:

                return jsonify(
                  name,  "هذا المساق يتعارض مع مساق اخر في نفس الوقت"
                )
          else:
            return jsonify(
               name, "انت بالفعل ملتحق بشعبة من هذا المساق يجب عليك حذف المساق ثم اعادة الالتحاق بشعبة اخرى"
            )
       


          

@app.route("/t_ajax", methods=['POST'])
def t_ajax():
     std_id = request.form['std_id']
     

     q=("select  temp_registered_courses.course_id ,course.course_name ,temp_registered_courses.sec_id,course.noOfHours from temp_registered_courses join course on course.course_id=temp_registered_courses.course_id where temp_registered_courses.std_id=(%s)")
     v=(std_id)
     cursor.execute(q,v)
     data=cursor.fetchall()
     section = []
     for result in data:
        contents = {'c_id': result[0],
                    'name': result[1],
                    'section': result[2],
                    'num': result[3],
                   
                    }
        section.append(contents)
        
     return jsonify(section)
     






@app.route("/process_ajax", methods=['POST'])
def process_ajax():
    cap=[]
    num=[]
    num2=[]
    num3=[]

    yes="مفتوحه"
    no="مغلقه"
    

    cl = request.form['cl']
    q = (
        "SELECT  DISTINCT section.course_id,section.section_id,CONCAT (section.building,'-' ,section.room_id) AS 'class_room',CONCAT ('[',section_time.start_time,' - ' ,section_time.end_time,'] ',section_time.day) AS 'time'    ,CONCAT( instructor_info.f_name ,' ', instructor_info.l_name  ) AS 'inst_name' , classroom.room_capacity FROM section JOIN classroom on section.room_id=classroom.room_id  and section.full_building_name=classroom.full_building_name join section_time on section.section_time= section_time.sec_time_id join  instructor_info on section.inst_id =instructor_info.inst_id  and  section.course_id=(%s)")
    v = (cl)
    cursor.execute(q, v)
    data = cursor.fetchall()

    for result in data:
     cap.append(result[1])
     print(cap)
    size = len(cap)
    for i in range(size):     
           qqq=("select  count(*) from  registered_courses where course_id=(%s) and sec_id=(%s)")
           vvv=(cl,cap[i])
           cursor.execute(qqq,vvv)
           ddaata = cursor.fetchone()[0]
           num.append(ddaata) 
    print(num)
    for j in range(size):
           
        qqq2=("select  classroom.room_capacity from  section join classroom on section.room_id=classroom.room_id and section.full_building_name=classroom.full_building_name where section.course_id=(%s) and section.section_id=(%s)")
        vvv2=(cl,cap[j])
        cursor.execute(qqq2,vvv2)
        ddaata2 = cursor.fetchone()[0]
        num2.append(ddaata2)       
    print(num2)
    for i in range(size):
       if(num[i]==num2[i]):
          num3.append(no) 
       else:
        num3.append(yes)
    i=0    
    section = []
    for result in data:
        contents = {'cap': num3[i],
                    'r_id': result[4],
                    's_time': result[3],
                    'inst_name': result[2],
                    's_id': result[1],
                    }
        section.append(contents)
        i=i+1
    return jsonify(section)


@app.route("/student_info_ajax", methods=['POST'])
def student_info_ajax():
    std_id = request.form['std_id']
    phone = request.form['phone']
    email = request.form['email']
    q = ("UPDATE std_info SET phone_number=(%s),email=(%s) where std_id=(%s)")
    v = (phone, email, std_id)
    cursor.execute(q, v)

    return jsonify(phone, email, "yes")


@app.route("/chgpass_ajax", methods=['POST'])
def chgpass_ajax():
    std_id = request.form['std_id']
    base = request.form['base']
    passOne = request.form['passOne']
    passTwo = request.form['passTwo']
    # print("eaffffffffffffffffffffffffffffffffffffffff")
    # print(std_id)
    # print(base)
    q = ("SELECT std_info.password from std_info where std_id=(%s)")
    v = (std_id)
    cursor.execute(q, v)
    data = cursor.fetchone()[0]
    # print(data)
    result = check_password_hash(data, base)

    if (result):
        password = generate_password_hash(passOne, method='sha256')
        q2 = ("UPDATE std_info SET password=(%s) where std_id=(%s)")
        v2 = (password, std_id)
        cursor.execute(q2, v2)
        return jsonify("yes")

    else:
        return jsonify("NO")


@app.route("/registration_ajax", methods=['POST'])
def registration_ajax():
 cl = request.form['cl']
 sl = request.form['sl']
 std_id = request.form['std_id']


 qqq=("select  count(*) from  registered_courses where course_id=(%s) and sec_id=(%s)")
 vvv=(cl,sl)
 cursor.execute(qqq,vvv)
 ddaata = cursor.fetchone()[0]

     
  
        
 qqq2=("select  classroom.room_capacity from  section join classroom on section.room_id=classroom.room_id and section.full_building_name=classroom.full_building_name where section.course_id=(%s) and section.section_id=(%s)")
 vvv2=(cl,sl)
 cursor.execute(qqq2,vvv2)
 ddaata2 = cursor.fetchone()[0]
          
    
 res=""
 if(ddaata==ddaata2):
         res="مغلقه"
 else:
        res="مفتوحه"
    

    
 if(res=="مفتوحه"):
    q = ("SELECT section.section_time from section where section.course_id=(%s) and section.section_id=(%s)")
    v = (cl, sl)
    cursor.execute(q, v)
    # section time id for course id
    curr_sec_time_id = cursor.fetchone()[0]

    q = ("SELECT count(*) from registered_courses where std_id=(%s) ")
    v = (std_id)
    cursor.execute(q, v)

    num = cursor.fetchone()[0]
    print(num)

    q = ("SELECT sum(course.noOfHours) from course join section on course.course_id=section.course_id join registered_courses on registered_courses.course_id = section.course_id  where  registered_courses.std_id=(%s) ")
    v = (std_id)
    cursor.execute(q, v)

    num1 = cursor.fetchone()[0]
    print(num1)


# and registered_courses.sec_id=(%s)
    q1 = ("select count(*) from registered_courses where registered_courses.course_id=(%s)  and registered_courses.std_id=(%s)")
    v1 = (cl,  std_id)
    cursor.execute(q1, v1)
    data2 = cursor.fetchone()[0]

    # q2 = ("select count(*) from registered_courses where registered_courses.course_id=(%s) and registered_courses.sec_id=(%s) and registered_courses.std_id=(%s)")
    # v2 = (cl, sl, std_id)
    # cursor.execute(q1, v1)
    # data2 = cursor.fetchone()[0]

    # q3 = ("select * from section_time where 'احد' LIKE CONCAT('%',day,'%')")
    # q3 = ("select * from section_time where  day like '%احد ثلاثاء خميس%' ")
    q3 = ("select section_time.sec_time_id from  section_time join section on section.section_time = section_time.sec_time_id join registered_courses on section.section_id=registered_courses.sec_id and section.course_id=registered_courses.course_id where registered_courses.std_id=(%s)")
    v3 = (std_id)
    cursor.execute(q3, v3)
    flag = true

    if (data2 == 0):

        for row in cursor:
            if row[0] == curr_sec_time_id:

                flag = false
                break
            elif curr_sec_time_id == 1 or curr_sec_time_id == 2:
                if(row[0] == 5 or row[0] == 10 or row[0] == 12):

                    flag = false
                    break

            elif curr_sec_time_id == 3 or curr_sec_time_id == 4:
                if(row[0] == 6 or row[0] == 11 or row[0] == 13):

                    flag = false
                    break

            elif curr_sec_time_id == 7 or curr_sec_time_id == 8:
                if(row[0] == 9 or row[0] == 14):

                    flag = false
                    break

            elif curr_sec_time_id == 5 or curr_sec_time_id == 10 or curr_sec_time_id == 12:
                if(row[0] == 1 or row[0] == 2):

                    flag = false
                    break

            elif (curr_sec_time_id == 6 or curr_sec_time_id == 11 or curr_sec_time_id == 13):
                if(row[0] == 3 or row[0] == 4):

                    flag = false
                    break

            elif curr_sec_time_id == 9 or curr_sec_time_id == 14:
                if(row[0] == 7 or row[0] == 8):

                    flag = false
                    break

            # else:

            continue
            # return jsonify("hiiiiiiiiiiiiiiiiiiiii")

        if flag == true:

            q4 = (
                "select std_info.financial_record from std_info where std_info.std_id=(%s)")
            v4 = (std_id)
            cursor.execute(q4, v4)
            fr = cursor.fetchone()[0]
            fr1 = fr

            q5 = ("select course.noOfHours from course where course.course_id=(%s)")
            v5 = (cl)
            cursor.execute(q5, v5)
            cp = cursor.fetchone()[0]
            print(cp)
            price = cp*24
            print(price)
            fr1 = fr1-price
            print(fr1)

            if fr1 >= 0:

                #q6 = ("select sum(course.noOfHours)  from course join section on course.course_id= section.course_id join registered_courses on (registered_courses.course_id=section.course_id) where registered_courses.std_id=(%s) group by course.course_id")
                #q6 = ("select distinct course.course_name,(course.noOfHours)  from course join section on course.course_id= section.course_id join registered_courses on (registered_courses.course_id=section.course_id) where registered_courses.std_id=(%s) group by course.course_id ")
                q6 = ("select std_info.hours from std_info where std_info.std_id = (%s)")

                v6 = (std_id)
                cursor.execute(q6, v6)
                dd = cursor.fetchone()[0]
                temp = 0
                # for i in dd:
                #     sum = sum + cursor.fetchone()[1]

                print(dd)

                #noh = cursor.fetchone()[0]
                # if (noh is None):
                #   noh = 0
                currnoh = cp
                temp = dd+currnoh

                #currnoh = currnoh + noh

                if temp <= 20:

                    #                     INSERT INTO table_name (column1, column2, column3, ...)
                    # VALUES (value1, value2, value3, ...);

                    q7 = (
                        "insert into mydb.registered_courses (std_id,course_id,sec_id) values (%s,%s,%s)")
                    v7 = (std_id, cl, sl)
                    cursor.execute(q7, v7)
                    connection.commit()

                    # q8 = ("select CONCAT ('[',section_time.start_time,' - ' ,section_time.end_time,'] ',section_time.day) AS 'time'    ,section.section_id, course.noOfHours,course.course_name,section.course_id from course join section on course.course_id = section.course_id join section_time on section_time.sec_time_id=section.section_time join registered_courses on (registered_courses.sec_id = section.section_id and registered_courses.course_id=section.course_id) where registered_courses.std_id =(%s) and registered_courses.course_id =(%s) and registered_courses.sec_id = (%s)")
                    # v8 = (std_id, cl, sl)

                    q8 = ("select CONCAT ('[',section_time.start_time,' - ' ,section_time.end_time,'] ',section_time.day) AS 'time' ,section.section_id, course.noOfHours,course.course_name,section.course_id from course join section on course.course_id = section.course_id join section_time on section_time.sec_time_id=section.section_time join registered_courses on (registered_courses.sec_id = section.section_id and registered_courses.course_id=section.course_id) where registered_courses.std_id =(%s)")
                    v8 = (std_id)
                    cursor.execute(q8, v8)
                    data8 = cursor.fetchall()

                    section8 = []
                    for result in data8:
                        vaar = {
                            'time': result[0],
                            's_id': result[1],
                            'nh': result[2],
                            'cn': result[3],
                            'c_id': result[4],
                        }
                        section8.append(vaar)
                    q9 = (
                        "UPDATE std_info SET std_info.hours = (%s) WHERE std_info.std_id = (%s)")
                    v9 = (temp, std_id)
                    cursor.execute(q9, v9)

                    q10 = (
                        "UPDATE std_info SET std_info.financial_record = (%s) WHERE std_info.std_id = (%s)")
                    v10 = (fr1, std_id)
                    cursor.execute(q10, v10)
                    # (section8)
                    # text = "اكتملت العملية بنجاح"
                    # speak(text)
                    q = ("select std_info.hours from std_info where std_info.std_id = (%s)")

                    v = (std_id)
                    cursor.execute(q, v)
                    dd = cursor.fetchone()[0]


                    return jsonify("اكتملت العملية بنجاح", section8,dd)

                else:

                    q8 = ("select CONCAT ('[',section_time.start_time,' - ' ,section_time.end_time,'] ',section_time.day) AS 'time' ,section.section_id, course.noOfHours,course.course_name,section.course_id from course join section on course.course_id = section.course_id join section_time on section_time.sec_time_id=section.section_time join registered_courses on (registered_courses.sec_id = section.section_id and registered_courses.course_id=section.course_id) where registered_courses.std_id =(%s)")
                    v8 = (std_id)
                    cursor.execute(q8, v8)
                    data8 = cursor.fetchall()

                    section8 = []
                    for result in data8:
                        vaar = {
                            'time': result[0],
                            's_id': result[1],
                            'nh': result[2],
                            'cn': result[3],
                            'c_id': result[4],
                        }
                    section8.append(vaar)

                    # text = "انت لا تستطيع تسجيل اكثر من 20 ساعة تتهورش"
                    # speak(text)
                    q = ("select std_info.hours from std_info where std_info.std_id = (%s)")

                    v = (std_id)
                    cursor.execute(q, v)
                    dd = cursor.fetchone()[0]

                    return jsonify(
                        "انت لا تستطيع تسجيل اكثر من 20 ساعة...تتهورش", section8,dd)

            else:
                q8 = ("select CONCAT ('[',section_time.start_time,' - ' ,section_time.end_time,'] ',section_time.day) AS 'time' ,section.section_id, course.noOfHours,course.course_name,section.course_id from course join section on course.course_id = section.course_id join section_time on section_time.sec_time_id=section.section_time join registered_courses on (registered_courses.sec_id = section.section_id and registered_courses.course_id=section.course_id) where registered_courses.std_id =(%s)")
                v8 = (std_id)
                cursor.execute(q8, v8)
                data8 = cursor.fetchall()

                section8 = []
                for result in data8:
                    vaar = {
                        'time': result[0],
                        's_id': result[1],
                        'nh': result[2],
                        'cn': result[3],
                        'c_id': result[4],
                    }
                    section8.append(vaar)
                #currnoh = currnoh - noh
                # text = "السجل المالي غير كافي"
                # speak(text)
                q = ("select std_info.hours from std_info where std_info.std_id = (%s)")

                v = (std_id)
                cursor.execute(q, v)
                dd = cursor.fetchone()[0]
                return jsonify(
                    "السجل المالي غير كافي", section8,dd)
        else:
            #currnoh = currnoh - noh
            q8 = ("select CONCAT ('[',section_time.start_time,' - ' ,section_time.end_time,'] ',section_time.day) AS 'time' ,section.section_id, course.noOfHours,course.course_name,section.course_id from course join section on course.course_id = section.course_id join section_time on section_time.sec_time_id=section.section_time join registered_courses on (registered_courses.sec_id = section.section_id and registered_courses.course_id=section.course_id) where registered_courses.std_id =(%s)")
            v8 = (std_id)
            cursor.execute(q8, v8)
            data8 = cursor.fetchall()

            section8 = []
            for result in data8:
                vaar = {
                    'time': result[0],
                    's_id': result[1],
                    'nh': result[2],
                    'cn': result[3],
                    'c_id': result[4],
                }
                section8.append(vaar)
            # text = "هذا المساق يتعارض مع مساق اخر في نفس الوقت"
            # speak(text)
            q = ("select std_info.hours from std_info where std_info.std_id = (%s)")

            v = (std_id)
            cursor.execute(q, v)
            dd = cursor.fetchone()[0]
            return jsonify(
                "هذا المساق يتعارض مع مساق اخر في نفس الوقت", section8,dd)

    else:
        #currnoh = currnoh - noh
        q8 = ("select CONCAT ('[',section_time.start_time,' - ' ,section_time.end_time,'] ',section_time.day) AS 'time' ,section.section_id, course.noOfHours,course.course_name,section.course_id from course join section on course.course_id = section.course_id join section_time on section_time.sec_time_id=section.section_time join registered_courses on (registered_courses.sec_id = section.section_id and registered_courses.course_id=section.course_id) where registered_courses.std_id =(%s)")
        v8 = (std_id)
        cursor.execute(q8, v8)
        data8 = cursor.fetchall()

        section8 = []
        for result in data8:
            vaar = {
                'time': result[0],
                's_id': result[1],
                'nh': result[2],
                'cn': result[3],
                'c_id': result[4],
            }
            section8.append(vaar)
            # connection.close()
        # text = "انت بالفعل مسجل في هذا المساق"
        # speak(text)
        q = ("select std_info.hours from std_info where std_info.std_id = (%s)")

        v = (std_id)
        cursor.execute(q, v)
        dd = cursor.fetchone()[0]
        return jsonify("انت بالفعل ملتحق بشعبة من هذا المساق يجب عليك حذف المساق ثم اعادة الالتحاق بشعبة اخرى", section8,dd)
 else:
    q8 = ("select CONCAT ('[',section_time.start_time,' - ' ,section_time.end_time,'] ',section_time.day) AS 'time' ,section.section_id, course.noOfHours,course.course_name,section.course_id from course join section on course.course_id = section.course_id join section_time on section_time.sec_time_id=section.section_time join registered_courses on (registered_courses.sec_id = section.section_id and registered_courses.course_id=section.course_id) where registered_courses.std_id =(%s)")
    v8 = (std_id)
    cursor.execute(q8, v8)
    data8 = cursor.fetchall()

    section8 = []
    for result in data8:
            vaar = {
                'time': result[0],
                's_id': result[1],
                'nh': result[2],
                'cn': result[3],
                'c_id': result[4],
            }
            section8.append(vaar)
          
    q = ("select std_info.hours from std_info where std_info.std_id = (%s)")
    v = (std_id)
    cursor.execute(q, v)
    dd = cursor.fetchone()[0]
 return jsonify("الشعبه مغلقه", section8,dd)






@app.route("/showreges_ajax", methods=['POST'])
def showreges_ajax():

 std_id = request.form['std_id']
 print(std_id)
 resultt=""
 qqq=("select  count(*) from  registered_courses where std_id=(%s)")
 vvv=(std_id)
 cursor.execute(qqq,vvv)
 ddaata = cursor.fetchone()[0]
 print(ddaata)
 if(ddaata==0):
    resultt="no"
 else:
    resultt="yes" 
 q8 = ("select CONCAT ('[',section_time.start_time,' - ' ,section_time.end_time,'] ',section_time.day) AS 'time' ,section.section_id, course.noOfHours,course.course_name,section.course_id from course join section on course.course_id = section.course_id join section_time on section_time.sec_time_id=section.section_time join registered_courses on (registered_courses.sec_id = section.section_id and registered_courses.course_id=section.course_id) where registered_courses.std_id =(%s)")
 v8 = (std_id)
 cursor.execute(q8, v8)
 data8 = cursor.fetchall()

 section8 = []
 for result in data8:
    vaar = {
         'time': result[0],
          's_id': result[1],
          'nh': result[2],
          'cn': result[3],
          'c_id': result[4],
                 }
    section8.append(vaar)
                  
 q = ("select std_info.hours from std_info where std_info.std_id = (%s)")

 v = (std_id)
 cursor.execute(q, v)
 dd = cursor.fetchone()[0]
 return jsonify( resultt,section8,dd)
 


    

@app.route("/delete_ajax", methods=['POST'])
def delete_ajax():
    cl = request.form['cl']
    sl = request.form['sl']
    std_id = request.form['std_id']
    print(std_id)
    print(sl)
    print(cl) 
    q=("select count(*) from  registered_courses where std_id=(%s) and course_id=(%s) and sec_id=(%s)")
    v=(std_id,cl,sl)
    cursor.execute(q, v)
    f = cursor.fetchone()[0]
    
    if(f!=0):
      q4 = (
        "select std_info.financial_record from std_info where std_info.std_id=(%s)")
      v4 = (std_id)
      cursor.execute(q4, v4)
      fr = cursor.fetchone()[0]
      fr1 = fr

      q5 = ("select course.noOfHours from course where course.course_id=(%s)")
      v5 = (cl)
      cursor.execute(q5, v5)
      cp = cursor.fetchone()[0]
      print(cp)
      price = cp*24
      print(price)
      fr1 = fr1+price
      print(fr1)
      # update finincial record to the value of fr1

      q6 = ("select std_info.hours from std_info where std_info.std_id = (%s)")

      v6 = (std_id)
      cursor.execute(q6, v6)
      dd = cursor.fetchone()[0]

      temp = dd - cp

      # update noOfHours to the value of the temp
      print(temp)

      q7 = (
        "delete from registered_courses where registered_courses.std_id =(%s) and registered_courses.course_id = (%s) and registered_courses.sec_id = (%s) ")
      v7 = (std_id, cl, sl)
      cursor.execute(q7, v7)
      connection.commit()

      # q8 = ("select CONCAT ('[',section_time.start_time,' - ' ,section_time.end_time,'] ',section_time.day) AS 'time'    ,section.section_id, course.noOfHours,course.course_name,section.course_id from course join section on course.course_id = section.course_id join section_time on section_time.sec_time_id=section.section_time join registered_courses on (registered_courses.sec_id = section.section_id and registered_courses.course_id=section.course_id) where registered_courses.std_id =(%s) and registered_courses.course_id =(%s) and registered_courses.sec_id = (%s)")
      # v8 = (std_id, cl, sl)

      q8 = ("select CONCAT ('[',section_time.start_time,' - ' ,section_time.end_time,'] ',section_time.day) AS 'time' ,section.section_id, course.noOfHours,course.course_name,section.course_id from course join section on course.course_id = section.course_id join section_time on section_time.sec_time_id=section.section_time join registered_courses on (registered_courses.sec_id = section.section_id and registered_courses.course_id=section.course_id) where registered_courses.std_id =(%s)")
      v8 = (std_id)
      cursor.execute(q8, v8)
      data8 = cursor.fetchall()

      section8 = []
      for result in data8:
        vaar = {
            'time': result[0],
            's_id': result[1],
            'nh': result[2],
            'cn': result[3],
            'c_id': result[4],
        }
        section8.append(vaar)
      q9 = (
        "UPDATE std_info SET std_info.hours = (%s) WHERE std_info.std_id = (%s)")
      v9 = (temp, std_id)
      cursor.execute(q9, v9)

      q10 = (
        "UPDATE std_info SET std_info.financial_record = (%s) WHERE std_info.std_id = (%s)")
      v10 = (fr1, std_id)
      cursor.execute(q10, v10)
      # (section8)
      q = ("select std_info.hours from std_info where std_info.std_id = (%s)")

      v = (std_id)
      cursor.execute(q, v)
      dd = cursor.fetchone()[0]
      return jsonify("اكتملت العملية بنجاح", section8,dd)
    else:
      q8 = ("select CONCAT ('[',section_time.start_time,' - ' ,section_time.end_time,'] ',section_time.day) AS 'time' ,section.section_id, course.noOfHours,course.course_name,section.course_id from course join section on course.course_id = section.course_id join section_time on section_time.sec_time_id=section.section_time join registered_courses on (registered_courses.sec_id = section.section_id and registered_courses.course_id=section.course_id) where registered_courses.std_id =(%s)")
      v8 = (std_id)
      cursor.execute(q8, v8)
      data8 = cursor.fetchall()

      section8 = []
      for result in data8:
        vaar = {
            'time': result[0],
            's_id': result[1],
            'nh': result[2],
            'cn': result[3],
            'c_id': result[4],
         }
        section8.append(vaar)   
      q = ("select std_info.hours from std_info where std_info.std_id = (%s)")

      v = (std_id)
      cursor.execute(q, v)
      dd = cursor.fetchone()[0]
      return jsonify(" محذوفه", section8,dd)

@app.route('/row_detail/<rowData>/<name>')
def row_detail(rowData, name):
    # q = ("SELECT classroom.room_capacity,instructor_info.inst_name,section_time.start_time,section.room_id,section.section_id FROM instructor_info JOIN section JOIN classroom JOIN course  on  section.course_id=(%s) and classroom.room_id=section.room_id and section.inst_id=instructor.inst_id ")
    q = ("SELECT section.course_id,section.section_id,section.room_id,section.section_time,section.inst_id FROM course JOIN section on course.course_id=section.course_id and section.course_id=(%s)")
    v = (rowData)
    cursor.execute(q, v)
    data = cursor.fetchall()

    q2 = ("SELECT course.course_id,course.course_name,course.noOfHours,plan.req_type FROM  course JOIN plan  on course.course_id=plan.course_id and dept_name=(%s)")
    v2 = (name)
    cursor.execute(q2, v2)
    data2 = cursor.fetchall()

    return render_template('StudentRegistration.html', value2=data, v=name, value=data2)


@app.route('/registerSection/<rowData>/<name>')
def registerSection(rowData, name):
    # q = ("SELECT classroom.room_capacity,instructor_info.inst_name,section_time.start_time,section.room_id,section.section_id FROM instructor_info JOIN section JOIN classroom JOIN course  on  section.course_id=(%s) and classroom.room_id=section.room_id and section.inst_id=instructor.inst_id ")
    q = ("SELECT section.course_id,section.section_id,section.room_id,section.section_time,section.inst_id FROM course JOIN section on course.course_id=section.course_id and section.course_id=(%s)")
    v = (rowData)
    cursor.execute(q, v)
    data = cursor.fetchall()

    q2 = ("SELECT course.course_id,course.course_name,course.noOfHours,plan.req_type FROM  course JOIN plan  on course.course_id=plan.course_id and dept_name=(%s)")
    v2 = (name)
    cursor.execute(q2, v2)
    data2 = cursor.fetchall()

    return render_template('StudentRegistration.html', value2=data, v=name, value=data2)

# @app.route("/selectSections/<name1>/<name2>/<name3>")
# def StudentRegistration(name1,name2,name3):
#     q = ("SELECT section.section_id,section.room_id,section_time.start_time,instructor_info.inst_name FROM  course JOIN plan  on course.course_id=plan.course_id and dept_name=(%s)")
#     v = (name)
#     cursor.execute(q, v)
#     data2 = cursor.fetchall()
#     return render_template("StudentRegistration.html", value=data2, v=name)

@app.route("/CourseSchedule", methods=['POST'])
def CourseSchedule():
   std_id = request.form.get("y")
   return render_template("CourseSchedule.html",v2=std_id)

@app.route("/cs_ajax", methods=['POST'])
def cs_ajax():
    
    # q = (
    #     "select concat (section.full_building_name,' (',section.building,')'), CONCAT (section.building,'-' ,section.room_id) AS 'class_room',CONCAT( instructor_info.f_name ,' ', instructor_info.l_name  ) AS 'inst_name' , CONCAT ('[',section_time.start_time,' - ' ,section_time.end_time,'] ',section_time.day) AS 'time' , section.section_id,course.noOfHours,course.course_name,section.course_id from section join course on course.course_id = section.course_id join instructor_info on instructor_info.inst_id = section.inst_id join section_time on section_time.sec_time_id = section.section_time join registered_courses on (registered_courses.course_id=section.course_id and registered_courses.sec_id= section.section_id) where registered_courses.std_id=(%s)")

    # q = ("SELECT course.course_id,course.course_name,course.noOfHours,plan.req_type FROM  course JOIN plan  on course.course_id=plan.course_id ")
    q = ("SELECT course.course_id , course.course_name  , course.noOfHours  , section.section_id ,    CONCAT ('[',section_time.start_time,' - ' ,section_time.end_time,'] ',section_time.day) AS 'time'    ,  CONCAT( instructor_info.f_name ,' ', instructor_info.l_name  ) AS 'inst_name'  , CONCAT (section.building,'-' ,section.room_id) AS 'class_room'   ,   concat (section.full_building_name,' (',section.building,')')  from section join course on course.course_id = section.course_id join instructor_info on instructor_info.inst_id = section.inst_id join section_time on section_time.sec_time_id = section.section_time")

    cursor.execute(q)
    data2 = cursor.fetchall()
    cap=[]
    cap2=[]
    for result in data2:
     cap.append(result[0])
     cap2.append(result[3])
     
    print(cap)
    print(cap2)
    num=[]
    num2=[]
    num3=[]
  
    size = len(cap)
    for i in range(size):     
           qqq=("select  count(*) from  registered_courses where course_id=(%s) and sec_id=(%s)")
           vvv=(cap[i],cap2[i])
           cursor.execute(qqq,vvv)
           ddaata = cursor.fetchone()[0]
           num.append(ddaata)
          
    print(num)
   
    for j in range(size):
           
        qqq2=("select  classroom.room_capacity from  section join classroom on section.room_id=classroom.room_id and section.full_building_name=classroom.full_building_name where section.course_id=(%s) and section.section_id=(%s)")
        vvv2=(cap[j],cap2[j])
        cursor.execute(qqq2,vvv2)
        ddaata2 = cursor.fetchone()[0]
        num2.append(ddaata2)  
    
    print(num2)

    yes="مفتوحه"
    no="مغلقه"
    for i in range(size):
      if(num[i]==num2[i]):
          num3.append(no)
        
      else:
        num3.append(yes)


    i=0 
    section = []
    for result in data2:
        
        contents = {'c_id': result[0],
                    'name': result[1],
                    'h': result[2],
                    's_id': result[3],
                    't': result[4],
                    'inst': result[5],
                    't2': num3[i],
                    'room': result[6],
                     'b': result[7],
                    }
        i=i+1
        section.append(contents)
               
    return jsonify(section)

@app.route("/show_ajax", methods=['POST'])
def   show_ajax():
    dep=request.form['department']
    type=request.form['type']
    # q = (
    #     "select concat (section.full_building_name,' (',section.building,')'), CONCAT (section.building,'-' ,section.room_id) AS 'class_room',CONCAT( instructor_info.f_name ,' ', instructor_info.l_name  ) AS 'inst_name' , CONCAT ('[',section_time.start_time,' - ' ,section_time.end_time,'] ',section_time.day) AS 'time' , section.section_id,course.noOfHours,course.course_name,section.course_id from section join course on course.course_id = section.course_id join instructor_info on instructor_info.inst_id = section.inst_id join section_time on section_time.sec_time_id = section.section_time join registered_courses on (registered_courses.course_id=section.course_id and registered_courses.sec_id= section.section_id) where registered_courses.std_id=(%s)")

    # q = ("SELECT course.course_id,course.course_name,course.noOfHours,plan.req_type FROM  course JOIN plan  on course.course_id=plan.course_id ")
    q = ("SELECT course.course_id , course.course_name  , course.noOfHours  , section.section_id ,    CONCAT ('[',section_time.start_time,' - ' ,section_time.end_time,'] ',section_time.day) AS 'time'    ,  CONCAT( instructor_info.f_name ,' ', instructor_info.l_name  ) AS 'inst_name'  , CONCAT (section.building,'-' ,section.room_id) AS 'class_room'   ,   concat (section.full_building_name,' (',section.building,')')  from section join course on course.course_id = section.course_id join instructor_info on instructor_info.inst_id = section.inst_id join section_time on section_time.sec_time_id = section.section_time join plan on course.course_id=plan.course_id where plan.dept_name=(%s) and plan.req_type=(%s)")
    v=(dep,type)
    cursor.execute(q,v)
    data2 = cursor.fetchall()
    cap=[]
    cap2=[]
    for result in data2:
     cap.append(result[0])
     cap2.append(result[3])
     
    print(cap)
    print(cap2)
    num=[]
    num2=[]
    num3=[]
  
    size = len(cap)
    for i in range(size):     
           qqq=("select  count(*) from  registered_courses where course_id=(%s) and sec_id=(%s)")
           vvv=(cap[i],cap2[i])
           cursor.execute(qqq,vvv)
           ddaata = cursor.fetchone()[0]
           num.append(ddaata)
          
    print(num)
   
    for j in range(size):
           
        qqq2=("select  classroom.room_capacity from  section join classroom on section.room_id=classroom.room_id and section.full_building_name=classroom.full_building_name where section.course_id=(%s) and section.section_id=(%s)")
        vvv2=(cap[j],cap2[j])
        cursor.execute(qqq2,vvv2)
        ddaata2 = cursor.fetchone()[0]
        num2.append(ddaata2)  
    
    print(num2)

    yes="مفتوحه"
    no="مغلقه"
    for i in range(size):
      if(num[i]==num2[i]):
          num3.append(no)
        
      else:
        num3.append(yes)


    i=0 
    section = []
    for result in data2:
        
        contents = {'c_id': result[0],
                    'name': result[1],
                    'h': result[2],
                    's_id': result[3],
                    't': result[4],
                    'inst': result[5],
                    't2': num3[i],
                    'room': result[6],
                     'b': result[7],
                    }
        i=i+1
        section.append(contents)
               
    return jsonify(section)
  

@app.route("/afterlogin", methods=['POST'])
def afterlogin():

    id = request.form.get("number")
    print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    b = int(id)
    q = ("SELECT * FROM  std_info WHERE std_id=(%s)")
    v = (b)
    cursor.execute(q, v)
    data = cursor.fetchall()
    return render_template("afterlogin.html", value=data)


@app.route("/financial", methods=['POST'])
def financial():
    std_id = request.form.get("x")
    q = ("select financial_record from std_info where std_info.std_id=(%s) ")
    v = (std_id)
    cursor.execute(q, v)
    data = cursor.fetchone()[0]

    return render_template("financial.html", finance=data, v2=std_id)


@app.route("/temporary_ajax", methods=['POST'])
def temporary_ajax():

    std = request.form.get("std_id")
    q=("select course_id,sec_id,noOfHours from temp_registered_courses join course on temp_registered_courses.course_id=course.course_id   join section on section.course_id=course.course_id where std_id=(%s)")
    v=(std)
    cursor.execute(q,v)
    data = cursor.fetchall
    section=[]
    for result in data:
      contents={'course':result[0],
      'section':result[1]}
     
    section.append(contents)
    return jsonify(section)




@app.route("/admin",methods=['POST'])
def admin():
 
    
   
   
    return render_template("admin.html")
   
 

@app.route("/createstudent", methods=['POST'])
def createstudent():

 return  render_template('createstudent.html')



@app.route("/editstudent", methods=['POST'])
def editstudent():

 return  render_template('editstudent.html')

@app.route("/creataccountajax", methods=['POST'])
def creataccountajax():
    num=request.form.get('num')
    numm=int(num)
    first=request.form.get('first')
    last=request.form.get('last')
    email=request.form.get('email')
    phone=request.form.get('phone')
    finance=request.form.get('finance')
    f=int(finance)
    gen=request.form.get('gen')
    passw=request.form.get('passw')
    dept=request.form.get('dept')
    hash= generate_password_hash(passw, method='sha256')
    h=int('0')   
    q = ("select  count(std_info.std_id) from std_info where std_info.std_id = (%s)")
    v = (numm)
    cursor.execute(q, v)
    dd = cursor.fetchone()[0]
    
    if dd!=0:
        return jsonify ("no")

    else:
       q2 = ("insert  into std_info  values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
       v2 = (numm,first,last,gen,email,phone,hash,dept,f,h)
       cursor.execute(q2, v2)
       return  jsonify ("yes")


@app.route("/student_ajax", methods=['POST'])
def student_ajax():
   
    q = ("select  std_info.std_id,concat(std_info.f_name,' ',std_info.l_name) as name ,std_info.email,std_info.phone_number from std_info ")
    cursor.execute(q)
    data = cursor.fetchall()
  
    section = []
    for result in data:
        vaar = {
                'id': result[0],
                'name': result[1],
                'email': result[2],
                'phone': result[3],
                
             }
        section.append(vaar)
      

    return jsonify (section)

@app.route("/editstudent_ajax", methods=['POST'])
def editstudent_ajax():
   id=request.form.get("id")
   id=int(id)
   passw=request.form.get("passw")
   hash=generate_password_hash(passw, method='sha256')
   q1=("select count(std_info.std_id) from std_info where std_info.std_id=(%s)")
   v1=(id)
   cursor.execute(q1,v1)
   data=cursor.fetchone()[0]
   bool="false"
   if(data!=0):
        bool="true"
        q3=("update std_info set std_info.password =(%s) where std_info.std_id=(%s)")
        v3=(hash,id)
        cursor.execute(q3,v3)
   else:
        bool="false"
   
   q2 = ("select  std_info.std_id,concat(std_info.f_name,' ',std_info.l_name) as name ,std_info.email,std_info.phone_number from std_info ")
   cursor.execute(q2)
   data2 = cursor.fetchall()
    
   section = []
   for result in data2:
        vaar = {
                'id': result[0],
                'name': result[1],
                'email': result[2],
                'phone': result[3],
                
             }
        section.append(vaar)
        

   return jsonify (bool,section)



@app.route("/course",methods=['POST'])
def course():
   
    q = ("SELECT course.course_id,course.course_name,course.noOfHours FROM  course ")
    cursor.execute(q)
    data = cursor.fetchall()
    return render_template("course.html", value=data)


@app.route("/section_ajax", methods=['POST'])
def section_ajax():
    cl = request.form['cl']
    q = (
      "SELECT  section.course_id,section.section_id,CONCAT (section.building,'-' ,section.room_id) AS 'class_room',CONCAT ('[',section_time.start_time,' - ' ,section_time.end_time,'] ',section_time.day) AS 'time'    ,CONCAT( instructor_info.f_name ,' ', instructor_info.l_name  ) AS 'inst_name' , classroom.room_capacity FROM section JOIN classroom on  section.room_id=classroom.room_id and section.building=classroom.building  join section_time on section.section_time= section_time.sec_time_id join  instructor_info on section.inst_id =instructor_info.inst_id  and  section.course_id=(%s)")

    v = (cl)
    cursor.execute(q, v)
    data = cursor.fetchall()
    
    cap=[]
    for result in data:
        cap.append(result[1])
   
    num=[]
    for i in cap:
       print(i)
       qqq=("select  count(*) from  registered_courses where course_id=(%s) and sec_id=(%s)")
       vvv=(cl,i)
       cursor.execute(qqq,vvv)
       ddaata = cursor.fetchone()[0]
       num.append(ddaata)
       
    i=0
    section = []
    for result in data:
        
        contents = {'cap': num[i],
                    'r_id': result[4],
                    's_time': result[3],
                    'inst_name': result[2],
                    's_id': result[1],
                    }
        i=i+1
        section.append(contents)
        
        
    return jsonify(section)


#delete

@app.route("/deletesection_ajax", methods=['POST'])
def deletesection_ajax():
    cl = request.form['ci']
    si = request.form['si']
    
    qq=("select  count(*) from  registered_courses where course_id=(%s) and sec_id=(%s)")
    vv=(cl,si)
    cursor.execute(qq,vv)
    dataa = cursor.fetchone()[0]
    res="false"
    
    if(dataa==0):
      res="true"
      qqq=("DELETE  from section where course_id=(%s) and section_id=(%s)")
      vvv=(cl,si)
      cursor.execute(qqq,vvv)
    else:
      res="false" 
    
    q = (
      "SELECT  section.course_id,section.section_id,CONCAT (section.building,'-' ,section.room_id) AS 'class_room',CONCAT ('[',section_time.start_time,' - ' ,section_time.end_time,'] ',section_time.day) AS 'time'    ,CONCAT( instructor_info.f_name ,' ', instructor_info.l_name  ) AS 'inst_name' , classroom.room_capacity FROM section JOIN classroom on  section.room_id=classroom.room_id and section.building=classroom.building  join section_time on section.section_time= section_time.sec_time_id join  instructor_info on section.inst_id =instructor_info.inst_id  and  section.course_id=(%s)")

    v = (cl)
    cursor.execute(q, v)
    data = cursor.fetchall()
    
    cap=[]
    for result in data:
        cap.append(result[1])
   
    num=[]
    for i in cap:
       print(i)
       qqq=("select  count(*) from  registered_courses where course_id=(%s) and sec_id=(%s)")
       vvv=(cl,i)
       cursor.execute(qqq,vvv)
       ddaata = cursor.fetchone()[0]
       num.append(ddaata)
       
    i=0
    section = []
    for result in data:
        
        contents = {'cap': num[i],
                    'r_id': result[4],
                    's_time': result[3],
                    'inst_name': result[2],
                    's_id': result[1],
                    }
        i=i+1
        section.append(contents)
        
        
    return jsonify(res,section)




@app.route("/addstudenttosection_ajax", methods=['POST'])
def addstudenttosection_ajax():
    ci = request.form['ci']
    si = request.form['si']
    std_id = request.form['std_id']
    resultttt=""
    s=("select count(*) from std_info where std_info.std_id=(%s)")
    c=(std_id)
    cursor.execute(s, c)
    dataw = cursor.fetchone()[0]
    if(dataw !=0 ):
        # ///////////////////////////////////////////////////
        q = ("SELECT section.section_time from section where section.course_id=(%s) and section.section_id=(%s)")
        v = (ci, si)
        cursor.execute(q, v)
        # section time id for course id
        curr_sec_time_id = cursor.fetchone()[0]


        # and registered_courses.sec_id=(%s)
        q1 = ("select count(*) from registered_courses where registered_courses.course_id=(%s)  and registered_courses.std_id=(%s)")
        v1 = (ci,  std_id)
        cursor.execute(q1, v1)
        data2 = cursor.fetchone()[0]

   
        q3 = ("select section_time.sec_time_id from  section_time join section on section.section_time = section_time.sec_time_id join registered_courses on section.section_id=registered_courses.sec_id and section.course_id=registered_courses.course_id where registered_courses.std_id=(%s)")
        v3 = (std_id)
        cursor.execute(q3, v3)
        flag = true

        if (data2 == 0):

          for row in cursor:
            if row[0] == curr_sec_time_id:

                flag = false
                break
            elif curr_sec_time_id == 1 or curr_sec_time_id == 2:
                if(row[0] == 5 or row[0] == 10 or row[0] == 12):

                    flag = false
                    break

            elif curr_sec_time_id == 3 or curr_sec_time_id == 4:
                if(row[0] == 6 or row[0] == 11 or row[0] == 13):

                    flag = false
                    break

            elif curr_sec_time_id == 7 or curr_sec_time_id == 8:
                if(row[0] == 9 or row[0] == 14):

                    flag = false
                    break

            elif curr_sec_time_id == 5 or curr_sec_time_id == 10 or curr_sec_time_id == 12:
                if(row[0] == 1 or row[0] == 2):

                    flag = false
                    break

            elif (curr_sec_time_id == 6 or curr_sec_time_id == 11 or curr_sec_time_id == 13):
                if(row[0] == 3 or row[0] == 4):

                    flag = false
                    break

            elif curr_sec_time_id == 9 or curr_sec_time_id == 14:
                if(row[0] == 7 or row[0] == 8):

                    flag = false
                    break

            # else:

            continue
            # return jsonify("hiiiiiiiiiiiiiiiiiiiii")

          if flag == true:

            q4 = (
                "select std_info.financial_record from std_info where std_info.std_id=(%s)")
            v4 = (std_id)
            cursor.execute(q4, v4)
            fr = cursor.fetchone()[0]
            fr1 = fr

            q5 = ("select course.noOfHours from course where course.course_id=(%s)")
            v5 = (ci)
            cursor.execute(q5, v5)
            cp = cursor.fetchone()[0]
            print(cp)
            price = cp*24
            print(price)
            fr1 = fr1-price
            print(fr1)

            if fr1 >= 0:

                #q6 = ("select sum(course.noOfHours)  from course join section on course.course_id= section.course_id join registered_courses on (registered_courses.course_id=section.course_id) where registered_courses.std_id=(%s) group by course.course_id")
                #q6 = ("select distinct course.course_name,(course.noOfHours)  from course join section on course.course_id= section.course_id join registered_courses on (registered_courses.course_id=section.course_id) where registered_courses.std_id=(%s) group by course.course_id ")
                q6 = ("select std_info.hours from std_info where std_info.std_id = (%s)")

                v6 = (std_id)
                cursor.execute(q6, v6)
                dd = cursor.fetchone()[0]
                temp = 0
                # for i in dd:
                #     sum = sum + cursor.fetchone()[1]

                print(dd)

                #noh = cursor.fetchone()[0]
                # if (noh is None):
                #   noh = 0
                currnoh = cp
                temp = dd+currnoh

                #currnoh = currnoh + noh

                if temp <= 20:
                  resulttt="true"
                  q2=("insert into  registered_courses values ((%s),(%s),(%s))")
                  v2=(std_id,ci,si)
                  cursor.execute(q2,v2)
                  resultttt="yes"

                  q9 = ("UPDATE std_info SET std_info.hours = (%s) WHERE std_info.std_id = (%s)")
                  v9 = (temp, std_id)
                  cursor.execute(q9, v9)

                  q10 = (
                 "UPDATE std_info SET std_info.financial_record = (%s) WHERE std_info.std_id = (%s)")
                  v10 = (fr1, std_id)
                  cursor.execute(q10, v10)

                  q11 =   (
                 "SELECT  distinct classroom.room_capacity FROM section JOIN classroom on section.room_id=classroom.room_id  join section_time on section.section_time= section_time.sec_time_id join  instructor_info on section.inst_id =instructor_info.inst_id  and  section.course_id=(%s) and section.section_id=(%s)")
                  v11 = (ci,si)
                  cursor.execute(q11, v11)
                  data11 = cursor.fetchone()[0]
                  data11=data11+1
                  q12 = (
                 "UPDATE section JOIN classroom on section.room_id=classroom.room_id and section.building=classroom.building  join section_time on section.section_time= section_time.sec_time_id join  instructor_info on section.inst_id =instructor_info.inst_id  SET classroom.room_capacity =(%s) where  section.course_id=(%s) and section.section_id=(%s)")
                  v12 = (data11, ci,si)
                  cursor.execute(q12, v12)    
                    

                else:
                 resulttt="hours"
                   
            else:
               resulttt="finance"
                   
          else:
            resulttt="conflict"

            
        else:
           resulttt="already"
        
        # ///////////////////////////////////////////////////////////////////////////////////
      
       
       
        
      
       
    else:
       resultttt="error" 
    q =("SELECT  section.course_id,section.section_id,CONCAT (section.building,'-' ,section.room_id) AS 'class_room',CONCAT ('[',section_time.start_time,' - ' ,section_time.end_time,'] ',section_time.day) AS 'time'    ,CONCAT( instructor_info.f_name ,' ', instructor_info.l_name  ) AS 'inst_name' , classroom.room_capacity FROM section JOIN classroom on  section.room_id=classroom.room_id and section.building=classroom.building  join section_time on section.section_time= section_time.sec_time_id join  instructor_info on section.inst_id =instructor_info.inst_id  and  section.course_id=(%s)")
    v = (ci)
    cursor.execute(q, v)
    data = cursor.fetchall()
    
    cap=[]
    for result in data:
     cap.append(result[1])
   
    num=[]
    
    for i in cap:
       print(i)
       qqq=("select  count(*) from  registered_courses where course_id=(%s) and sec_id=(%s)")
       vvv=(ci,i)
       cursor.execute(qqq,vvv)
       ddaata = cursor.fetchone()[0]
       num.append(ddaata)
       
    i=0
    section = []
    for result in data:
        
        contents = {'cap': num[i],
                    'r_id': result[4],
                    's_time': result[3],
                    'inst_name': result[2],
                    's_id': result[1],
                    }
        i=i+1
        section.append(contents)
               
    return jsonify(resultttt,section)

#add section


@app.route("/addsection_ajax", methods=['POST'])
def addsection_ajax():
    ci = request.form['ci']
    inst = request.form['inst']
    section = request.form['section']
    building = request.form['building']
    section_time = request.form['section_time']
    room_id = request.form['room_id']
    name= request.form['name']
    flag=true
    resultttt=""
    section=int(section)
    section_time=int(section_time)
    ci=int(ci)
    inst=int(inst)

    print(ci,inst,section,building,section_time,room_id,name)
       
    dd=("select count(*) from section join section_time on section.section_time = section_time.sec_time_id  where section.course_id=(%s)")
    vv=(ci)
    cursor.execute(dd,vv)
    dat=cursor.fetchone()[0]
    print("//////////////////")
    print(dat)
    if (dat !=0):
        
        ff=("select section.section_id from section join section_time on section.section_time = section_time.sec_time_id  where section.course_id=(%s)")
        gg=(ci)
        cursor.execute(ff,gg)
        data = cursor.fetchall()
        print("/////////////")
        print(data)
        for r in data:
            if r[0]==section:
               flag = false
               print("ggggggggggggggggggggggggggggggggg")
               break
            
            
            continue
        
        if(flag==true):
          print("oooooooooooooooooooooooooooook")
          q1 = ("select section_time.sec_time_id from  section_time join section on section.section_time = section_time.sec_time_id  where section.course_id=(%s)")
          v1 = (ci)
          cursor.execute(q1, v1)
          data2 = cursor.fetchall()
          
    
          for row in data2:
            if row[0] == section_time:
              flag = false
              break  
               
                       
            continue
            # return jsonify("hiiiiiiiiiiiiiiiiiiiii")

          if flag == true:
           print("uuuuuuuuuuuuuuuuuuuu")
           resultttt="yes" 
           qqq=(" INSERT INTO section VALUES ((%s),(%s),(%s),(%s),(%s),(%s),(%s))")
           vvv=(section,ci,room_id,section_time,inst,building,name)
           cursor.execute(qqq, vvv)
     
          else:
           resultttt="no"  
        else:
           resultttt="no"
    else:
       resultttt="yes" 
       qq=("insert into section values ((%s),(%s),(%s),(%s),(%s),(%s),(%s))")
       vv=(section,ci,room_id,section_time,inst,building,name)
       cursor.execute(qq, vv)      
    
    
    
    q =("SELECT  section.course_id,section.section_id,CONCAT (section.building,'-' ,section.room_id) AS 'class_room',CONCAT ('[',section_time.start_time,' - ' ,section_time.end_time,'] ',section_time.day) AS 'time'    ,CONCAT( instructor_info.f_name ,' ', instructor_info.l_name  ) AS 'inst_name' , classroom.room_capacity FROM section JOIN classroom on  section.room_id=classroom.room_id and section.building=classroom.building  join section_time on section.section_time= section_time.sec_time_id join  instructor_info on section.inst_id =instructor_info.inst_id  and  section.course_id=(%s)")
    v = (ci)
    cursor.execute(q, v)
    data = cursor.fetchall()
    
    cap=[]
    for result in data:
     cap.append(result[1])
   
    num=[]
    
    for i in cap:
       print(i)
       qqq=("select  count(*) from  registered_courses where course_id=(%s) and sec_id=(%s)")
       vvv=(ci,i)
       cursor.execute(qqq,vvv)
       ddaata = cursor.fetchone()[0]
       num.append(ddaata)
       
    i=0
    section = []
    for result in data:
        
        contents = {'cap': num[i],
                    'r_id': result[4],
                    's_time': result[3],
                    'inst_name': result[2],
                    's_id': result[1],
                    }
        i=i+1
        section.append(contents)
               
    return jsonify(resultttt,section)



@app.route("/editsection_ajax", methods=['POST'])
def editsection_ajax():
    ci = request.form['ci']
    inst = request.form['inst']
    section = request.form['section']
    building = request.form['building']
    section_time = request.form['section_time']
    room_id = request.form['room_id']
    name= request.form['name']
    flag=true
    resultttt=""
    section=int(section)
    section_time=int(section_time)
    ci=int(ci)
    inst=int(inst)

    print(ci,inst,section,building,section_time,room_id,name)
       
    dd=("select count(*) from section join section_time on section.section_time = section_time.sec_time_id  where section.course_id=(%s)")
    vv=(ci)
    cursor.execute(dd,vv)
    dat=cursor.fetchone()[0]
    print("//////////////////")
    print(dat)
    if (dat !=0):
        
        ff=("select section.section_id from section join section_time on section.section_time = section_time.sec_time_id  where section.course_id=(%s)")
        gg=(ci)
        cursor.execute(ff,gg)
        data = cursor.fetchall()
        print("/////////////")
        print(data)
        flag=false
        for r in data:
            if r[0]==section:
               flag = true
               print("ggggggggggggggggggggggggggggggggg")
               break
            
            
            continue
        
        if(flag==true):
          print("oooooooooooooooooooooooooooook")
          q1 = ("select section_time.sec_time_id from  section_time join section on section.section_time = section_time.sec_time_id  where section.course_id=(%s)")
          v1 = (ci)
          cursor.execute(q1, v1)
          data2 = cursor.fetchall()
          print(data2)
          print(section_time)
          
          flag=true
          for row in data2:
              print("hhhhhhhhhh")
              if row[0] == section_time :
                 flag = false
                 break 

              continue
            # return jsonify("hiiiiiiiiiiiiiiiiiiiii")

          if flag == true:
           print("uuuuuuuuuuuuuuuuuuuu")
           resultttt="yes" 
           qqq=(" update section  set room_id=(%s),section_time=(%s),inst_id=(%s),building=(%s),full_building_name=(%s) where section_id=(%s)and course_id=(%s)")
           vvv=(room_id,section_time,inst,building,name,section,ci)
           cursor.execute(qqq, vvv)
     
          else:
              print("dfdgddddddddddddddddddddddddddd")
              print(section)
              print(section_time)
              flag=false
             
              q = ("select section_time.sec_time_id ,section.section_id from  section_time join section on section.section_time = section_time.sec_time_id  where section.course_id=(%s)")
              v = (ci)
              cursor.execute(q,v)
              f=cursor.fetchall()
              
              for row in f:
                print(row[0])
                print(row[1])
                if((row[0]==section_time) and (row[1]==section)):
                    flag=true
                    break

                continue

              if(flag==true): 
                 resultttt="yes"
                 qqq=(" update section  set room_id=(%s),section_time=(%s),inst_id=(%s),building=(%s),full_building_name=(%s) where section_id=(%s)and course_id=(%s)")
                 vvv=(room_id,section_time,inst,building,name,section,ci)
                 cursor.execute(qqq, vvv)

              else:
                 resulttt="no"
        else:
           resultttt="no"
    else:
       resultttt="no" 
            
    
    
    
    q =("SELECT  section.course_id,section.section_id,CONCAT (section.building,'-' ,section.room_id) AS 'class_room',CONCAT ('[',section_time.start_time,' - ' ,section_time.end_time,'] ',section_time.day) AS 'time'    ,CONCAT( instructor_info.f_name ,' ', instructor_info.l_name  ) AS 'inst_name' , classroom.room_capacity FROM section JOIN classroom on  section.room_id=classroom.room_id and section.building=classroom.building  join section_time on section.section_time= section_time.sec_time_id join  instructor_info on section.inst_id =instructor_info.inst_id  and  section.course_id=(%s)")
    v = (ci)
    cursor.execute(q, v)
    data = cursor.fetchall()
    
    cap=[]
    for result in data:
     cap.append(result[1])
   
    num=[]
    
    for i in cap:
       print(i)
       qqq=("select  count(*) from  registered_courses where course_id=(%s) and sec_id=(%s)")
       vvv=(ci,i)
       cursor.execute(qqq,vvv)
       ddaata = cursor.fetchone()[0]
       num.append(ddaata)
       
    i=0
    section = []
    for result in data:
        
        contents = {'cap': num[i],
                    'r_id': result[4],
                    's_time': result[3],
                    'inst_name': result[2],
                    's_id': result[1],
                    }
        i=i+1
        section.append(contents)
               
    return jsonify(resultttt,section)



if __name__ == "__main__":
    app.run(port=9000)
