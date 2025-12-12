"""
Content adaptation API for personalized learning experience
Modifies content based on user's hardware, experience, and preferences
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
import logging

from config import settings
from models import get_db
from models.user import UserProfile, ExperienceLevel, JetsonModel, RobotType

logger = logging.getLogger(__name__)
router = APIRouter()


class AdaptationRule(BaseModel):
    """A single content adaptation"""
    position: str = Field(..., description="Where to insert: 'before', 'after', 'replace'")
    target_heading: Optional[str] = Field(None, description="Heading to target (None = start of document)")
    content: str = Field(..., description="Content to insert/replace")
    reason: str = Field(..., description="Why this adaptation was applied")


class AdaptContentRequest(BaseModel):
    """Request to adapt content for user"""
    section_id: str = Field(..., description="Section to adapt (e.g., 'modules/ros2/index')")
    user_id: str = Field(..., description="User ID for profile lookup")


class AdaptContentResponse(BaseModel):
    """Response with adapted content"""
    section_id: str
    original_length: int
    adapted_length: int
    adaptations: List[AdaptationRule]
    adapted_content: str


def generate_hardware_adaptations(profile: UserProfile) -> List[AdaptationRule]:
    """Generate hardware-based content adaptations"""
    adaptations = []

    # No RTX GPU - suggest cloud alternatives
    if not profile.has_rtx_gpu:
        adaptations.append(AdaptationRule(
            position="after",
            target_heading="Hardware Requirements",
            content="""
### ☁️ Cloud GPU Alternative (For Your Setup)

Since you don't have a local RTX GPU, consider these cloud options:

| Service | GPU Options | Cost | Best For |
|---------|-------------|------|----------|
| **Google Colab** | T4 (free), A100 (paid) | $0-10/month | Learning, prototyping |
| **Paperspace Gradient** | RTX 4000+ | ~$0.50/hr | Training, Isaac Sim |
| **AWS EC2 (g4dn)** | Tesla T4 | ~$0.50/hr | Production workloads |

**Setup Steps**:
1. Create account on chosen platform
2. Install Isaac Sim or ROS 2 via Docker
3. Use Jupyter notebooks for remote development
4. Transfer trained models to edge device for deployment

💡 **Tip**: Start with free Google Colab tier for learning, upgrade to Paperspace when you need Isaac Sim.
""",
            reason="User has no RTX GPU"
        ))

    # No Jetson - emphasize simulation workflow
    if profile.jetson_model == JetsonModel.NONE:
        adaptations.append(AdaptationRule(
            position="after",
            target_heading="Edge Deployment",
            content="""
### 🖥️ Simulation-First Workflow (For Your Setup)

Without a Jetson device, focus on simulation and cloud deployment:

**Phase 1: Simulation (Current)**
- Develop and test entirely in Gazebo/Isaac Sim
- Use Docker containers for consistent environments
- Validate algorithms with simulated sensors

**Phase 2: Cloud Deployment**
- Deploy trained models to cloud inference endpoints
- Use AWS Lambda or Google Cloud Run for serverless ML
- Stream sensor data from physical robot (if available) to cloud

**Phase 3: Future Jetson Purchase** (Optional)
- When ready, Jetson Orin Nano ($499) recommended
- Transfer Docker containers directly to Jetson
- Zero code changes needed - same ROS 2 packages run on edge

💰 **Cost**: Simulation is free, cloud inference ~$10-50/month depending on usage.
""",
            reason="User has no Jetson device"
        ))

    # Has Jetson - provide optimization tips
    elif profile.jetson_model != JetsonModel.NONE:
        jetson_model_name = profile.jetson_model.value.replace('_', ' ').title()
        adaptations.append(AdaptationRule(
            position="after",
            target_heading="Edge Deployment",
            content=f"""
### ⚡ Jetson {jetson_model_name} Optimization Tips

Your Jetson {jetson_model_name} setup:

