# practical_2

# Run EDGETPU instance: edgetpu.py image_path
## number of operations: 88, running on tpu:84, running on cpu: 4
## MobileNetV2 UNET architecture
## Results: edgetpu.png
## Model architect: model_quantized_edgetpu.tflite.svg
## Anotation Results: edge_tpu_cpu.png

# Run EDGECPU instance: edgecpu.py image_path
## number of operations: 88 all run on CPU.
## Results: edgecpu.png
## Model architect: model_quantized.tflite.svg
## Anotation Results: edge_tpu_cpu.png

# Server Complex Model:
## MobileNetV2 UNET architecture
## Anotation Results: server.png and server_annotation_results.png
## Model architect: final_model.h5.svg and first Tensorflow TFLITE without quantization: model.tflite.svg

# Secure Script for IoT devices: test-5001-kafka-db.py and test-5002-kafka-db.py
# Setup