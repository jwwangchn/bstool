import bstool
import csv
import argparse


def write_results2csv(results, meta_info=None):
    print("meta_info: ", meta_info)
    segmentation_eval_results = results[0]
    with open(meta_info['summary_file'], 'w') as summary:
        csv_writer = csv.writer(summary, delimiter=',')
        csv_writer.writerow(['Meta Info'])
        csv_writer.writerow(['model', meta_info['model']])
        csv_writer.writerow(['anno_file', meta_info['anno_file']])
        csv_writer.writerow(['gt_roof_csv_file', meta_info['gt_roof_csv_file']])
        csv_writer.writerow(['gt_footprint_csv_file', meta_info['gt_footprint_csv_file']])
        csv_writer.writerow(['vis_dir', meta_info['vis_dir']])
        csv_writer.writerow([''])
        for mask_type in ['roof', 'footprint']:
            csv_writer.writerow([mask_type])
            csv_writer.writerow([segmentation_eval_results[mask_type]])
            csv_writer.writerow(['F1 Score', segmentation_eval_results[mask_type]['F1_score']])
            csv_writer.writerow(['Precision', segmentation_eval_results[mask_type]['Precision']])
            csv_writer.writerow(['Recall', segmentation_eval_results[mask_type]['Recall']])
            csv_writer.writerow(['True Positive', segmentation_eval_results[mask_type]['TP']])
            csv_writer.writerow(['False Positive', segmentation_eval_results[mask_type]['FP']])
            csv_writer.writerow(['False Negative', segmentation_eval_results[mask_type]['FN']])
            csv_writer.writerow([''])

        csv_writer.writerow([''])

ALL_MODELS = [
            'bc_v100.01.01_offset_rcnn_r50_1x_public_20201027_baseline',
            'bc_v100.01.02_offset_rcnn_r50_1x_public_20201027_lr0.01',
            'bc_v100.01.03_offset_rcnn_r50_1x_public_20201028_lr_0.02',
            'bc_v100.01.04_offset_rcnn_r50_2x_public_20201028_lr_0.02',
            'bc_v100.01.05_offset_rcnn_r50_2x_public_20201028_sample_num',
            'bc_v100.01.06_offset_rcnn_r50_3x_public_20201028_lr_0.02',
            'bc_v100.01.07_offset_rcnn_r50_2x_public_20201027_lr_0.02',
            'bc_v100.01.08_offset_rcnn_r50_2x_public_20201028_footprint_bbox_footprint_mask_baseline',
            'bc_v100.01.09_offset_rcnn_r50_2x_public_20201028_building_bbox_footprint_mask_baseline',
            'bc_v100.01.10_offset_rcnn_r50_2x_public_20201028_footprint_bbox_footprint_mask_baseline_no_aug',
            'bc_v100.01.11_offset_rcnn_r50_2x_public_20201028_building_bbox_footprint_mask_baseline_no_aug',
            'bc_v100.01.12_offset_rcnn_r50_1x_public_20201028_footprint_bbox_footprint_mask_baseline_simple',
            'bc_v100.02.01_offset_rcnn_r50_2x_public_20201028_rotate_offset_4_angles',
            'bc_v100.02.02_offset_rcnn_r50_2x_public_20201028_rotate_offset_4_angles_decouple',
            'bc_v100.02.03_offset_rcnn_r50_2x_public_20201028_rotate_offset_4_angles_minarea_500',
            'bc_v100.02.04_offset_rcnn_r50_2x_public_20201028_rotate_offset_4_angles_arg',
            'bc_v100.03.01_semi_offset_rcnn_r50_2x_public_20201028_arg_pretrain',
            'bc_v100.03.02_semi_offset_rcnn_r50_2x_public_20201028_real_semi',
            'bc_v100.03.03_semi_offset_rcnn_r50_2x_public_20201028_real_semi_resume',
            'bc_v100.03.04_semi_offset_rcnn_r50_2x_public_20201028_arg_pretrain_lr0.01',
            'bc_v100.03.05_semi_offset_rcnn_r50_2x_public_20201028_real_semi_lr0.02',
            'bc_v100.03.06_semi_offset_rcnn_r50_2x_public_20201028_arg_pretrain_4x',
            'bc_v100.03.07_semi_offset_rcnn_r50_2x_public_20201028_real_semi_lr0.02_arg_google',
            'bc_v100.03.09_semi_offset_rcnn_r101_2x_public_20201028_arg_pretrain_resnet101',
            'bc_v100.03.10_offset_rcnn_r50_2x_public_20201028_footprint_bbox_footprint_mask_baseline_arg',
            'bc_v100.03.11_semi_offset_rcnn_r50_2x_public_20201028_arg_pretrain_no_footprint',
            'bc_v100.03.12_semi_offset_rcnn_r50_2x_public_20201028_real_semi_lr0.02_finetune_03.11',
            'bc_v100.03.13_semi_offset_rcnn_r50_2x_public_20201028_full_data',
            'bc_v100.03.14_semi_offset_rcnn_r50_2x_public_20201028_full_data_no_footprint',
            'bc_v100.03.15_semi_offset_rcnn_r50_2x_public_20201028_full_data_iou_loss'
            ]

