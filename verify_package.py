import os
import sys

# Ensure the package is in the path
sys.path.append(os.getcwd())

from pgx_toolkit.core.genotype import UserGenotype
from pgx_toolkit.core.annotation import PharmGKB
from pgx_toolkit.core.matcher import PGxMatcher
from pgx_toolkit.analysis.network import InteractionNetwork
from pgx_toolkit.viz.graph_plot import plot_network

def main():
    print("Starting PGx Toolkit Verification...")

    # Paths to data
    genotype_path = "23andme_v5_hg19_ref.txt/23andme_v5_hg19_ref.txt"
    annotation_path = "variantAnnotations/var_drug_ann.tsv"

    # 1. Load Data
    print(f"Loading Genotype from {genotype_path}...")
    user_genotype = UserGenotype.from_23andme(genotype_path)
    print(f"Loaded {len(user_genotype)} genotype entries.")

    print(f"Loading Annotations from {annotation_path}...")
    pharmgkb = PharmGKB.from_tsv(annotation_path)
    print(f"Loaded {len(pharmgkb)} annotations.")

    # 2. Match
    print("Matching variants...")
    matcher = PGxMatcher()
    matches = matcher.match(user_genotype, pharmgkb)
    print(f"Found {len(matches)} matched variants.")

    if len(matches) == 0:
        print("No matches found. Check data or matching logic.")
        return

    # 3. Build Network
    print("Building Interaction Network...")
    network = InteractionNetwork()
    network.build_graph(matches)
    
    # 4. Analysis
    print("\n--- Top High Impact Genes (Degree Centrality) ---")
    top_genes = network.get_high_impact_genes(top_n=5)
    for gene, degree in top_genes:
        print(f"{gene}: {degree} drugs")

    print("\n--- Top Multi-gene Drugs (Degree Centrality) ---")
    top_drugs = network.get_multigene_drugs(top_n=5)
    for drug, degree in top_drugs:
        print(f"{drug}: {degree} genes")

    # 5. Visualization
    output_plot = "pgx_network_plot.png"
    print(f"\nGenerating network plot to {output_plot}...")
    plot_network(network, output_plot)

    print("\nVerification Complete!")

if __name__ == "__main__":
    main()
