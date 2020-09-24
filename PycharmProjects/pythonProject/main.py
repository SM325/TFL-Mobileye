# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from hwltd.organization import HelloWorld
from worekers.person import Person, Phone, StreetAddress, PobAddress
from worekers.structure import Group, Worker, Engineer, SalesPerson
from hwltd.reports import get_avarge_salary, get_relational_salary, get_num_employees


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    try:
        phon1=Phone('0536478908')
        phon2=Phone('+972-29765438')
        phon3=Phone('0298387797')
        ad1=StreetAddress("con1", "city1", "str", 1)
        add2=PobAddress("con2", "cty2", 33)
        p1 = Person("p1", "p22", 1990, "ss@bae..hwltd.com")
        p1.addPhone([phon1 , phon2])
        p1.addAdd(ad1)
        p2 = Person("p2", "p22", 1990, "ss@baa.hwltd.com")
        p2.addPhone([phon3])
        p2.addAdd(ad1)
        p3 = Person("p33", "1", 1990, "ss@baa.hwltd.com")
        p3.addPhone([])
        p3.addAdd(add2)
        a=p2.address.theAddIs()
        print(f'p3name, {p3.firstName}')  # Press Ctrl+F8 to toggle the breakpoint.
        print(f'p2add, {p2.address.theAddIs()}')  # Press Ctrl+F8 to toggle the breakpoint.
        print(f'p3add, {p3.address.theAddIs()}')  # Press Ctrl+F8 to toggle the breakpoint.
        grp1 = Group("g1", "d1", None)
        grp2 = Group("g2", "d2", grp1)
        grp3 = Group("g3", "d3", grp2)
        pGrp1 = grp1.get_parents()
        pGrp2 = grp2.get_parents()
        pGrp3 = grp3.get_parents()

        print(f'g1 , {grp1.get_parents()}')  # Press Ctrl+F8 to toggle the breakpoint.
        print(f'g2 , {grp2.get_parents()[0].name}')  # Press Ctrl+F8 to toggle the breakpoint.
        print(f'g3 , {grp3.get_parents()[1].name}, {grp3.get_parents()[0].name}')  # Press Ctrl+F8 to toggle the breakpoint.
        w1 = Worker(p1, 200)
        w2 = Engineer(p2, 200, 200)
        w3 = SalesPerson(p3, 200, 2)
        grp1.workers = [w1]
        grp1.subGrp
        grp2.subGrp = [grp1]
        grp2.workers = [w2, w3]
        grp3.subGrp = [grp2, grp1]
        grp3.workers = [w1]
        worg1 = grp2.get_workers()
        grp3Workers = grp3.get_workers()
        print(f'g1w , {worg1[1].person.firstName}, {worg1[0].person.firstName}, {worg1[2].person.firstName}')  # Press Ctrl+F8 to toggle the breakpoint.
        print(f'g3w , {grp3Workers[1].person.firstName}, {grp3Workers[0].person.firstName}, {grp3Workers[2].person.firstName},{grp3Workers[3].person.firstName}, {grp3Workers[3].person.firstName}')  # Press Ctrl+F8 to toggle the breakpoint.
        #print(grp3Workers)

        ###p2

        hw = HelloWorld( r"C:\Users\sara leah\Downloads\prework-python-data.txt" )
        get_avarge_salary(hw.engGrp.subGrp[0])
        u1=get_relational_salary(hw.engGrp.subGrp[0].subGrp[1].workers[0])
        g=get_num_employees(hw.engGrp, 2)
        print(u1)
        print(len(hw.engGrp.subGrp[0].get_workers()))
    except Exception as e:
        print("incorrect val")




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
