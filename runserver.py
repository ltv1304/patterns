from server import TestServer
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run test http server')
    parser.add_argument('port', type=int, help='port')
    parser.add_argument('--host', type=str, help='host')
    args = parser.parse_args()
    server = TestServer()

    server.runserver()

