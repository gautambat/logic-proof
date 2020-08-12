statements = []
symbols = ['!', '&', '|', '>', '=', '(', ')']

def to_prefix(prop):
    # print(prop)
    values = []
    ops = []
    i = 0
    while i < len(prop):

        if prop[i] not in symbols:
            values.append(prop[i])
            i += 1

        elif prop[i] == '&' or prop[i] == '|' or prop[i] == '=' or prop[i] == '>':
            ops.append(prop[i])
            i += 1

        elif prop[i] == '!':
            if prop[i+1] == '(':
                i += 2
                sub_str = ''
                count = 1
                while count != 0:
                    if prop[i] == '(':
                        count += 1
                    elif prop[i] == ')':
                        count -= 1
                    if count > 0:
                        sub_str += prop[i]
                    i += 1      
                values.append(['!', to_prefix(sub_str)])
            else:
                values.append(['!', prop[i+1]])
                i += 2

        elif prop[i] == '(':
            i += 1
            sub_str = ''
            count = 1
            while count != 0:
                if prop[i] == '(':
                    count += 1
                elif prop[i] == ')':
                    count -= 1
                if count > 0:
                    sub_str += prop[i]
                i += 1
            values.append(to_prefix(sub_str))

    # print(values)
    # print(ops)
    while ops:
        operand1 = values.pop()
        operand2 = values.pop()
        op = ops.pop()
        values.append([op, operand2, operand1])

    if len(values) == 1:
        return values[0]
    return values

# def to_prefix(prop):
#     op = []
#     values = []
#     i = 0
#     while i < len(prop):
    
#         if prop[i] not in symbols:
#             values.append(prop[i])
#         elif prop[i] == '(' or prop[i] == '!':
#             op.append(prop[i])
            
#         elif prop[i] == ')':
            
#             while len(op) != 0 and op[-1] != '(':
                        
#                 val2 = values.pop() 
#                 val1 = values.pop() 
#                 ops = op.pop() 
                
#                 values.append(simplify(val1, val2, ops))  
#             op.pop()
        
#         else:
#             while (len(op) != 0 and
#                 precedence(op[-1]) >= precedence(prop[i])): 
                          
#                 val2 = values.pop() 
#                 val1 = values.pop() 
#                 ops = op.pop() 
                  
#                 values.append(simplify(val1, val2, ops)) 
              
#             # Push current token to 'ops'. 
#             op.append(prop[i])
        

#         i = i + 1
#     while len(op) != 0:
#         val2 = values.pop() 
#         val1 = values.pop() 
#         ops = op.pop() 
            
#         values.append(simplify(val1, val2, ops))

#     print('op: ',op)
#     print('values: ',values)  

def precedence(op): 
      
    if op == '&' or op == '|': 
        return 1
    if op == '>' or op == '=': 
        return 2
    return 0


def simplify(prop):
    res = []
    for i in range(len(prop)):
        if i == 0:
            continue
        if len(prop[i]) > 1:
            prop[i] = simplify(prop[i])

    op = prop[0]
    if len(prop) == 3:
        if op == '=':
            res.append('&')
            
            temp = []
            temp.append('|')
            temp.append(['!', prop[1]])
            temp.append(prop[2])
            res.append(temp)

            temp = []
            temp.append('|')
            temp.append(['!', prop[2]])
            temp.append(prop[1])
            res.append(temp)
        
        elif op == '>':
            res.append('|')
            res.append(['!', prop[1]])
            res.append(prop[2])
        
        else:
            res = prop
    else:
        res = prop
    
    return res

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
    res = []
    for i in range(len(prop)):
        if i == 0:
            continue
        if len(prop[i]) > 1:
            prop[i] = break_paranthesis(prop[i])
    op = prop[0]
    if op == '!' and len(prop[1]) > 1:
        if prop[1][0] == '!':
            return prop[1][1]
        elif prop[1][0] == '|':
            res.append('&')
            res.append(['!', prop[1][1]])
            res.append(['!', prop[1][2]])
        elif prop[1][0] == '&':
            res.append('|')
            res.append(['!', prop[1][1]])
            res.append(['!', prop[1][2]])
    else:
        res = prop   
    
    return res

def distribute(prop):
    ctr = 0
    if prop[0] == '|':
        for i in range(1,3):
            if len(prop[i]) > 1 and prop[i][0] == '&':
                ctr = 1
    else:
        return prop
    if ctr == 0:
        return prop

    res = []
    res.append('&')
    if prop[1][0] == '&' and prop[2][0] == '&':
        res.append(distribute(['|', prop[1][1], prop[2][1]]))
        temp = res.pop()
        res.append(distribute(['&', temp, ['|', prop[1][1], prop[2][2]]]))
        temp = res.pop()
        res.append(distribute(['&', temp, ['|', prop[1][2], prop[2][1]]]))
        res.append(distribute(['|', prop[1][2], prop[2][2]]))
    
    elif prop[1][0] == '&' and prop[2][0] != '&':
       res.append(distribute(['|', prop[1][1], prop[2]]))
       res.append(distribute(['|', prop[1][2], prop[2]]))

    elif prop[2][0] == '&' and prop[1][0] != '&':
       res.append(distribute(['|', prop[1], prop[2][1]]))
       res.append(distribute(['|', prop[1], prop[2][2]]))

    return res

