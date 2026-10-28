<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img alt="Johnathan Lee, Sr. HPC System Architect at Arizona State University" src="assets/banner-light.svg" width="100%">
</picture>

<p align="center">
  <a href="https://slurmdash.com"><img src="https://img.shields.io/badge/slurmdash.com-0d1117?style=flat-square&logoColor=white&logo=googlechrome" alt="slurmdash.com"></a>
  <a href="https://obleth.com"><img src="https://img.shields.io/badge/obleth.com-0d1117?style=flat-square&logoColor=white&logo=googlechrome" alt="obleth.com"></a>
  <a href="https://thediymaker.github.io/slides-carcc2026/"><img src="https://img.shields.io/badge/CaRCC%202026%20talk-0d1117?style=flat-square&logoColor=white&logo=googleslides" alt="CaRCC 2026 talk"></a>
</p>

HPC system architect at Arizona State University Research Computing. I work on Slurm and Kubernetes clusters and self-hosted LLM inference on Intel Gaudi, and build open tools for both. Outside of work: 3D printing, ESP32 and IoT projects, and general tinkering.

## Projects

<table>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/thediymaker/slurm-node-dashboard"><img src="https://raw.githubusercontent.com/thediymaker/slurm-node-dashboard/main/images/dashboard1.png" alt="Slurm Node Dashboard"></a>
<h3><a href="https://github.com/thediymaker/slurm-node-dashboard">Slurm Node Dashboard</a></h3>
Live node status for Slurm clusters: node states, CPU, memory and GPU use, job history and metrics.
Runs standalone or inside Open OnDemand.<br><br>
<a href="https://slurmdash.com"><b>slurmdash.com</b></a> ·
<img src="https://img.shields.io/github/stars/thediymaker/slurm-node-dashboard?style=flat-square&label=%E2%98%85&color=a3212b" alt="stars">
<img src="https://img.shields.io/github/v/release/thediymaker/slurm-node-dashboard?style=flat-square&label=&color=30363d" alt="release">
</td>
<td width="50%" valign="top">
<a href="https://github.com/thediymaker/obleth-gateway"><img src="https://raw.githubusercontent.com/thediymaker/obleth-gateway/main/.github/assets/dashboard.png" alt="obleth gateway"></a>
<h3><a href="https://github.com/thediymaker/obleth-gateway">obleth gateway</a></h3>
An AI gateway for shared GPU clusters, written in Rust. Fairshare scheduling, model routing
and usage accounting in front of any OpenAI-compatible backend.<br><br>
<a href="https://obleth.com"><b>obleth.com</b></a> ·
<img src="https://img.shields.io/github/stars/thediymaker/obleth-gateway?style=flat-square&label=%E2%98%85&color=a3212b" alt="stars">
<img src="https://img.shields.io/github/v/release/thediymaker/obleth-gateway?style=flat-square&label=&color=30363d" alt="release">
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/thediymaker/obleth-chat"><img src="https://raw.githubusercontent.com/thediymaker/obleth-chat/main/.github/assets/screenshots/workspace-build.png" alt="obleth-chat"></a>
<h3><a href="https://github.com/thediymaker/obleth-chat">obleth-chat</a></h3>
A self-hosted chat app for obleth or any OpenAI-compatible API, with document search,
coding workspaces, and Slurm and Kubernetes tools.<br><br>
<a href="https://www.obleth.com/docs/chat/introduction"><b>Docs</b></a> ·
<img src="https://img.shields.io/github/v/release/thediymaker/obleth-chat?style=flat-square&label=&color=30363d" alt="release">
</td>
<td width="50%" valign="top">
<a href="https://github.com/thediymaker/gaudi-cookbook"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/gaudi-dark.svg">
  <img src="assets/gaudi-light.svg" alt="MXFP4 MoE decode on Gaudi 2: up to 2.5x faster">
</picture></a>
<h3><a href="https://github.com/thediymaker/gaudi-cookbook">Gaudi Cookbook</a></h3>
Recipes, fixes and kernels for running vLLM on Intel Gaudi 2, tested in production.<br><br>
<a href="https://thediymaker.github.io/gaudi-cookbook/"><b>Read the cookbook</b></a> ·
<img src="https://img.shields.io/github/stars/thediymaker/gaudi-cookbook?style=flat-square&label=%E2%98%85&color=a3212b" alt="stars">
</td>
</tr>
<tr>
<td colspan="2" valign="top">
<br>
<p align="center">
<img src="https://raw.githubusercontent.com/thediymaker/voron-knomi/main/docs/images/face.png" width="150" alt="KNOMI-NG eyes">
<img src="https://raw.githubusercontent.com/thediymaker/voron-knomi/main/docs/images/print.png" width="150" alt="Print progress">
<img src="https://raw.githubusercontent.com/thediymaker/voron-knomi/main/docs/images/lanes.png" width="150" alt="Box Turtle lanes">
<img src="https://raw.githubusercontent.com/thediymaker/voron-knomi/main/docs/images/temps.png" width="150" alt="Temperatures">
</p>
<h3 align="center"><a href="https://github.com/thediymaker/voron-knomi">KNOMI-NG</a></h3>
<p align="center">
Custom firmware for the BTT KNOMI V2 display on Klipper printers: animated eyes, print progress,
temperatures and Box Turtle lane control. Installs from the browser.<br><br>
<a href="https://thediymaker.github.io/voron-knomi/"><b>Install from the browser</b></a> ·
<img src="https://img.shields.io/github/v/release/thediymaker/voron-knomi?style=flat-square&label=&color=30363d" alt="release">
</p>
</td>
</tr>
</table>

