import socket
import json
import base64
import logging
import os

server_address = ('172.16.16.101', 7777)
local_directory = 'progjar4a'
remote_directory = 'files'

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message {command_str}")
        sock.sendall(command_str.encode())
        data_received = ""
        while True:
            data = sock.recv(16)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
        hasil = json.loads(data_received.strip())
        logging.warning(f"data received from server: {hasil}")
        return hasil
    except Exception as e:
        logging.warning(f"error during data receiving: {e}")
        return False

def remote_list():
    command_str = f"list"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str = f"get {filename}"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        namafile = hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile,'wb+')
        fp.write(isifile)
        print(f"File {namafile} berhasil didapatkan")
        return True
    else:
        print("Gagal")
        return False

def remote_upload(filepath=""):
    try:
        filename=filepath.split('/')[-1]
        with open(f"{filepath}",'rb') as fp:
            isifile = base64.b64encode(fp.read()).decode()
        command_str=f"upload {filename} {isifile}"
        hasil=send_command(command_str)
        if hasil['status'] == 'OK':
            print("File berhasil diupload")
            return True
        else:
            print("Gagal mengupload file")
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def remote_delete(filename=""):
    command_str = f"delete {filename}"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        print("File berhasil dihapus")
        return True
    else:
        print("Gagal menghapus file")
        return False

if __name__=='__main__':
    server_address = ('172.16.16.101', 7777)
    while True:
        print("""Command: 
        1. list
        2. get <filename>
        3. upload <filename>
        4. delete <filename>
        5. exit""")
        command = input("Enter command: ")
        if command == "list":
            remote_list()
        elif command.startswith("get"):
            filename = command.split(" ")[1]
            remote_get(filename)
        elif command.startswith("upload"):
            filepath = command.split(" ")[1]
            remote_upload(filepath)
        elif command.startswith("delete"):
            filename = command.split(" ")[1]
            remote_delete(filename)
        elif command == "exit":
            break
        else:
            print("Unknown command")
