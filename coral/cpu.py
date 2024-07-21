import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from PIL import Image
import tflite_runtime.interpreter as tflite
import time

data_dir = '/home/maith/Desktop/cityscapes'
test_images_dir = os.path.join(data_dir, 'leftImg8bit/test')
test_labels_dir = os.path.join(data_dir, 'gtFine/test')

def preprocess_image(image_path, target_size=(256, 512)):
    image = Image.open(image_path).convert('RGB')
    image = image.resize(target_size, Image.Resampling.LANCZOS)
    image = np.array(image, dtype=np.uint8)
    return image

def create_color_mask(mask):
    cityscapes_colors = {
        0: (128, 64, 128), 1: (244, 35, 232), 2: (70, 70, 70), 3: (102, 102, 156),
        4: (190, 153, 153), 5: (153, 153, 153), 6: (250, 170, 30), 7: (220, 220, 0),
        8: (107, 142, 35), 9: (152, 251, 152), 10: (70, 130, 180), 11: (220, 20, 60),
        12: (255, 0, 0), 13: (0, 0, 142), 14: (0, 0, 70), 15: (0, 60, 100),
        16: (0, 80, 100), 17: (0, 0, 230), 18: (119, 11, 32), 19: (0, 0, 0),
        20: (0, 0, 0), 21: (0, 0, 0), 22: (0, 0, 0), 23: (0, 0, 70),
        24: (0, 60, 100), 25: (0, 80, 100), 26: (0, 0, 230), 27: (119, 11, 32),
        28: (70, 70, 70), 29: (102, 102, 156), 30: (190, 153, 153), 31: (153, 153, 153),
        32: (250, 170, 30), 33: (220, 220, 0),
    }
    color_mask = np.zeros((*mask.shape, 3), dtype=np.uint8)
    for class_id, color in cityscapes_colors.items():
        color_mask[mask == class_id] = color
    return color_mask

def overlay_annotation_on_image(image, annotation, alpha=0.5):
    color_annotation = create_color_mask(annotation)
    overlay_image = (alpha * image + (1 - alpha) * color_annotation).astype(np.uint8)
    return overlay_image

def run_inference_on_image(interpreter, image):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    input_data = np.expand_dims(image, axis=0).astype(np.uint8)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    
    start_time = time.time()
    interpreter.invoke()
    inference_time = (time.time() - start_time) * 1000  # convert to milliseconds
    
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return np.argmax(output_data, axis=-1).squeeze(), inference_time

def calculate_statistics(annotation):
    unique, counts = np.unique(annotation, return_counts=True)
    stats = dict(zip(unique, counts))
    return stats

def main(image_path):
    print("Initializing TF Lite interpreter...")
    interpreter = tflite.Interpreter(model_path="model_quantized.tflite")
    interpreter.allocate_tensors()
    print("INFO: Initialized TensorFlow Lite runtime.")
    
    test_image = preprocess_image(image_path, target_size=(256, 512))
    test_image_resized = tf.image.resize(test_image, [256, 512]).numpy()

    print("----INFERENCE TIME----")
    inference_times = []
    for _ in range(5):  # warm-up runs
        _, inference_time = run_inference_on_image(interpreter, test_image_resized)
        inference_times.append(inference_time)
        print(f"{inference_time:.1f}ms")

    predicted_annotation, inference_time = run_inference_on_image(interpreter, test_image_resized)
    predicted_annotation_resized = np.expand_dims(predicted_annotation, axis=-1)
    predicted_annotation_resized = tf.image.resize(predicted_annotation_resized, [test_image.shape[0], test_image.shape[1]], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR).numpy()
    predicted_annotation_resized = np.squeeze(predicted_annotation_resized, axis=-1)

    overlayed_image = overlay_annotation_on_image(test_image, predicted_annotation_resized)
    
    # Save the output image
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))
    axs[0].imshow(test_image)
    axs[0].axis('off')
    axs[0].set_title('Input Image')
    axs[1].imshow(overlayed_image)
    axs[1].axis('off')
    axs[1].set_title('Overlay Annotation')
    plt.tight_layout()
    plt.savefig('output_annotation.png')
    
    # Display statistics
    stats = calculate_statistics(predicted_annotation_resized)
    print("-------RESULTS--------")
    for class_id, count in stats.items():
        print(f"Class {class_id}: {count} pixels")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Run inference on an input image and visualize the result.')
    parser.add_argument('image_path', type=str, help='Path to the input image.')
    args = parser.parse_args()
    main(args.image_path)
