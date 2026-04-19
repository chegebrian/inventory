from app import create_app

app = create_app()

# =================================
# BASIC ROUTES (health checks)
# =================================
@app.route("/")
def home():
    return {"message": "LocalShop Backend Live 🚀"}

@app.route("/api/test")
def test():
    return {"status": "Backend working perfectly"}

# =================================
# RUN APP
# =================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)