---
name: code-validator
description: Validate code examples in documentation for syntax, correctness, and best practices. Use when reviewing or creating tutorials with code samples. Essential for ensuring all examples work.
allowed_tools: Read, Bash, Grep, Glob
---

# Code Validator Skill

## Purpose

Ensure all code examples in the Physical AI & Humanoid Robotics textbook are syntactically correct, runnable, and follow best practices.

## Validation Commands

### Python Code

```bash
# Syntax check
python -m py_compile file.py

# Full execution
python file.py

# Type checking (if using types)
mypy file.py
```

### ROS 2 Code

```bash
# Check package structure
colcon build --packages-select <package>

# Launch file syntax
ros2 launch <package> <launch_file> --dry-run
```

### Bash Scripts

```bash
# Syntax check
bash -n script.sh

# ShellCheck (if available)
shellcheck script.sh
```

### YAML/JSON

```bash
# Python YAML validation
python -c "import yaml; yaml.safe_load(open('file.yaml'))"

# Python JSON validation
python -c "import json; json.load(open('file.json'))"
```

## Code Style Guidelines

### Python

```python
# Good: PEP 8 compliant
def calculate_velocity(distance: float, time: float) -> float:
    """Calculate velocity from distance and time."""
    if time <= 0:
        raise ValueError("Time must be positive")
    return distance / time


# Bad: No types, poor naming
def calc(d, t):
    return d/t
```

### ROS 2 Python

```python
# Good: Modern ROS 2 patterns
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class PublisherNode(Node):
    def __init__(self):
        super().__init__('publisher_node')
        self.publisher = self.create_publisher(String, 'topic', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello, ROS 2!'
        self.publisher.publish(msg)
```

### Bash

```bash
#!/bin/bash
# Good: Proper shebang, error handling, quoting

set -euo pipefail

source /opt/ros/humble/setup.bash

ros2 run "${PACKAGE_NAME}" "${NODE_NAME}"
```

## Validation Report Template

```markdown
## Code Validation Report

**Document:** `docs/modules/ros2/example.md`
**Date:** YYYY-MM-DD
**Validator:** code-validator skill

### Summary

| Metric | Count |
|--------|-------|
| Total Examples | X |
| Passed | Y |
| Failed | Z |
| Warnings | W |

### Detailed Results

#### Example 1: ROS 2 Publisher (Line 45)

**Language:** Python
**Status:** PASS

```python
# Tested code
import rclpy
...
```

**Output:**
```
[INFO] Publisher created successfully
```

#### Example 2: Launch File (Line 120)

**Language:** Python (launch)
**Status:** FAIL

**Error:**
```
ModuleNotFoundError: No module named 'launch_ros'
```

**Fix:** Add `launch_ros` to package dependencies.

### Recommendations

1. Add missing import in Example 2
2. Consider adding error handling in Example 3
```

## Common Issues

### Missing Dependencies

```python
# Document required packages
# Requirements: rclpy, std_msgs, geometry_msgs
import rclpy
from std_msgs.msg import String
```

### Deprecated APIs

| Old (Foxy) | New (Humble) |
|------------|--------------|
| `create_subscription(msg, topic, cb, 10)` | `create_subscription(msg, topic, cb, 10)` |
| `Node.get_parameter()` | `Node.get_parameter_or()` |

### Platform-Specific Code

```python
# Document platform requirements
# Platform: Linux (Ubuntu 22.04)
# ROS 2 Version: Humble

import os
workspace_path = os.path.expanduser('~/ros2_ws')  # Linux path
```

## Automated Validation Script

```bash
#!/bin/bash
# validate-examples.sh

find docs -name "*.md" | while read file; do
    echo "Checking: $file"
    # Extract Python code blocks and validate
    grep -Pzo '```python\n\K[^`]+' "$file" | \
        python -m py_compile /dev/stdin 2>&1 || \
        echo "FAIL: $file"
done
```

## Integration with CI

Add to GitHub Actions:

```yaml
- name: Validate Code Examples
  run: |
    python scripts/validate_code_examples.py docs/
```
