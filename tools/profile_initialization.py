#!/usr/bin/env python3
"""
Profile SOCCoder initialization to identify startup bottlenecks
"""

import cProfile
import io
import pstats
import time
from occupationcoder.coder import SOCCoder


def profile_initialization():
    """Profile SOCCoder initialization to identify bottlenecks."""
    print("Profiling SOCCoder initialization...")
    
    # Run profiler
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Time the initialization
    start_time = time.perf_counter()
    coder = SOCCoder()
    end_time = time.perf_counter()
    
    profiler.disable()
    
    print(f"Total initialization time: {end_time - start_time:.4f}s")
    
    # Analyze results
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s)
    ps.sort_stats('cumulative')
    ps.print_stats(30)  # Top 30 functions for detailed analysis
    
    print("\nProfile Results for SOCCoder Initialization:")
    print("=" * 70)
    print(s.getvalue())
    
    return coder


if __name__ == "__main__":
    profile_initialization()
