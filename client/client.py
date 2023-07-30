import socket
from PIL import Image
from time import sleep
HOST = '127.0.0.1'
PORT = 6009


def genData(data):
    newd = []
    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd


def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if (pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if (pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)
    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1


def encode(text):
    image = Image.open("input.png", 'r')
    data = text
    if (len(data) == 0):
        raise ValueError('DATA IS EMPTY')
    newimg = image.copy()
    encode_enc(newimg, data)
    new_img_name = "Encoded.png"
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print("CONNECTION ESTABLISHED SUCCESSFULLY - ", HOST)
    client.send(b'IMAGE')
    file = open('Encoded.png', 'rb')
    sleep(1)
    image_data = file.read(2048)
    while image_data:
        client.sendall(image_data)
        image_data = file.read(2048)
    file.close()
    print("KEY HAS BEEN ENCRYPTED SUCCESSFULLY AND SENDING IMAGE TO SERVER....")
    print("***IMAGE SENT TO SERVER***")
    client.close()
    sleep(1)


def decode():
    img = "server_copy.png"
    image = Image.open(img, 'r')

    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]

        binstr = ''
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data


def main():
    while True:
        print()
        print("1.ENCODE")
        print("2.DECODE")

        a = int(input("ENTER YOUR CHOICE : "))

        if (a == 1):
            text = input("Enter the KEY : ")
            encode(text)

        if (a == 2):

            print("*** RECEIVING IMAGE FROM SERVER ***")
            client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client2.connect((HOST, PORT))
            client2.send(b'SENDIMAGE')
            image = client2.recv(2050)
            file = open('server_copy.png', 'wb')
            while image:
                file.write(image)
                image = client2.recv(2050)
            file.close()
            client2.close()
            print("IMAGE RECEIVED 'server.png'")
            print("DECODED WORD : " + decode())
            print()
            print()
            print("*** PROCESS TERMINATED AT CLIENT SIDE ***")
            quit()


if __name__ == '__main__':
    main()
