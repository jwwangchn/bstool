import os
import bstool


if __name__ == '__main__':

    sub_folds = ['arg', 'google', 'ms']

    for sub_fold in sub_folds:
        image_dir = '/home/jwwangchn/Documents/Nutstore/100-Work/110-Projects/2020-BS/01-CVPR/01-绘图/01-不同时间拍摄的图像'

        rgb_file = os.path.join(image_dir, f'{sub_fold}_L18_106968_219488.jpg')

        # shp_file = '/data/buildchange/v0/shanghai/shp_4326/L18_106968_219320.shp'
        shp_file = '/data/buildchange/v0/shanghai/merged_shp/_L18_106968_219488.shp'
        geo_file = '/data/buildchange/v0/shanghai/geo_info/_L18_106968_219488.png'
        rgb_file = '/data/buildchange/v0/shanghai/images/_L18_106968_219488.jpg'

        objects = bstool.shp_parse(shp_file=shp_file,
                                    geo_file=geo_file,
                                    src_coord='4326',
                                    dst_coord='pixel')

        polygons = [obj['polygon'] for obj in objects]
        masks = [obj['mask'] for obj in objects]
        bboxes = [obj['bbox'] for obj in objects]

        bstool.show_polygon(polygons)
        bstool.show_masks_on_image(rgb_file, masks)
        bstool.show_bboxs_on_image(rgb_file, bboxes)