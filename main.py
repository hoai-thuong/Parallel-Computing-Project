from PIL import Image, ImageDraw
#pip install Pillow     

# Đọc ảnh và chuyển sang ảnh xám
image = Image.open('/Users/hoaithuong/Desktop/haha.png').convert('L')
width, height = image.size

# Chuyển thành mảng numpy
image_array = list(image.getdata())
image_array = [image_array[offset:offset + width] for offset in range(0, width * height, width)]

# Thang độ xám
threshold = 128  # Ngưỡng để tách nền và ký tự
binary_image = [[0 if pixel < threshold else 255 for pixel in row] for row in image_array]

# Tìm ký tự bằng cách xác định vùng chứa
def find_contours(image_array, width, height):
    contours = []
    for y in range(height):
        for x in range(width):
            if image_array[y][x] == 0:  # Điểm đen (ký tự)
                x0, x1, y0, y1 = x, x, y, y
                stack = [(x, y)]

                while stack:
                    px, py = stack.pop()
                    if px >= 0 and px < width and py >= 0 and py < height and image_array[py][px] == 0:
                        image_array[py][px] = 255
                        x0, x1 = min(x0, px), max(x1, px)
                        y0, y1 = min(y0, py), max(y1, py)
                        stack.extend(((px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)))

                if x1 - x0 > 10 and y1 - y0 > 10:  # Điều kiện để loại bỏ các vùng nhỏ
                    contours.append((x0, y0, x1, y1))

    return contours

contours = find_contours(binary_image, width, height)

# Sắp xếp các vùng chứa theo thứ tự từ trái sang phải, từ trên xuống dưới
contours.sort(key=lambda c: (c[0], c[1]))
# Vẽ khung xung quanh ký tự trên ảnh gốc
draw = ImageDraw.Draw(image)
for x0, y0, x1, y1 in contours:
    char_image = image.crop((x0, y0, x1, y1))  # Tạo ảnh con chứa ký tự
    if char_image.getbbox() is not None:  # Kiểm tra xem có ký tự trong ảnh không
        draw.rectangle([(x0, y0), (x1, y1)], outline='green')


image_with_boxes = Image.open('/Users/hoaithuong/Desktop/haha.png')
draw = ImageDraw.Draw(image_with_boxes)
for x0, y0, x1, y1 in contours:
    draw.rectangle([x0, y0, x1, y1], outline='green')
# Lưu ảnh gốc với khung xung quanh ký tự
image.save('hinh_anh_khung.png')

# Hiển thị ảnh gốc với khung xung quanh ký tự
image.show()
# Lấy từng ký tự và lưu thành ảnh riêng biệt theo thứ tự
for i, (x0, y0, x1, y1) in enumerate(contours):
    char_image = image.crop((x0, y0, x1, y1))  # Tạo ảnh con chứa ký tự
    filename = f'ky_tu_{i}.png'
    char_image.save(filename)  # Lưu ảnh con chứa ký tự ra tệp

# Hiển thị ảnh gốc với khung xung quanh ký tự
image.show()

