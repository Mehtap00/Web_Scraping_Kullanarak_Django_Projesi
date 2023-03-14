from django.shortcuts import render
from django.db import connection


def index(request):
    cursor = connection.cursor()
    cursor.execute("SELECT UrunId,Max(Puan) FROM ProductPricesPoints WHERE UrunId in(SELECT UrunId FROM ProductPricesPoints GROUP BY UrunId HAVING Count(UrunId)>=3) GROUP BY UrunId ORDER BY Max(Puan) desc")
    product_prices_points = cursor.fetchall()
    price = []
    attribute = []
    attributes = []
    link = ""
    link_head = "http://.../product"  ## link eklenmeli

    for p in range(0, len(product_prices_points)):
        link_end = str(product_prices_points[p][0])
        link = link_head + link_end

        cursor.execute("SELECT * FROM ProductAttributes WHERE UrunId=%s", [product_prices_points[p][0]])
        attrs = cursor.fetchall()
        for attr in range(0, len(attrs)):
            attribute.extend(attrs[attr])

        attribute.append(link)
        cursor.execute("SELECT * FROM ProductPricesPoints WHERE UrunId=%s ORDER BY Fiyat", [product_prices_points[p][0]])
        prs = cursor.fetchall()
        for pr in range(0, len(prs)):
            price.extend(prs[pr])
            cursor.execute("SELECT * FROM Website WHERE SiteId=%s", [prs[pr][4]])
            site = cursor.fetchall()
            price.append(site[0][1])
        attribute.extend(price)

        attributes += [attribute]
        attribute = []
        price = []

    cursor.close()

    context = {'attributes': attributes}

    return render(request, 'index.html', context)


def product(request, i):
    cursor = connection.cursor()

    price = []
    attribute = []
    attributes = []

    cursor.execute("SELECT * FROM ProductAttributes WHERE UrunId=%s", [int(i)])
    attrs = cursor.fetchall()
    for attr in range(0, len(attrs)):
        attribute.extend(attrs[attr])

    cursor.execute("SELECT * FROM ProductPricesPoints WHERE UrunId=%s ORDER BY Fiyat", [int(i)])
    prs = cursor.fetchall()
    for pr in range(0, len(prs)):
        price.extend(prs[pr])
        cursor.execute("SELECT * FROM Website WHERE SiteId=%s", [prs[pr][4]])
        site = cursor.fetchall()
        price.append(site[0][1])
    attribute.extend(price)

    attributes += [attribute]
    attribute = []
    price = []

    cursor.close()

    context = {'attributes': attributes, 'i': i}

    return render(request, 'product_detail.html', context)


def fiyata_gore_artan(request):
    cursor = connection.cursor()
    cursor.execute("SELECT UrunId,Min(Fiyat) FROM ProductPricesPoints WHERE UrunId in(SELECT UrunId FROM ProductPricesPoints GROUP BY UrunId HAVING Count(UrunId)>=3) GROUP BY UrunId ORDER BY Min(Fiyat)")
    product_prices_points = cursor.fetchall()
    price = []
    attribute = []
    attributes = []
    link = ""
    link_head = "http:/.../product"  ## link eklenmeli

    for p in range(0, len(product_prices_points)):
        link_end = str(product_prices_points[p][0])
        link = link_head + link_end

        cursor.execute("SELECT * FROM ProductAttributes WHERE UrunId=%s", [product_prices_points[p][0]])
        attrs = cursor.fetchall()
        for attr in range(0, len(attrs)):
            attribute.extend(attrs[attr])

        attribute.append(link)
        cursor.execute("SELECT * FROM ProductPricesPoints WHERE UrunId=%s ORDER BY Fiyat", [product_prices_points[p][0]])
        prs = cursor.fetchall()
        for pr in range(0, len(prs)):
            price.extend(prs[pr])
            cursor.execute("SELECT * FROM Website WHERE SiteId=%s", [prs[pr][4]])
            site = cursor.fetchall()
            price.append(site[0][1])
        attribute.extend(price)

        attributes += [attribute]
        attribute = []
        price = []

    cursor.close()

    context = {'attributes': attributes}

    return render(request, 'index.html', context)


def fiyata_gore_azalan(request):
    cursor = connection.cursor()
    cursor.execute("SELECT UrunId,Min(Fiyat) FROM ProductPricesPoints WHERE UrunId in(SELECT UrunId FROM ProductPricesPoints GROUP BY UrunId HAVING Count(UrunId)>=3) GROUP BY UrunId ORDER BY Min(Fiyat) desc")
    product_prices_points = cursor.fetchall()
    price = []
    attribute = []
    attributes = []
    link = ""
    link_head = "http://.../product"  ## link eklenmeli

    for p in range(0, len(product_prices_points)):
        link_end = str(product_prices_points[p][0])
        link = link_head + link_end

        cursor.execute("SELECT * FROM ProductAttributes WHERE UrunId=%s", [product_prices_points[p][0]])
        attrs = cursor.fetchall()
        for attr in range(0, len(attrs)):
            attribute.extend(attrs[attr])

        attribute.append(link)
        cursor.execute("SELECT * FROM ProductPricesPoints WHERE UrunId=%s ORDER BY Fiyat", [product_prices_points[p][0]])
        prs = cursor.fetchall()
        for pr in range(0, len(prs)):
            price.extend(prs[pr])
            cursor.execute("SELECT * FROM Website WHERE SiteId=%s", [prs[pr][4]])
            site = cursor.fetchall()
            price.append(site[0][1])
        attribute.extend(price)

        attributes += [attribute]
        attribute = []
        price = []

    cursor.close()

    context = {'attributes': attributes}

    return render(request, 'index.html', context)


def puana_gore_artan(request):
    cursor = connection.cursor()
    cursor.execute("SELECT UrunId,Max(Puan) FROM ProductPricesPoints WHERE UrunId in(SELECT UrunId FROM ProductPricesPoints GROUP BY UrunId HAVING Count(UrunId)>=3) GROUP BY UrunId ORDER BY Max(Puan)")
    product_prices_points = cursor.fetchall()
    price = []
    attribute = []
    attributes = []
    link = ""
    link_head = "http://.../product"  ## link eklenmeli

    for p in range(0, len(product_prices_points)):
        link_end = str(product_prices_points[p][0])
        link = link_head + link_end

        cursor.execute("SELECT * FROM ProductAttributes WHERE UrunId=%s", [product_prices_points[p][0]])
        attrs = cursor.fetchall()
        for attr in range(0, len(attrs)):
            attribute.extend(attrs[attr])

        attribute.append(link)
        cursor.execute("SELECT * FROM ProductPricesPoints WHERE UrunId=%s ORDER BY Fiyat", [product_prices_points[p][0]])
        prs = cursor.fetchall()
        for pr in range(0, len(prs)):
            price.extend(prs[pr])
            cursor.execute("SELECT * FROM Website WHERE SiteId=%s", [prs[pr][4]])
            site = cursor.fetchall()
            price.append(site[0][1])
        attribute.extend(price)

        attributes += [attribute]
        attribute = []
        price = []

    cursor.close()

    context = {'attributes': attributes}

    return render(request, 'index.html', context)
