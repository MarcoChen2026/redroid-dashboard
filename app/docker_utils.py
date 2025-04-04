import docker
import socket

client = docker.from_env()

def get_public_ip():
    import requests
    try:
        return requests.get('https://ifconfig.me').text
    except:
        return "<your-server-ip>"

def list_redroid_containers():
    containers = client.containers.list(all=True, filters={"name": "redroid"})
    ip = get_public_ip()
    result = []
    for c in containers:
        try:
            port = c.attrs['NetworkSettings']['Ports']['5555/tcp'][0]['HostPort']
        except:
            port = "N/A"
        status = c.status
        adb_cmd = f"adb connect {ip}:{port}" if status == 'running' else "(容器未运行)"
        result.append({
            'name': c.name,
            'status': status,
            'port': port,
            'adb_cmd': adb_cmd
        })
    return result

def start_container(name):
    container = client.containers.get(name)
    container.start()

def stop_container(name):
    container = client.containers.get(name)
    container.stop()

def restart_container(name):
    container = client.containers.get(name)
    container.restart()

def create_redroid_instance():
    client.containers.run("redroid/redroid:11.0.0-latest", detach=True)
