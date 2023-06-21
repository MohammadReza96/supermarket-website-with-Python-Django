import random

# code_maker module for making random code for verifying user by sms
#-------------------------------------------------------
def code_maker(number):
    code=random.randint(10**(number-1),(10**(number))-1)
    return code

# for testing module
#------------------------
if __name__=="__main__":
    print(code_maker(6))