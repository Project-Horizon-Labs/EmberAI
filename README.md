# EmberAI 🔥

**AI-Powered Ember Detection from Thermal Video for Wildfire Management**

## Overview

Ember AI is a computer vision system that detects and tracks embers using thermal video footage. This project was inspired by the devastating Los Angeles wildfires and aims to support wildfire management by providing real-time insight into ember trajectories. By detecting and predicting ember paths, firefighters can more effectively allocate resources and reduce the risk of secondary fires.

## Team

- **Shobhin Basu** – sbasu25@wisc.edu  
- **Kathan Reddy** – ktreddy2@wisc.edu  

## Project Goals

- Detect embers using thermal cameras in smoke-obscured wildfire environments.
- Track ember trajectories to understand and predict fire spread.
- Provide useful data to first responders in real-time or near real-time.

## Technologies Used

- **ThermalMaster P2 Pro Camera**  
  - 256×192 resolution  
  - -4°F to 1112°F temperature range  
  - Detects differences as small as 0.04°C  
  - 15x zoom  
  - Ultra-lightweight (9g), ideal for drone integration

- **Computer Vision Stack**
  - **OpenCV**: Core image processing toolkit
  - **Blob Detection**: Isolates embers by detecting thermal "blobs"
  - **Frame Differencing**: Detects moving embers by comparing video frames

## Key Findings

- **Blob detection** is effective at close range but weakens as embers move away and cool.
- **Dynamic thresholding** is needed to improve detection at various ember temperatures and distances.
- **Thermal signature decay** affects long-range accuracy; adaptive models are required.

## Challenges

- **Data Collection**: Limited access to controlled burn sites. Current data gathered from small campfires.
- **Processing Speed**: Need to reduce lag in thermal video processing for field deployment.
- **Drone Integration**: High-temp environments, payload limits, and signal stability are current obstacles.

## Future Directions

- 📈 **Expand Dataset**: Partner with fire research facilities or firefighting schools to obtain diverse ember footage.
- ⚡ **Real-Time Processing**: Optimize algorithms and explore edge computing for faster thermal video analysis.
- 🚁 **Drone Deployment**: Adapt the system for drone-mounted use, beginning with stationary tests.

## Impact

This technology has the potential to assist wildfire responders by predicting the direction and risk of fire spread based on ember behavior. Real-time ember detection could significantly reduce the occurrence of spot fires, ultimately helping protect ecosystems, property, and human life.

---

> 🔥 “Pushing the frontier of mind and machine—one ember at a time.”
