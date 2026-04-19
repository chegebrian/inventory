from app import create_app

app = create_app()

@app.route("/")
def home():
    return {"message": "LocalShop Backend Live 🚀"}

@app.route("/api/test")
def test():
    return {"status": "Backend working perfectly"}

if __name__ == "__main__":
    app.run(debug=True)