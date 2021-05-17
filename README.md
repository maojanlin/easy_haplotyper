# easy_haplotyper
haplotyping tool for nanopore sam file

_Updated: May 17, 2021_
## easy_haplotyper

Usage:
```
./run.sh
```

In `run.sh`, only `haplotyper.py` is used
- -fs option: target sam file to analyze
- -pos option: target phasing positions, should start with chr_name, follow by positions, separated with colons (e.g. "chr17:51720:53080")
- -fo option: output phasing report

In default, `phase_report.tsv` will be generated after running `run.sh`.

`haplotyper.py` also supports phasing with more than two positions (e.g. "chr17:51720:53080:54007:55368"). Multiple phasing in one run or phasing with pair-end reads are not supported currently.
