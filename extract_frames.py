import os
import cv2
import json
import argparse

def main(args):
    
    if not args.train and not args.bench:
        print("No dataset is selected... Please add --train or --bench option to your command.")
        return

    # Extract STATUS Train images
    if args.train:
        print("Start to extract STATUS Train...")

        with open("Train/STATUS_Train.json", "r") as f:
            train_list = json.load(f)
        
        train_image_dir = "Train/images"
        os.makedirs(train_image_dir, exist_ok=True)
        
        for sample in train_list:
            video_path = os.path.join(args.ego4d_dir, sample["video_id"]+".mp4")
            out_path = os.path.join(train_image_dir, sample["image_id"]+".png")
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise RuntimeError("Fail to open the video (video_id: {})".format(sample["video_id"]))

            cap.set(cv2.CAP_PROP_POS_FRAMES, sample["frame"])
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(out_path, frame)
            else:
                raise RuntimeError("Fail to read the frame (video_id: {}, frame_number: {})".format(sample["video_id"], sample["frame"]))
    
    if args.bench:
        print("Start to extract STATUS Bench...")

        with open("Bench/STATUS_Bench.json", "r") as f:
            bench_list = json.load(f)
        
        bench_image_dir = "Bench/images"
        os.makedirs(bench_image_dir, exist_ok=True)
        
        for sample in bench_list:
            video_path = os.path.join(args.ego4d_dir, sample["video_id"]+".mp4")
            out_path0 = os.path.join(bench_image_dir, sample["image_0"]+".png")
            out_path1 = os.path.join(bench_image_dir, sample["image_1"]+".png")
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise RuntimeError("Fail to open the video (video_id: {})".format(sample["video_id"]))

            cap.set(cv2.CAP_PROP_POS_FRAMES, sample["frame_0"])
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(out_path0, frame)
            else:
                raise RuntimeError("Fail to read the frame (video_id: {}, frame_number: {})".format(sample["video_id"], sample["frame_0"]))
            
            cap.set(cv2.CAP_PROP_POS_FRAMES, sample["frame_1"])
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(out_path1, frame)
            else:
                raise RuntimeError("Fail to read the frame (video_id: {}, frame_number: {})".format(sample["video_id"], sample["frame_1"]))
        
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ego4d_dir", help="path to Ego4D")
    parser.add_argument("--train", action="store_true", help="Enable to extract STATUS Train images")
    parser.add_argument("--bench", action="store_true", help="Enable to extract STATUS Bench images")
    args = parser.parse_args()

    main(args)