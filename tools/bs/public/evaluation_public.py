import bstool
import csv

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
            'bc_v100.02.01_offset_rcnn_r50_2x_public_20201028_rotate_offset_4_angles',
            'bc_v100.02.02_offset_rcnn_r50_2x_public_20201028_rotate_offset_4_angles_decouple'
            ]

if __name__ == '__main__':
    models = [model for model in ALL_MODELS[1:] if 'v100.01.07' in model]
    cities = ['dalian', 'xian']

    with_only_vis = False
    with_offset = True
    save_merged_csv = True

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
            
            if city == 'xian':
                anno_file = f'./data/buildchange/v1/coco/annotations/buildchange_v1_val_xian_fine.json'
                gt_roof_csv_file = './data/buildchange/public/xian_val_roof_crop1024_gt_minarea100.csv'
                gt_footprint_csv_file = './data/buildchange/public/xian_val_footprint_crop1024_gt_minarea100.csv'
                image_dir = f'./data/buildchange/v0/xian_fine/images'
            else:
                raise NotImplementedError("do not support city: ", city)

            if 'xian' in city:
                pkl_file = f'../mmdetv2-bc/results/buildchange/{model}/{model}_xian_coco_results.pkl'
            elif 'dalian' in city:
                pkl_file = f'../mmdetv2-bc/results/buildchange/{model}/{model}_dalian_coco_results.pkl'
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
                                        show=True,
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
                evaluation.visualization_boundary(image_dir=image_dir, vis_dir=vis_boundary_dir)
                for with_footprint in [True, False]:
                    evaluation.visualization_offset(image_dir=image_dir, vis_dir=vis_offset_dir, with_footprint=with_footprint)

            else:
                evaluation.visualization_boundary(image_dir=image_dir, vis_dir=vis_boundary_dir)
                for with_footprint in [True, False]:
                    evaluation.visualization_offset(image_dir=image_dir, vis_dir=vis_offset_dir, with_footprint=with_footprint)