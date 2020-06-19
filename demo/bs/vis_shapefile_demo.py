import bstool


if __name__ == '__main__':
    # shp_file = '/data/buildchange/v0/shanghai/shp_4326/L18_106968_219320.shp'
    shp_file = '/data/buildchange/v0/shanghai/merged_shp/L18_106968_219320.shp'
    geo_file = '/data/buildchange/v0/shanghai/geo_info/L18_106968_219320.png'
    rgb_file = '/data/buildchange/v0/shanghai/images/L18_106968_219320.jpg'

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