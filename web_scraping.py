from bs4 import BeautifulSoup
import requests
import pyodbc

model_no_s=["R9","R7","R6","R5","R4","R3","I9","I7","I5","I3","Intel","İntel","Ryzen","Amd","Core","N4120"]##"Oled"
model_no_s2=[".Nesil",'"',"''"]

isletim_sistemi_s="İşletim Sistemi"
islemci_modeli_s="İşlemci Modeli"
islemci_tipi_s="İşlemci"
ram_s="Bellek Kapasitesi"
disk_boyutu_s="Disk Kapasitesi"
ekran_boyutu_s="Ekran Boyutu"
ekran_cozunurlugu_s="Ekran Çözünürlüğü"
disk_turu_s="Disk Türü"
model_s="Model"
marka_s="Marka"
ekran_karti_modeli_s="Ekran Kartı Modeli"
islemci_hizi_s="İşlemci Hızı"
cekirdek_sayisi_s="İşlemci Çekirdek Sayısı"

database=pyodbc.connect('Driver={};'
    'Server=;'
    'Database=;'
    'Trusted_Connection=;')

## database baglanti bolumu doldurulmali

try:
    cursor=database.cursor()
except Exception as e:
    print(e)


def urun_var_mi():
    cursor.execute("SELECT UrunId FROM ProductAttributes WHERE ModelNo=?",model_no)
    urun_id = cursor.fetchall()
    if len(urun_id) !=0:
        return urun_id[0][0]
    else:
        return -1

