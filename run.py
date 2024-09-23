import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db, socketio
from app.models import serialNumber

if __name__ == '__main__':
    app.run(debug=True)
    socketio.run(app, debug=True, host='0.0.0.0' , port=5001)
    
@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'serialNumber': serialNumber}