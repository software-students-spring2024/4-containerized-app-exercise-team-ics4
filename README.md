![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
![Pytest](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/pytest-workflow.yml/badge.svg)

# About

This containerized app takes real-time audio feed from users and classifies the it into categories. It then shows metadata about what it believes the sounds to be, and the confidence level for each category.

# Instructions

To run this project, build the docker containers using docker-compose. Pre-requisite is to have docker installed on your system. In the root directory, run:

- `docker-compose up --build`

# References

[Github Blog on Implementing OpenCV and Live Video Feed](https://github.com/google/mediapipe/issues/4448)

[Used example code from MediaPipe](https://codepen.io/mediapipe-preview/pen/wvxYYmy)

# Team Members

- [Eric Lin](https://github.com/exl7954)
- [Alice Ding](https://github.com/ayd2134)
- [Justin Zhao](https://github.com/zhaojustin)
