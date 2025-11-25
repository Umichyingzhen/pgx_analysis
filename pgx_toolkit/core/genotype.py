import pandas as pd

class GenotypeEntry:
    def __init__(self, rsid, chromosome, position, genotype):
        self.rsid = rsid
        self.chromosome = chromosome
        self.position = position
        self.genotype = genotype

    def __repr__(self):
        return f"GenotypeEntry(rsid='{self.rsid}', genotype='{self.genotype}')"

class UserGenotype:
    def __init__(self, entries=None):
        self.entries = entries if entries is not None else []
        self._entry_map = {e.rsid: e for e in self.entries}

    def add_entry(self, entry):
        self.entries.append(entry)
        self._entry_map[entry.rsid] = entry

    def get_entry(self, rsid):
        return self._entry_map.get(rsid)

    @classmethod
    def from_23andme(cls, filepath):
        """
        Parses a 23andMe raw data file.
        Assumes standard 23andMe format (header lines start with #).
        Columns: rsid, chromosome, position, genotype
        """
        entries = []
        try:
            # Read file, skipping comments
            df = pd.read_csv(filepath, sep='\t', comment='#', header=None, 
                             names=['chromosome', 'position', 'rsid', 'genotype'],
                             dtype={'rsid': str, 'chromosome': str, 'position': int, 'genotype': str})
            
            for _, row in df.iterrows():
                entry = GenotypeEntry(row['rsid'], row['chromosome'], row['position'], row['genotype'])
                entries.append(entry)
                
        except Exception as e:
            print(f"Error loading 23andMe file: {e}")
            raise

        return cls(entries)

    def __len__(self):
        return len(self.entries)
