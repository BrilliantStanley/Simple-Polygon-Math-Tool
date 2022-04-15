import turtle
import math

#Functions
def color_check(fill,outline):
    screen1=turtle.Screen()
    turtle.TurtleScreen._RUNNING=True
    test = turtle.Turtle()
    test.pu()
    
    if fill == "0" :
        fill = ""
        fill_bool = True
    else :
        try :
            test.pencolor(fill)
            fill_bool = True
        except :
            fill = ""
            fill_bool = False
    if outline == "0" :
        
        outline = "black"
        outline_bool = True
    else :
        try :
            test.pencolor(outline)
            outline_bool = True
        except :
            outline = "black"
            outline_bool = False
            print(0)
    turtle.done
    screen1.bye()
    return fill, outline, fill_bool, outline_bool
    
def save_file():
    global poly_dict, color_dict
    while True :
        file_name = input("Enter output filename: ")
        try:
            outfile = open(file_name, "w")
            break
        except FileNotFoundError:
            print("Can't open file. Try again.")
    for no in poly_dict :
        for i in range(len(poly_dict[no])-1):
            print(f"({poly_dict[no][i][0]:.2f},{poly_dict[no][i][1]:.2f})",file=outfile,end=",")
        print(f"({poly_dict[no][len(poly_dict[no])-1][0]:.2f},{poly_dict[no][len(poly_dict[no])-1][1]:.2f})",file=outfile,end=":")
        print(f"{color_dict[no][0]},{color_dict[no][1]}.",file=outfile)
    outfile.close()
        
def poly_dict_print():
    global poly_dict
    if len(poly_dict) == 1:
        polygon_xy = poly_dict[1]
        n = 1
    else :
        for no in poly_dict :
            print(f"Polygon {no:>3d} : ",end="")
            for i in range(len(poly_dict[no])-1):
                print(f"({poly_dict[no][i][0]:.2f},{poly_dict[no][i][0]:.2f})",end=" , ")
            print(f"({poly_dict[no][-1][0]:.2f},{poly_dict[no][-1][0]:.2f})")
        n = int(input("Enter polygon number : "))
        
        while not n in range(1,len(poly_dict)+1):
            n = int(input("Out of range! Re-enter polygon number : "))
    return n
            
def check_point(xy_list,x,y) :
    if border(xy_list)[2] <= x <= border(xy_list)[0] and border(xy_list)[3] <= y <= border(xy_list)[1] :
        if (x,y) in xy_list :
            return "Point located  right on the polygon vertex"
        n = 0
        for i in range(len(xy_list)) :
            if i == len(xy_list)-1:
                x1, y1 = xy_list[-1][0] , xy_list[-1][1]
                x2, y2 = xy_list[0][0] , xy_list[0][1]
            else :
                x1, y1 = xy_list[i][0] , xy_list[i][1]
                x2, y2 = xy_list[i+1][0] , xy_list[i+1][1]

            if x1 - x != 0 :
                m1 = (y1-y)/(x1-x)
            else :
                m1 = "inf"

            if x - x2 != 0 :
                m2 = (y-y2)/(x-x2)
            else :
                m2 = "inf"

            if m1 == m2 and ((x1<=x2 and x1<=x<=x2)or(x2<=x1 and x2<=x<=x1))and ((y1<=y2 and y1<=y<=y2)or(y2<=y1 and y2<=y<=y1)):
                return "Point located right on the polygon vertice"
            elif intersectCheck(x1,y1,x2,y2,x,y,border(xy_list)[0]+2,y+1) :
                n += 1
                
        if n % 2 == 0 :
            return "Point located outside of the polygon"
        else :
            return "Point located inside of the polygon"
    else :
        return "Point located outside of the polygon"
        print(0)
def area(xy_list):
    area_sum = 0
    for n in range(len(xy_list)-1):
        area_sum += (xy_list[n][0]*xy_list[n+1][1] - xy_list[n][1]*xy_list[n+1][0])
    area_sum += xy_list[len(xy_list)-1][0]*xy_list[0][1] - xy_list[len(xy_list)-1][1]*xy_list[0][0]  
    area_sum = abs(area_sum/2)
    return area_sum

