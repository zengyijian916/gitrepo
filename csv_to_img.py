import csv
import binascii
from PIL import Image, ImageDraw, ImageFont
import textwrap
import glob

# the part to modify
data_to_process_path = 'data_to_process'

# variable initialization
dt_csv = glob.glob(data_to_process_path + '/' + '*.csv')
dt_csv = dt_csv[0]
dt_txt = dt_csv.replace('.csv','.txt')

# FROM CSV TO TXT
with open(dt_csv, 'r') as f_in, open(dt_txt, 'w') as f_out:
    csvreader = csv.reader(f_in)
    for i, line in enumerate(csvreader):
        line_content = (' <> ').join(line)
        if len(line_content)>0:
            line_content = line_content.encode()
            line_content = binascii.b2a_hex(line_content)
            print(line_content)
            line_content = int(line_content, 16)
            line_content = str(line_content)
            f_out.write(line_content)
        f_out.write('\n')
f_in.close()
f_out.close()

# FROM TXT TO img
with open(dt_txt, 'r') as f_in:
    txtreader = f_in.readlines()
    img_string_old = ''
    i = 0
    for j, line_content in enumerate(txtreader):
        print(line_content)
        if len(line_content) >= 3000:
            print('one row is too long and exceeds 3000 digits')
            break
        line_content = line_content.replace(' ','').replace('\n','') + ' 0000000000 '
        img_string_new = img_string_old + line_content
        print(img_string_old)
        if len(img_string_new) < 3000:
            img_string_old = img_string_new
            continue
        else:
            fnt = ImageFont.truetype('arial.ttf', 30)
            w, h = 1800, 1200
            image = Image.new(mode="RGB", size=(w,h), color='white')
            draw = ImageDraw.Draw(image)
            img_string_old = img_string_old.replace(' ','').replace('\n','')
            img_string_old = textwrap.fill(text=img_string_old, width=95)
            # print(img_string_old)
            i = i + 1
            l, t = 30, 30
            w, h = w-30, h-30
            draw.rectangle([(l,t), (w,h)], outline='blue', width=5)
            draw.text((l+50, t+60), img_string_old, font=fnt, fill='black')
            file_name = f'{data_to_process_path}/{str(i).zfill(3)}.png'
            image.save(file_name)
            img_string_old = line_content
f_in.close()