**Power Modes**:
```bash
# Check current mode
sudo nvpmodel -q

# Set to max performance (for development)
sudo nvpmodel -m 0

# Set to power-efficient (for deployment)
sudo nvpmodel -m 2
```

**TensorRT Conversion** (5-10x faster inference):
```python
# Convert PyTorch to TensorRT
import torch_tensorrt

model_trt = torch_tensorrt.compile(
    model,
    inputs=[torch_tensorrt.Input((1, 3, 224, 224))],
    enabled_precisions={{torch.float16}}  # FP16 for Jetson
)
```

**Monitoring**:
```bash
# Watch GPU/CPU usage
sudo tegrastats
```

💡 **Tip**: Always test with `tegrastats` running to ensure you stay within thermal limits.
""",
            reason=f"User has Jetson {jetson_model_name}"
        ))

    # No robot - focus on simulation
    if profile.robot_type == RobotType.NONE:
        adaptations.append(AdaptationRule(
            position="after",
            target_heading="Testing",
            content="""
### 🎮 Simulation Testing (For Your Setup)

Without a physical robot, use these simulation strategies:

**Gazebo Classic** (Lightweight)
```bash
# Launch TurtleBot3 in empty world
export TURTLEBOT3_MODEL=waffle
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

**Isaac Sim** (Photorealistic)
- Use synthetic data generation for training
- Test sensor fusion with perfect ground truth
- Validate before deploying to real hardware

**Hardware-in-the-Loop (Future)**
- When you get a robot, simulation nodes can stay the same
- Only swap `/camera/image` from simulated to real sensor
- Gradual transition: test one sensor at a time

🎯 **Goal**: Build algorithms that work in simulation, deploy to real robot later with minimal changes.
""",
            reason="User has no robot"
        ))

    # Has specific robot - provide robot-specific tips
    elif profile.robot_type != RobotType.NONE:
        robot_name = profile.robot_type.value.replace('_', ' ').title()
        adaptations.append(AdaptationRule(
            position="after",
            target_heading="Hardware Setup",
            content=f"""
### 🤖 {robot_name} Integration

Your {robot_name} setup tips:

**Driver Installation**:
```bash
# Install robot-specific ROS 2 packages
sudo apt install ros-humble-{profile.robot_type.value.replace('_', '-')}-*
```

**Calibration**:
- Run camera calibration before using for perception
- Verify joint limits match URDF
- Test emergency stop button functionality

**Common Issues**:
- USB bandwidth: Use separate USB controllers for multiple cameras
- Latency: Prioritize critical topics with QoS settings
- Overheating: Monitor motor temperatures during long runs

📚 **Resources**: Check `docs/hardware/{profile.robot_type.value}/` for detailed setup guide.
""",
            reason=f"User has {robot_name}"
        ))

    return adaptations


def generate_experience_adaptations(profile: UserProfile) -> List[AdaptationRule]:
    """Generate experience-level based adaptations"""
    adaptations = []

    # ROS 2 beginner - add prerequisites
    if profile.ros2_experience == ExperienceLevel.NONE or profile.ros2_experience == ExperienceLevel.BEGINNER:
        adaptations.append(AdaptationRule(
            position="before",
            target_heading=None,  # Start of document
            content="""
> 📚 **New to ROS 2?** This chapter assumes basic ROS 2 knowledge. If you're just starting:
> 1. Complete [ROS 2 Basics Tutorial](https://docs.ros.org/en/humble/Tutorials.html) (2-3 hours)
> 2. Understand nodes, topics, and launch files
> 3. Then return here for Physical AI applications
>
> **Quick Check**: Can you create a publisher/subscriber in Python? If not, start with basics first.
""",
            reason="User is ROS 2 beginner"
        ))

    # ROS 2 advanced - link to research papers
    if profile.ros2_experience == ExperienceLevel.EXPERT:
        adaptations.append(AdaptationRule(
            position="after",
            target_heading="Further Reading",
            content="""
### 🔬 Advanced Research (For Experts)

Since you're experienced with ROS 2, explore cutting-edge research:

**Recent Papers**:
- [RT-2: Vision-Language-Action Models](https://robotics-transformer2.github.io/) (Google, 2023)
- [Mobile ALOHA](https://mobile-aloha.github.io/) (Stanford, 2024) - Low-cost bimanual manipulation
- [Dobb·E: Learning Household Tasks](https://dobb-e.com/) (NYU, 2024)

**Open Challenges**:
- Real-time VLA inference on edge devices
- Sim-to-real transfer for contact-rich tasks
- Multi-robot coordination with LLM planning

💡 **Contribute**: All above projects are open-source. Consider contributing improvements!
""",
            reason="User is ROS 2 expert"
        ))

    # ML beginner - simplify technical terms
    if profile.ml_experience == ExperienceLevel.NONE or profile.ml_experience == ExperienceLevel.BEGINNER:
        adaptations.append(AdaptationRule(
            position="after",
            target_heading="Machine Learning Integration",
            content="""
### 🧠 ML Concepts Simplified

**Don't worry if ML terminology seems complex!** Here's a plain-English guide:

| Term | What It Means | Example |
|------|---------------|---------|
| **Model** | A program that learned patterns from examples | Like learning to recognize cats after seeing 1000 cat photos |
| **Inference** | Using the trained model on new data | Showing the model a new photo and asking "is this a cat?" |
| **Embedding** | Converting data (images/text) to numbers | Turning photo into list of 512 numbers that capture its meaning |
| **Fine-tuning** | Adjusting pre-trained model for your task | Taking a model trained on ImageNet, adjusting for your robot's camera |

**Learning Path**:
1. Start with pre-trained models (don't train from scratch)
2. Learn to run inference first (training comes later)
3. Use high-level tools (avoid low-level ML frameworks initially)

🎯 **Goal**: You don't need a PhD to use ML in robotics - focus on integration, not theory.
""",
            reason="User is ML beginner"
        ))

    # ML advanced - show optimization techniques
    if profile.ml_experience == ExperienceLevel.EXPERT:
        adaptations.append(AdaptationRule(
            position="after",
            target_heading="Performance Optimization",
            content="""
### ⚡ ML Optimization Techniques (Advanced)

**Model Quantization** (INT8 for 4x speedup):
```python
import torch

