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

### profile_initialization.py
Profiles the SOCCoder initialization process to identify startup bottlenecks.
Useful for understanding and optimizing one-time setup costs.

Usage:
```bash
cd /path/to/occupationcoder
source venv/bin/activate
python tools/profile_initialization.py
```

## Performance Notes

The SOCCoder automatically creates a cache of cleaned job titles on first use to dramatically speed up subsequent initializations:

- **First run**: ~2.8s (creates cache with user feedback)
- **Subsequent runs**: ~0.5s (loads from cache)

The cache is automatically created in `occupationcoder/dictionaries/titles_cleaned_cache.pkl` and excluded from version control for licensing reasons.

## Note
These tools require the virtual environment to be activated and all dependencies installed.
They use the test data from `tests/test_vacancies.csv` for consistent benchmarking.
