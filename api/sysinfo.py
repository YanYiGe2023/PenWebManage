import os
import time


def get_cpu_percent():
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


def get_mem_info():
    info = {}
    with open("/proc/meminfo") as f:
        for line in f:
            k, v = line.split(":", 1)
            info[k.strip()] = int(v.split()[0])
    total = info["MemTotal"]
    available = info.get("MemAvailable", info["MemFree"])
    used = total - available
    return {
        "percent": round(used / total * 100, 1),
        "used_mb": used // 1024,
        "total_mb": total // 1024,
    }


def human_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}TB"


def get_disk_info(path="/sys_data"):
    st = os.statvfs(path)
    total = st.f_blocks * st.f_frsize
    free = st.f_bavail * st.f_frsize
    used = total - free
    return {
        "percent": round(used / total * 100, 1) if total else 0,
        "used": human_size(used),
        "total": human_size(total),
    }


def get_cpu_temp():
    for zone in range(5):
        p = f"/sys/class/thermal/thermal_zone{zone}/temp"
        if os.path.exists(p):
            with open(p) as f:
                return f"{int(f.read()) / 1000:.1f}"
    return "N/A"


def collect_status():
    mem = get_mem_info()
    disk = get_disk_info("/sys_data")
    return {
        "cpu_percent": get_cpu_percent(),
        "mem_percent": mem["percent"],
        "mem_used_mb": mem["used_mb"],
        "mem_total_mb": mem["total_mb"],
        "disk_percent": disk["percent"],
        "disk_used": disk["used"],
        "disk_total": disk["total"],
        "cpu_temp": get_cpu_temp(),
    }


"""假数据，解决macOS平台问题
def collect_status():
    return {
        "cpu_percent": 12.3,
        "mem_percent": 45.6,
        "mem_used_mb": 120,
        "mem_total_mb": 256,
        "disk_percent": 30.0,
        "disk_used": "120.0MB",
        "disk_total": "400.0MB",
        "cpu_temp": "42.5",
    }
"""