from website import create_app
from website.models import initialize_database
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        initialize_database()
    app.run(debug=True)
