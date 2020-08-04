import bstool
import pandas
import shapely
import os
import cv2


if __name__ == '__main__':

    image_dir = '/data/urban3d/v1/val/images'
    csv_df = pandas.read_csv('/data/urban3d/v0/val/urban3d_2048_roof_gt.csv')

    for image_name in os.listdir(image_dir):
        image_file = os.path.join(image_dir, image_name)
        image_basename = bstool.get_basename(image_name)

        img = cv2.imread(image_file)
 
        roof_masks = []
        for idx, row in csv_df[csv_df.ImageId == image_basename].iterrows():
            roof_polygon = shapely.wkt.loads(row.PolygonWKT_Pix)

            roof_mask = bstool.polygon2mask(roof_polygon)
            roof_masks.append(roof_mask)

        if len(roof_masks) == 0:
            continue
        
        img = bstool.draw_mask_boundary(img, roof_masks)
        bstool.show_image(img)