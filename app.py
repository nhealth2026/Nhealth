"""
Nhealth - Healthcare at Home
Application Entry Point
Modularized Architecture: Flask App Factory pattern via backend package.
"""

import os
from backend import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("==================================================")
    print("   Nhealth - Healthcare at Home Server Started   ")
    print(f"   Serving on: http://0.0.0.0:{port}             ")
    print("==================================================")
    app.run(host='0.0.0.0', port=port, debug=False)
