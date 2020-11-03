import math

def get_expression(s):      #make a raw string to a list of operator and operand 
                            #that we can easy to calculate
    s = s.replace(" ", "")
    operator = ['+', '-', '*', '/', '(', ')']   #List of operator
    expression = []
    expression.append(s[0])
    if(s[0] == '('):
        expression.append('')
    for i in range(1, len(s)):
        if s[i] in operator:
            if(expression[-1] != ''):
                expression.append(s[i])
            else:
                expression[-1] = s[i]
            expression.append('')
        else:
            expression[-1] += s[i]
    if(s[-1] in operator):
        expression.append(s[-1])
    return expression

def calc(a, op, b):         #Calculate: a op b = ?
    if(op == '+'):
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    else:
        return a / b
        
def calculate(row, expression):
    operand_stack = []
    operator_stack = []
    operator = {'+' : 0, '-' : 0, '*' : 1, '/' : 1}         #List of operator and priority
    for x in expression:
        if(x != '(' and x != ')' and x not in operator):    #if x is an operand 
                                                                #then push is to operand stack
            if(x.isnumeric()):
                operand_stack.append(float(x))
            else:
                operand_stack.append(row[x])
        if(x == '('):                                       #If x is open bracket
                                                                #then push is to operator stack
            operator_stack.append(x)
        if(x in operator):                                  #If x is and operator
                                                            #If that is an operator that has priority not greater than x
                                                                #We pop 2 operand and 1 operator to calulate 
                                                                # and push it to operand stack
                                                            #Otherwise, just push to operator stack
            while(len(operator_stack) > 0 and operator_stack[-1] != '(' and operator[x] <= operator[operator_stack[-1]]):
                a = operand_stack.pop()
                b = operand_stack.pop()
                op = operator_stack.pop()
                operand_stack.append(calc(a, op, b))
            operator_stack.append(x)
        if(x == ')'):                                   #If x is close bracket
                                                            #We pop 2 operand and 1 operator to calculate
                                                            #until top of operator stack is open bracket
            while(operator_stack[-1] != '('):
                a = operand_stack.pop()
                b = operand_stack.pop()
                op = operator_stack.pop()
                operand_stack.append(calc(b, op, a))
            operator_stack.pop()
    while(len(operator_stack) > 0):                     #pop 2 operand and 1 operator to calculate 'til operator stack is empty
        a = operand_stack.pop()
        b = operand_stack.pop()
        op = operator_stack.pop()
        operand_stack.append(calc(b, op, a))
    
    return operand_stack.pop()     