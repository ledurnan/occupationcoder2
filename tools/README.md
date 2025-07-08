# Development Tools

This directory contains development and analysis tools for the occupationcoder project.

## Scripts

### benchmark_speed.py
Performance benchmark suite that measures:
- SOCCoder initialization time
- Single record processing speed
- DataFrame batch processing throughput
- Scaling performance across different dataset sizes

Usage:
```bash
cd /path/to/occupationcoder
source venv/bin/activate
python tools/benchmark_speed.py
```

Results are saved with timestamps for performance tracking over time.

### profile_per_record.py
Detailed performance profiler for identifying bottlenecks in per-record processing.
Uses Python's cProfile to show exactly where time is being spent.

Usage:
```bash
cd /path/to/occupationcoder
source venv/bin/activate
python tools/profile_per_record.py
```

Shows the top 20 functions by cumulative time to help identify optimization opportunities.

## Note
These tools require the virtual environment to be activated and all dependencies installed.
They use the test data from `tests/test_vacancies.csv` for consistent benchmarking.
