Description



To get genomic neighbourhood of Shield subtypes

**Athenian.sh** :Uses bedtools and faidx to retrieve neighbourhood. Also requires efetch. Runs ./Athenian <file with Nuccore/start/stop>


Then run PADLOC/Defense finder and AMRFInder separately and combine with: 

[Link to script] (https://github.com/GM110Z/Phage-defence-scripts/blob/main/Prophage-encoded-defence/PHORIFIC.py) 

[Link to script] (https://github.com/GM110Z/Phage-defence-scripts/blob/main/Prophage-encoded-defence/edison.py)

[Link to script] (https://github.com/GM110Z/Phage-defence-scripts/blob/main/Prophage-encoded-defence/SantasHelper.py)

**extract_operons.py** From phorific, extracts operons that contain protein of interest (in this example, looking for ShdA for Shield subtypes) 

**ICARUS.py** Uses python to download representative sequences for each predicted operons found by extract_operons.py with efetch and then runs cblaster to determine if this is effectively an operon (occurs in multiple genomes). Cblaster run is times so it does not overwhelm blast.

**get_binary_files.sh** extracts only the binary files produced by cblaster if they have 100 or more lines (thus 100 or more operons) and moves them in a different folder

