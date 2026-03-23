import json
import os
import time

JSON_FILE = "status_agentes.json"

AGENTS = [
    "Tutor-Pro", "Quiz-Master", "Vision-VAR", "Sentinel-Log", 
    "Scraper-X", "Office-Clerk", "Audio-Sentry", "Cloud-Syncer", 
    "Game-Server", "Neural-Net"
]

STATUSES = ["online", "error", "off"]

def load_status():
    if not os.path.exists(JSON_FILE):
        return {agent: "off" for agent in AGENTS}
    with open(JSON_FILE, "r") as f:
        return json.load(f)

def save_status(data):
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=2)

def main():
    print("--- NEMOCLAW FOCUS TESTER ---")
    data = load_status()
    
    while True:
        print("\nAgentes actuales:")
        for idx, agent in enumerate(AGENTS, 1):
            print(f"{idx}. {agent} [{data.get(agent, 'off')}]")
        
        try:
            choice = input("\nSelecciona un agente (1-10) o 'q' para salir: ")
            if choice.lower() == 'q':
                break
            
            idx = int(choice) - 1
            if 0 <= idx < len(AGENTS):
                agent = AGENTS[idx]
                print(f"\nEstados disponibles: 1. Online, 2. Error, 3. Offline")
                s_choice = input(f"Nuevo estado para {agent}: ")
                
                if s_choice == "1":
                    data[agent] = "online"
                elif s_choice == "2":
                    data[agent] = "error"
                elif s_choice == "3":
                    data[agent] = "off"
                else:
                    print("Opción inválida.")
                    continue
                
                save_status(data)
                print(f"Update: {agent} -> {data[agent]}")
            else:
                print("Número fuera de rango.")
        except ValueError:
            print("Entrada no válida.")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
