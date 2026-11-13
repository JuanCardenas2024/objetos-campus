from app.health import estado_general

if __name__ == "__main__":
    for servicio, (ok, msg) in estado_general().items():
        print(f"{servicio:10} -> {'✔' if ok else '✘'} {msg}")