def to_infix(prop):
    
    if len(prop) == 3:
        op = prop[0]
        o1 = prop[1]
        o2 = prop[2]
        if len(o1) > 1:
            o1 = '('+to_infix(o1)+')'
        
        if len(o2) > 1:
            o2 = '('+to_infix(o2)+')'
        
        return o1+op+o2
    
    elif len(prop) == 2:
        op = prop[0]
        o1 = prop[1]
        if len(o1) == 3:
            o1 = '('+to_infix(o1)+')'
        elif len(o1) == 2:
            return o1[1]
        return op+o1
    else:
        return prop

def simplification(props):
    while 1:
        ctr = 0
        temp = []
        for prop in props:
            if prop[0] == '&':
                ctr = 1
                temp = prop
                break
        if ctr == 0:
            break
        props.append(temp[1])
        props.append(temp[2])
        props.remove(temp)
    
    return props

def add_or(lits):
    if len(lits)==1:
        return lits[0]
    while 1:
        if len(lits)==1 and lits[0][0]=='|':
            return lits[0]
        a_lit = lits.pop(0)
        b_lit = lits.pop(0)
        lits.append(['|',a_lit,b_lit])

def break_or(props):
    while 1:
        ctr = 0
        temp = []
        for prop in props:
            if prop[0] == '|':
                ctr = 1
                temp = prop
                break
        if ctr == 0:
            break
        props.append(temp[1])
        props.append(temp[2])
        props.remove(temp)
    
    return props


def resolvable(prop, ps):
    #print('p ', prop, ' ',ps)
    prop_lit = break_or([prop])
    #print('-----')
    #print(prop_lit)
    #print('-----')
    #print(ps)
    ps_lit = break_or([ps])
    #print('ps_lit: ',ps_lit)
    #print(ps_lit)
    for lit in prop_lit:
        #print('prop_lit: ', lit)
        neg_lit = break_paranthesis(['!', lit])
        if neg_lit in ps_lit or neg_lit == ps_lit:
            #print('true')
            return True
    return False

def check(lit, props):
    if len(lit) == 2:
        inv_lit = [lit[1], lit[0]]
        for p in props:
            if len(p) == 3:
                #print(p)
                temp = break_or([p])
                if p == lit or p == inv_lit:
                    return False
        return True

def refutation_resolution(props, neg_conclusion):
    proof_steps = neg_conclusion
    

    while 1:
        pairs = []
        for ps in proof_steps:
            #print(ps)
            for prop in props:
                #print(prop)
                if prop != ps and resolvable(prop, ps):
                    pair = [prop, ps]
                    #print(pair, 'pair')
                    #print('statements: ',statements)
                    if pair not in statements:
                        #print('pair: ', pair)
                        pairs.append(pair)
        #print('pairs: ',pairs)

        if len(pairs) == 0:
            for prop1 in props:
                for prop2 in props:
                    if prop1 != prop2 and resolvable(prop1, prop2):
                        pair = [prop2, prop1]
                        if pair not in statements:
                            pairs.append(pair)

        if len(pairs) == 0:
            proof_steps.append('True Clause')
            return False, proof_steps
        
        
        all_deductions = []
        for pair in pairs:
            a_lit = break_or([pair[0]])
            b_lit = break_or([pair[1]])
            temp = []
            temp2 = []
            for lit in a_lit:
                neg_lit = break_paranthesis(['!', lit])
                if neg_lit in b_lit:
                    temp2.append(neg_lit)
                else:
                    temp.append(lit)
        
            for t in temp2:
                b_lit.remove(t)
            
            for lit in b_lit:
                if lit not in temp:
                    temp.append(lit)
            
            statements.append(pair)
            if len(temp) == 0:
                proof_steps.append('Empty Clause')
                return True, proof_steps
            
            #if check(temp, all_deductions):
            temp = add_or(temp)
            #print(temp)
            
            all_deductions.append(temp)

        # for p in proof_steps:
        #     print('p: ', p)

        for p in all_deductions:
            if break_paranthesis(['!', p]) in proof_steps:
                proof_steps.append(p)
                proof_steps.append('Empty Clause')
                return True, proof_steps
            if p not in proof_steps:
                proof_steps.append(p)
            
        
        
            
line = input()
x, y = line.split()
n = int(x)
m = int(y)
#m = int(input())
propostions = []
for i in range(n):
    #print('i: ',i)
    temp = input()
    propostions.append(to_prefix(temp))
temp = input()
conclusion = to_prefix(temp)
#print('------')
# for p in propostions:
#     print(p)
#print('------')
#print(conclusion)
#print('------')
cnf = []
for prop in propostions:
    temp = prop
    if len(prop) > 1:
    
        temp = simplify(temp)
        temp = break_paranthesis(temp)
        temp = distribute(temp)
        #print(temp)
    cnf.append(temp)
if len(conclusion) > 1:
    conclusion = simplify(conclusion)
    conclusion = break_paranthesis(conclusion)
    conclusion = distribute(conclusion)

neg_conclusion = [break_paranthesis(['!', conclusion])]
cnf.append(break_paranthesis(['!', conclusion]))
  
cnf = simplification(cnf)
# for c in cnf:
#     print(c)
#print('------')
ans, proof = refutation_resolution(cnf, neg_conclusion)
infix_proof = []
for i in range(len(cnf) - 1):
    temp = to_infix(cnf[i])
    infix_proof.append(temp)
    #print(temp)
for p in proof:
    temp = to_infix(p)
    infix_proof.append(temp)
    #print(temp)

# if ans == True:
#         print('1')
# else:
#     print('0')

if m == 1:
    #print('------')
    for p in infix_proof:
        print(p)
    #print('------')
    if ans == True:
        print('1')
    else:
        print('0')
else:
    #print('------')
    if ans == True:
        print('1')
    else:
        print('0')
    



    