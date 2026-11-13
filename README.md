<a href="https://pypi.org/project/mechiviz/"><img src="https://img.shields.io/pypi/v/mechiviz.svg" alt="PyPI"></a>
<p align="center">
<img src="https://github.com/user-attachments/assets/42110c43-c27b-449b-b039-bb3d5ad73f43" height="320" alt="logo">
</p>


---

**GPU-resident compute and visualization for interactive mechanistic interpretability**

MechiViz lets you watch and interrogate models live, at full scale. Model tensors are drawn directly from GPU memory with no copies made to the CPU.

<p align="center">
  <img src="https://github.com/user-attachments/assets/fb6926fd-5f51-44cb-9ccd-d7d581d8c29d" width="49.5%">
  <img src="https://github.com/user-attachments/assets/8fea512a-fc79-4583-8a7e-d3ff73d979ce" width="49.5%">
</p>
<img width="100%" alt="output" src="https://github.com/user-attachments/assets/d4a7b988-747c-4a3a-a62b-2aea7e7122a6" />


- **Zero host round trip**: PyTorch / tinygrad tensors and fastplotlib graphics share the same GPU buffers
- **Live training views**: see activations, weights, and dynamics update every step
- **Interactive interrogation**: ablate weights, perturb inputs, and see the effect immediately

## How it works

MechiViz allocates exportable Vulkan buffers through a patched [wgpu-native](https://github.com/gfx-rs/wgpu-native) and imports them into CUDA. Your model writes to the buffer, [fastplotlib](https://github.com/fastplotlib/fastplotlib) renders from it, and the data never leaves the GPU.

<img width="885" height="558" alt="shared-path" src="https://github.com/user-attachments/assets/58a48924-c31b-4bcb-bd68-b4f745e6574f" />

## Benchmarks

Median FPS vs. data size for image, scatter, and line graphics during scripted interaction (pan, zoom, click-drag). The **shared** path holds interactive frame rates as data grows; the **host** path does not.

<img width="2633" height="1838" alt="fps_vs_mb_panzoom_4gpu" src="https://github.com/user-attachments/assets/f01a8b08-36fe-452f-9910-abeec4068c02" />

> [!NOTE]
> Performance degrades for NVIDIA H100 GPUs even in the shared path solution because the H100 is designed primarily for compute, so most graphics pipelines have been stripped away.

## Installation
 
```bash
pip install mechiviz
```
 
or with [uv](https://docs.astral.sh/uv/):
 
```bash
uv add mechiviz
```
 
To run the examples:
 
```bash
pip install "mechiviz[examples]"
```

> [!IMPORTANT]
> Import mechiviz **before** fastplotlib, pygfx, or wgpu. mechiviz ships a patched wgpu-native and has to point wgpu at it first.
> ```python
> import mechiviz
> import fastplotlib as fpl
> ```


## Supported Devices
| | |
|---|---|
| **OS** | Linux x86_64 (glibc ≥ 2.28: Ubuntu 20.04+, Debian 10+, RHEL/Rocky 8+, Fedora) |
| **GPU** | NVIDIA, with Vulkan and CUDA drivers installed |
| **Python** | 3.12+ |
| **Backends** | PyTorch (CUDA), tinygrad |
| **Not yet supported** | macOS, Windows, AMD / Intel GPUs, ARM Linux |

## For Developers
 
```bash
git clone https://github.com/mechiviz/mechiviz.git
cd mechiviz
uv sync --all-extras
```
 
```bash
uv sync --extra dev    # to get dev dependencies
uv lock --upgrade      # to update deps when necessary
 
# Common tasks:
uv run ruff format     # auto-format
uv run ruff check      # lint
uv run pytest tests    # run unit tests
```
