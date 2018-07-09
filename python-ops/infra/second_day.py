'''
Class OOPs

function inside a class is calle method
self is the instance of the object that is created

'''

'''
class Testme:
    
    def vol_sphere(self, r):
        v = (4/3.0) * 3.14 * r **3
        return v


a = Testme()

print a.vol_sphere(45)
'''
'''
class Employee:

    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def PrintMe(self):
        print "My name is {}".format(self.name)

a = Employee('Amit', 25, 'amit@gmail.com')

a.PrintMe()
'''


'''
Abstract class
class abc:
    pass
'''

'''
class Parent(object):

    def __init__(self):
        print 'Parent constructor'

    def Function1(self):
        print 'Parent function'

class Child(Parent):

    def __init__(self):
        print 'Child Constructor'

    def Function2(self):
        print 'Child function'

    def Function1(self):
        print 'Same as Parent function'
        super(Child, self).Function1()


a = Child()
a.Function2()
a.Function1()
'''

'''
static method
class method
decorators
operator overloading

'''

with open('test-1.txt', 'r') as a:
    #print a.readline()
    #print a.next()
    b = 0
    for i in a:
        b+=1
        if b==3:
            with open('test.txt', 'w') as wt:
                      wt.write(i)
            







