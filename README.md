<p align="center">
<img src="https://github.com/user-attachments/assets/42110c43-c27b-449b-b039-bb3d5ad73f43" height="320" alt="logo">
</p>


---

GPU-resident compute and visualization for interactive mechanistic interpretability 



https://github.com/user-attachments/assets/33c269db-ff70-4160-8bd2-7a998b58f6df




## Installation 

1. Clone the repo 
```bash
git clone https://github.com/clewis7/mechiviz.git
cd mechiviz
```
2. Install deps using [uv](https://docs.astral.sh/uv/)
```bash
uv sync --all-extras 
```

## For developers

```bash
uv sync --extra dev    # to get dev dependencies
uv lock --upgrade      # to update deps when necessary

# Common tasks:
uv run ruff format     # auto-format
uv run ruff check      # lint
uv run pytest tests    # run unit tests
```
