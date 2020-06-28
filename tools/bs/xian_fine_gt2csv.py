import os
import bstool
import numpy as np
import rasterio as rio
import cv2
import pandas
import glob


if __name__ == '__main__':
    sub_folds = ['arg', 'google', 'ms']

    csv_file = './data/buildchange/v0/xian_fine/xian_fine_2048_gt.csv'
    first_in = True

    for sub_fold in sub_folds:
        shp_dir = f'./data/buildchange/v0/xian_fine/{sub_fold}/merged_shp'
        rgb_img_dir = f'./data/buildchange/v0/xian_fine/{sub_fold}/images'

        shp_file_list = glob.glob("{}/*.shp".format(shp_dir))
        for shp_file in shp_file_list:
            base_name = bstool.get_basename(shp_file)

            rgb_img_file = os.path.join(rgb_img_dir, base_name + '.jpg')

            objects = bstool.shp_parse(shp_file=shp_file,
                                        geo_file=rgb_img_file,
                                        src_coord='pixel',
                                        dst_coord='pixel',
                                        keep_polarity=False)

            gt_polygons = [obj['polygon'] for obj in objects]

            csv_image = pandas.DataFrame({'ImageId': base_name,
                                          'BuildingId': range(len(gt_polygons)),
                                          'PolygonWKT_Pix': gt_polygons,
                                          'Confidence': 1})
            if first_in:
                csv_dataset = csv_image
                first_in = False
            else:
                csv_dataset = csv_dataset.append(csv_image)

    csv_dataset.to_csv(csv_file, index=False)