import errno
import selectors
import socket
import pathlib
import threading
import queue

import paramiko

class Handler(paramiko.ServerInterface):

    def __init__(self, server, client_conn):
        self.server = server
        self.socket, self.conn = client_conn

        # holds list of commands issued for this connection (can be verified in unittest)
        self.commands = []
        self.queue = queue.Queue()

        self.transport = paramiko.Transport(self.socket)
        self.transport.add_server_key(paramiko.RSAKey(filename=str(pathlib.Path(__file__).with_name("test_server.key"))))

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def get_allowed_auths(self, username):
        return "publickey"

    def check_auth_publickey(self, username: str, key: paramiko.PKey) -> int:
        # TODO: check pkey for username
        # import ipdb; ipdb.set_trace()
        if (
            username in ('user', 'service') and
            # TODO: should verify signature somehow ?
            key.public_blob.key_type == 'ssh-rsa-cert-v01@openssh.com'
        ):
            return paramiko.AUTH_SUCCESSFUL
        return super().check_auth_publickey(username, key)

    def check_channel_exec_request(self, channel: paramiko.Channel, command: bytes) -> bool:
        # Put recevide command in queue ... handler thread will echo it back and close the channel
        self.queue.put(command)
        # channel.transport.get_username() == "user"
        return True
        # return super().check_channel_exec_request(channel, command)

    def run(self):
        self.transport.start_server(server=self)
        while True:
            channel = self.transport.accept()
            if channel is None:
                break
            # channel.chanid
            t = threading.Thread(target=self.handle, args=(channel,))
            t.setDaemon(True)
            t.start()

    def handle(self, channel):
        try:
            command = self.queue.get(block=True)
            self.commands.append(command.decode('utf-8'))
            channel.sendall(command)
            channel.send_exit_status(0)
            # what to do with channel?
            pass
        except Exception as e:
            print(e)
        finally:
            try:
                channel.close()
            except EOFError:
                print("close failed")


class Server:

    host = "127.0.0.1"

    def __init__(self, port=22):
        self._socket = None
        self._thread = None
        self._handler = None
        self._port = port

    def __enter__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((self.host, self._port))
        self._socket.listen(5)
        self._thread = threading.Thread(target=self._run)
        self._thread.setDaemon(True)
        self._thread.start()
        return self

    def _run(self):
        # grab a reference to self_socket (in case it get's cleanup in __exit__)
        sock = self._socket
        selector = selectors.DefaultSelector()
        selector.register(sock, selectors.EVENT_READ)
        while sock.fileno() > 0:
            events = selector.select(timeout=2.0)
            if events:
                try:
                    conn, addr = sock.accept()
                except OSError as e:
                    if e.errno in (errno.EBADF, errno.EINVAL):
                        break
                    raise
                self._handler = Handler(self, (conn, addr))
                t = threading.Thread(target=self._handler.run)
                t.setDaemon(True)
                t.start()

    def __exit__(self, *exc_info):
        print("exiting and close socket for server")
        try:
            self._socket.shutdown(socket.SHUT_RDWR)
            self._socket.close()
        except Exception as e:
            print(e)
            # pass
        
        self._socket = None
        self._thread = None
        self._handler = None

    @property
    def port(self):
        return self._socket.getsockname()[1]

    @property
    def commands(self):
        return self._handler.commands