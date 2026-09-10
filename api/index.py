from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        payload = {
            "competition": "myInsight - MDS Datathon Challenge 2026 (FTU2)",
            "award": "1st Runner-up (Á Quân)",
            "team": "FUU",
            "members": [
                {"name": "Dang Nguyen Thu Ha", "role": "Team Leader", "school": "FTU2"},
                {"name": "Le Chi Hoang", "role": "Member", "school": "UIT"},
                {"name": "Huynh Trung Nghia", "role": "Member", "school": "HCMTUE"}
            ],
            "dataset": {
                "sample_size": 2600,
                "waves": [2024, 2025],
                "topic": "Brand Health Tracking & Growth Strategy for Cozy RTD Tea Vietnam"
            },
            "status": "ready"
        }
        self.wfile.write(json.dumps(payload, ensure_ascii=False, indent=2).encode('utf-8'))
