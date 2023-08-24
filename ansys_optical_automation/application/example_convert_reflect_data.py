import os
import tkinter as tk
from tkinter import filedialog

import numpy as np

# file = r"D:\Customer\Continental\Reflet\LAB_Anisotropic_BSDF_Surface (4)\test.txt"
#
# phi_list = []
# theta_list = []
# bsdf = []
# with open(file) as myfile:
#     for idx, line in enumerate(myfile):
#         if idx == 0:
#             phi_list = [float(item) for item in line.split()]
#         else:
#             line_content = [float(item) for item in line.split()]
#             theta_list.append(line_content[0])
#             bsdf.append(line_content[1:])
# def get_val(theta, phi):
#     theta_id = theta_list.index(theta)
#     phi_id = phi_list.index(phi)
#     return bsdf[theta_id][phi_id]
#
# theta_2d_ressampled, phi_2d_ressampled = np.meshgrid(np.array(theta_list), np.array(phi_list))
# bsdf_resample = []
# phi_temp = phi_2d_ressampled.reshape(-1)
# theta_temp = theta_2d_ressampled.reshape(-1)
# for idx, item in enumerate(phi_temp):
#     bsdf_resample.append(get_val(theta_temp[idx],phi_temp[idx]))
#
# bsdf_resample = np.array(bsdf_resample)
# bsdf_resample = bsdf_resample.reshape(np.shape(theta_2d_ressampled)[0], np.shape(theta_2d_ressampled)[1])
# print(np.shape(bsdf_resample), np.shape(theta_2d_ressampled))
# # samples on which integrande is known
# theta_rad, phi_rad = np.radians(theta_2d_ressampled), np.radians(phi_2d_ressampled)
# integrande = (1 / math.pi) * bsdf_resample * np.sin(theta_rad)  # *theta for polar integration
# f = interpolate.interp2d(theta_rad, phi_rad, integrande, kind="linear", bounds_error=False, fill_value=0)
# # calculation of integrande as from samples
# r = nquad(f, [[0, math.pi / 2], [0, 2 * math.pi]], opts=[{"epsabs": 0.1}, {"epsabs": 0.1}])
# print(r)

# x = np.linspace(-5, 5, 5)
# y = np.linspace(-4, 4, 5)
# X, Y = np.meshgrid(x, y)
# print(X, Y)
# Z = Y**2 + X**2
# print(Z)


def getfilepath():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    return folder_selected


def read_reflect_data(file):
    flg = False
    phi_step = 0
    in_theta_list = []
    in_bsdf = []
    with open(file) as myfile:
        for line in myfile:
            if "Phi measure step" in line:
                phi_step = float(line.split(":")[1])
                continue
            if "Theta Lighting" in line:
                flg = True
                continue
            if flg is True:
                content = [float(item) for item in line.split()]
                in_theta_list.append(content[0])
                in_bsdf.append(content[1:])
    in_phi_list = np.arange(-90, 90 + phi_step, phi_step).tolist()
    out_theta_list = [item for item in in_theta_list if item >= 0]
    out_phi_list = np.arange(0, 360 + phi_step, phi_step).tolist()
    return in_theta_list, in_phi_list, out_theta_list, out_phi_list, in_bsdf


def coordinate_convert(o_theta, o_phi):
    i_phi = 0
    i_theta = 0
    if o_phi <= 90 or o_phi >= 270:
        i_theta = -o_theta
        i_phi = o_phi if o_phi <= 90 else o_phi - 360
    else:
        i_theta = o_theta
        i_phi = o_phi - 180
    return i_theta, i_phi


def convert_bsdf(out_theta_list, out_phi_list, in_theta_list, in_phi_list, in_bsdf):
    def get_val(theta, phi):
        return in_bsdf[in_theta_list.index(theta)][in_phi_list.index(phi)]

    out_bsdf = []
    for o_theta in out_theta_list:
        out_bsdf_list = []
        for o_phi in out_phi_list:
            i_theta, i_phi = coordinate_convert(o_theta, o_phi)
            o_bsdf = get_val(i_theta, i_phi)
            # print(i_theta, i_phi, o_theta, o_phi, o_bsdf)
            out_bsdf_list.append(o_bsdf)
        out_bsdf.append(out_bsdf_list)
    return out_bsdf


def write_header(incident_file_list, file_out):
    file_out.write("OPTIS - Anisotropic BSDF surface file v7.0\n")
    file_out.write("0\n")
    file_out.write("Comment\n")
    file_out.write("23\n")
    file_out.write("Measurement description\n")
    file_out.write("1\t0\t0\n")
    file_out.write("1\t0\n")
    file_out.write("0\n")
    file_out.write("1\n")
    file_out.write("0\n")
    file_out.write(str(len(incident_file_list)) + "\n")
    content = "\t".join(
        [
            str(float(os.path.splitext(os.path.basename(incident_file).split("_")[4])[0]) / 10)
            for incident_file in incident_file_list
        ]
    )
    file_out.write(content + "\n")
    file_out.write("6\t0\n\n")
    file_out.write("2\n")
    file_out.write("350\t92.4711\n")
    file_out.write("850\t92.4711\n")


def write_out(bsdf, out_theta_list, out_phi_list, file_out):
    separator = "\t"
    file_out.write(str(len(out_theta_list)) + "\t" + str(len(out_phi_list)) + "\n")
    content = separator.join("{:.2f}".format(item) for item in out_phi_list) + "\n"
    file_out.write(content)
    for bsdf_idx, bsdf_line in enumerate(bsdf):
        content = "{:.3f}".format(out_theta_list[bsdf_idx]) + "\t"
        content += separator.join("{:.8f}".format(item) for item in bsdf_line) + "\n"
        file_out.write(content)


def main():
    reflect_dir = getfilepath()
    groups = {}
    for filename in os.listdir(reflect_dir):
        # if filename == "LightTools_Export3_0_BRDF_800.txt":
        if filename.endswith("txt") and "LightTools" in filename:
            orientation = filename.split("_")[2]
            if not orientation.isnumeric():
                continue
            if orientation not in groups:
                groups[orientation] = []
            groups[orientation].append(os.path.join(reflect_dir, filename))

    for group in groups:
        out_file = os.path.join(reflect_dir, "out_" + group + ".anisotropicbsdf")
        if os.path.isfile(out_file):
            os.remove(out_file)
        file_out = open(out_file, "a")
        write_header(groups[group], file_out)
        for file_dir in groups[group]:
            in_theta_list, in_phi_list, out_theta_list, out_phi_list, in_bsdf = read_reflect_data(file_dir)
            out_bsdf = convert_bsdf(out_theta_list, out_phi_list, in_theta_list, in_phi_list, in_bsdf)
            write_out(out_bsdf, out_theta_list, out_phi_list, file_out)
        file_out.write("End of file\n")
        file_out.close()


main()