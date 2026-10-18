from app import create_app  # adjust import if needed

app = create_app("testing")

print("Testing app created.")
print("DATABASE =", app.config["DATABASE"])
print("TESTING =", app.config.get("TESTING"))