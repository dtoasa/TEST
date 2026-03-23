import json
import os
import time

JSON_FILE = "status_agentes.json"
PULSE_DIR = "pulses" # Directorio donde los agentes dejan su "latido"

AGENTS = [
    "Tutor-Pro", "Quiz-Master", "Vision-VAR", "Sentinel-Log", 
    "Scraper-X", "Office-Clerk", "Audio-Sentry", "Cloud-Syncer", 
    "Game-Server", "Neural-Net"
]

def init_pulses():
    if not os.path.exists(PULSE_DIR):
        os.makedirs(PULSE_DIR)

def check_pulse(agent):
    pulse_file = os.path.join(PULSE_DIR, f"{agent}.pulse")
    if not os.path.exists(pulse_file):
        return "off"
    
    # Verificar tiempo de última modificación
    last_pulse = os.path.getmtime(pulse_file)
    elapsed = time.time() - last_pulse
    
    if elapsed < 5:
        return "online"
    elif elapsed < 15: # Margen de gracia antes de error
        return "online"
    else:
        return "error"

def main():
    init_pulses()
    print(f"--- NEMOCLAW PULSE MONITOR ---")
    print(f"Buscando señales en: {os.path.abspath(PULSE_DIR)}")
    
    # Cargar estado actual para detectar caídas
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            current_status = json.load(f)
    else:
        current_status = {agent: "off" for agent in AGENTS}

    while True:
        updates_made = False
        new_status = {}
        
        for agent in AGENTS:
            status = check_pulse(agent)
            
            # Lógica de Alerta de Caída:
            # Si estaba en "online" y ahora el pulse falla (>5s), pasa a "error"
            if current_status.get(agent) == "online" and status == "off":
                 status = "error"
            
            # Si el pulse es muy viejo, es error
            if status == "error":
                if current_status.get(agent) != "error":
                    print(f"[ALERTA] {agent} ha dejado de responder!")
                    updates_made = True
            
            if status != current_status.get(agent):
                updates_made = True
            
            new_status[agent] = status
        
        if updates_made:
            current_status = new_status
            with open(JSON_FILE, "w") as f:
                json.dump(current_status, f, indent=2)
            # print("JSON Actualizado.")
            
        time.sleep(2)

if __name__ == "__main__":
    main()