# Post-training quantization
model_int8 = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)

# Quantization-aware training (better accuracy)
model.qconfig = torch.quantization.get_default_qat_qconfig('fbgemm')
torch.quantization.prepare_qat(model, inplace=True)
# ... train ...
torch.quantization.convert(model, inplace=True)
```

**Knowledge Distillation** (Smaller model, similar accuracy):
```python
# Student learns from teacher's soft predictions
loss = F.kl_div(
    F.log_softmax(student_logits / T, dim=1),
    F.softmax(teacher_logits / T, dim=1),
    reduction='batchmean'
) * (T ** 2)
```

**Pruning** (Remove 50-90% of weights):
```python
import torch.nn.utils.prune as prune

# Structured pruning (entire channels)
prune.ln_structured(module, name='weight', amount=0.5, n=2, dim=0)
```

🎯 **When to Use**: Quantization (always on edge), Distillation (when latency critical), Pruning (when memory limited).
""",
            reason="User is ML expert"
        ))

    return adaptations


@router.post("/adapt-content", response_model=AdaptContentResponse, tags=["Personalization"])
async def adapt_content(request: AdaptContentRequest, db: Session = Depends(get_db)):
    """
    Adapt content based on user profile

    Process:
    1. Fetch user profile
    2. Load original content
    3. Generate hardware-based adaptations
    4. Generate experience-based adaptations
    5. Apply adaptations to content
    6. Return adapted version

    Adaptations include:
    - Hardware alternatives (cloud GPU for no RTX, simulation for no Jetson)
    - Experience-level content (prerequisites for beginners, research papers for experts)
    - Robot-specific instructions
    """
    try:
        # Step 1: Fetch user profile
        profile = db.query(UserProfile).filter(UserProfile.id == request.user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found")

        # Step 2: Load original content
        # TODO: Load from actual markdown files
        # For now, using placeholder
        original_content = f"# {request.section_id}\n\nOriginal content here..."

        # Step 3: Generate hardware adaptations
        logger.info(f"Generating hardware adaptations for user {request.user_id}")
        hardware_adaptations = generate_hardware_adaptations(profile)

        # Step 4: Generate experience adaptations
        logger.info(f"Generating experience adaptations for user {request.user_id}")
        experience_adaptations = generate_experience_adaptations(profile)

        # Combine all adaptations
        all_adaptations = hardware_adaptations + experience_adaptations

        # Step 5: Apply adaptations
        adapted_content = original_content

        # Sort adaptations: 'before' first, then 'after', then 'replace'
        position_order = {'before': 0, 'after': 1, 'replace': 2}
        sorted_adaptations = sorted(all_adaptations, key=lambda x: position_order[x.position])

        for adaptation in sorted_adaptations:
            if adaptation.position == "before" and adaptation.target_heading is None:
                # Insert at start of document
                adapted_content = adaptation.content + "\n\n" + adapted_content
            elif adaptation.target_heading:
                # Find target heading and insert relative to it
                target = f"## {adaptation.target_heading}"
                if target in adapted_content:
                    if adaptation.position == "after":
                        # Insert after the next heading or at end of section
                        parts = adapted_content.split(target)
                        # Find next heading (## or ###)
                        next_heading_idx = parts[1].find("\n## ")
                        if next_heading_idx != -1:
                            parts[1] = (parts[1][:next_heading_idx] +
                                      "\n\n" + adaptation.content +
                                      parts[1][next_heading_idx:])
                        else:
                            parts[1] = parts[1] + "\n\n" + adaptation.content
                        adapted_content = target.join(parts)
                    elif adaptation.position == "before":
                        adapted_content = adapted_content.replace(
                            target,
                            adaptation.content + "\n\n" + target
                        )

        logger.info(f"Applied {len(all_adaptations)} adaptations to {request.section_id}")

        return AdaptContentResponse(
            section_id=request.section_id,
            original_length=len(original_content),
            adapted_length=len(adapted_content),
            adaptations=all_adaptations,
            adapted_content=adapted_content
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in adapt_content: {e}")
        raise HTTPException(status_code=500, detail="Failed to adapt content")


@router.get("/preview/{user_id}", tags=["Personalization"])
async def preview_adaptations(user_id: str, db: Session = Depends(get_db)):
    """
    Preview what adaptations would be applied for this user

    Useful for showing users what personalization looks like before applying
    """
    try:
        profile = db.query(UserProfile).filter(UserProfile.id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found")

        hardware_adaptations = generate_hardware_adaptations(profile)
        experience_adaptations = generate_experience_adaptations(profile)

        return {
            "user_id": user_id,
            "profile_summary": {
                "hardware": {
                    "rtx_gpu": profile.has_rtx_gpu,
                    "jetson": profile.jetson_model.value if profile.jetson_model else "none",
                    "robot": profile.robot_type.value if profile.robot_type else "none"
                },
                "experience": {
                    "ros2": profile.ros2_experience.value if profile.ros2_experience else "none",
                    "ml": profile.ml_experience.value if profile.ml_experience else "none"
                }
            },
            "adaptations": {
                "hardware": [{"reason": a.reason, "position": a.position} for a in hardware_adaptations],
                "experience": [{"reason": a.reason, "position": a.position} for a in experience_adaptations]
            },
            "total_adaptations": len(hardware_adaptations) + len(experience_adaptations)
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in preview_adaptations: {e}")
        raise HTTPException(status_code=500, detail="Failed to preview adaptations")
