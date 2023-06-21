from kavenegar import *

# sms message sender
#----------------------------------------------------- 
def send_sms(mobile_number,message):
    try:
        api = KavenegarAPI('586C572B4E73445A5964732B504B72503258486446527949484637473134566946387373614D35797871493D')
        params = {
            'sender': '',   #optional (the number you buy from kavenegar (it is not neccesary))
            'receptor': mobile_number ,   #multiple mobile number, split by comma
            'message': message,
        } 
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)