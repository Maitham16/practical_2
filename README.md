# Practical 2: Secure Software Platform Design and Implementation

## Introduction

This repository contains the code and resources for Practical 2, which extends the work from Practical 1 by focusing on secure data transmission and hardware acceleration for AI applications. The project is divided into two main parts:

1. **Ensuring Safe Data Sharing:** Implementing secure data transmission using IoT devices for environmental monitoring.
2. **Hardware Acceleration for AI Applications:** Enhancing real-time processing capabilities using Google Coral USB with Raspberry Pi 5.

## Part 1: Ensuring Safe Data Sharing

### Insight into IoT Arrangement and Security Measures

We developed a robust setup to ensure secure data sharing using IoT devices (DHT11, DHT22, DHT20) controlled by ESP8266 Mini D1 Pro boards. Data transmission is secured using HTTPS protocols, private networks, and unique device identifiers with secret keys.

### Gathering and Sending Data

IoT devices collect environmental data, timestamp it, and securely transmit it via HTTPS. Unauthorized data transmission attempts are automatically rejected.

### Server-Side Data Handling

A Flask application on the server validates the incoming data, stores it in InfluxDB, and forwards it to Kafka for further processing.

### Keeping Eyes on System Performance with Grafana

Grafana is used for real-time monitoring of system performance, displaying data trends and device statuses.

### Pseudo code for Part 1

\`\`\`plaintext
INITIALIZE IoT Devices with specifications:
  - Devices: DHT11, DHT22, DHT20
  - Controllers: ESP8266 Mini D1 Pro
  - Communication Protocol: HTTPS
  - Security: Unique Device ID, Secret Key

SETUP Network:
  - Configure private network settings
  - Establish secure HTTPS connections for data transmission

FUNCTION Collect_Data:
  - READ temperature and humidity from DHT sensors
  - GET current timestamp from NTP client
  - FORMAT data as JSON:
    {
      "temperature": temperature_value,
      "humidity": humidity_value,
      "timestamp": current_time,
      "deviceID": device_id,
      "secretKey": secret_key
    }
  - SEND JSON data to server via HTTPS POST request

FUNCTION Handle_Incoming_Data (HTTP POST endpoint):
  - RECEIVE JSON data
  - VALIDATE secretKey against stored value
  IF valid:
    - EXTRACT temperature, humidity, deviceID, timestamp from JSON
    - CALL Store_In_Database
    - CALL Produce_To_Kafka
  ELSE:
    - RETURN "Unauthorized Access"

CONFIGURE Grafana:
  - CONNECT to InfluxDB database
  - SET UP dashboards for real-time monitoring:
    - DISPLAY temperature and humidity trends
    - SHOW device operational status and data reception timestamps
\`\`\`

## Part 2: Hardware Acceleration for AI Applications

### Introduction

This part explores the real-time processing capabilities of edge devices, focusing on anomaly detection to enhance network security. We used a Raspberry Pi 5 with 8GB RAM, both standalone and with a Google Coral USB accelerator.

### Experiment Setup - Hardware and Software

We set up the experiment using two configurations:
- **Standalone Raspberry Pi**: Utilizing only the Raspberry Pi’s CPU.
- **Raspberry Pi with Google Coral USB**: Using the Coral TPU to accelerate specific tasks.

### Creating and Training the Model

We developed and trained models on a high-performance laptop before adapting them for the Raspberry Pi and Coral TPU. TensorFlow and TensorFlow Lite were used for model optimization and deployment.

### Inference Performance

We evaluated model performance based on inference time and accuracy. The Coral TPU significantly improved processing times but required older software versions for compatibility.

### Results and Discussion

The results demonstrated the potential of hardware accelerators like Google Coral to enhance edge AI applications, despite challenges with software compatibility. Detailed experiment results, including screenshots and performance metrics, are available in the repository.

### Pseudo code for Part 2

\`\`\`plaintext
FUNCTION TrainModel
INPUT: Dataset, ModelArchitecture
OUTPUT: TrainedModel

Initialize Model based on Architecture
FOR each Epoch in TrainingCycles
  FOR each Batch in Dataset
    Perform Forward Pass
    Compute Loss
    Perform Backward Pass to Update Model Weights
  END FOR
  Evaluate Model on Validation Set
  IF Performance Improvement is Minimal
    Terminate Training Early
  END IF
END FOR
RETURN TrainedModel

FUNCTION QuantizeModel
INPUT: TrainedModel
OUTPUT: QuantizedModel

DEFINE QuantizationParameters
APPLY Quantization to TrainedModel using Parameters
RETURN QuantizedModel

FUNCTION PerformInference
INPUT: Model, InputData
OUTPUT: InferenceResults

Load Model into Device Memory
FOR each Input in InputData
  Preprocess Input to Match Model Requirements
  Run Model on Input
  Postprocess Output for Desired Format
  Store Inference Results
END FOR
RETURN InferenceResults

FUNCTION MonitorResources
INPUT: None
OUTPUT: ResourceUsageData

WHILE Model is Running
  Check CPU Usage
  Check Memory Usage
  Check Disk IO
  Log Resource Usage
END WHILE
RETURN ResourceUsageData
\`\`\`

## Repository Structure

- **main repository**: [Practical 2 Main Repository](https://github.com/Maitham16/practical_2)
- **models**:
  - [Cityscapes ENet Model](https://github.com/Maitham16/cityscapes_ENet)
  - [Cityscapes ICNet Model](https://github.com/Maitham16/cityscapes_ICNet)
  - [Cityscapes UNet Model](https://github.com/Maitham16/cityscapes_unet)
  - [Cityscapes UNet Accurate Model](https://github.com/Maitham16/cityscapes_unet_accurate)
  - [Cityscapes UNet Enhanced Model](https://github.com/Maitham16/cityscapes_unet_enhanced)

## Run Instructions

### Run EDGETPU instance: `edgetpu.py image_path`
- Number of operations: 88, running on TPU: 84, running on CPU: 4
- Model architecture: MobileNetV2 UNET
- Results: `edgetpu.png`
- Model architecture visualization: `model_quantized_edgetpu.tflite.svg`
- Annotation results: `edge_tpu_cpu.png`

### Run EDGECPU instance: `edgecpu.py image_path`
- Number of operations: 88, all run on CPU.
- Results: `edgecpu.png`
- Model architecture visualization: `model_quantized.tflite.svg`
- Annotation results: `edge_tpu_cpu.png`

### Server Complex Model
- Model architecture: MobileNetV2 UNET
- Annotation results: `server.png`, `server_annotation_results.png`
- Model architecture visualizations: `final_model.h5.svg`, `model.tflite.svg`

### Secure Script for IoT Devices
- Scripts: `test-5001-kafka-db.py`, `test-5002-kafka-db.py`

## References

[1] Main Repository: https://github.com/Maitham16/practical_2  
[2] Cityscapes ENet Model: https://github.com/Maitham16/cityscapes_ENet  
[3] Cityscapes ICNet Model: https://github.com/Maitham16/cityscapes_ICNet  
[4] Cityscapes UNet Model: https://github.com/Maitham16/cityscapes_unet  
[5] Cityscapes UNet Accurate Model: https://github.com/Maitham16/cityscapes_unet_accurate  
[6] Cityscapes UNet Enhanced Model: https://github.com/Maitham16/cityscapes_unet_enhanced  
[7] Compiler version: https://coral.ai/docs/edgetpu/compiler/#compiler-and-runtime-versions  
[8] Supported layers: https://coral.ai/docs/edgetpu/models-intro/#quantization