def perimeter(xy_list) :
    perimeter_sum = 0
    for n in range(len(xy_list)-1) :
        perimeter_sum += math.sqrt((xy_list[n+1][0]-xy_list[n][0])**2 + (xy_list[n+1][1] - xy_list[n][1])**2 )
    perimeter_sum += math.sqrt((xy_list[0][0]-xy_list[len(xy_list)-1][0])**2 + (xy_list[0][1] - xy_list[len(xy_list)-1][1])**2 )
    return perimeter_sum

def scale(xy_list,k,x,y):
    for i in range(len(xy_list)) :
        x_o = xy_list[i][0]
        y_o = xy_list[i][1]
        x_n = k*(x_o-x)+x
        y_n = k*(y_o-y)+y
        xy_list[i] = (x_n,y_n)
    return xy_list

def centroid(xy_list):
    x_list = [ xy[0] for xy in xy_list ]
    y_list = [ xy[1] for xy in xy_list ]
    x_c = sum(x_list)/len(xy_list)
    y_c = sum(y_list)/len(xy_list)
    return (x_c,y_c)
    
def rotate(xy_list,teta,x,y):
    teta_rad = math.radians(teta)
    for i in range(len(xy_list)) :
        x_o = xy_list[i][0]
        y_o = xy_list[i][1]
        x_n = math.cos(teta_rad)*(x_o - x) - math.sin(teta_rad)*(y_o - y) + x
        y_n = math.sin(teta_rad)*(x_o - x) + math.cos(teta_rad)*(y_o - y) + y
        xy_list[i] = (x_n,y_n)
    return xy_list

def move(xy_list,x,y):
    for i in range(len(xy_list)) :
        x_n = xy_list[i][0] + x
        y_n = xy_list[i][1] + y
        xy_list[i] = (x_n,y_n)
    return xy_list

def border(xy_list):
    x_list = [ xy[0] for xy in xy_list ]
    y_list = [ xy[1] for xy in xy_list ]
    x_list.sort()
    y_list.sort()
    return ( x_list[-1], y_list[-1], x_list[0], y_list[0] )#max,max,min,min
    
def intersectCheck(x1,y1,x2,y2,x3,y3,x4,y4):
    if x1 - x2 != 0 :
        m1 = (y1-y2)/(x1-x2)
    else :
        m1 = "inf"
    if x3 - x4 != 0 :
        m2 = (y3-y4)/(x3-x4)
    else :
        m2 = "inf"
    if m1 != m2 :
        u = ((x1-x3)*(y1-y2)-(y1-y3)*(x1-x2))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
        v = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
        if (0.0 <= u <= 1.0) and (0.0 <= v <= 1.0):
            return True
    else :
        return False
    
def coord_check(x , y, xy_list):

    if (x,y) in xy_list :
        return (False,"Same point is given")
    
    if 0 == len(xy_list):
        return (True,0) 

    if len(xy_list) > 1 :
        x3 = xy_list[len(xy_list)-1][0]
        y3 = xy_list[len(xy_list)-1][1]
        x4 = xy_list[len(xy_list)-2][0]
        y4 = xy_list[len(xy_list)-2][1]

        if x3 - x4 != 0 :
            m1 = (y3-y4)/(x3-x4)
        else :
            m1 = "inf"

        if x - x3 != 0 :
            m2 = (y-y3)/(x-x3)
        else :
            m2 = "inf"

        if  m1 == m2 :
            return (False,"Straight line was formed")

    if len(xy_list) > 2 :
        for i in range(0,len(xy_list)-2) :

            x1 = xy_list[i][0]
            y1 = xy_list[i][1]
            x2 = xy_list[i+1][0]
            y2 = xy_list[i+1][1]

            if intersectCheck(x1,y1,x2,y2,x3,y3,x,y):
                return (False, f"Point given intersect with line {i+1}",i+2)
            
    return (True,0)

