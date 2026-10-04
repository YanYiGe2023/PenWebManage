import os
import sys
import time

IS_LINUX = sys.platform.startswith("linux")


# ---------- Linux 真实采集 ----------

def _cpu_percent_linux():
    def read_stat():
        with open("/proc/stat") as f:
            parts = f.readline().split()
        idle = int(parts[4])
        total = sum(int(x) for x in parts[1:8])
        return idle, total

    idle1, total1 = read_stat()
    time.sleep(0.5)
    idle2, total2 = read_stat()
    total_delta = total2 - total1
    if total_delta == 0:
        return 0.0
    return round((1 - (idle2 - idle1) / total_delta) * 100, 1)


def _mem_raw_linux():
    info = {}
    with open("/proc/meminfo") as f:
        for line in f:
            k, v = line.split(":", 1)
            info[k.strip()] = int(v.split()[0])
    total = info["MemTotal"] * 1024
    available = info.get("MemAvailable", info["MemFree"]) * 1024
    return {"total": total, "available": available}


def _disk_raw_linux(path="/sys_data"):
    if not os.path.exists(path):
        path = "/"
    st = os.statvfs(path)
    total = st.f_blocks * st.f_frsize
    free = st.f_bavail * st.f_frsize
    return {"total": total, "free": free, "path": path}


def _cpu_temp_linux():
    for zone in range(5):
        p = f"/sys/class/thermal/thermal_zone{zone}/temp"
        if os.path.exists(p):
            with open(p) as f:
                return int(f.read())
    return None


# ---------- 对外接口 ----------

def collect_status():
    if not IS_LINUX:
        # 非 Linux 平台：返回全 0，并标记不支持
        return {
            "platform_ok": False,
            "platform": sys.platform,
            "cpu_percent": 0,
            "mem": {"total": 0, "available": 0},
            "disk": {"total": 0, "free": 0, "path": ""},
            "cpu_temp": None,
        }

    return {
        "platform_ok": True,
        "platform": sys.platform,
        "cpu_percent": _cpu_percent_linux(),
        "mem": _mem_raw_linux(),
        "disk": _disk_raw_linux(),
        "cpu_temp": _cpu_temp_linux(),
    }