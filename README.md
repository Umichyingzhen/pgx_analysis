# PGx Toolkit

A Python toolkit for personalized pharmacogenomic (PGx) network analysis. This package allows you to integrate user genotype data (e.g., from 23andMe) with pharmacogenomic annotations (e.g., from PharmGKB) to build and analyze gene-drug interaction networks.

## Features

- **Data Ingestion**: Parsers for 23andMe raw data and PharmGKB variant annotations.
- **Variant Matching**: Matches user genotypes to known pharmacogenomic variants.
- **Network Analysis**: Builds a Gene-Drug interaction graph and calculates centrality metrics to identify:
    - **High Impact Genes**: Genes that modulate multiple drugs in the user's profile.
    - **Multi-gene Drugs**: Drugs affected by multiple variants in the user's genome.
- **Visualization**: Generates static network plots of the interactions.

## Installation

```bash
pip install .
```

## Usage

```python
from pgx_toolkit.core.genotype import UserGenotype
from pgx_toolkit.core.annotation import PharmGKB
from pgx_toolkit.core.matcher import PGxMatcher
from pgx_toolkit.analysis.network import InteractionNetwork
from pgx_toolkit.viz.graph_plot import plot_network

# 1. Load Data
user_genotype = UserGenotype.from_23andme("path/to/23andme_data.txt")
pharmgkb = PharmGKB.from_tsv("path/to/var_drug_ann.tsv")

# 2. Match Variants
matcher = PGxMatcher()
matches = matcher.match(user_genotype, pharmgkb)

# 3. Build Network
network = InteractionNetwork()
network.build_graph(matches)

# 4. Analyze
top_genes = network.get_high_impact_genes(top_n=5)
print("Top Genes:", top_genes)

# 5. Visualize
plot_network(network, "my_pgx_network.png")
```

## Documentation

Full documentation is available in the `docs/` directory.
