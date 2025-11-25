import matplotlib.pyplot as plt
import networkx as nx

def plot_network(interaction_network, output_path):
    """
    Generates a static plot of the gene-drug interaction graph.
    """
    G = interaction_network.graph
    if len(G.nodes) == 0:
        print("Graph is empty. Nothing to plot.")
        return

    plt.figure(figsize=(12, 12))
    
    # Layout
    pos = nx.spring_layout(G, k=0.3, iterations=50)
    
    # Separate nodes by type for coloring
    gene_nodes = [n for n, d in G.nodes(data=True) if d.get('type') == 'gene']
    drug_nodes = [n for n, d in G.nodes(data=True) if d.get('type') == 'drug']
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, nodelist=gene_nodes, node_color='lightblue', node_size=800, label='Genes')
    nx.draw_networkx_nodes(G, pos, nodelist=drug_nodes, node_color='lightgreen', node_size=600, label='Drugs')
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
    
    plt.title("Gene-Drug Interaction Network (Personalized PGx)", fontsize=16)
    plt.legend()
    plt.axis('off')
    
    plt.savefig(output_path, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Network plot saved to {output_path}")
