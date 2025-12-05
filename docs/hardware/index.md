# Hardware Requirements

## Overview

This book supports **tiered hardware paths** based on your budget and which modules you want to complete. You can start with **simulation-only** (Modules 1-2) and progressively add hardware for physical deployment (Modules 3-4).

## Hardware Categories

### 1. Simulation Rig (Required for Module 3: Isaac)

**Purpose**: Run Isaac Sim for photorealistic robot simulation and synthetic data generation

| Component | Minimum | Recommended | Cloud Alternative |
|-----------|---------|-------------|-------------------|
| **GPU** | NVIDIA RTX 3070 (8GB VRAM) | NVIDIA RTX 4090 (24GB VRAM) | AWS g5.xlarge ($1.20/hr) |
| **CPU** | Intel i7 / AMD Ryzen 7 | Intel i9 / AMD Ryzen 9 | AWS g5.xlarge (8 vCPUs) |
| **RAM** | 16GB | 32GB | AWS g5.xlarge (32GB) |
| **Storage** | 512GB SSD | 1TB NVMe SSD | AWS EBS (500GB) |

**Cost Estimate**: $1,500 - $3,500 (one-time) OR $50-200/month (cloud)

**Modules Enabled**: Module 3 (Isaac Sim, Isaac ROS)

**Budget Alternative**: Use Gazebo (Module 2) instead of Isaac Sim. Isaac concepts can be learned without running simulations.

---

### 2. Edge AI Kit (Required for Module 4: VLA)

**Purpose**: Deploy perception and VLA inference on robot hardware

| Option | TOPS | RAM | Price | Use Case |
|--------|------|-----|-------|----------|
| **Jetson Orin Nano 4GB** | 20 | 4GB | $399 | Basic ROS 2, lightweight perception |
| **Jetson Orin Nano 8GB** | 40 | 8GB | $499 | Module 3 (Isaac ROS VSLAM, Nav2) |
| **Jetson Orin NX 8GB** | 70 | 8GB | $599 | Module 4 (VLA with local LLM) |
| **Jetson Orin NX 16GB** | 100 | 16GB | $899 | Full VLA + Isaac ROS perception |

**Recommended Path**:
- **Modules 1-2**: No Jetson needed (simulation only)
- **Module 3**: Orin Nano 8GB (sufficient for Isaac ROS)
- **Module 4**: Orin NX 16GB (handles VLA workloads)

**Cloud Alternative**: Run perception and LLM inference on cloud (AWS, RunPod) and send commands to simulated robot

---

### 3. Sensors (Optional for Physical Deployment)

**Purpose**: Provide vision, depth, and spatial awareness for real robots

| Sensor | Purpose | Price | Modules |
|--------|---------|-------|---------|
| **RealSense D435i** | RGB-D camera + IMU | $200 | Module 3 (VSLAM, object detection) |
| **RPLiDAR A1** | 2D laser scanner | $100 | Module 3 (Nav2 costmaps) |
| **ZED 2i** | Stereo camera + depth + IMU | $450 | Module 3 (high-quality VSLAM) |
| **USB Microphone** | Voice input for VLA | $10-50 | Module 4 (Whisper voice commands) |

**Minimum for Physical Testing**: RealSense D435i ($200)

---

### 4. Robot Platforms (Optional for Capstone Deployment)

**Purpose**: Physical humanoid or mobile robot for deploying trained behaviors

| Robot | Type | Price | Use Case |
|-------|------|-------|----------|
| **Proxy Torso Kit** | Upper-body humanoid | $200-500 | Tabletop manipulation, gestures |
| **Unitree Go2** | Quadruped | $1,600 | Navigation, perception, VLA locomotion |
| **Robotis OP3** | Bipedal humanoid | $10,000 | Full humanoid control, walking, manipulation |
| **Unitree G1** | Advanced humanoid | $16,000 | Industry-grade, dexterous hands, robust |

**Recommended Progression**: Start with **simulation** → Add **Go2** for locomotion testing → Upgrade to **OP3/G1** for full humanoid capstone

**Simulation-Only Option**: Complete entire course using simulated robots (Gazebo, Unity, Isaac Sim)

---

## Decision Tree

**Question 1: What modules do you want to complete?**

- **Modules 1-2 only** (ROS 2 + Digital Twin)
  - ✅ **Hardware**: Laptop/desktop with integrated graphics
  - ❌ **Not Needed**: Jetson, RTX GPU, sensors, robot

- **Modules 1-3** (ROS 2 + Simulation + Isaac)
  - ✅ **Simulation Rig**: RTX GPU (or cloud GPU)
  - ✅ **Edge AI Kit**: Jetson Orin Nano 8GB (for Isaac ROS deployment)
  - ❌ **Not Needed**: Sensors, robot (use simulation)

- **All Modules + Capstone**
  - ✅ **Simulation Rig**: RTX 4090 recommended
  - ✅ **Edge AI Kit**: Jetson Orin NX 16GB
  - ✅ **Sensors**: RealSense D435i
  - ✅ **Robot**: Unitree Go2 (minimum) or OP3/G1 (advanced)

**Question 2: What's your budget?**

| Budget | Recommended Path |
|--------|------------------|
| **$0-500** | Simulation-only (use personal computer + cloud GPU as needed) |
| **$500-1000** | Jetson Orin Nano 8GB + RealSense D435i (edge AI + basic sensors) |
| **$1000-2000** | RTX 3070 workstation OR Jetson NX + RealSense + Go2 |
| **$2000-5000** | RTX 4090 workstation + Jetson NX + RealSense + Go2 |
| **$5000+** | Full stack (RTX 4090, Jetson NX, RealSense, ZED 2i, OP3/G1) |

---

## Cloud vs. On-Premises

| Factor | Cloud GPU | On-Premises (RTX) |
|--------|-----------|-------------------|
| **Upfront Cost** | $0 | $1,500-3,500 |
| **Monthly Cost** | $50-200 | $0 (electricity only) |
| **Latency** | 50-100ms (for sim-to-robot commands) | &lt;1ms (local) |
| **Scalability** | Spin up 10+ instances | Limited to one workstation |
| **Best For** | Experimentation, learning | Production, real-time control |

**Recommendation**: Use **cloud GPU** for learning and prototyping, switch to **on-prem RTX** for final deployment if latency matters.

---

## Next Steps

1. **Assess Your Goals**: Which modules do you want to complete?
2. **Check Your Budget**: How much can you invest upfront?
3. **Start with Simulation**: Complete Modules 1-2 with existing hardware
4. **Add Hardware Incrementally**: Buy Jetson → RTX GPU → Sensors → Robot as you progress

**Personalization Feature**: This book adapts content based on your hardware profile. Sign up and tell us what you have!

## References

NVIDIA. (2024). *Jetson Orin Series Specifications*. Retrieved from https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/

Intel. (2024). *RealSense D400 Series Documentation*. Retrieved from https://www.intelrealsense.com/depth-camera-d435i/

Unitree Robotics. (2024). *Unitree Go2 Specifications*. Retrieved from https://www.unitree.com/go2
