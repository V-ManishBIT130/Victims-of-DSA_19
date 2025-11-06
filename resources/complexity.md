# Time and Space Complexity Guide

Understanding complexity is crucial for writing efficient code. This guide will help you analyze and optimize your algorithms.

## 📊 What is Complexity?

**Complexity analysis** measures how the runtime or memory usage of an algorithm scales with input size.

- **Time Complexity**: How long an algorithm takes to run
- **Space Complexity**: How much memory an algorithm uses

## 🎯 Big O Notation

Big O describes the **worst-case** scenario - the upper bound of an algorithm's performance.

### Common Complexity Classes (from best to worst)

| Notation | Name | Description | Example |
|----------|------|-------------|---------|
| O(1) | Constant | Same time regardless of input | Array access, hash lookup |
| O(log n) | Logarithmic | Halves the problem each step | Binary search |
| O(n) | Linear | Proportional to input size | Linear search |
| O(n log n) | Linearithmic | Efficient sorting | Merge sort, quick sort |
| O(n²) | Quadratic | Nested loops | Bubble sort, simple comparisons |
| O(n³) | Cubic | Triple nested loops | Matrix multiplication |
| O(2ⁿ) | Exponential | Doubles with each addition | Recursive Fibonacci |
| O(n!) | Factorial | Permutations | Traveling salesman |

### Visual Growth Rates

```
Speed (Operations for n=100):
O(1)      →           1 operation
O(log n)  →           7 operations
O(n)      →         100 operations
O(n log n) →        664 operations
O(n²)     →      10,000 operations
O(2ⁿ)     → 1.27×10³⁰ operations
O(n!)     → 9.33×10¹⁵⁷ operations
```

## ⏱️ Time Complexity Analysis

### Rules for Calculating Time Complexity

1. **Drop Constants**: O(2n) → O(n)
2. **Drop Non-Dominant Terms**: O(n² + n) → O(n²)
3. **Different Inputs**: Use different variables (O(a + b), not O(n))
4. **Nested Loops**: Multiply complexities

### Examples

#### Example 1: O(1) - Constant Time
```python
def get_first_element(arr):
    return arr[0]  # Always one operation
```

#### Example 2: O(n) - Linear Time
```python
def print_all_elements(arr):
    for element in arr:  # Loop runs n times
        print(element)
```

#### Example 3: O(n²) - Quadratic Time
```python
def print_all_pairs(arr):
    for i in arr:          # n times
        for j in arr:      # n times each
            print(i, j)    # n × n = n²
```

#### Example 4: O(log n) - Logarithmic Time
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1  # Divides search space in half each time
```

#### Example 5: O(n log n) - Linearithmic Time
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])    # Divides: log n levels
    right = merge_sort(arr[mid:])
    
    return merge(left, right)       # Merge: n operations per level
    # Total: n operations × log n levels = O(n log n)
```

### Common Operations Complexity

#### Arrays
- Access: O(1)
- Search: O(n)
- Insert (at end): O(1)
- Insert (at beginning): O(n)
- Delete: O(n)

#### Linked Lists
- Access: O(n)
- Search: O(n)
- Insert (at head): O(1)
- Insert (at tail): O(1) with tail pointer
- Delete: O(1) if node is known

#### Hash Tables
- Average: O(1) for insert, delete, search
- Worst: O(n) with collisions

#### Binary Search Trees
- Average: O(log n) for insert, delete, search
- Worst: O(n) if unbalanced

#### Heaps
- Insert: O(log n)
- Extract Min/Max: O(log n)
- Peek: O(1)

## 💾 Space Complexity

Space complexity measures memory usage, including:
1. **Input Space**: Memory for input (usually not counted)
2. **Auxiliary Space**: Extra space used by algorithm
3. **Call Stack**: For recursive algorithms

### Examples

#### Example 1: O(1) - Constant Space
```python
def sum_array(arr):
    total = 0  # Only one variable
    for num in arr:
        total += num
    return total
```

#### Example 2: O(n) - Linear Space
```python
def create_copy(arr):
    new_arr = []
    for element in arr:
        new_arr.append(element)  # New array of size n
    return new_arr
```

#### Example 3: O(n) - Recursive Call Stack
```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)  # n recursive calls on stack
```

#### Example 4: O(log n) - Binary Search Space
```python
def binary_search_recursive(arr, target, left, right):
    if left > right:
        return -1
    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)
    # Call stack depth: log n
```

## 🎯 Optimization Strategies

### 1. Use Better Data Structures
- Hash Table instead of Array for lookups: O(n) → O(1)
- Heap instead of Array for min/max: O(n) → O(log n)

### 2. Avoid Nested Loops
- Use hash maps to eliminate inner loops
- Binary search instead of linear search

### 3. Cache Results (Memoization)
- Store computed results to avoid recalculation
- Dynamic programming approach

### 4. Early Termination
- Break loops when answer is found
- Use conditions to skip unnecessary work

### 5. Divide and Conquer
- Break problem into smaller subproblems
- Often achieves O(n log n) instead of O(n²)

## 📝 Practice Problems by Complexity

### O(n) Problems
- Two Sum (with hash map)
- Maximum Subarray Sum
- Reverse Array

### O(n log n) Problems
- Merge Sort
- Quick Sort
- Kth Largest Element

### O(log n) Problems
- Binary Search
- Search in Rotated Array
- First/Last Position in Sorted Array

### O(n²) Problems
- Bubble Sort (can be avoided)
- Check all pairs
- Naive pattern matching

## 🔍 How to Analyze Your Code

1. **Identify loops**: Each loop typically adds n to complexity
2. **Check nesting**: Nested loops multiply complexities
3. **Look for recursion**: Calculate recursion tree depth and branching
4. **Count operations**: How many times does each line execute?

### Quick Reference

```
Single loop                    → O(n)
Two nested loops              → O(n²)
Loop + Binary Search          → O(n log n)
Recursion splitting in half   → O(log n)
Building all combinations     → O(2ⁿ)
```

## 💡 Tips for Interviews

1. **Always analyze complexity**: Mention time and space complexity
2. **Discuss trade-offs**: "We can optimize time with more space"
3. **Start with brute force**: Then optimize
4. **Know common complexities**: Sorting is O(n log n), hash lookup is O(1)
5. **Consider best/average/worst**: Especially for quicksort

## 📚 Further Reading

- Master Theorem for recursive algorithms
- Amortized analysis for dynamic arrays
- Average vs worst-case complexity
- Big O, Big Omega, Big Theta differences

---

*Guide created by BIT ISE Team for Axiom 2025*

Master complexity analysis and become a better programmer! 🚀