def ProductAttributesKayitEkle():
    cursor.execute("SELECT UrunId FROM ProductAttributes WHERE ModelNo=?",model_no)
    urun = cursor.fetchall()
    if len(urun)==0:
        cursor.execute("INSERT INTO ProductAttributes VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (marka, model, model_no, islemci_tipi, islemci_nesli, islemci_modeli, ram, disk_boyutu, disk_turu,isletim_sistemi, ekran_boyutu, cozunurluk_standarti, ekran_cozunurlugu, ekran_karti_modeli, islemci_hizi, cekirdek_sayisi, img))
        cursor.commit()

def ProductPricesPointsKayitEkle(urun,price,prdct_point,real_link):
    cursor.execute("SELECT Fiyat FROM ProductPricesPoints WHERE SiteId=? and UrunId=?",site_id,urun)
    fiyatlar = cursor.fetchall()
    if len(fiyatlar)!=0:
        for f in fiyatlar:
            if price<f[0]:
                cursor.execute("UPDATE ProductPricesPoints SET Fiyat=?,Puan=?,UrunLinki=? WHERE Urun_id=? and SiteId=?", price, prdct_point, real_link,urun,site_id)
                cursor.commit()
    else:
        cursor.execute("INSERT INTO ProductPricesPoints VALUES(?,?,?,?,?)",(urun, price, prdct_point, real_link, site_id))
        cursor.commit()


cursor.execute("SELECT COUNT(*) FROM ProductAttributes")
kayit_sayisi = cursor.fetchall()
print(kayit_sayisi)

header = {'User-Agent':''}  ## user agent bilgisi eklenmeli

if kayit_sayisi[0][0]==0:
    check = False
    model_no_check = False
    site_id = 1

    for page_value in range(1, 18):
        if page_value == 1:
            req = requests.get("") ## site linki eklenmeli

        else:
            page_link = "&pg=" + str(page_value)
            req = requests.get("" + page_link)  ## site linki eklenmeli

        try:
            s = BeautifulSoup(req.content, "html.parser")
            prdct_cntnr = s.find("ul", attrs={"class": "list-ul"})
            prdcts = prdct_cntnr.find_all("li", attrs={"class": "column"})
        except Exception as e:
            print(e)
            break

        u=0
        for link in prdcts:
            try:
                real_link = link.a.get("href")
                print(real_link)

                prdct_info = link.a.get("title")
                print(prdct_info)
                marka = prdct_info.split()[0]

                pro = link.find("div", attrs={"class": "pro"})
                price_cntnr = pro.find("div", attrs={"class": "proDetail"})
                price_c = price_cntnr.find("span", attrs={"class": "newPrice"})
                price = price_c.find("ins").text
                print("Fiyat - " + price)
                zero = 0
                for zero in range(0, len(price)):
                    if price[zero] == ".":
                        break
                zero = 3 - zero
                zero_s = ""
                for k in range(0, zero):
                    zero_s += "0"
                price = zero_s + price

                req2 = requests.get(real_link)
                s2 = BeautifulSoup(req2.content, "html.parser")

                model_no = "Belirtilmemiş"
                disk_turu = "SSD"
                cozunurluk_standarti = "Belirtilmemiş"
                ekran_karti_modeli = "Belirtilmemiş"
                islemci_hizi = "Belirtilmemiş"
                cekirdek_sayisi = "Belirtilmemiş"

                img_c = s2.find("img", attrs={"class": "lazy"})
                img=img_c.get("data-src")
                print(img)

                try:
                    prdct_comment = s2.find("div", attrs={"class": "ratingCont"})
                    prdct_point = prdct_comment.find("strong", attrs={"class": "ratingScore"}).text
                    print("Puan - " + prdct_point)
                except Exception as e:
                    print(e)
                    prdct_point="0"

                u_list = s2.find("ul", attrs={"class": "unf-prop-list"})
                attrs = u_list.find_all("li", attrs={"class": "unf-prop-list-item"})

                for attr2 in attrs:
                    labels2 = attr2.find("p", attrs={"class": "unf-prop-list-title"}).text

                    if labels2 == marka_s:
                        marka = attr2.find("p", attrs={"class": "unf-prop-list-prop"}).text
                        marka = marka.strip()
                        print(labels2 + " - " + marka)

                    elif labels2 == isletim_sistemi_s:
                        isletim_sistemi = attr2.find("p", attrs={"class": "unf-prop-list-prop"}).text
                        isletim_sistemi = isletim_sistemi.strip()
                        print(labels2 + " - " + isletim_sistemi)

                    elif labels2 == islemci_tipi_s:
                        islemci_tipi = attr2.find("p", attrs={"class": "unf-prop-list-prop"}).text
                        islemci_tipi = islemci_tipi.strip()
                        print(labels2 + " - " + islemci_tipi)

                    elif labels2 == islemci_modeli_s:
                        islemci_modeli1 = attr2.find("p", attrs={"class": "unf-prop-list-prop"}).text
                        islemci_modeli1 = islemci_modeli1.strip()
                        islemci_modeli2 = islemci_modeli1.split("-")

                        if len(islemci_modeli2) == 2:
                            islemci_modeli = islemci_modeli2[1]

                            if islemci_modeli[0] == "1":
                                islemci_nesli = islemci_modeli[0] + islemci_modeli[1] + ".Nesil"
                            elif islemci_modeli[0] == "3" or islemci_modeli[0] == "4" or islemci_modeli[0] == "5" or \
                                    islemci_modeli[0] == "6" or islemci_modeli[0] == "7" or islemci_modeli[0] == "9":
                                islemci_nesli = islemci_modeli[0] + ".Nesil"
                            else:
                                islemci_nesli = "Belirtilmemiş"

                        else:
                            islemci_modeli2 = islemci_modeli1.split()
                            islemci_modeli = islemci_modeli2[len(islemci_modeli2) - 1]
                            islemci_nesli = "Belirtilmemiş"

                        print(labels2 + " - " + islemci_modeli)
                        print("İşlemci Nesli" + " - " + islemci_nesli)

                    elif labels2 == ram_s:
                        ram = attr2.find("p", attrs={"class": "unf-prop-list-prop"}).text
                        ram = ram.strip()
                        print(labels2 + " - " + ram)

                    elif labels2 == disk_boyutu_s:
                        disk_boyutu = attr2.find("p", attrs={"class": "unf-prop-list-prop"}).text
                        disk_boyutu = disk_boyutu.strip()
                        print(labels2 + " - " + disk_boyutu)

                    elif labels2 == ekran_boyutu_s:
                        ekran_boyutu = attr2.find("p", attrs={"class": "unf-prop-list-prop"}).text
                        ekran_boyutu = ekran_boyutu.strip()
                        print(labels2 + " - " + ekran_boyutu)

                    elif labels2 == ekran_cozunurlugu_s:
                        ekran_cozunurlugu = attr2.find("p", attrs={"class": "unf-prop-list-prop"}).text
                        ekran_cozunurlugu = ekran_cozunurlugu.strip()

                        if ekran_cozunurlugu == "1280 x 720":
                            cozunurluk_standarti = "HD"
                        elif ekran_cozunurlugu == "1366 x 768":
                            cozunurluk_standarti = "HD"
                        elif ekran_cozunurlugu == "1600 x 900":
                            cozunurluk_standarti = "HD+"
                        elif ekran_cozunurlugu == "1920 x 1080":
                            cozunurluk_standarti = "FHD"
                        elif ekran_cozunurlugu == "2560 x 1440":
                            cozunurluk_standarti = "QHD"
                        elif ekran_cozunurlugu == "3200 x 1800":
                            cozunurluk_standarti = "QHD+"
                        elif ekran_cozunurlugu == "3840 x 2160":
                            cozunurluk_standarti = "4K UHD"
                        else:
                            cozunurluk_standarti = "Belirtilmemiş"

                        print(labels2 + " - " + ekran_cozunurlugu)
                        print("Çözünürlük standartı" + " - " + cozunurluk_standarti)

                    elif labels2 == disk_turu_s:
                        disk_turu = attr2.find("p", attrs={"class": "unf-prop-list-prop"}).text
                        disk_turu = disk_turu.strip()
                        print(labels2 + " - " + disk_turu)

                    elif labels2 == ekran_karti_modeli_s:
                        ekran_karti_modeli = attr2.find("p", attrs={"class": "unf-prop-list-prop"}).text
                        ekran_karti_modeli = ekran_karti_modeli.strip()
                        print(labels2 + " - " + ekran_karti_modeli)

                    elif labels2 == islemci_hizi_s:
                        islemci_hizi = attr2.find("p", attrs={"class": "unf-prop-list-prop"}).text
                        islemci_hizi = islemci_hizi.strip()
                        print(labels2 + " - " + islemci_hizi)

                    elif labels2 == cekirdek_sayisi_s:
                        cekirdek_sayisi = attr2.find("p", attrs={"class": "unf-prop-list-prop"}).text
                        cekirdek_sayisi = cekirdek_sayisi.strip()
                        print(labels2 + " - " + cekirdek_sayisi)

                    elif labels2 == model_s:
                        model_no1 = attr2.find("p", attrs={"class": "unf-prop-list-prop"}).text
                        model_no1 = model_no1.strip()
                        model_no2 = model_no1.split()
                        model_no = model_no2[len(model_no2) - 1]
                        if len(model_no)<=2:
                            model_no_head=model_no2[len(model_no2) - 2]
                            model_no=model_no_head+model_no
                        model_no = model_no.upper()
                        print(labels2 + " - " + model_no)

                    else:
                        continue

                model = ""
                model1 = prdct_info.split()
                for n in range(1, len(model1)):
                    if model1[n].casefold().find(model_no.casefold()) >= 0:
                        for h in range(1, n):
                            model += model1[h] + " "
                        break

                if model == "":
                    model = model_no
                model = model.strip()
                print("Model - " + model)

                ProductAttributesKayitEkle()
                urun = urun_var_mi()
                if urun >= 0:
                    ProductPricesPointsKayitEkle(urun, price, prdct_point, real_link)
                print(" ")

            except Exception as e:
                print(e)
                continue

            finally:
                u+=1


    def verilerial1(urun_id):
        try:
            str_c = link.find("div", attrs={"class": "ratings-container"})
            stars = str_c.find_all("div", attrs={"class": "star-w"})

            point_sub = 0.0
            for star in stars:
                str_width = star.find("div", attrs={"class": "full"}).get("style")
                str_width = str_width.replace(" ", "")
                str_width = str_width.replace("max-width:100%", "")
                str_width = str_width.replace("%", "")
                str_width = str_width.replace(";", "")
                str_width = str_width.replace("width:", "")
                points = float(str_width) / 100.0
                point_sub += points

            prdct_point1 = round(point_sub, 1)
            prdct_point=str(prdct_point1)
            print("Puan - " + prdct_point)


            price = s2.find("span", attrs={"class": "prc-dsc"}).text
            print("Fiyat - " + price)
            zero = 0
            for zero in range(0, len(price)):
                if price[zero] == ".":
                    break
            zero = 3 - zero
            zero_s = ""
            for k in range(0, zero):
                zero_s += "0"
            price = zero_s + price

            ProductPricesPointsKayitEkle(urun_id, price, prdct_point, real_link)
            print(" ")
            return 0

        except Exception as e:
            print(e)
            return 1

    check = False
    model_no_check = False
    site_id = 2

    for page_value in range(1, 53):
        if page_value == 1:
            req = requests.get("")  ## site linki eklenmeli
        else:
            page_link = "&pi=" + str(page_value)
            req = requests.get("" + page_link)  ## site linki eklenmeli

        try:
            s = BeautifulSoup(req.content, "html.parser")
            prdct_cntnr = s.find("div", attrs={"class": "prdct-cntnr-wrppr"})
            prdcts = prdct_cntnr.find_all("div", attrs={"class": "card-border"})
        except Exception as e:
            print(e)
            break

        for link in prdcts:
            try:
                link_end = link.a.get("href")
                link_head = ""  ## site linki eklenmeli
                real_link = link_head + link_end
                print(real_link)

                prdct_info_w = link.find("div", attrs={"class": "prdct-desc-cntnr"})
                prdct_title = prdct_info_w.find("div", attrs={"class": "prdct-desc-cntnr-ttl-w"})
                marka = prdct_title.find("span", attrs={"class": "prdct-desc-cntnr-ttl"}).text
                print(marka,end=" ")

                req2 = requests.get(real_link)
                s2 = BeautifulSoup(req2.content, "html.parser")

                prdct_info_w = s2.find("div", attrs={"class": "pr-in-w"})
                prdct_title = prdct_info_w.find("div", attrs={"class": "pr-in-cn"})
                prdct_info_c = prdct_title.find("h1", attrs={"class": "pr-new-br"})
                prdct_info = prdct_info_c.find("span").text
                prdct_info=prdct_info.strip()
                print(prdct_info)

                model_no1 = prdct_info.split()
                model_no = model_no1[len(model_no1) - 1]
                model_no = model_no.upper()
                print(model_no)

                urun = urun_var_mi()
                if urun >= 0:
                    verilerial1(urun)
                else:
                    for c in range(0, len(model_no1)):
                        for d in range(0, len(model_no_s)):
                            if model_no1[c].casefold().find(model_no_s[d].casefold())==0  or model_no1[c].casefold().find(model_no_s2[0].casefold()) >= 0 or model_no1[c].casefold().find(model_no_s2[1].casefold())>=0 or model_no1[c].casefold().find(model_no_s2[2].casefold())>=0:
                                if c != 0:
                                    model_no = model_no1[c - 1]
                                    model_no = model_no.upper()
                                    print(model_no)
                                    urun = urun_var_mi()
                                    if urun >= 0:
                                        verilerial1(urun)
                                        model_no_check = True
                                check = True
                                break

                        if check == True:
                            break
                    check = False

                if model_no_check == False:
                    if marka.casefold() == "Asus".casefold():
                        for h in range(0, len(model_no1)):
                            if model_no1[h].casefold() == "Oled".casefold():
                                model_no = model_no1[h - 1]
                                model_no = model_no.upper()
                                print(model_no)
                                urun = urun_var_mi()
                                if urun >= 0:
                                    verilerial1(urun)

                    elif marka.casefold() == "Dell".casefold() or marka.casefold() == "Lenovo".casefold():
                        for h in range(0, len(model_no1)):
                            if model_no1[h].casefold() == "Gaming".casefold():
                                model_no = model_no1[h - 1]
                                model_no = model_no.upper()
                                print(model_no)
                                urun = urun_var_mi()
                                if urun >= 0:
                                    verilerial1(urun)

                    elif marka.casefold() == "Hp".casefold():
                        for h in range(0, len(model_no1)):
                            if model_no1[h].casefold() == "Victus".casefold():
                                model_no = model_no1[h - 1]
                                model_no = model_no.upper()
                                print(model_no)
                                urun = urun_var_mi()
                                if urun >= 0:
                                    verilerial1(urun)
            except Exception as e:
                print(e)
            finally:
                model_no_check = False


    def verilerial4(urun_id):
        try:
            price_cntnr = s2.find("span", attrs={"class": "price"})
            price_c = price_cntnr.find("span", attrs={"data-bind": "markupText:'currentPriceBeforePoint'"}).text
            price_c += ","
            price_c2 = price_cntnr.find("span", attrs={"data-bind": "markupText:'currentPriceAfterPoint'"}).text
            price_c2 += " TL"
            price = price_c + price_c2
            print("Fiyat - " + price)
            zero = 0
            for zero in range(0, len(price)):
                if price[zero] == ".":
                    break
            zero = 3 - zero
            zero_s = ""
            for k in range(0, zero):
                zero_s += "0"
            price = zero_s + price

            prdct_point = s2.find("a", attrs={"id": "productReviews"}).text
            prdct_point = prdct_point.replace(" ", "")
            prdct_point = prdct_point.replace("\n", "")
            prdct_point = prdct_point.replace("Henüzdeğerlendirilmemişİlksendeğerlendir", "0,0")
            print("Puan - " + prdct_point)

            ProductPricesPointsKayitEkle(urun_id, price, prdct_point, real_link)
            print(" ")
            return 0
        except Exception as e:
            print(e)
            return 1

    check = False
    model_no_check = False
    site_id = 3

    for page_value in range(1, 30):
        if page_value == 1:
            req = requests.get("", headers=header) ## site linki eklenmeli

        else:
            page_link = "&sayfa=" + str(page_value)
            req = requests.get("" + page_link,headers=header) ## site linki eklenmeli

        try:
            s = BeautifulSoup(req.content, "html.parser")
            prdct_cntnr = s.find("ul", attrs={"class": "productListContent-frGrtf5XrVXRwJ05HUfU"})
            prdcts = prdct_cntnr.find_all("li", attrs={"class": "productListContent-zAP0Y5msy8OHn5z7T_K_"})
        except Exception as e:
            print(e)
            break

        for links in prdcts:
            try:
                link = links.find("div", attrs={"class": "moria-ProductCard-joawUM"})
                link_end = link.a.get("href")

                if link_end[0] != "h":
                    link_head = ""  ## site linki eklenmeli
                    real_link = link_head + link_end

                else:
                    real_link = link_end
                print(real_link)

                req2 = requests.get(real_link, headers=header)
                s2 = BeautifulSoup(req2.content, "html.parser")

                prdct_info = s2.find("h1", attrs={"class": "product-name best-price-trick"}).text
                prdct_info = prdct_info.strip()
                print(prdct_info)

                model_no1 = prdct_info.split()
                marka = model_no1[0]
                model_no = model_no1[len(model_no1) - 1]
                model_no = model_no.upper()
                print(model_no)
                urun = urun_var_mi()
                if urun >= 0:
                    verilerial4(urun)
                else:
                    for c in range(0, len(model_no1)):
                        for d in range(0, len(model_no_s)):
                            if model_no1[c].casefold().find(model_no_s[d].casefold())==0  or model_no1[c].casefold().find(model_no_s2[0].casefold())>=0 or model_no1[c].casefold().find(model_no_s2[1].casefold())>=0 or model_no1[c].casefold().find(model_no_s2[2].casefold())>=0:
                                model_no = model_no1[c - 1]
                                model_no = model_no.replace("(", "")
                                model_no = model_no.replace(")", "")
                                model_no = model_no.upper()
                                print(model_no)
                                urun = urun_var_mi()
                                if urun >= 0:
                                    verilerial4(urun)
                                    model_no_check = True
                                check = True
                                break

                        if check == True:
                            break
                    check = False

                    if model_no_check == False:
                        if marka.casefold() == "Asus".casefold():
                            for h in range(0, len(model_no1)):
                                if model_no1[h].casefold() == "Oled".casefold():
                                    model_no = model_no1[h - 1]
                                    model_no = model_no.upper()
                                    print(model_no)
                                    urun = urun_var_mi()
                                    if urun >= 0:
                                        verilerial4(urun)

                        elif marka.casefold() == "Dell".casefold() or marka.casefold() == "Acer".casefold():
                            for h in range(0, len(model_no1)):
                                if model_no1[h].casefold() == "Taşınabilir".casefold():
                                    model_no = model_no1[h - 1]
                                    model_no = model_no.upper()
                                    print(model_no)
                                    urun = urun_var_mi()
                                    if urun >= 0:
                                        verilerial4(urun)
                    model_no_check = False

            except Exception as e:
                print(e)
                continue

            finally:
                model_no_check = False


    def verilerial5(urun_id):
        try:
            prdct_point_c = "0.0"
            print("Puan - " + prdct_point_c)

            price = s2.find("span", attrs={"class": "prc"}).text
            print("Fiyat - " + price)
            zero = 0
            for zero in range(0, len(price)):
                if price[zero] == ".":
                    break
            zero = 3 - zero
            zero_s = ""
            for k in range(0, zero):
                zero_s += "0"
            price = zero_s + price

            ProductPricesPointsKayitEkle(urun_id, price, prdct_point_c, real_link)
            print(" ")
            return 0
        except Exception as e:
            print(e)
            return 1

    model_no_s1 = "Model Kodu"
    check = False
    model_no_check = False
    site_id = 4

    for page_value in range(0, 10):
        if page_value == 0:
            req = requests.get("")  ## site linki eklenmeli
        else:
            page_link = "?s=%3Arelevance&page=" + str(page_value)
            req = requests.get("" + page_link)  ## site linki eklenmeli

        try:
            s = BeautifulSoup(req.content, "html.parser")
            prdct_cntnr = s.find("div", attrs={"class": "products"})
            prdcts = prdct_cntnr.find_all("div", attrs={"class": "prd"})
        except Exception as e:
            print(e)
            break

        for link in prdcts:
            try:
                link_end = link.a.get("href")
                link_head = ""  ## site linki eklenmeli
                real_link = link_head + link_end
                print(real_link)

                req2 = requests.get(real_link)
                s2 = BeautifulSoup(req2.content, "html.parser")

                prdct_info = s2.find("h1", attrs={"class": "pdp-title"}).text
                prdct_info = prdct_info.strip()
                print(prdct_info)

                table5 = s2.find("div", attrs={"class": "ptf-body"})
                attrs5 = table5.find_all("table")

                for attr5 in attrs5:
                    tr5 = attr5.find_all("tr")
                    labels5 = tr5[0].find_all("th")

                    for h in range(0, len(labels5)):
                        if labels5[h].text == model_no_s1:
                            values5 = tr5[1].find_all("td")
                            model_no = values5[h].text
                            model_no = model_no.upper()
                            print(model_no)
                            urun = urun_var_mi()
                            if urun >= 0:
                                verilerial5(urun)
                                model_no_check = True
                            check = True
                            break

                    if check == True:
                        break
                check = False

                if model_no_check == False:
                    model_no1 = prdct_info.split()
                    marka = model_no1[0]
                    model_no = model_no1[len(model_no1) - 1]
                    model_no = model_no.upper()
                    print(model_no)
                    urun = urun_var_mi()
                    if urun >= 0:
                        verilerial5(urun)
                    else:
                        for c in range(0, len(model_no1)):
                            for d in range(0, len(model_no_s)):
                                if model_no1[c].casefold().find(model_no_s[d].casefold())==0 or model_no1[c].casefold().find(model_no_s2[0].casefold())>=0 or model_no1[c].casefold().find(model_no_s2[1].casefold())>=0 or model_no1[c].casefold().find(model_no_s2[2].casefold())>=0:
                                    model_no = model_no1[c - 1]
                                    model_no = model_no.replace("(", "")
                                    model_no = model_no.replace(")", "")
                                    model_no = model_no.upper()
                                    print(model_no)
                                    urun = urun_var_mi()
                                    if urun >= 0:
                                        verilerial5(urun)
                                        model_no_check = True
                                    check = True
                                    break

                            if check == True:
                                break
                        check = False

                        if model_no_check == False:
                            if marka.casefold() == "Asus".casefold():
                                for h in range(0, len(model_no1)):
                                    if model_no1[h].casefold() == "Oled".casefold():
                                        model_no = model_no1[h - 1]
                                        model_no = model_no.upper()
                                        print(model_no)
                                        urun = urun_var_mi()
                                        if urun >= 0:
                                            verilerial5(urun)
                model_no_check = False

            except Exception as e:
                print(e)
                continue

            finally:
                model_no_check = False


    site_id = 5
    def verilerial3(urun_id):
        try:
            prdct_info_w3 = s2.find("div", attrs={"class": "product-list__content product-detail-big-price"})
            prdct_info = prdct_info_w3.find("h1", attrs={"class": "product-list__product-name"}).text
            prdct_info = prdct_info.replace("\n", "")
            prdct_info = prdct_info.strip()

            if prdct_info.split()[1] == "By" or prdct_info.split()[1] == "BY":
                marka = prdct_info.split()[2]

            else:
                marka = prdct_info.split()[0]

            if marka == "MacBook":
                marka = "Apple"

            print(prdct_info)

            price = s2.find("span", attrs={"class": "product-list__price"}).text
            print("Fiyat - " + price)
            zero = 0
            for zero in range(0, len(price)):
                if price[zero] == ".":
                    break
            zero = 3 - zero
            zero_s = ""
            for k in range(0, zero):
                zero_s += "0"
            price = zero_s + price

            p3 = s2.find("div", attrs={"class": "col-lg-8 col-md-8 col-sm-8 col-xs-12"})
            prdct_comment = p3.find("div", attrs={"class": "wrapper-star"})
            prdct_point = prdct_comment.find("strong", attrs={"id": "averageRankNum"}).text
            print("Puan - " + prdct_point)

            ProductPricesPointsKayitEkle(urun_id, price, prdct_point, real_link)
            print(" ")
            return 0
        except Exception as e:
            print(e)
            return 1

    for page_value in range(1, 9):
        if page_value == 1:
            req = requests.get("")  ## site linki eklenmeli

        else:
            page_link = "?page=" + str(page_value)
            req = requests.get("" + page_link)  ## site linki eklenmeli

        try:
            s = BeautifulSoup(req.content, "html.parser")
            prdct_cntnr = s.find("div", attrs={"class": "wrapper-product wrapper-product--list-page clearfix"})
            prdcts = prdct_cntnr.find_all("div", attrs={"class": "product-list product-list--list-page"})
        except Exception as e:
            print(e)
            break

        for link in prdcts:
            try:
                link_end = link.a.get("href")
                link_head = ""  ## site linki eklenmeli
                real_link = link_head + link_end
                print(real_link)

                req2 = requests.get(real_link)
                s2 = BeautifulSoup(req2.content, "html.parser")

                model_no1 = s2.find("div", attrs={"class": "product-list__product-code pull-left product-id"}).text
                model_no1 = model_no1.strip()
                model_no2 = model_no1.split(" / ")
                model_no = model_no2[0].replace("-Gaming","")
                model_no1=model_no.split()
                model_no=model_no1[len(model_no1)-1]
                model_no = model_no.upper()
                print(model_no)

                urun = urun_var_mi()
                if urun >= 0:
                    verilerial3(urun)

            except Exception as e:
                print(e)
                continue

    ##3 sitede ortak olan bilgisayarlar
    cursor.execute("SELECT UrunId FROM ProductPricesPoints GROUP BY UrunId HAVING Count(SiteId)=3")
    urun_idleri = cursor.fetchall()

    for ur in urun_idleri:
        cursor.execute("SELECT Fiyat,Puan FROM ProductPricesPoints WHERE UrunId=? ",ur[0])
        urun_fiyatlari = cursor.fetchall()

        cursor.execute("INSERT INTO ProductPricesPoints VALUES (?,?,?,'bm',6)", ur[0],urun_fiyatlari[0][0],urun_fiyatlari[0][1])
        cursor.commit()

else:
    cursor.execute("SELECT UrunId,Fiyat,SiteId,UrunLinki FROM ProductPricesPoints")
    urun_fiyatlari = cursor.fetchall()

    for urunler in urun_fiyatlari:
        if urunler[2]==1:
            try:
                print(urunler[3])
                req = requests.get(urunler[3])
                s = BeautifulSoup(req.content, "html.parser")

                stok=s.find("button", attrs={"type": "submit"}).get("class")

                if stok[0]=="addBasketUnify":
                    prdct_comment = s.find("div", attrs={"class": "ratingCont"})
                    prdct_point = prdct_comment.find("strong", attrs={"class": "ratingScore"}).text

                    cursor.execute("SELECT * FROM ProductAttributes WHERE UrunId=?", urunler[0])
                    urun_ozellikleri = cursor.fetchall()

                    link_end = ""
                    for k in range(1, 6):
                        if k == 5 or k == 4:
                            continue
                        link_end += urun_ozellikleri[0][k].replace(" ", "+") + "+"
                    link_end += "dizustu+bilgisayar"
                    link_head = "" ## site linki eklenmeli
                    real_link = link_head + link_end
                    print(real_link)

                    try:
                        req = requests.get(real_link)
                        s = BeautifulSoup(req.content, "html.parser")

                        prdct_cntnr2 = s.find("ul", attrs={"class": "list-ul"})
                        prdcts2 = prdct_cntnr2.find_all("li", attrs={"class": "column"})
                        real_link2 = prdcts2[0].a.get("href")
                        print(real_link2)

                        pro = prdcts2[0].find("div", attrs={"class": "pro"})
                        price_cntnr2 = pro.find("div", attrs={"class": "proDetail"})
                        price_c2 = price_cntnr2.find("span", attrs={"class": "newPrice"})
                        price2 = price_c2.find("ins").text
                        price2 = price2.strip()
                        print("Fiyat - " + price2)
                        zero = 0
                        for zero in range(0, len(price2)):
                            if price2[zero] == ".":
                                break
                        zero = 3 - zero
                        zero_s = ""
                        for k in range(0, zero):
                            zero_s += "0"
                        price2 = zero_s + price2

                        cursor.execute("UPDATE ProductPricesPoints SET Fiyat=?,Puan=?,UrunLinki=? WHERE UrunLinki=?",
                                      price2, prdct_point, real_link2, urunler[3])
                        cursor.commit()

                    except Exception as e:
                        print(e)
                        cursor.execute("DELETE ProductPricesPoints WHERE UrunLinki=?", urunler[3])
                        cursor.commit()

                else:
                    print("Urun stokta yok")
                    cursor.execute("DELETE ProductPricesPoints WHERE UrunLinki=?", urunler[3])
                    cursor.commit()

            except Exception as e:
                print(e)
                cursor.execute("DELETE ProductPricesPoints WHERE UrunLinki=?", urunler[3])
                cursor.commit()

        elif urunler[2]==2:
            try:
                print(urunler[3])
                req = requests.get(urunler[3])
                s = BeautifulSoup(req.content, "html.parser")

                price_cntnr = s.find("div", attrs={"class": "product-button-container"})
                price_c = price_cntnr.find_all("button")
                if price_c[0].get("class")[0]!="add-to-basket":
                    raise Exception

                price = s.find("span", attrs={"class": "prc-dsc"}).text
                price = price.strip()
                print("Fiyat 1 - " + price)
                zero = 0
                for zero in range(0, len(price)):
                    if price[zero] == ".":
                        break
                zero = 3 - zero
                zero_s = ""
                for k in range(0, zero):
                    zero_s += "0"
                price = zero_s + price

            except Exception as e:
                print("Urun stokta yok")
                cursor.execute("DELETE ProductPricesPoints WHERE UrunLinki=?", urunler[3])
                cursor.commit()
            else:
                try:
                    pro = s.find("div", attrs={"class": "pr-omc"})
                    pro_cntnr=pro.find("div", attrs={"class": "omc-cntr"})
                    li = pro_cntnr.find_all("div", attrs={"class": "pr-mc-w gnr-cnt-br"})
                    li1 = li[0].find("div", attrs={"class": "mc-ct-rght"})
                    price2=li1.find("span", attrs={"class": "prc-dsc"}).text
                    price2 = price2.strip()
                    link_son_c = li1.find("div", attrs={"class": "pr-om-lnk"})
                    link_son = link_son_c.a.get("href")
                    link_bas = ""  ## site linki eklenmeli
                    link = link_bas + link_son
                    print(link)

                    print("Fiyat 2 - " + price2)
                    zero = 0
                    for zero in range(0, len(price2)):
                        if price2[zero] == ".":
                            break
                    zero = 3 - zero
                    zero_s = ""
                    for k in range(0, zero):
                        zero_s += "0"
                    price2 = zero_s + price2

                    if price <= price2:
                        cursor.execute("UPDATE ProductPricesPoints SET Fiyat=? WHERE UrunLinki=?", price, urunler[3])
                        cursor.commit()
                    else:
                        cursor.execute("UPDATE ProductPricesPoints SET Fiyat=?,UrunLinki=? WHERE UrunLinki=?", price2,link,urunler[3])
                        cursor.commit()
                except Exception as e:
                    print(e)
                    cursor.execute("UPDATE ProductPricesPoints SET Fiyat=? WHERE UrunLinki=?", price, urunler[3])
                    cursor.commit()

        elif urunler[2] == 3:
            try:
                print(urunler[3])
                req = requests.get(urunler[3],headers=header)
                s = BeautifulSoup(req.content, "html.parser")

                prdct_point = s.find("a", attrs={"id": "productReviews"}).text
                prdct_point = prdct_point.replace(" ", "")
                prdct_point = prdct_point.replace("\n", "")
                prdct_point = prdct_point.replace("Henüzdeğerlendirilmemişİlksendeğerlendir", "0,0")

                price_cntnr = s.find("span", attrs={"class": "price"})
                price_c=price_cntnr.find("span", attrs={"data-bind": "markupText:'currentPriceBeforePoint'"}).text
                price_c+=","
                price_c2=price_cntnr.find("span", attrs={"data-bind": "markupText:'currentPriceAfterPoint'"}).text
                price_c2+=" TL"
                price=price_c+price_c2
                price = price.strip()
                print("Fiyat 1 - " + price)
                if price=="0,00 TL" or price=="0.00 TL":
                    raise Exception
                zero = 0
                for zero in range(0, len(price)):
                    if price[zero] == ".":
                        break
                zero = 3 - zero
                zero_s = ""
                for k in range(0, zero):
                    zero_s += "0"
                price = zero_s + price

            except Exception as e:
                print("Stok yok")
                cursor.execute("DELETE ProductPricesPoints WHERE UrunLinki=?", urunler[3])
                cursor.commit()
            else:
                try:
                    pro = s.find("div", attrs={"class": "marketplace-list"})
                    pro_c = pro.find("table")
                    tr = pro_c.find_all("tr")
                    td= tr[0].find_all("td")
                    price2=td[1].find("span", attrs={"class": "price-text"}).text
                    price2 = price2.strip()
                    magaza=td[0].find("div", attrs={"class": "merchant-info"})
                    magaza1=magaza.find("a").text
                    magaza1=magaza1.replace(" ","%20")
                    if magaza1=="":
                        raise Exception

                    link_son="?magaza="+magaza1
                    i=urunler[3].find("?magaza=")
                    if i>0:
                        link=urunler[3][:i]+link_son
                    else:
                        link =urunler[3]+link_son
                    print(link)

                    print("Fiyat 2 - " + price2)
                    zero = 0
                    for zero in range(0, len(price2)):
                        if price2[zero] == ".":
                            break
                    zero = 3 - zero
                    zero_s = ""
                    for k in range(0, zero):
                        zero_s += "0"
                    price2 = zero_s + price2

                    if price <= price2:
                        cursor.execute("UPDATE ProductPricesPoints SET Fiyat=?,Puan=? WHERE UrunLinki=?", price,prdct_point, urunler[3])
                        cursor.commit()
                    else:
                        cursor.execute("UPDATE ProductPricesPoints SET Fiyat=?,Puan=?,UrunLinki=? WHERE UrunLinki=?", price2,prdct_point,link,urunler[3])
                        cursor.commit()
                except Exception as e:
                    print("Urun tek magazada satiliyor.")
                    cursor.execute("UPDATE ProductPricesPoints SET Fiyat=?,Puan=? WHERE UrunLinki=?", price,prdct_point, urunler[3])
                    cursor.commit()

        elif urunler[2] == 4:
            print(urunler[3])
            try:
                req = requests.get(urunler[3])
                s = BeautifulSoup(req.content, "html.parser")
                price = s.find("span", attrs={"class": "prc"}).text
                price=price.strip()
                if price=="000":
                    raise Exception
                print("Fiyat 1 - "+price)
                zero = 0
                for zero in range(0, len(price)):
                    if price[zero] == ".":
                        break
                zero = 3 - zero
                zero_s = ""
                for k in range(0, zero):
                    zero_s += "0"
                price = zero_s + price
                if price=="000":
                    raise Exception

            except Exception as e:
                print("Stok yok")
                cursor.execute("DELETE ProductPricesPoints WHERE UrunLinki=?", urunler[3])
                cursor.commit()
            else:
                try:
                    pro = s.find("div", attrs={"class": "pdp-sellers-items"})
                    pro_c = pro.find_all("div", attrs={"class": "pds"})  ## active
                    tr = pro_c[0].find("div", attrs={"class": "pds-prices"})
                    td= s.find("div", attrs={"class": "pds-price2"})
                    price2=td.find("span", attrs={"class": "prc"}).text ## prc-last
                    price2 = price2.strip()
                    link_son=pro.find("div", attrs={"class": "pds"}).get("data-prod-seller-url") ## active
                    link_bas = ""  ## site linki eklenmeli
                    link = link_bas + link_son
                    print(link)

                    print("Fiyat 2 - " + price2)
                    zero = 0
                    for zero in range(0, len(price2)):
                        if price2[zero] == ".":
                            break
                    zero = 3 - zero
                    zero_s = ""
                    for k in range(0, zero):
                        zero_s += "0"
                    price2 = zero_s + price2

                    if price <= price2:
                        cursor.execute("UPDATE ProductPricesPoints SET Fiyat=? WHERE UrunLinki=?", price, urunler[3])
                        cursor.commit()
                    else:
                        cursor.execute("UPDATE ProductPricesPoints SET Fiyat=?,UrunLinki=? WHERE UrunLinki=?", price2,link,urunler[3])
                        cursor.commit()
                except Exception as e:
                    print(e)
                    cursor.execute("UPDATE ProductPricesPoints SET Fiyat=? WHERE UrunLinki=?", price, urunler[3])
                    cursor.commit()

        elif urunler[2] == 5:
            print(urunler[1])
            try:
                req = requests.get(urunler[3])
                s = BeautifulSoup(req.content, "html.parser")
                p3 = s.find("div", attrs={"class": "col-lg-8 col-md-8 col-sm-8 col-xs-12"})
                prdct_comment = p3.find("div", attrs={"class": "wrapper-star"})
                prdct_point = prdct_comment.find("strong", attrs={"id": "averageRankNum"}).text

                price = s.find("span", attrs={"class": "product-list__price"}).text
                price = price.strip()
                print("Fiyat 1 -" + price)
                zero = 0
                for zero in range(0, len(price)):
                    if price[zero] == ".":
                        break
                zero = 3 - zero
                zero_s = ""
                for k in range(0, zero):
                    zero_s += "0"
                price = zero_s + price

                cursor.execute("UPDATE ProductPricesPoints SET Fiyat=?,Puan=? WHERE UrunLinki=?", price, prdct_point, urunler[3])
                cursor.commit()

            except Exception as e:
                print(e)
                cursor.execute("DELETE ProductPricesPoints WHERE UrunLinki=?", urunler[3])
                cursor.commit()

database.close()