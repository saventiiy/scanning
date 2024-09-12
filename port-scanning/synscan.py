from scapy.layers.inet import ICMP, IP, TCP, sr1
import socket
from datetime import datetime
import argparse
import sys


def create_parser():
  parser = argparse.ArgumentParser()
  parser.add_argument('-t', help='Target hostname/IP Address')
  parser.add_argument('-p', default="20, 21, 22", help='Ports range')
  parser.add_argument('-s', help='Scan type. Example: SS, US')
  return parser


//at first checking if server is runnig
def icmp_test(TARGET_IP):
  icmp = IP(dst=TARGET_IP) / ICMP()
  resp_packet = sr1(icmp, timeout=10, verbose=False)
  return resp_packet is not None

//making
def syn_scan(TARGET_IP, POTRTS):
  for RPORT in PORTS:
    syn_packet = IP(dst=TARGET_IP) / TCP(dport=RPORT, flags="S")
    resp_packet = sr1(syn_packet, timeout=5, verbose=False)
    if resp_packet is not None:
      tcp_layer = resp_packet.getlayer('TCP')
      if tcp_layer and tcp_layer.flags & 0x12 != 0:
        serv = get_service_name(RPORT, 'tcp')
        print('Port {}:		Open | {}'.format(RPORT, serv)) 


def udp_scan(TARGET_IP, PORTS):
  for RPORT in PORTS:
    MESSAGE = 'ping'
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPORTO_UDP)
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_RAM, socket.IPPORTO_ICMP)
    try: 
      client.sendto(MESSAGE.endcode("utf_8"), (TARGET_IP, RPORT))
      sock1.settimeout(1)	
      data, addr = sock1.recvfrom(1024)
    except socket.timeout: 
      serv = get_service_name(RPORT, 'udp')
      if not serv:
        pass
      else:
        print('Port {}:		Open | {}'.format(RPORT, serv))
    except socket.error as sock_err:
      if sock_err.errno == socket.errno.ECONNREFUSED:
        print(sock_err('Connection refused'))
      client.close()
      sock1.close


def get_service_name(port, proto):
  try: 
    name = socket.getservbyport(int(port), proto)
  except:
    return None
  return name


def scan(TARGET_IP, PORTS, SCAN):
  match SCAN: 
    case "SS":
      if icmp_test(TARGET_IP):
           syn_scan(TARGET_IP, PORTS)
      else: 
        print("Failed to send ICMP")
    case "US":
      if icmp_test(TARGET_IP):
        udp_scan(TARGET_IP, PORTS)
      else:
        print("Failed to send ICMP")


if __name__ == "__main__":
  start = datetime.now()
  parser = create_parser()
  parser_args = parser.parse_args()
  TARGET_IP = parser_args.t
  PORTS = parser_args.p
  SCAN = parser_args.s


  if "-" in PORTS: 
    ports_range = PORTS.split("-")
    PORTS = list(range(int(ports_range[0]), int(ports_range[1]) + 1))
  else: 
    PORTS = list(map(int, PORTS.split(",")))
  try: 
   resolved_ip = socket.gethostbyname(TARGET_IP)
  except: 
    print("wrong ip")
    sys.exit()
  scan(resolved_ip, PORTS, SCAN)
  print("FINISH")
  ends = datetime.now()
  runtime = ends - start
  print(f"TIME:{runtime}")  



