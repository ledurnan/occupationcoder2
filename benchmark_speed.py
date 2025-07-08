#!/usr/bin/env python3
"""
Speed benchmark for occupationcoder

This script benchmarks the performance of the SOCCoder on the test dataset
to establish baseline performance metrics before optimization.
"""

import time
import pandas as pd
import statistics
from pathlib import Path
from occupationcoder.coder import SOCCoder


def time_function(func, *args, **kwargs):
    """Time a function execution and return result and elapsed time."""
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    return result, elapsed


def benchmark_single_record(coder, test_data):
    """Benchmark coding individual records."""
    print("=== Single Record Benchmarks ===")
    times = []
    
    for idx, row in test_data.iterrows():
        result, elapsed = time_function(
            coder.code_record,
            row['job_title'],
            row['job_description'],
            row['job_sector']
        )
        times.append(elapsed)
        print(f"Record {idx + 1}: {elapsed:.4f}s -> SOC {result}")
    
    print(f"\nSingle Record Stats:")
    print(f"  Mean time: {statistics.mean(times):.4f}s")
    print(f"  Median time: {statistics.median(times):.4f}s")
    print(f"  Min time: {min(times):.4f}s")
    print(f"  Max time: {max(times):.4f}s")
    print(f"  Std dev: {statistics.stdev(times) if len(times) > 1 else 0:.4f}s")
    
    return times


def benchmark_dataframe_coding(coder, test_data):
    """Benchmark coding entire dataframe."""
    print("\n=== DataFrame Batch Coding ===")
    
    # Test the dataframe method with explicit column names
    df_copy = test_data.copy()
    result, elapsed = time_function(
        coder.code_data_frame, 
        df_copy,
        title_column='job_title',
        sector_column='job_sector', 
        description_column='job_description'
    )
    
    print(f"DataFrame coding time: {elapsed:.4f}s")
    print(f"Records per second: {len(test_data) / elapsed:.2f}")
    print(f"Average per record: {elapsed / len(test_data):.4f}s")
    
    print(f"\nResults:")
    for idx, row in result.iterrows():
        print(f"  {row['job_title'][:30]:<30} -> SOC {row['SOC_code']}")
    
    return elapsed


def benchmark_initialization():
    """Benchmark SOCCoder initialization time."""
    print("=== Initialization Benchmark ===")
    
    result, elapsed = time_function(SOCCoder)
    print(f"SOCCoder initialization: {elapsed:.4f}s")
    
    return result, elapsed


def create_larger_test_dataset(base_data, multiplier=10):
    """Create a larger test dataset by repeating the base data."""
    larger_data = pd.concat([base_data] * multiplier, ignore_index=True)
    # Add some variation to avoid caching effects
    for i in range(len(larger_data)):
        if i > 0:
            larger_data.loc[i, 'job_title'] += f" (variation {i})"
    return larger_data


def benchmark_scaling(coder, base_data):
    """Benchmark performance scaling with dataset size."""
    print("\n=== Scaling Benchmark ===")
    
    sizes = [1, 3, 10, 30]  # Multiples of the base 3-record dataset
    results = []
    
    for size in sizes:
        if size == 1:
            test_data = base_data.iloc[:1].copy()
        elif size == 3:
            test_data = base_data.copy()
        else:
            test_data = create_larger_test_dataset(base_data, size // 3)
        
        df_copy = test_data.copy()
        result, elapsed = time_function(
            coder.code_data_frame, 
            df_copy,
            title_column='job_title',
            sector_column='job_sector', 
            description_column='job_description'
        )
        
        records_per_sec = len(test_data) / elapsed
        avg_per_record = elapsed / len(test_data)
        
        results.append({
            'size': len(test_data),
            'total_time': elapsed,
            'records_per_sec': records_per_sec,
            'avg_per_record': avg_per_record
        })
        
        print(f"Size {len(test_data):2d}: {elapsed:.4f}s total, {records_per_sec:.2f} rec/sec, {avg_per_record:.4f}s avg")
    
    return results


def main():
    """Run comprehensive benchmark suite."""
    print("SOCCoder Performance Benchmark")
    print("=" * 50)
    
    # Load test data
    test_file = Path(__file__).parent / "tests" / "test_vacancies.csv"
    if not test_file.exists():
        print(f"Error: Test file not found at {test_file}")
        return
    
    test_data = pd.read_csv(test_file)
    print(f"Loaded {len(test_data)} test records")
    
    # Benchmark initialization
    coder, init_time = benchmark_initialization()
    
    # Benchmark single records
    single_times = benchmark_single_record(coder, test_data)
    
    # Benchmark dataframe coding
    df_time = benchmark_dataframe_coding(coder, test_data)
    
    # Benchmark scaling
    scaling_results = benchmark_scaling(coder, test_data)
    
    # Summary
    print("\n" + "=" * 50)
    print("BENCHMARK SUMMARY")
    print("=" * 50)
    print(f"Initialization time: {init_time:.4f}s")
    print(f"Average single record: {statistics.mean(single_times):.4f}s")
    print(f"DataFrame batch (3 records): {df_time:.4f}s")
    print(f"DataFrame efficiency: {df_time / sum(single_times):.2f}x vs individual")
    print(f"Best throughput: {max(r['records_per_sec'] for r in scaling_results):.2f} records/sec")
    
    # Save results for comparison
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    results_file = f"benchmark_results_{timestamp}.txt"
    
    with open(results_file, 'w') as f:
        f.write("SOCCoder Performance Benchmark Results\n")
        f.write("=" * 50 + "\n")
        f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Initialization time: {init_time:.4f}s\n")
        f.write(f"Average single record: {statistics.mean(single_times):.4f}s\n")
        f.write(f"DataFrame batch (3 records): {df_time:.4f}s\n")
        f.write("\nScaling Results:\n")
        for r in scaling_results:
            f.write(f"Size {r['size']:2d}: {r['total_time']:.4f}s, {r['records_per_sec']:.2f} rec/sec\n")
    
    print(f"\nResults saved to: {results_file}")


if __name__ == "__main__":
    main()
