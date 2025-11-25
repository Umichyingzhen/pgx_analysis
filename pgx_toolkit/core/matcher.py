from .genotype import UserGenotype
from .annotation import PharmGKB

class MatchedVariant:
    def __init__(self, genotype_entry, annotation):
        self.genotype_entry = genotype_entry
        self.annotation = annotation
    
    @property
    def rsid(self):
        return self.genotype_entry.rsid
    
    @property
    def gene(self):
        return self.annotation.gene
    
    @property
    def drug(self):
        return self.annotation.drug
    
    @property
    def user_genotype(self):
        return self.genotype_entry.genotype

    def __repr__(self):
        return f"MatchedVariant(rsid='{self.rsid}', gene='{self.gene}', drug='{self.drug}', genotype='{self.user_genotype}')"

class PGxMatcher:
    def __init__(self):
        pass

    def match(self, user_genotype: UserGenotype, pharmgkb: PharmGKB):
        """
        Matches variants in the user's genotype with PharmGKB annotations.
        Returns a list of MatchedVariant objects.
        """
        matches = []
        
        # Iterate through user's genotype entries
        for entry in user_genotype.entries:
            # Look up annotations for this rsID
            annotations = pharmgkb.get_annotations(entry.rsid)
            
            for ann in annotations:
                # Basic matching logic: 
                # If the annotation exists for this rsID, we consider it a "match" in terms of 
                # "this variant is relevant to this drug".
                # A more complex logic could check if the user's specific alleles match the 'Alleles' field in annotation,
                # but for network analysis (Gene-Drug association), presence is the primary link.
                
                # Filter for Significance="yes" and Phenotype Category="Efficacy" as per original notebook logic
                # to focus on high-confidence, efficacy-related interactions.
                if ann.significance == 'yes' and ann.phenotype_category == 'Efficacy':
                     matches.append(MatchedVariant(entry, ann))
        
        return matches
