# Common DSA Patterns

Recognizing patterns is key to solving problems efficiently. This guide covers the most common patterns you'll encounter.

## 🎯 Pattern Recognition

Learning these patterns helps you:
- Quickly identify solution approaches
- Choose the right data structure
- Optimize your solutions
- Handle similar problems with confidence

## 📚 Essential Patterns

### 1. Two Pointers Pattern

**When to Use**: Arrays, strings, linked lists - when you need to search pairs or process from both ends.

**How it Works**: Use two pointers moving towards each other or in the same direction.

**Time Complexity**: O(n)

**Example Problems**:
- Two Sum (sorted array)
- Remove duplicates from sorted array
- Container with most water
- Valid palindrome

**Template**:
```python
def two_pointer_pattern(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        # Process elements at left and right
        if condition:
            # Move pointers based on condition
            left += 1
        else:
            right -= 1
    return result
```

### 2. Sliding Window Pattern

**When to Use**: Finding subarrays/substrings with specific properties.

**How it Works**: Maintain a window of elements and slide it through the array.

**Time Complexity**: O(n)

**Example Problems**:
- Maximum sum subarray of size k
- Longest substring without repeating characters
- Minimum window substring
- Find all anagrams in a string

**Template**:
```python
def sliding_window(arr, k):
    window_start = 0
    window_sum = 0
    max_sum = 0
    
    for window_end in range(len(arr)):
        window_sum += arr[window_end]
        
        if window_end >= k - 1:
            max_sum = max(max_sum, window_sum)
            window_sum -= arr[window_start]
            window_start += 1
    
    return max_sum
```

### 3. Fast & Slow Pointers (Floyd's Algorithm)

**When to Use**: Linked lists, cycle detection, finding middle element.

**How it Works**: Two pointers move at different speeds.

**Time Complexity**: O(n)

**Example Problems**:
- Detect cycle in linked list
- Find middle of linked list
- Happy number
- Linked list cycle start

**Template**:
```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

### 4. Binary Search Pattern

**When to Use**: Sorted arrays, finding boundaries, optimization problems.

**How it Works**: Eliminate half the search space in each iteration.

**Time Complexity**: O(log n)

**Example Problems**:
- Search in sorted array
- First/last position of element
- Search in rotated sorted array
- Find minimum in rotated array

**Template**:
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

### 5. Hash Map Pattern

**When to Use**: Need fast lookup, counting frequencies, finding pairs.

**How it Works**: Store data in key-value pairs for O(1) access.

**Time Complexity**: O(n)

**Example Problems**:
- Two Sum
- Group anagrams
- Longest consecutive sequence
- Subarray sum equals k

**Template**:
```python
def hash_map_pattern(arr):
    freq_map = {}
    
    for element in arr:
        freq_map[element] = freq_map.get(element, 0) + 1
    
    # Process the frequency map
    return result
```

### 6. Backtracking Pattern

**When to Use**: Finding all solutions, combinatorial problems, constraints satisfaction.

**How it Works**: Try all possibilities, backtrack when a path fails.

**Time Complexity**: Often O(2ⁿ) or O(n!)

**Example Problems**:
- Generate all subsets
- Generate all permutations
- N-Queens problem
- Sudoku solver

**Template**:
```python
def backtrack(path, options):
    if is_valid_solution(path):
        result.append(path[:])
        return
    
    for option in options:
        # Choose
        path.append(option)
        
        # Explore
        backtrack(path, get_new_options())
        
        # Unchoose (backtrack)
        path.pop()
```

### 7. Dynamic Programming Pattern

**When to Use**: Overlapping subproblems, optimal substructure.

**How it Works**: Store results of subproblems to avoid recomputation.

**Time Complexity**: Varies (often O(n²))

**Example Problems**:
- Fibonacci numbers
- Climbing stairs
- Longest common subsequence
- Coin change

**Template (Top-Down)**:
```python
def dp_top_down(n, memo={}):
    if n in memo:
        return memo[n]
    
    if base_case(n):
        return base_result
    
    memo[n] = combine(dp_top_down(n-1), dp_top_down(n-2))
    return memo[n]
```

**Template (Bottom-Up)**:
```python
def dp_bottom_up(n):
    dp = [0] * (n + 1)
    dp[0] = base_case_0
    dp[1] = base_case_1
    
    for i in range(2, n + 1):
        dp[i] = combine(dp[i-1], dp[i-2])
    
    return dp[n]
