# -*- coding: utf-8 -*-
import os
import socket
import ssl
import time
import traceback
import httpx


def get_domain_cert(domain,port):
    socket.setdefaulttimeout(5)
    cxt = ssl.create_default_context()
    skt = cxt.wrap_socket(socket.socket(), server_hostname=domain)
    skt.connect((domain, port))
    cert = skt.getpeercert()
    skt.close()
    return cert


if __name__ == "__main__":
    f = open("domains.txt", "r")
    result = ""
    for domain in f:
        if domain.strip() == "":
            continue
        try:
            cert = get_domain_cert(
                domain.strip().split(":")[0],
                int(domain.strip().split(":")[1] if len(domain.strip().split(":")) > 1 else 443)
            )
            target_timestamp = time.mktime(time.strptime(cert['notAfter'].replace(" GMT", ""), "%b %d %H:%M:%S %Y"))
            countdown = target_timestamp - time.time()
            print(f"{domain} 证书剩余时间：{countdown / 86400:.2f}天")
            result += f"{domain} 证书剩余时间：{countdown / 86400:.2f}天\n"
        except Exception as e:
            print(f"{domain} 获取证书信息失败")
            traceback.print_exc()
            result += f"{domain} 获取证书信息失败\n"
    if os.getenv("WEBHOOK"):
        httpx.post(os.getenv("WEBHOOK"), json={
            "msg_type": "text",
            "content": {
                "text": result
            }
        })
