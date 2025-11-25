import networkx as nx
import pandas as pd
from collections import Counter

class InteractionNetwork:
    def __init__(self):
        self.graph = nx.Graph()
        self.matched_variants = []

    def build_graph(self, matched_variants):
        """
        Builds a bipartite-like graph from matched variants.
        Nodes: Genes, Drugs
        Edges: Interaction (annotated by rsID)
        """
        self.matched_variants = matched_variants
        self.graph.clear()

        for mv in matched_variants:
            gene = mv.gene
            # Drugs field can contain multiple drugs separated by commas or other delimiters.
            # We'll do simple splitting by comma for now.
            drugs = [d.strip() for d in mv.drug.split(',')]
            
            if not gene:
                continue

            # Add Gene Node
            self.graph.add_node(gene, type='gene')

            for drug in drugs:
                if not drug:
                    continue
                # Add Drug Node
                self.graph.add_node(drug, type='drug')
                
                # Add Edge
                # We can add weight or metadata to the edge (e.g., rsID count)
                if self.graph.has_edge(gene, drug):
                    self.graph[gene][drug]['weight'] += 1
                    self.graph[gene][drug]['rsids'].append(mv.rsid)
                else:
                    self.graph.add_edge(gene, drug, weight=1, rsids=[mv.rsid])

    def get_high_impact_genes(self, top_n=5):
        """
        Returns top N genes by degree centrality (number of connected drugs).
        """
        gene_nodes = [n for n, d in self.graph.nodes(data=True) if d.get('type') == 'gene']
        degrees = {n: self.graph.degree(n) for n in gene_nodes}
        sorted_genes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
        return sorted_genes[:top_n]

    def get_multigene_drugs(self, top_n=5):
        """
        Returns top N drugs by degree centrality (number of connected genes).
        """
        drug_nodes = [n for n, d in self.graph.nodes(data=True) if d.get('type') == 'drug']
        degrees = {n: self.graph.degree(n) for n in drug_nodes}
        sorted_drugs = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
        return sorted_drugs[:top_n]

    def export_summary(self):
        """
        Returns a DataFrame summarizing the network.
        """
        data = []
        for u, v, d in self.graph.edges(data=True):
            # Determine which is gene and which is drug (graph is undirected)
            node_u_type = self.graph.nodes[u].get('type')
            if node_u_type == 'gene':
                gene, drug = u, v
            else:
                gene, drug = v, u
            
            data.append({
                'Gene': gene,
                'Drug': drug,
                'Interaction_Count': d['weight'],
                'rsIDs': ','.join(set(d['rsids']))
            })
        
        return pd.DataFrame(data)
