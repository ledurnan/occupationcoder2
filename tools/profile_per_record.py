#!/usr/bin/env python3
"""
Profile per-record processing to identify bottlenecks
"""

import cProfile
import io
import pstats
import pandas as pd
from pathlib import Path
from occupationcoder.coder import SOCCoder


def profile_single_record():
    """Profile a single record processing to identify bottlenecks."""
    # Load test data (adjust path since we're in tools/ subdirectory)
    test_file = Path(__file__).parent.parent / "tests" / "test_vacancies.csv"
    test_data = pd.read_csv(test_file)
    
    # Initialize coder (one-time cost)
    coder = SOCCoder()
    
    # Profile the first record
    first_record = test_data.iloc[0]
    
    def process_record():
        return coder.code_record(
            first_record['job_title'],
            first_record['job_description'], 
            first_record['job_sector']
        )
    
    # Run profiler
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Process multiple times to get better statistics
    for _ in range(10):
        result = process_record()
    
    profiler.disable()
    
    # Analyze results
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s)
    ps.sort_stats('cumulative')
    ps.print_stats(20)  # Top 20 functions
    
    print("Profile Results for Single Record Processing:")
    print("=" * 60)
    print(s.getvalue())
    
    return result


if __name__ == "__main__":
    profile_single_record()
