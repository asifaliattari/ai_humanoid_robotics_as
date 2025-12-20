---
name: technical-doc-writer
description: Write clear, well-structured technical documentation for robotics topics. Use when creating tutorials, API docs, module guides, or any educational content. Ensures consistency with project documentation standards.
allowed_tools: Read, Edit, Write, Glob
---

# Technical Documentation Writer Skill

## Purpose

Create high-quality technical documentation for the Physical AI & Humanoid Robotics textbook that is clear, accurate, and educational.

## Writing Standards

### Document Structure

```markdown
---
sidebar_position: X
title: "Clear Title"
description: "One-line description for SEO"
---

# Main Title

Brief introduction (2-3 sentences)

## Learning Objectives

By the end of this section, you will:
- Objective 1
- Objective 2
- Objective 3

## Prerequisites

- Prerequisite 1
- Prerequisite 2

## Main Content

### Section 1
Content...

### Section 2
Content...

## Summary

Key takeaways...

## Next Steps

- Link to related topics
```

### Code Examples Format

Always include:
1. Language identifier in code blocks
2. Comments explaining key lines
3. Expected output (when applicable)

```python
# Example: ROS 2 Node
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')
        self.get_logger().info('Node started!')  # Log startup

def main():
    rclpy.init()
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()

# Output: [INFO] [my_node]: Node started!
```

### Terminology

Use consistent terms:
- "ROS 2" (not "ROS2" or "ros2")
- "Gazebo" (not "gazebo sim")
- "NVIDIA Isaac Sim" (not "Isaac")
- "VLA" spelled out on first use: "Vision-Language-Action (VLA)"

### Tone Guidelines

- Professional but approachable
- Second person ("you will learn...")
- Active voice preferred
- Avoid jargon without explanation
- Include analogies for complex concepts

## Templates

### Tutorial Template

```markdown
# Tutorial: [Action] with [Technology]

**Time Required:** X minutes
**Difficulty:** Beginner/Intermediate/Advanced

## What You'll Build

Description and image of final result.

## Step 1: [First Step]

Explanation...

```code
example
```

## Step 2: [Second Step]

...

## Troubleshooting

### Common Issue 1
Solution...

## Complete Code

Full working example...
```

### Concept Explanation Template

```markdown
# Understanding [Concept]

## What is [Concept]?

Simple definition...

## Why It Matters

Real-world applications...

## How It Works

Technical explanation with diagrams...

## Key Takeaways

- Point 1
- Point 2
```

## Quality Checklist

Before completing any documentation:

- [ ] Title is clear and descriptive
- [ ] Introduction hooks the reader
- [ ] Learning objectives are defined
- [ ] Prerequisites are listed
- [ ] Code examples are tested
- [ ] Images have alt text
- [ ] Links are relative and working
- [ ] Summary reinforces key points
- [ ] Next steps guide the reader forward

## File Naming

- Use kebab-case: `ros2-navigation-basics.md`
- Be descriptive: `gazebo-world-creation.md` not `tutorial1.md`
- Include module prefix when needed: `isaac-sim-setup.md`
