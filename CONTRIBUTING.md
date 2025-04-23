# Contributing to FB-BEV PandaSet Integration

Our objective is to adapt the FB-BEV framework—originally developed for nuScenes—to support inference using the PandaSet dataset with camera-only inputs.

This guide outlines how to contribute effectively and maintain consistency across the codebase.

## Table of Contents

- How to Contribute
- Development Guidelines
- Pull Request Process
- Style Guide
- Reporting Issues
- License

## How to Contribute

We welcome contributions in the following areas:

- Improvements to the camera-only data pipeline
- Bug reports and fixes
- Unit tests for PandaSet compatibility
- Configuration updates and dataset format converters
- Documentation improvements

## Development Guidelines

- Place utility scripts or helpers in the appropriate `tools/` or `mmdet3d/datasets/` subdirectory
- Write clear and concise code with comments where necessary
- Avoid hardcoded paths; use variables such as `data_root` to reference dataset locations

## Pull Request Process

    1. Fork the repository and create a new branch:
    
        git checkout -b your-feature-branch

    2. Make your changes with clear and descriptive commit messages

    3. Push your changes to your fork
    
    4. Open a pull request and describe the purpose of your contribution

Please keep pull requests focused and small where possible.

## Style Guide

- Follow PEP8 standards
- Include docstrings for new functions or classes
- Use snake_case for variables and functions

## Reporting Issues

When reporting a bug or requesting a feature, please provide:

- A clear title and description
- Steps to reproduce the issue, if applicable

Issues can be submitted through the GitHub Issues tab.

## License

This project is released under the NVIDIA Source Code License-NC. Ensure all contributions comply with this license.