def input_poly():
    method = (input("Choose of those methods, '1' = enter manually or '2' = input from file : "))
    if method == "1" :
        input_poly_manual()
    elif method == "2" :
        input_poly_file()
    else : input_poly()

def input_poly_manual() :
    global poly_dict
    print(f"Polygon {len(poly_dict)+1}")
    polygon_xy1=[]

    #input color
    fill = input("Enter fill color ('0' for default) : ")
    outline = input("Enter outline color ('0' for default) : ")
    
    while not color_check(fill,outline)[2]:
        fill = input("Invalid, Re-nter fill color ('0' for default) : ")
    while not color_check(fill,outline)[3]:
        outline = input("Invalid, Re-nter outline color ('0' for default) : ")
    
    #input no of vertices
    while True :
        try :
            no_vertices = int(input("Input number of polygon vertices : "))
            while no_vertices < 3 :
                no_vertices = int(input(f"Minimal vertices to draw polygon are 3.\nInput number of polygon vertices : "))
            break
        except :
            print("Invalid input")
            continue
        
    #input coordinates
    for vertex in range(1, no_vertices + 1):
        while True :
            try :
                x = float(input(f"Enter x coordinate of vertex {vertex} : "))
                y = float(input(f"Enter y coordinate of vertex {vertex} : "))
                while not coord_check(x, y,polygon_xy1)[0] :
                    x = float(input(f"Invalid! {coord_check(x, y,polygon_xy1)[1]}!\nRe-enter x coordinate of vertex {vertex} : "))
                    y = float(input(f"Re-enter y coordinate of vertex {vertex} : "))
                if vertex == no_vertices :
                    if not coord_check(polygon_xy1[0][0],polygon_xy1[0][1],polygon_xy1[1:]+[(x,y)])[0] :
                        x = float(input(f"Invalid! Point given intersect with line {coord_check(polygon_xy1[0][0],polygon_xy1[0][1],polygon_xy1[1:]+[(x,y)])[2]}!\nRe-enter x coordinate of vertex {vertex} : "))
                        y = float(input(f"Re-enter y coordinate of vertex {vertex} : "))
                break
            except:
                print("Invalid input")
                continue
        
        polygon_xy1.append((x,y))
        
    poly_dict[len(poly_dict)+1] = polygon_xy1
    color_dict[len(poly_dict)] = (color_check(fill,outline)[0],color_check(fill,outline)[1])
    draw()

def input_poly_file() :
    print("Supported format : '(x1,y1),(x2,y2),...:FillColor,OutlineColor.'")
    file_name = input("Enter filename : ")
    while True :
        try:
            file = open(file_name,"r")
            break
        except FileNotFoundError :
            print("File not found!")
            file_name = input("Re-enter filename including file extension : ")
    global poly_dict, color_dict
    line_no = 0
    for line1 in file :
        try :
            separator_i = line1.find(":")
            line2 = line1[separator_i+1::]
            comma_i = line2.find(",")
            end_i = line2.find(".")
            
            if separator_i == -1 or comma_i == -1:
                fill_outline = ("white","black")
                
            else :
                fill = line2[0:comma_i]
                outline = line2[comma_i+1:end_i]
                fill_outline = color_check(fill,outline)[0:2]
                
        except :
            fill_outline = ("white","black")
            
        line_no += 1
        try :
            line = line1[1:separator_i-1].split("),(")
            polygon_xy2 = []
            for xy in line :
                x,y = float(xy.split(",")[0]) , float(xy.split(",")[1])
                if not coord_check(x, y,polygon_xy2)[0]:
                    print(f"Point{x},{y} invalid, {coord_check(x, y,polygon_xy2)[1]}, line {line_no} is ommited.")
                    polygon_xy2 = []
                    break
                if line[-1] == xy :
                    if not coord_check(polygon_xy2[0][0],polygon_xy2[0][1],polygon_xy2[1:]+[(x,y)])[0] :
                        print(f"Point{x},{y} invalid, line {line_no} is ommited.")
                        polygon_xy2 = []
                        break
                polygon_xy2.append((x,y))
        except :
            print(f"Error reading line {line_no},this line is ommited.")
            polygon_xy2 = []
        if polygon_xy2 :
            poly_dict[len(poly_dict)+1] = polygon_xy2
            color_dict[len(poly_dict)] = (fill_outline[0],fill_outline[1])
    draw()           

