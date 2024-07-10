input0 = '''
    function tan(x: Number): Number => sin(x) / cos(x);
function cot(x) => 1 / tan(x);
function operate(x, y) {
    print(x + y);
    print(x - y);
    print(x * y);
    print(x / y);
}
function fib(n) => if (n == 0 | n == 1) 1 else fib(n-1) + fib(n-2);
function fact(x) => let f = 1 in for (i in range(1, x+1)) f := f * i;
function gcd(a, b) => while (a > 0)
        let m = a % b in {
            b := a;
            a := m;
        };
protocol Hashable {
    hash(): Number;
}
protocol Equatable extends Hashable {
    equals(other: Object): Boolean;
}

type Point(x,y) {
    x = x;
    y = y;

    getX() => self.x;
    getY() => self.y;

    setX(x) => self.x := x;
    setY(y) => self.y := y;

    hash() => 7;
}
type PolarPoint(phi, rho) inherits Point(rho * sin(phi), rho * cos(phi)) {
    rho() => sqrt(self.getX() ^ 2 + self.getY() ^ 2);
}
type Knight (name,last) inherits Person (name,last) {
    name() => "Sir" @@ base();
}
type Person(firstname: String, lastname:String) {
    firstname = firstname;
    lastname = lastname;

    name() => self.firstname @@ self.lastname;
    hash() : Number {
        5;
    }
}
type Superman {
}
type Bird {
}
type Plane {
}
type A {
    hello() => print("A");
}

type B inherits A {
    hello() => print("B");
}

type C inherits A {
    hello() => print("C");
}

{
    42;
    print(42);
    print((((1 + 2) ^ 3) * 4) / 5);
    print("Hello World");
    print("The message is \\"Hello World\\"");
    print("The meaning of life is " @ 42);
    print(sin(2 * PI) ^ 2 + cos(3 * PI / log(64)));
    {
        print(42);
        print(sin(PI/2));
        print("Hello World");
    }


    print(tan(PI) ** 2 + cot(PI) ** 2);

    let msg = "Hello World" in print(msg);
    let number = 42, text = "The meaning of life is" in
        print(text @ number);
    let number = 42 in
        let text = "The meaning of life is" in
            print(text @ number);
    let number = 42 in (
        let text = "The meaning of life is" in (
                print(text @ number)
            )
        );
    let a = 6, b = a * 7 in print(b);
    let a = 6 in
        let b = a * 7 in
            print(b);
    let a = 5, b = 10, c = 20 in {
        print(a+b);
        print(b*c);
        print(c/a);
    };
    let a = (let b = 6 in b * 7) in print(a);
    print(let b = 6 in b * 7);
    let a = 20 in {
        let a = 42 in print(a);
        print(a);
    };
    let a = 7, a = 7 * 6 in print(a);
    let a = 7 in
        let a = 7 * 6 in
            print(a);
    let a = 0 in {
        print(a);
        a := 1;
        print(a);
    };
    let a = 0 in
        let b = a := 1 in {
            print(a);
            print(b);
        };
    let a = 42 in if (a % 2 == 0) print("Even") else print("odd");
    let a = 42 in print(if (a % 2 == 0) "even" else "odd");
    let a = 42 in
        if (a % 2 == 0) {
            print(a);
            print("Even");
        }
        else print("Odd");
    let a = 42, mod = a % 3 in 
        print(
            if (mod == 0) "Magic"
            elif (mod % 3 == 1) "Woke"
            else "Dumb"
        );
    let a = 10 in while (a >= 0) {
        print(a);
        a := a - 1;
    };
    
    for (x in range(0, 10)) print(x);
    let iterable = range(0, 10) in
        while (iterable.next())
            let x = iterable.current() in
                print(x);

    let pt = new Point(3,4) in 
        print("x: " @ pt.getX() @ "; y: " @ pt.getY());
    let pt = new Point(3,4) in
        print("x: " @ pt.getX() @ "; y: " @ pt.getY());
    let pt = new PolarPoint(3,4) in
        print("rho: " @ pt.rho());

    let p = new Knight("Phil", "Collins") in
        print(p.name());
    let p: Person = new Knight("Phil", "Collins") in print(p.name());
    let x: Number = 42 in print(x);

    let x = new Superman() in
        print(
            if (x is Bird) "It's bird!"
            elif (x is Plane) "It's a plane!"
            else "No, it's Superman!"
        );
    let x = 42 in print(x);
    let total = ({ print("Total"); 5; }) + 6 in print(total);
    let x : A = if (rand() < 0.5) new B() else new C() in
        if (x is B)
            let y : B = x as B in {
                y.hello();
            }
        else {
            print("x cannot be downcasted to B");
        };

    let numbers = [1,2,3,4,5,6,7,8,9] in
        for (x in numbers)
            print(x);
    let numbers = [1,2,3,4,5,6,7,8,9] in print(numbers[7]);
    let squares = [x^2 || x in range(1,10)] in print(squares); 
    let squares = [x^2 || x in range(1,10)] in for (x in squares) print(x);
    let x : Hashable = new Person("Ro","Fu") in print(x.hash());
    let x : Hashable = new Point(0,0) in print(x.hash()); 
}
'''
# input1 = "let number = 42 in let text = \"The meaning of life is\" in print(text @ number);"
  
