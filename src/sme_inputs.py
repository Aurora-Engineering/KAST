from .predicate import Predicate

def comparative_operators():
    # should add capability to add in names of predicates before frame - SMEs should specify these relationships first and then we build predicates from the frame
    new_variable = input("Please enter the name of the variable considered by the predicate: ")
    if new_variable == "STOP":
        return None
    urnary_operator = input("Please enter one of the follow operators [<,>,=]: ")
    numerical_val = input("Please enter a numerical value: ")
    pred_name = input("Please enter a predicate descriptor: ")

    pred = Predicate(new_variable,urnary_operator,numerical_val)
    print(f'Returning: ({pred_name}: {pred})')
    return({pred_name: pred})

def turnary_operators():
    pass