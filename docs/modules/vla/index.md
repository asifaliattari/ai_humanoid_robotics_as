# Module 4: Vision-Language-Action (VLA)

## Overview

**Vision-Language-Action (VLA)** systems enable humanoid robots to:
1. **Understand** natural language commands (voice or text)
2. **Perceive** the environment using vision (cameras, depth sensors)
3. **Plan** action sequences using large language models (LLMs)
4. **Execute** actions via ROS 2 controllers

**Why VLA for Humanoid Robotics?**
- **Natural Interaction**: Users give commands like "go to the kitchen and bring me water"
- **Cognitive Planning**: LLMs reason about multi-step tasks ("to bring water, I must first navigate, then locate the glass, then grasp it")
- **Multimodal Perception**: Combine vision (object detection) with language (user intent)
- **Generalization**: LLMs can handle novel commands without task-specific programming

## Learning Outcomes

After completing this module, you will understand:
1. ✅ How Whisper transcribes voice commands to text
2. ✅ How LLMs (GPT-4, Claude) plan action sequences from language
3. ✅ How skill primitives bridge LLM outputs to ROS 2 actions
4. ✅ How multimodal models (vision + language) enhance robot cognition

## Key Concepts

### 1. Voice-to-Action Pipeline

```mermaid
graph LR
    A[Microphone] -->|Audio| B[Whisper]
    B -->|Text: 'Go to kitchen'| C[LLM Planner]
    C -->|Skill: navigate_to('kitchen')| D[ROS 2 Action Server]
    D -->|/cmd_vel| E[Robot Base Controller]
```

**Whisper**: OpenAI's speech-to-text model (multilingual, robust to noise)

### 2. LLM-Based Planning

**Input**: User command + scene description
**Output**: Sequence of skill primitives

**Example**:
```
User: "Bring me the red cup from the table"
LLM Output:
1. navigate_to("table")
2. detect_object("red cup")
3. grasp_object("red cup")
4. navigate_to("user")
5. release_object()
```

**Why LLMs?**
- **Few-Shot Learning**: Provide examples, LLM generalizes to new commands
- **Common-Sense Reasoning**: "To grasp something, you must first navigate to it"
- **Error Handling**: If step fails, LLM can replan

### 3. Skill Primitives

**Definition**: Reusable robot actions exposed as functions

**Core Skills for Humanoid Robots**:
- `navigate_to(location: str)` → Move to named location
- `pick_object(target: str)` → Grasp object by name/description
- `scan_environment()` → Use cameras to build object map
- `speak(text: str)` → Text-to-speech output

**Implementation**: Each skill maps to ROS 2 Action or Service

### 4. Multimodal Interaction

**Vision + Language**:
- **Object Grounding**: "Bring the red cup" → LLM uses vision model to identify which object is "red cup"
- **Spatial Reasoning**: "Put the book on the left shelf" → Vision determines "left" relative to robot pose

**Vision Models**:
- **CLIP**: Zero-shot object classification ("Is this object a cup?")
- **OWL-ViT**: Open-vocabulary object detection ("Find all cups in the scene")

## Prerequisites

- **Software**: ROS 2 (Module 1), Isaac ROS perception (Module 3), OpenAI/Anthropic API
- **Hardware**: Jetson Orin NX (100 TOPS) OR cloud compute (for LLM inference)
- **Experience**: Advanced (requires understanding of ROS 2, perception, and LLM APIs)

### Hardware Recommendations

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **Edge AI Kit** | Jetson Orin Nano (40 TOPS) | Jetson Orin NX (100 TOPS) |
| **Microphone** | USB mic ($10) | Array mic with noise cancellation ($50) |
| **Camera** | RealSense D435i ($200) | Stereolabs ZED 2i ($450) |

**Cloud Alternative**: Run LLM inference on cloud (OpenAI API, Anthropic Claude) if Jetson has limited compute

## Connection to Other Modules

**← Module 1 (ROS 2)**: Skills are implemented as ROS 2 Actions and Services
**← Module 2 (Simulation)**: Test VLA pipelines in Gazebo/Unity before hardware
**← Module 3 (Isaac)**: Use Isaac ROS perception for object detection and navigation
**→ Capstone**: VLA is the cognitive layer that orchestrates all other modules

## Next Steps

**In Iteration 2**, you will learn:
- How to integrate Whisper for real-time voice transcription
- How to prompt LLMs for robot task planning
- How to implement skill primitives in ROS 2 Python
- How to deploy VLA systems on Jetson Orin with Isaac ROS

## References

Radford, A., Kim, J. W., Xu, T., Brockman, G., McLeavey, C., & Sutskever, I. (2022). *Robust Speech Recognition via Large-Scale Weak Supervision*. arXiv preprint arXiv:2212.04356.

Ahn, M., Brohan, A., Brown, N., et al. (2022). *Do As I Can, Not As I Say: Grounding Language in Robotic Affordances*. Conference on Robot Learning (CoRL).

Driess, D., Xia, F., Sajjadi, M. S., et al. (2023). *PaLM-E: An Embodied Multimodal Language Model*. arXiv preprint arXiv:2303.03378.
