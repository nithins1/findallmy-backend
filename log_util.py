def log(message: str, filename: str = "output.log"):
    with open(filename, "a") as f:
        f.write(message + "\n\n")

def reset_log(filename: str = "output.log"):
    with open(filename, "w") as f:
        f.write("")  