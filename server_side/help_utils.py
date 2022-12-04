from datetime import datetime
import base64




####################### help functions #######################################
def is_num(s):
    b_Int = True
    try:
        # converting to integer
        int(s)
    except ValueError:
        b_Int = False
    return b_Int


def ask_list_index(instruction, list_len):
    op = input(instruction)
    cond = is_num(op) and int(op)>=1 and int(op) < list_len+1

    while(not cond):
        print('please choose number from the list!')
        op = input(instruction)
        cond = is_num(op) and int(op)>=1 and int(op) < list_len+1
    index = int(op)-1
    return index


def curr_date_and_time():
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%D/%m/%Y %H:%M:%S")
    return dt_string


def isBase64(s):
    try:
        return base64.b64encode(base64.b64decode(s)) == s
    except Exception:
        return False