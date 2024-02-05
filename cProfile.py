import cProfile

def your_slow_function():
    # Your actual code goes here
    total = 0
    for i in range(1000000):
        total += i
    return total

# Wrap your code with cProfile
if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    # Call the function you want to profile
    result = your_slow_function()

    profiler.disable()
    
    # You can print the profiling results or save them to a file
    profiler.print_stats(sort='cumulative')
    # profiler.dump_stats('profile_results.prof')
