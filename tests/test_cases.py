input0 = '''
    type Point {
        x  = 0;
        y  = "feo";

        getX() => self.x;
        getY() => self.y;
        
        setX(x: Number) : Number => self.x := x;
        setY(y: String) : String => self.y := y;
    }

    let pt = new Point() in {
        print(pt.getX());
        pt.setX(5);
        print(pt.getX());
    } 
'''
input1 = "let number = 42 in let text = \"The meaning of life is\" in print(text @ number);"
  
input2 = "let a = 5, b = 1, c = 10 in { print(a+b); print(b*c); b + c/a; }"

input3 = '''
    let a : String = 0 in {
        print(a);
        a := 1;
        print(a);
    }'''

input4 = '''
    function cot(x) => 1 / tan(x);
    function tan(x) => sin(x) / cos(x);
    print(tan(PI) ** 2 + cot(PI) ** 2);'''

input5 = "let a = 42, b=10, c=20 in if (a % 2 == 0) print(\"Even\") else print(\"odd\");"

input6 = '''
    let a = 42, mod = a % 3 in
        print(
            if (mod == 0) "Magic"
            elif (mod % 3 == 1) "Woke"
            else "Dumb"
        );
        '''

input7 = '''
    
    function tan(x: Number): Number => sin(x) / cos(x);

    type Point inherits PolarPoint {
        x = 0;
        y = 0;

        getX() => self.x;
        getY() => self.y;

        setX(x) => self.x := x;
        setY(y) => self.y := y;
    }

    type PolarPoint inherits Point {
        rho() => sqrt(self.getX() ^ 2 + self.getY() ^ 2);
    }

    type Person(first, last) {
        firstname = first;
        lastname = last;

        name() => self.firstname @@ self.lastname;
    }

    function gcd(a, b) => while (a > 0)
        let m = a % b in {
            b := a;
            a := m;
        };

    type Knight inherits Person {
        name() => "Sir" @@ base();
    }

    let a = 10 in while (a >= 0) {
        print(a);
        for (x in range(0, 10)) print(x);
        let pt = new Point() in {
            print("x: " @ pt.getX() @ "; y: " @ pt.getY());
            let x = new Superman() in
                print(
                    if (x is Bird) "It's bird!"
                    elif (x is Plane) "It's a plane!"
                    else "No, it's Superman!"
                );
            let x : A = if (rand() < 0.5) new B() else new C() in
                if (x is B)
                    let y : B = x as B in {
                        x + 7;
                    }
                else {
                    x @@ 3;
                };
              
            };
        a := a - 1;
    }'''

input8 =  '''
    type PolarPoint(phi, rho) {
        x = phi;
        y = rho;
        strin = "ijbhuh"; 
                      
        retornaphi() => self.x;            
    }
    1;
'''


input9 =  '''
    function tan(x: Number): Number => sin(x) / cos(x);
    function gcd(a, b) => while (a > 0)
        let m = a % b in {
            a := b;
            b := m;
            a;
        };
    print(gcd(4,5));
'''

input10 = '''
    let a = 1 in {
        a+2;
    };
    '''
    
input11 = '''
    print(\"HOLA MUNDO\")
'''

input12 = '''
    type Point (a : Number, b : Number){      
        x = a;
        y = b;

        getX() => self.x;
        getY() => self.y;
    }
    type PolarPoint(x : Number,y : Number,z : Number) inherits Point(x+y, y+z){
        a = x;
        
        rho() => self.a;
        
    }
    let pt = new PolarPoint() in {
        print(pt.rho());
        print(pt.getX());
    } 
'''

input13 = '''
    let a = 10 in while (a >= 0) {
        print(a);
        a := a - 1;
    }
'''
input14 = '''
    function fib(n) {
        if (n < 2) 1 else fib(n-1) + fib(n-2);
    }
    let x = fib(5) in print(x);
'''

input15 = '''
    let iterable = range(0, 10) in
        while (iterable.next())
            let x = iterable.current() in
                print(x);
'''

input16 = '''
    type Est {
        nota = 2;

        calc(self) => self.nota;
    }

    let x: Object = 5 in x:= new Est();
'''


test_cases = [
    input0,
    input1, input2, input3, 
    input4,input5, input6, 
    input7, input8, 
    input9, input10, 
    input11, input12, input13,
    input14 ,input15,input16
]
# function tan(x: Number): Number => sin(x) / cos(x);



# function tan(x: Number: Number => sin(x / cos(x;
