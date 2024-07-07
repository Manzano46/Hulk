input1 = "let number = 42 in let text = \"The meaning of life is\" in print(text @ number);"
  
input2 = "let a = 5 in { print(a+b); print(b*c); print(c/a); }"

input3 = '''
    let a = 0 in {
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
        );'''

input7 = '''
    function tan(x: Number): Number => sin(x) / cos(x);
    type Point {
        x = 0;
        y = 0;

        getX() => self.x;
        getY() => self.y;

        setX(x) => self.x := x;
        setY(y) => self.y := y;
    }
    type PolarPoint(phi, rho) inherits Point(rho * sin(phi), rho * cos(phi)) {
            strin = "ijbhuh";       
        }
    function gcd(a, b) => while (a > 0)
        let m = a % b in {
            b := a;
            a := m;
        };
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
                      
        retornaphi() => self.phi;            
    }
    x + 3;
'''


input9 =  '''
    function tan(x: Number): Number => sin(x) / cos(x);
    function gcd(a, b) => while (a > 0)
        let m = a % b in {
            b := a;
            a := m;
        };
    print(gcd(4,5));
'''

input10 = '''
    let a = 1 in {
        a+2;
    };
    '''

test_cases = [input1, input2, input3, input4, input5, input6, input7, input8, input9, input10]
# function tan(x: Number): Number => sin(x) / cos(x);


# function tan(x: Number: Number => sin(x / cos(x;
