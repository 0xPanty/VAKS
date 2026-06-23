# VAKS Guarded Answer Runtime Comparison R1.2

This bounded sandbox compares three local answer paths:

1. old_path: synthetic unbraked_direct_baseline that releases the draft as-is;
2. disclaimer_path: synthetic disclaimer-only baseline that adds an unverified
   warning but keeps the draft;
3. guarded_path: R1.1 binding -> brake -> safe renderer -> Guard -> commit.

The purpose is to quantify whether the guarded path is safer while preserving
supported content. It is an ablation comparison, not a production runtime test
or a representative production traffic estimate.
