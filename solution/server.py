from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random
from urllib.parse import urlparse,parse_qs

partidas = []

class Player:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.id = 0
            cls._instance.player = ""
            cls._instance.number = 0
            cls._instance.attempts = []
            cls._instance.status = ""

        return cls._instance
    def crear_partida(self,nom):
        self.id = self.id + 1
        self.player = nom
        self.status = "En progreso"
        opciones = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100]
        self.number = random.choice(opciones)
        self.attempts = []
    def jugar_partida(self,numjug):
        self.attempts.append(numjug)
        if numjug == self.number:
            print("Felicitaciones")
            self.status = "Finalizado"
        elif numjug < self.number:
            print("el número a adivinar es mayor")
        elif numjug > self.number:
            print("el número a adivinar es menor")
        
    def to_dict(self):
        return {"player":self.player,"number": self.number, "attempts": self.attempts,"satatus":self.status},

class PartidasHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        if self.path == "/guess":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(partidas).encode("utf-8"))
        elif parsed_path.path == "/guess":
            if "resultado" in query_params:
                Resultado = query_params["resultado"][0]
                partidas_filtradas = [
                    partida
                    for partida in partidas
                    if partida["resultado"]
                ]
                if partidas_filtradas != []:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(partidas_filtradas).encode("utf-8"))
                else:
                    self.send_response(204)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps([]).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/guess":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            nombre = json.loads(post_data.decode("utf-8"))["player"]
            player.crear_partida(nombre)
            self.send_response(201)
            self.end_headers()
            partida = {
                "id": player.id,
                "player": player.player,
                "number": player.number,
                "attempts": player.attempts,
                "status": player.status
                }
            
            player_data = player.to_dict()
            partidas.append(partida)
            self.wfile.write(json.dumps(player_data).encode("utf-8"))
            
            #self.wfile.write(player_data.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
    def do_PUT(self):
        if self.path == "/guess":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            attempt = json.loads(post_data.decode("utf-8"))["attempt"]
            player.jugar_partida(attempt)
            self.send_response(201)
            self.end_headers()
            self.wfile.write(json.dumps(partidas).encode("utf-8"))
        
def main():
    global player
    player = Player()

    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, PartidasHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()

if __name__ == "__main__":
    main()