def draw():
    global poly_dict, color_dict,test
    window = turtle.Screen()
    turtle.TurtleScreen._RUNNING=True
    t = turtle.Turtle()
    window.setup(width=0.5,height=1.0,startx=-0,starty=-0)
    if window.window_height() >= window.window_width():
        newHeight = window.window_width()
        newWidth = window.window_width()
    else :
        newHeight = window.window_height()
        newWidth = window.window_height()
    window.setup(width=newWidth,height=newHeight,startx=-1,starty=None)

    rootwindow = window.getcanvas().winfo_toplevel()
    rootwindow.call('wm', 'attributes', '.', '-topmost', '1')
    rootwindow.call('wm', 'attributes', '.', '-topmost', '0')
    window.title("Simple Polygon Math Tool. Close this window to continue program.")  # Set the window title
    window.screensize(0.9*newWidth,0.9*newHeight)

    list_xy=[]
    for no in poly_dict:
        list_xy += poly_dict[no]
    X_max, Y_max, X_min, Y_min = border(list_xy)[0],border(list_xy)[1],border(list_xy)[2],border(list_xy)[3]
    if X_max >= Y_max :
        XY_max = int(X_max)+1
    else :
        XY_max = int(Y_max)+1
    if X_min <= Y_min :
        XY_min = int(X_min)-2
    else :
        XY_min = int(Y_min)-2
    window.setworldcoordinates(XY_min,XY_min,XY_max,XY_max)

    t.speed(0)
    for no1 in poly_dict :

        t.hideturtle()
        t.pu()
        t.pencolor(color_dict[no1][1])
        t.fillcolor(color_dict[no1][0])
        t.goto(poly_dict[no1][0])
        t.pd()
        t.begin_fill()
        
        for xy in range(1,len(poly_dict[no1])):
            t.goto(poly_dict[no1][xy])
        t.goto(poly_dict[no1][0])
        t.end_fill()
    if len(poly_dict) == 1 :
        s,verb = "","is"
    else:
        s,verb = "s","are"
    print(f"Polygon{s} {verb} drawn on the other window. Close that window when you want to continue the program.")
    turtle.done()
    

