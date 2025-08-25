import socket
import threading
import json
import numpy as np

class RLServer:
    def __init__(self, host='127.0.0.1', port=5557):
        self.host = host
        self.port = port
        self.thread = None
        self.actions = {"move_f":0,"move_b":0,"move_l":0,"move_r":0,"jump":0}
        self.get_obs_fn = None
        self.apply_act_fn = None
        self.running = False

    def start(self, get_obs_fn, apply_act_fn):
        self.get_obs_fn = get_obs_fn
        self.apply_act_fn = apply_act_fn
        self.running = True
        self.thread = threading.Thread(target=self._serve, daemon=True)
        self.thread.start()

    def _serve(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen(1)
            while self.running:
                conn, _ = s.accept()
                with conn:
                    while self.running:
                        data = conn.recv(8192)
                        if not data: 
                            break
                        try:
                            msg = json.loads(data.decode())
                        except Exception:
                            continue
                        if msg.get("type") == "OBSERVE":
                            obs = self.get_obs_fn() if self.get_obs_fn else {}
                            conn.sendall(json.dumps(obs).encode("utf-8"))
                        elif msg.get("type") == "ACT":
                            self.actions.update(msg.get("data", {}))
                            if self.apply_act_fn:
                                self.apply_act_fn(self.actions)
                            # ✅ fixed response
                            conn.sendall(json.dumps({"ok": True}).encode("utf-8"))

