from flask import Flask, request
import subprocess
import json
import os

app = Flask(__name__)

@app.route('/configure', methods=['POST'])
def configure():
    data = request.get_json(force=True)
    if not data or 'hostname' not in data or 'rendered_config' not in data:
        return "Invalid payload", 400

    hostname = data["hostname"]
    rendered_config = data["rendered_config"]

    print(hostname)

    os.makedirs("/home/!user!/ansible/config/", exist_ok=True) # Change "!user!" to your Ansible Username
    config_file = f"/home/!user!/ansible/config/{hostname}.cfg" # Change "!user!" to your Ansible Username
    with open(config_file, "w") as f:
        f.write(str(rendered_config))

    extra_vars = json.dumps({
        "hostname": hostname,
        "rendered_config": rendered_config
    })
    print(extra_vars)

    ansible_command = [
        "ansible-playbook",
        "-i", "/home/!user!/ansible/netbox_inventory.yml", # Change "!user!" to your Ansible Username
        "/home/!user!/ansible/playbooks/config_transfer.yaml", # Change "!user!" to your Ansible Username
        "--extra-vars", extra_vars, "-vvv"
    ]
    print("Executing:", " ".join(ansible_command))

    result = subprocess.run(ansible_command, capture_output=True, text=True)
    return f"Ansible return code: {result.returncode}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
