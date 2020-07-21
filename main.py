statements = []
symbols = ['!', '&', '|', '>', '=', '(', ')']

def precedence(op): 
      
    if op == '&' or op == '|': 
        return 1
    if op == '>' or op == '=': 
        return 2
    return 0


def simplify(o1, o2, op):
    if op == '>':        
        return '!'+o1+'|'+o2
    elif op == '=':
        return '(!'+o1+'|'+o2+')&'+'(!'+o2+'|'+o1+')'
    elif op == '!':
        return '!'+o1
    else:
        return o1+op+o2
    

def double_negation(prop):
    sol = ''
    i = 0
    while i < len(prop) - 1:
        if prop[i] == '!' and prop[i+1] == '!':
            i = i + 1
        else:
            sol = sol + prop[i]
        i = i + 1
    return sol

def break_paranthesis(prop):
    for i in range(len(prop)):
        if prop[i] == '!':
            i = i + 1
            o1 = o2 = op = ''
            if prop[i] == '(':
                i = i + 1
                s = i
                ctr = 1
                while ctr != 0:
                    if prop[i] == '(':
                        ctr = ctr + 1
                    elif prop[i] == ')':
                        ctr = ctr - 1
                    i = i + 1
                print(prop[s:i-s])
                #values.append('(')
                #parse(prop[s:i-s])
            else:
                values.append("!"+prop[i])
        

def parse(prop):
    op = []
    values = []
    i = 0
    while i < len(prop):
    
        if prop[i] not in symbols:
            values.append(prop[i])
        elif prop[i] == '(' or prop[i] == '!':
            op.append(prop[i])
            
        elif prop[i] == ')':
            
            while len(op) != 0 and op[-1] != '(':
                        
                val2 = values.pop() 
                val1 = values.pop() 
                ops = op.pop() 
                
                values.append(simplify(val1, val2, ops))  
            op.pop()
        
        else:
            while (len(op) != 0 and
                precedence(op[-1]) >= precedence(prop[i])): 
                          
                val2 = values.pop() 
                val1 = values.pop() 
                ops = op.pop() 
                  
                values.append(simplify(val1, val2, ops)) 
              
            # Push current token to 'ops'. 
            op.append(prop[i])
        

        i = i + 1
    while len(op) != 0:
        val2 = values.pop() 
        val1 = values.pop() 
        ops = op.pop() 
            
        values.append(simplify(val1, val2, ops))

    print('op: ',op)
    print('values: ',values)  



n = int(input())
m = int(input())
propostions = []
for i in range(n):
    print('i: ',i)
    temp = input()
    propostions.append(temp)
    parse(temp)
answer = input()


    