```

### 8. BFS (Breadth-First Search) Pattern

**When to Use**: Level-order traversal, shortest path in unweighted graphs.

**How it Works**: Explore nodes level by level using a queue.

**Time Complexity**: O(V + E) for graphs, O(n) for trees

**Example Problems**:
- Binary tree level order traversal
- Shortest path in maze
- Word ladder
- Number of islands

**Template**:
```python
from collections import deque

def bfs(start):
    queue = deque([start])
    visited = {start}
    
    while queue:
        node = queue.popleft()
        
        # Process node
        process(node)
        
        # Add neighbors
        for neighbor in get_neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

### 9. DFS (Depth-First Search) Pattern

**When to Use**: Exploring all paths, tree/graph traversal.

**How it Works**: Explore as deep as possible before backtracking.

**Time Complexity**: O(V + E) for graphs, O(n) for trees

**Example Problems**:
- Binary tree traversal
- Number of islands
- Path sum in tree
- Clone graph

**Template (Recursive)**:
```python
def dfs(node, visited):
    if node is None or node in visited:
        return
    
    visited.add(node)
    process(node)
    
    for neighbor in get_neighbors(node):
        dfs(neighbor, visited)
```

**Template (Iterative)**:
```python
def dfs_iterative(start):
    stack = [start]
    visited = set()
    
    while stack:
        node = stack.pop()
        
        if node in visited:
            continue
        
        visited.add(node)
        process(node)
        
        for neighbor in get_neighbors(node):
            stack.append(neighbor)
```

### 10. Greedy Pattern

**When to Use**: Problems where local optimal choices lead to global optimum.

**How it Works**: Make the best choice at each step.

**Time Complexity**: Varies (often O(n log n) due to sorting)

**Example Problems**:
- Activity selection
- Jump game
- Gas station
- Fractional knapsack

**Template**:
```python
def greedy_pattern(arr):
    # Often need to sort first
    arr.sort()
    
    result = 0
    for element in arr:
        # Make greedy choice
        if is_best_choice(element):
            result += element
    
    return result
```

## 🎓 Pattern Selection Guide

### Problem → Pattern Mapping

| Problem Type | Likely Pattern |
|--------------|----------------|
| Find pairs summing to target | Two Pointers / Hash Map |
| Subarray/substring problems | Sliding Window |
| Linked list cycle/middle | Fast & Slow Pointers |
| Sorted array search | Binary Search |
| All combinations/permutations | Backtracking |
| Optimization with subproblems | Dynamic Programming |
| Tree level traversal | BFS |
| Tree/graph path problems | DFS |
| Optimal selection problems | Greedy |
| Need fast lookup/counting | Hash Map |

## 💡 Tips for Recognizing Patterns

1. **Read carefully**: Keywords often hint at patterns
   - "Sorted" → Binary Search
   - "Subarray" → Sliding Window
   - "All combinations" → Backtracking
   - "Shortest path" → BFS

2. **Analyze constraints**:
   - Small input (n ≤ 20) → Backtracking might work
   - Large input → Need O(n) or O(n log n) solution

3. **Look for structure**:
   - Overlapping subproblems → DP
   - Greedy choice property → Greedy
   - Graph/tree → BFS/DFS

4. **Consider optimization**:
   - Brute force is O(n²) → Can we use hash map for O(n)?
   - Need sorted → Binary search possible?

## 🔄 Pattern Combinations

Some problems require multiple patterns:
- **Sliding Window + Hash Map**: Longest substring without repeating characters
- **Binary Search + Two Pointers**: 3Sum closest
- **DFS + DP**: Tree DP problems
- **BFS + Hash Map**: Word ladder

## 📝 Practice Strategy

1. **Learn one pattern at a time**: Master before moving to next
2. **Solve 10+ problems per pattern**: Build pattern recognition
3. **Time yourself**: Improve speed
4. **Review solutions**: Learn alternative approaches
5. **Identify patterns in new problems**: Train your intuition

## 🎯 Pattern Practice Checklist

- [ ] Master Two Pointers (10 problems)
- [ ] Master Sliding Window (10 problems)
- [ ] Master Fast & Slow Pointers (5 problems)
- [ ] Master Binary Search (10 problems)
- [ ] Master Hash Map (10 problems)
- [ ] Master Backtracking (10 problems)
- [ ] Master Dynamic Programming (15 problems)
- [ ] Master BFS (10 problems)
- [ ] Master DFS (10 problems)
- [ ] Master Greedy (10 problems)

---

*Pattern guide created by BIT ISE Team for Axiom 2025*

Master these patterns and solve problems with confidence! 🚀