#Menu
def menu():
    global poly_dict
    
    while True :
        print(f"========================================\nWhat do you want to do with the polygon?")
        print(f" 1 | Modify\n 2 | Create multiple copies\n 3 | Analyze\n 4 | Create new polygon\n 5 | Save to file\n 6 | Exit Program")
        
        while True :
            try :
                menu = int(input("Enter one of the value above : "))
                if menu in range(1,7):
                    break
                else :
                    continue
            except ValueError :
                print("Invalid")
                
        if menu == 4 :
            input_poly()
            print("Done")
            continue
        elif menu == 5 :
            save_file()
            continue
        elif menu == 6 :
            print("Thank you for using this beta program!")
            print("Have a Nice Day :)")
            break
            
        n = poly_dict_print()
        polygon_xy = poly_dict[n]
        
        while menu == 1 :
            
            print(f"================\nWhat to modify ?\n 1 | Edit Vertex\n 2 | Move\n 3 | Rotate\n 4 | Scale\n 5 | Back to main menu")
            while True :
                try:
                    modify = int(input("Enter one of the value above : "))
                    while not modify in range(1,6):
                        modify = int(input("Invalid! Re-enter one of the value above : "))
                    break
                except :
                    print("Invalid input")
                    continue

            if modify == 5 :
                break
            while modify == 1 :
                while True :
                    try :
                        back = False
                        edit_del = input(f"Enter vertex no followed by function (Ex. '4d' means delete vertex 4 or '1e' means edit vertex 1)\nor enter 'e' to exit : ")
                        if edit_del == "e" :
                            back = True
                        task = edit_del[-1]
                        vertex_no = int(edit_del[-2::-1])
                        break
                    except :
                        print("Invalid input")
                        continue
                if back :
                    break
                
                if task == "d" :
                    if len(polygon_xy) == 3 :
                        print("Cannot delete because vertex will be less than 3!")
                        continue
                    elif vertex_no in range(1,len(polygon_xy)+1) :
                        new_polygon = polygon_xy.copy()
                        new_polygon.pop(vertex_no-1)
                        for a in range(len(new_polygon)-1) :
                            if coord_check(new_polygon[a+1][0],new_polygon[a+1][1],new_polygon[0:a])[0]:
                                change = True
                                if a == len(new_polygon)-1 and not coord_check(new_polygon[0][0],new_polygon[0][1],new_polygon[1:])[0]:
                                    change = False
                                    break
                            else :
                                change = False
                                break
                        if change :       
                            polygon_xy.pop(vertex_no-1)
                            poly_dict[n] = polygon_xy
                            print("Success")
                            draw()
                        else :
                            print("Fail, invalid polygon is formed")
                        break
                    else :
                        print("Value out of range!")
                        continue
                elif task == "e":
                    if vertex_no in range(1,len(polygon_xy)+1) :
                        while True :
                            try :
                                edit_x = float(input(f"Enter new x coordinate of vertex {vertex_no} : "))
                                edit_y = float(input(f"Enter new y coordinate of vertex {vertex_no} : "))
                                break
                            except :
                                print("Invalid input")
                                continue
                            
                        new_polygon = polygon_xy.copy()
                        new_polygon[vertex_no-1] = (edit_x,edit_y)
                        for a in range(len(new_polygon)-1) :
                            if coord_check(new_polygon[a+1][0],new_polygon[a+1][1],new_polygon[0:a])[0]:
                                change = True
                                if a == len(new_polygon)-1 and not coord_check(new_polygon[0][0],new_polygon[0][1],new_polygon[1:])[0]:
                                    change = False
                                    break
                            else :
                                change = False
                                break
                        if change :       
                            polygon_xy[vertex_no-1] = (edit_x,edit_y)
                            poly_dict[n] = polygon_xy
                            print("Success")
                            draw()
                        else :
                            print("Fail, intersection or same coordinate or straight line between 2 vertexes is found!")
                            break
                    else :
                        print("Value out of range!")
                        continue
                break

            
            while modify == 2 :
                while True :
                    try :
                        x = float(input("Enter value to move on x axis : "))
                        y = float(input("Enter value to move on y axis : "))
                        break
                    except :
                        print("Invalid input")
                        continue
                move(polygon_xy,x,y)
                poly_dict[n] = polygon_xy
                print("Success")
                draw()
                break
            
            while modify == 3 :
                while True :
                    try :
                        teta = float(input("Enter rotation angle in degrees : "))
                        rotate_point = input("Enter point/origin of rotation in 'x,y' or enter 'c' for centroid : ")
                        if rotate_point == "c" :
                            x = centroid(polygon_xy)[0]
                            y = centroid(polygon_xy)[1]
                        else :
                            x = float(rotate_point.split(",")[0])
                            y = float(rotate_point.split(",")[1])
                        break
                    except :
                        print("Invalid input")
                        continue
                rotate(polygon_xy,teta,x,y)
                poly_dict[n] = polygon_xy
                print("Success")
                draw()
                break
            
            while modify == 4 :
                while True :
                    try :
                        k = float(input("Enter scaling factor : "))
                        factor_origin = input("Enter origin in 'x,y' or 'c' for centroid or 'o' for origin : ")
                        if factor_origin == "c" :
                            x , y = centroid(polygon_xy)[0], centroid(polygon_xy)[1]
                        elif factor_origin == "o" :
                            x , y = 0 , 0
                        else :
                            x = float(factor_origin.split(",")[0])
                            y = float(factor_origin.split(",")[1])
                        break
                    except :
                        print("Invalid input")
                        continue
                scale(polygon_xy,k,x,y)
                poly_dict[n] = polygon_xy
                print("Success")
                draw()
                break
            #end of menu 1
            
        while menu == 2 :
            while True :
                try :
                    copy = input(f"Enter the tranformation step for the copies separated with spaces.\nExample : 'scale rotate'\nAvailable transformation : scale, rotate, move.\nNote : input order affects result.\n")
                    no_copy = int(input("Enter number of copies : "))
                    copy_no = n
                    copy_step = copy.split(" ")
                    poly_to_copy = poly_dict[copy_no].copy()
                    break
                except :
                    print("Invalid input")
                    continue

            for no_ in range(no_copy) :
                for step in copy_step :
                    if step == "scale" :
                        if no_ < 1 :
                            while True :
                                try :
                                    k = float(input("Enter scaling factor : "))
                                    factor_origin = input("Enter origin in 'x,y' or 'c' for centroid or 'o' for origin : ")
                                    if factor_origin == "c" :
                                        x , y = centroid(poly_to_copy)[0], centroid(poly_to_copy)[1]
                                    elif factor_origin == "o" :
                                        x , y = 0 , 0
                                    else :
                                        x = float(factor_origin.split(",")[0])
                                        y = float(factor_origin.split(",")[1])
                                    break
                                except :
                                    print("Invalid input")
                                    continue
                        poly_to_copy = scale(poly_to_copy,k,x,y)
                            
                    elif step == "rotate":
                        if no_ < 1 :
                            while True :
                                try :
                                    teta = float(input("Enter rotation angle in degrees : "))
                                    rotate_point = input("Enter point/origin of rotation in 'x,y' or enter 'c' for centroid : ")
                                    if rotate_point == "c" :
                                        x_step_rotate = centroid(poly_to_copy)[0]
                                        y_step_rotate = centroid(poly_to_copy)[1]
                                    else :
                                        x_step_rotate = float(rotate_point.split(",")[0])
                                        y_step_rotate = float(rotate_point.split(",")[1])
                                    break
                    
                                except :
                                    print("Invalid input")
                                    continue
                        poly_to_copy = rotate(poly_to_copy,teta,x_step_rotate,y_step_rotate)
                        
                    elif step == "move":
                        if no_ < 1 :
                            x_step_move = float(input("Enter value to move on x axis : "))
                            y_step_move = float(input("Enter value to move on y axis : "))
                        
                        poly_to_copy = move(poly_to_copy,x_step_move,y_step_move)
                poly_dict[len(poly_dict)+1] = poly_to_copy.copy()
                color_dict[len(poly_dict)]= color_dict[copy_no]
            print("Done")
            draw()
            break
            #end of menu 2

        while menu == 3 :
            analyze_no = n
            
            poly_analyze = poly_dict[analyze_no].copy()
            
            print("====================")
            while True :
                try :
                    analyze = int(input(f" 1 | Calculate Area \n 2 | Calculate perimeter \n 3 | Check a point if it is inside or outside the polygon\n 4 | Back to Main Menu\nEnter a value : "))
                    if analyze not  in range(1,5):
                        continue
                    break
                except :
                    print("Invalid input")
                    continue
            if analyze == 5:
                break
            elif analyze == 1 :
                print(f"The area of polygon {analyze_no} is {area(poly_analyze):.2f}")
            elif analyze == 2 :
                print(f"The perimeter of polygon {analyze_no} is {perimeter(poly_analyze):.2f}")
            elif analyze == 3 :
                while True :
                    try :
                        point_check = input(f"Enter a point to check in polygon {analyze_no} in format 'x,y' : ")
                        x_check = float(point_check.split(",")[0])
                        y_check = float(point_check.split(",")[1])
                        break
                    except :
                        print("Invalid input")
                        continue
                print(check_point(poly_analyze,x_check,y_check))
            break
                
#Main Program
        
print("POLYGON MATH TOOL")
poly_dict={}
color_dict={}
input_poly()
menu()
        
        
            
            
        
            
        
        
            
    




