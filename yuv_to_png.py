import numpy as np
import scipy.misc as smp
from PIL import Image

kek = 0


def to_data_1(x):
    if x > 0:
        return x
    return 0


def to_data_2(x):
    if x < 0:
        return abs(x)
    return 0


def read_shifted_img(shift):
    data1 = np.zeros((1080, 1920, 3), dtype=np.int32)
    data2 = np.zeros((1080, 1920, 3), dtype=np.int32)
    for y in range(1080):
        for x in range(1920):
            data1[y, x] = [to_data_1(vals[x + y * 1920] >> shift),
                           to_data_1(vals[x + y * 1920 + (1919 + 1079 * 1920)] >> shift),
                           to_data_1(vals[x + y * 1920 + (1919 + 1079 * 1920) * 2] >> shift)]
            data2[y, x] = [to_data_2(vals[x + y * 1920]) >> shift,
                           to_data_2(vals[x + y * 1920 + (1919 + 1079 * 1920)]) >> shift,
                           to_data_2(vals[x + y * 1920 + (1919 + 1079 * 1920) * 2]) >> shift]
    return data1, data2


kek_val = ["1_parsing", "2_tco_image_shift_all", "3_tco_image_apply_partial_idwt_hor",
           "4_tco_image_apply_partial_idwt_hor_2", "5_tco_image_apply_partial_idwt_ver", "6_tco_image_apply_irct",
           "7_tco_image_apply_offset", "8_tco_image_shift_all", "9_tco_image_clamp"]
for kek in range(len(kek_val)):
    f = open("yuv/" + str(kek + 1) + ".yuv", "r")
    vals = np.fromfile(f, dtype=np.int32)
    print(vals)
    np.set_printoptions(formatter={'int': hex})
    for shift in range(0, 32, 8):
        data1, data0 = read_shifted_img(shift)
        print("data1:", data1, data0)
        img = Image.fromarray(data0.astype(np.uint8))  # Create a PIL image
        # img.show()  # View in default viewer
        img.save("png/" + kek_val[kek] + "/" + "pos_" + str(shift) + ".png")
        img = Image.fromarray(data1.astype(np.uint8))  # Create a PIL image
        img.save("png/" + kek_val[kek] + "/" + "neg_" + str(shift) + ".png")
        # img.show()  # View in default viewer