# input2 = '''let a = 5, b = 1, c = 10 in { 
#     print(a+b); 
#     print(b*c); 
#     b + c/a; 
#     let numbers = [1,2,3,4,5,6,7,8,9] in
#     for (x in numbers)
#         print(x);
#     let numbers = [1,2,3,4,5,6,7,8,9] in print(numbers[7]);
#     }'''   

# input3 = '''
#     let a : String = 0 in {
#         print(a);
#         a := 1;
#         let iterable = range(0, 10) in
#         while (iterable.next())
#             let x = iterable.current() in {
#                 x+1;
#             };
#         print(a);
#     }'''

# input4 = '''
#     function cot(x) => 1 / tan(x);
#     function tan(x) => sin(x) / cos(x);
#     print(tan(PI) ** 2 + cot(PI) ** 2);'''

# input5 = "let a = 42, b=10, c=20 in if (a % 2 == 0) print(\"Even\") else print(\"odd\");"

# input6 = '''
#     let a = 42, mod = a % 3 in
#         print(
#             if (mod == 0) "Magic"
#             elif (mod % 3 == 1) "Woke"
#             else "Dumb"
#         );
#         '''

# input7 = '''
    
#     function tan(x: Number): Number => sin(x) / cos(x);

#     type Point inherits PolarPoint {
#         x = 0;
#         y = 0;

#         getX() => self.x;
#         getY() => self.y;

#         setX(x) => self.x := x;
#         setY(y) => self.y := y;
#     }

#     type PolarPoint inherits Point {
#         rho() => sqrt(self.getX() ^ 2 + self.getY() ^ 2);
#     }

#     type Person(first, last) {
#         firstname = first;
#         lastname = last;

#         name() => self.firstname @@ self.lastname;
#     }

#     function gcd(a, b) => while (a > 0)
#         let m = a % b in {
#             b := a;
#             a := m;
#         };

#     type Knight inherits Person {
#         name() => "Sir" @@ base();
#     }

#     let a = 10 in while (a >= 0) {
#         print(a);
#         for (x in range(0, 10)) print(x);
#         let pt = new Point() in {
#             print("x: " @ pt.getX() @ "; y: " @ pt.getY());
#             let x = new Superman() in
#                 print(
#                     if (x is Bird) "It's bird!"
#                     elif (x is Plane) "It's a plane!"
#                     else "No, it's Superman!"
#                 );
#             let x : A = if (rand() < 0.5) new B() else new C() in
#                 if (x is B)
#                     let y : B = x as B in {
#                         x + 7;
#                     }
#                 else {
#                     x @@ 3;
#                 };
              
#             };
#         a := a - 1;
#     }'''

# input8 =  '''
#     type PolarPoint(phi, rho) {
#         x = phi;
#         y = rho;
#         strin = "ijbhuh"; 
                      
#         retornaphi() => self.x;            
#     }
#     1;
# '''


# input9 =  '''
#     function tan(x: Number): Number => sin(x) / cos(x);
#     function gcd(a, b) => while (a > 0)
#         let m = a % b in {
#             a := b;
#             b := m;
#             a;
#         };
#     print(gcd(4,5));
# '''

# input10 = '''
#     let a = 1 in {
#         a+2;
#     };
#     '''
    
# input11 = '''
#     print(\"HOLA MUNDO\")
# '''

# input12 = '''
#     type Point (a : Number, b : Number){      
#         x = a;
#         y = b;

#         getX() => self.x;
#         getY() => self.y;
#     }
#     type PolarPoint(x : Number,y : Number,z : Number) inherits Point(x+y, y+z){
#         a = x;
        
#         rho() => self.a;
        
#     }
#     let pt = new PolarPoint(1,2,3) in {
#         print(pt.rho());
#         print(pt.getX());
#     } 
# '''

# input13 = '''
#     let a = 10 in while (a >= 0) {
#         print(a);
#         a := a - 1;
#     }
# '''
# input14 = '''
#     function fib(n) {
#         if (n < 2) 1 else fib(n-1) + fib(n-2);
#     }
#     let x = fib(5) in print(x);
# '''

# input15 = '''
#     let iterable = range(0, 10) in
#         while (iterable.next())
#             let x = iterable.current() in
#                 print(x);
# '''
# input16 = '''
#     type Point (a : Number, b : Number){      
#         x = a;
#         y = b;

#         getX() => self.x;
#         getY() => self.y;
#     }
#     type PolarPoint(x : Number,y : Number,z : Number) inherits Point(x+y, y+z){
#         a = x;
        
#         rho() => self.a;
        
#     }
#     let pt = new PolarPoint(3,4,5) in {
#         print(pt.rho());
#         print(pt.getX());
#     } 
# '''

# input16 = '''
#     type Est {
#         nota = 2;

#         calc(self) => self.nota;
#     }

#     let x: Object = 5 in x:= new Est();
# '''


test_cases = [input0]
#     input1, input2, input3, 
#     input4,input5, input6, 
#     input7, input8, 
#     input9, input10, 
#     input11, input12, input13,
#     input14 ,input15,input16
# ]
# # function tan(x: Number): Number => sin(x) / cos(x);



# # function tan(x: Number: Number => sin(x / cos(x;
