import pandas as pd
import re

class DrugAnnotation:
    def __init__(self, rsid, gene, drug, phenotype_category, significance, notes, sentence, alleles):
        self.rsid = rsid
        self.gene = gene
        self.drug = drug
        self.phenotype_category = phenotype_category
        self.significance = significance
        self.notes = notes
        self.sentence = sentence
        self.alleles = alleles

    def __repr__(self):
        return f"DrugAnnotation(rsid='{self.rsid}', gene='{self.gene}', drug='{self.drug}')"

class PharmGKB:
    def __init__(self, annotations=None):
        self.annotations = annotations if annotations is not None else []
        # Index by rsID for faster lookup. Note: One rsID can have multiple annotations.
        self._annotation_map = {}
        for ann in self.annotations:
            if ann.rsid not in self._annotation_map:
                self._annotation_map[ann.rsid] = []
            self._annotation_map[ann.rsid].append(ann)

    def get_annotations(self, rsid):
        return self._annotation_map.get(rsid, [])

    @classmethod
    def from_tsv(cls, filepath):
        """
        Parses the PharmGKB variant annotation TSV file.
        Expected columns include 'Variant/Haplotypes', 'Gene', 'Drug(s)', etc.
        """
        annotations = []
        try:
            df = pd.read_csv(filepath, sep='\t', dtype=str)
            
            # Regex to extract rsID
            rsid_pattern = re.compile(r"rs[0-9]+")

            for _, row in df.iterrows():
                variant_text = str(row.get('Variant/Haplotypes', ''))
                match = rsid_pattern.search(variant_text)
                if match:
                    rsid = match.group(0)
                    
                    # Create annotation object
                    ann = DrugAnnotation(
                        rsid=rsid,
                        gene=row.get('Gene', ''),
                        drug=row.get('Drug(s)', ''),
                        phenotype_category=row.get('Phenotype Category', ''),
                        significance=row.get('Significance', ''),
                        notes=row.get('Notes', ''),
                        sentence=row.get('Sentence', ''),
                        alleles=row.get('Alleles', '')
                    )
                    annotations.append(ann)
                    
        except Exception as e:
            print(f"Error loading PharmGKB file: {e}")
            raise

        return cls(annotations)

    def __len__(self):
        return len(self.annotations)
