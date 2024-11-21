from flask import render_template
from app import create_app


app = create_app()

@app.errorhandler(403)
def forbidden_error(e):
    return render_template('403.html'), 403

if __name__ == "__main__":
    app.run(debug=True)