<details>
<summary><b>More tools</b></summary>
<br>

- [**slurm-history-ingestor**](https://github.com/thediymaker/slurm-history-ingestor): loads Slurm job history into PostgreSQL for reporting
- [**ood-status-iframe**](https://github.com/thediymaker/ood-status-iframe): embeds a dashboard as an Open OnDemand app
- [**autoresearch-gaudi**](https://github.com/thediymaker/autoresearch-gaudi): karpathy/autoresearch ported to Intel Gaudi 2
- [**slides-carcc2026**](https://github.com/thediymaker/slides-carcc2026): slides from my CaRCC 2026 talk on campus LLM hosting

</details>

## Cluster activity

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/cluster-dark.svg">
  <img alt="Contribution activity for the last 12 months, drawn as Slurm node tiles" src="assets/cluster-light.svg" width="100%">
</picture>

## Recently shipped

<!-- releases:start -->
| Project | Release | Date |
|---|---|---|
| [obleth-chat](https://github.com/thediymaker/obleth-chat) | [`v0.9.2`](https://github.com/thediymaker/obleth-chat/releases/tag/v0.9.2) | 2026-10-28 |
| [voron-knomi](https://github.com/thediymaker/voron-knomi) | [`v0.4.0`](https://github.com/thediymaker/voron-knomi/releases/tag/v0.4.0) | 2026-10-27 |
| [slurm-history-ingestor](https://github.com/thediymaker/slurm-history-ingestor) | [`v1.1.5`](https://github.com/thediymaker/slurm-history-ingestor/releases/tag/v1.1.5) | 2026-10-26 |
| [slurm-node-dashboard](https://github.com/thediymaker/slurm-node-dashboard) | [`v3.1.0`](https://github.com/thediymaker/slurm-node-dashboard/releases/tag/v3.1.0) | 2026-10-25 |
| [obleth-gateway](https://github.com/thediymaker/obleth-gateway) | [`v2.4.0`](https://github.com/thediymaker/obleth-gateway/releases/tag/v2.4.0) | 2026-10-24 |
<!-- releases:end -->

## Tools

<p>
<img src="https://img.shields.io/badge/Rust-0d1117?style=flat-square&logo=rust&logoColor=white" alt="Rust">
<img src="https://img.shields.io/badge/Go-0d1117?style=flat-square&logo=go&logoColor=white" alt="Go">
<img src="https://img.shields.io/badge/TypeScript-0d1117?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript">
<img src="https://img.shields.io/badge/Python-0d1117?style=flat-square&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/C++-0d1117?style=flat-square&logo=cplusplus&logoColor=white" alt="C++">
<img src="https://img.shields.io/badge/Next.js-0d1117?style=flat-square&logo=nextdotjs&logoColor=white" alt="Next.js">
<br>
<img src="https://img.shields.io/badge/Slurm-0d1117?style=flat-square&logo=linux&logoColor=white" alt="Slurm">
<img src="https://img.shields.io/badge/Kubernetes-0d1117?style=flat-square&logo=kubernetes&logoColor=white" alt="Kubernetes">
<img src="https://img.shields.io/badge/vLLM-0d1117?style=flat-square&logo=pytorch&logoColor=white" alt="vLLM">
<img src="https://img.shields.io/badge/Intel%20Gaudi-0d1117?style=flat-square&logo=intel&logoColor=white" alt="Intel Gaudi">
<img src="https://img.shields.io/badge/PostgreSQL-0d1117?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL">
<img src="https://img.shields.io/badge/ClickHouse-0d1117?style=flat-square&logo=clickhouse&logoColor=white" alt="ClickHouse">
<img src="https://img.shields.io/badge/Redis-0d1117?style=flat-square&logo=redis&logoColor=white" alt="Redis">
<img src="https://img.shields.io/badge/Prometheus-0d1117?style=flat-square&logo=prometheus&logoColor=white" alt="Prometheus">
<br>
<img src="https://img.shields.io/badge/Klipper-0d1117?style=flat-square&logo=klipper&logoColor=white" alt="Klipper">
<img src="https://img.shields.io/badge/ESP32-0d1117?style=flat-square&logo=espressif&logoColor=white" alt="ESP32">
<img src="https://img.shields.io/badge/PlatformIO-0d1117?style=flat-square&logo=platformio&logoColor=white" alt="PlatformIO">
<img src="https://img.shields.io/badge/Voron-0d1117?style=flat-square&logo=v&logoColor=white" alt="Voron">
</p>

<sub>The banner, activity card and release list rebuild every night from <a href="scripts/build.py">scripts/build.py</a>.</sub>