def parse_args():
    parser = argparse.ArgumentParser(
        description='MMDet eval on semantic segmentation')
    parser.add_argument(
        '--version',
        type=str,
        default='v100.03.13', 
        help='dataset for evaluation')

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = parse_args()

    models = [model for model in ALL_MODELS[0:] if args.version in model]
    # cities = ['shanghai_public', 'xian_public']
    cities = ['xian_public']
    # cities = ['xian_public', 'shanghai_public']
    
    with_vis = False
    with_only_vis = False
    with_offset = True
    save_merged_csv = False

    if save_merged_csv:
        csv_info = 'merged'
    else:
        csv_info = 'splitted'

    for model in models:
        version = model.split('_')[1]
        score_threshold = 0.4

        for city in cities:
            print(f"========== {model} ========== {city} ==========")

            output_dir = f'./data/buildchange/statistic/{model}/{city}'
            bstool.mkdir_or_exist(output_dir)
            vis_boundary_dir = f'./data/buildchange/vis/{model}/{city}/boundary'
            bstool.mkdir_or_exist(vis_boundary_dir)
            vis_offset_dir = f'./data/buildchange/vis/{model}/{city}/offset'
            bstool.mkdir_or_exist(vis_offset_dir)
            summary_file = f'./data/buildchange/summary/{model}/{model}_{city}_eval_summary_{csv_info}.csv'
            bstool.mkdir_or_exist(f'./data/buildchange/summary/{model}')
            
            if city == 'xian_public':
                anno_file = f'./data/buildchange/public/20201028/coco/annotations/buildchange_public_20201028_val_xian_fine.json'
                gt_roof_csv_file = './data/buildchange/public/20201028/xian_val_roof_crop1024_gt_minarea500.csv'
                gt_footprint_csv_file = './data/buildchange/public/20201028/xian_val_footprint_crop1024_gt_minarea500.csv'
                image_dir = f'./data/buildchange/public/20201028/xian_fine/images'
            elif city == 'shanghai_public':
                anno_file = f'./data/buildchange/public/20201028/coco/annotations/buildchange_public_20201028_val_shanghai_fine_minarea_500.json'
                gt_roof_csv_file = './data/buildchange/public/20201028/shanghai_val_v2_roof_crop1024_gt_minarea500.csv'
                gt_footprint_csv_file = './data/buildchange/public/20201028/shanghai_val_v2_footprint_crop1024_gt_minarea500.csv'
                image_dir = f'./data/buildchange/public/20201028/shanghai_fine/images'
            else:
                raise NotImplementedError("do not support city: ", city)

            if 'xian' in city:
                pkl_file = f'../mmdetv2-bc/results/buildchange/{model}/{model}_{city}_coco_results.pkl'
            elif 'shanghai' in city:
                pkl_file = f'../mmdetv2-bc/results/buildchange/{model}/{model}_{city}_coco_results.pkl'
            else:
                raise NotImplementedError("do not support city: ", city)
            
            roof_csv_file = f'../mmdetv2-bc/results/buildchange/{model}/{model}_{city}_roof_{csv_info}.csv'
            rootprint_csv_file = f'../mmdetv2-bc/results/buildchange/{model}/{model}_{city}_footprint_{csv_info}.csv'

            evaluation = bstool.Evaluation(model=model,
                                        anno_file=anno_file,
                                        pkl_file=pkl_file,
                                        gt_roof_csv_file=gt_roof_csv_file,
                                        gt_footprint_csv_file=gt_footprint_csv_file,
                                        roof_csv_file=roof_csv_file,
                                        rootprint_csv_file=rootprint_csv_file,
                                        iou_threshold=0.1,
                                        score_threshold=score_threshold,
                                        output_dir=output_dir,
                                        with_offset=with_offset,
                                        show=False,
                                        save_merged_csv=save_merged_csv)

            title = city + version
            if with_only_vis is False:
                # evaluation
                segmentation_eval_results = evaluation.segmentation()
                meta_info = dict(summary_file=summary_file,
                                 model=model,
                                 anno_file=anno_file,
                                 gt_roof_csv_file=gt_roof_csv_file,
                                 gt_footprint_csv_file=gt_footprint_csv_file,
                                 vis_dir=vis_boundary_dir)
                write_results2csv([segmentation_eval_results], meta_info)

                # vis
                if with_vis:
                    evaluation.visualization_boundary(image_dir=image_dir, vis_dir=vis_boundary_dir)
                    for with_footprint in [True, False]:
                        evaluation.visualization_offset(image_dir=image_dir, vis_dir=vis_offset_dir, with_footprint=with_footprint)
            else:
                evaluation.visualization_boundary(image_dir=image_dir, vis_dir=vis_boundary_dir)
                for with_footprint in [True, False]:
                    evaluation.visualization_offset(image_dir=image_dir, vis_dir=vis_offset_dir, with_footprint=with_footprint)
