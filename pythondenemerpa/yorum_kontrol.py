import re
import json
import xml.etree.ElementTree as ET

def yorumlari_kontrol_et(dosya_adi="ornek_kod.py"):
    sonuclar = []

    # GELİŞTİRİLMİŞ REGEX
    desen = re.compile(
    r"#\s?[A-ZÇĞİÖŞÜ][a-zçğıöşü0-9\s,;.-]*\b(for|if|else|elif|while|try|except|function|loop|condition|koşul|döngü|fonksiyon|veri|işlem|parametre|method|değişken|class|yapı|kontrol)\b[^#]*[.!?]?$",
    re.IGNORECASE
)


    try:
        # 1. Yorumları kontrol et
        with open(dosya_adi, "r", encoding="utf-8") as dosya:
            satirlar = dosya.readlines()

        for i, satir in enumerate(satirlar):
            if satir.strip().startswith("#"):
                kelime_sayisi = len(satir.strip("# ").split())
                durum = "Doğru" if desen.match(satir.strip()) and kelime_sayisi >= 3 else "Yanlış"
                sonuclar.append({
                    "satir": i + 1,
                    "yorum": satir.strip(),
                    "sonuc": durum,
                    "oneri": "En az 3 kelime, büyük harf, anahtar kelime içermeli ve nokta ile bitmeli." if durum == "Yanlış" else ""
                })

        # 2. JSON çıktısı
        with open("rapor.json", "w", encoding="utf-8") as cikti:
            json.dump(sonuclar, cikti, indent=4, ensure_ascii=False)

        # 3. XML çıktısı
        def json_to_xml(json_path="rapor.json", xml_path="rapor.xml"):
            with open(json_path, "r", encoding="utf-8") as dosya:
                veriler = json.load(dosya)

            root = ET.Element("Yorumlar")

            for veri in veriler:
                yorum_eleman = ET.SubElement(root, "Yorum")
                ET.SubElement(yorum_eleman, "Satir").text = str(veri["satir"])
                ET.SubElement(yorum_eleman, "YorumMetni").text = veri["yorum"]
                ET.SubElement(yorum_eleman, "Sonuc").text = veri["sonuc"]
                ET.SubElement(yorum_eleman, "Oneri").text = veri["oneri"]

            agac = ET.ElementTree(root)
            agac.write(xml_path, encoding="utf-8", xml_declaration=True)

        json_to_xml("rapor.json", "rapor.xml")

        # 4. Renkli kod çıktısı (⚠️ ile işaretle)
        with open(dosya_adi, "r", encoding="utf-8") as orijinal:
            satirlar = orijinal.readlines()

        with open("ornek_kod_renkli.py", "w", encoding="utf-8") as yeni:
            for i, satir in enumerate(satirlar):
                if satir.strip().startswith("#"):
                    ilgili_yorum = next((item for item in sonuclar if item["satir"] == i + 1), None)
                    if ilgili_yorum and ilgili_yorum["sonuc"] == "Yanlış":
                        yeni.write(f"⚠️ {satir.strip()}  # HATALI YORUM\n")
                    else:
                        yeni.write(satir)
                else:
                    yeni.write(satir)

        # 5. UiPath'e JSON string döndür
        return json.dumps({
            "durum": "Başarılı",
            "toplam_yorum": len(sonuclar),
            "dogru_yorum": len([x for x in sonuclar if x["sonuc"] == "Doğru"]),
            "yanlis_yorum": len([x for x in sonuclar if x["sonuc"] == "Yanlış"]),
            "rapor_json": "rapor.json",
            "rapor_xml": "rapor.xml",
            "renkli_kod": "ornek_kod_renkli.py"
        }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"durum": "Hata", "mesaj": str(e)})