import os
import socket
import re
import uuid
from datetime import datetime
from email.message import Message
from io import BytesIO

class SocketServer:
    def __init__(self):
        self.bufsize = 1024  # 버퍼 크기 설정
        with open('./response.bin', 'rb') as file:
            self.RESPONSE = file.read()  # 응답 파일 읽기
        self.DIR_PATH = './request'
        self.IMAGE_PATH = './images'
        self.createDir(self.DIR_PATH)
        self.createDir(self.IMAGE_PATH)

    def createDir(self, path):
        """디렉토리 생성"""
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError:
            print("Error: Failed to create the directory.")

    def parse_multipart(self, data):
        """멀티파트 데이터에서 이미지 파일 추출"""
        try:
            # HTTP 요청에서 헤더와 바디 분리
            data_str = data.decode('utf-8', errors='ignore')
            if '\r\n\r\n' in data_str:
                headers_part, body_part = data_str.split('\r\n\r\n', 1)
            else:
                return None
            
            # Content-Type에서 boundary 추출
            content_type_match = re.search(r'Content-Type: multipart/form-data; boundary=([^\r\n]+)', headers_part, re.IGNORECASE)
            if not content_type_match:
                return None
            
            boundary = content_type_match.group(1).strip()
            
            # 멀티파트 데이터를 바이트로 다시 변환
            body_bytes = data[data.find(b'\r\n\r\n') + 4:]
            
            # boundary로 파트 분리
            boundary_bytes = ('--' + boundary).encode()
            parts = body_bytes.split(boundary_bytes)
            
            for part in parts:
                if b'Content-Type: image/' in part and b'\r\n\r\n' in part:
                    # 파트 헤더와 데이터 분리
                    part_headers, part_data = part.split(b'\r\n\r\n', 1)
                    
                    # 파일명 추출
                    filename_match = re.search(rb'filename="([^"]*)"', part_headers)
                    if filename_match:
                        filename = filename_match.group(1).decode('utf-8', errors='ignore')
                    else:
                        # 파일명이 없으면 확장자 추출해서 UUID로 생성
                        content_type_match = re.search(rb'Content-Type: image/(\w+)', part_headers)
                        if content_type_match:
                            ext = content_type_match.group(1).decode()
                            filename = f"{uuid.uuid4().hex}.{ext}"
                        else:
                            filename = f"{uuid.uuid4().hex}.jpg"  # 기본값
                    
                    # 파일 데이터에서 끝부분 경계 제거
                    if part_data.endswith(b'\r\n'):
                        part_data = part_data[:-2]
                    
                    return filename, part_data
            
            return None
        except Exception as e:
            print(f"멀티파트 파싱 오류: {e}")
            return None

    def run(self, ip, port):
        """서버 실행"""
        # 소켓 생성
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((ip, port))
        self.sock.listen(10)
        print("Start the socket server...")
        print("\"Ctrl+C\" for stopping the server!\r\n")

        try:
            while True:
                # 클라이언트의 요청 대기
                clnt_sock, req_addr = self.sock.accept()
                clnt_sock.settimeout(5.0)  # 타임아웃 설정(5초)
                print("Request message...\r\n")
                response = b""

                # ============================
                # 요청 데이터 읽기
                while True:
                    try:
                        data = clnt_sock.recv(self.bufsize)
                        if not data:
                            break
                        response += data
                    except socket.timeout:
                        break

                # 파일명 생성 (년-월-일-시-분-초)
                now = datetime.now()
                filename = now.strftime("%Y-%m-%d-%H-%M-%S.bin")
                filepath = os.path.join(self.DIR_PATH, filename)
                # 요청 데이터 저장 (실습 1)
                with open(filepath, 'wb') as f:
                    f.write(response)
                print(f"Request saved to: {filepath}")
                
                # 멀티파트 데이터 처리 (실습 2)
                if b'multipart/form-data' in response:
                    image_result = self.parse_multipart(response)
                    if image_result:
                        image_filename, image_data = image_result
                        image_filepath = os.path.join(self.IMAGE_PATH, image_filename)
                        with open(image_filepath, 'wb') as f:
                            f.write(image_data)
                        print(f"Image saved to: {image_filepath}")
                        print(f"Image size: {len(image_data)} bytes")
                    else:
                        print("No valid image found in multipart data")
                # ============================

                # 응답 전송
                clnt_sock.sendall(self.RESPONSE)
                # 클라이언트 소켓 닫기
                clnt_sock.close()
        except KeyboardInterrupt:
            print("\r\nStop the server...")
            # 서버 소켓 닫기
            self.sock.close()

if __name__ == "__main__":
    server = SocketServer()
    server.run("127.0.0.1", 8000)