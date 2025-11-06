"""
Problem: Two Sum
Approach: Hash Map (Optimal Solution)
Time Complexity: O(n)
Space Complexity: O(n)
Author: BIT ISE Team - Axiom 2025
"""

def two_sum(nums, target):
    """
    Find two numbers in the array that add up to the target.
    
    Args:
        nums: List of integers
        target: Target sum
    
    Returns:
        List of two indices whose values add up to target
    
    Example:
        >>> two_sum([2, 7, 11, 15], 9)
        [0, 1]
    """
    # Dictionary to store value -> index mapping
    seen = {}
    
    # Iterate through the array
    for i, num in enumerate(nums):
        # Calculate the complement (value needed to reach target)
        complement = target - num
        
        # Check if complement exists in our hash map
        if complement in seen:
            # Found the pair! Return indices
            return [seen[complement], i]
        
        # Store current number and its index
        seen[num] = i
    
    # No solution found (though problem guarantees one exists)
    return []


def two_sum_brute_force(nums, target):
    """
    Brute force approach - check all pairs.
    Time Complexity: O(n²)
    Space Complexity: O(1)
    
    This approach is less efficient but easier to understand.
    """
    n = len(nums)
    
    # Check every pair of elements
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    
    return []


# Test cases
if __name__ == "__main__":
    # Test Case 1
    nums1 = [2, 7, 11, 15]
    target1 = 9
    print(f"Input: nums = {nums1}, target = {target1}")
    print(f"Output: {two_sum(nums1, target1)}")
    print(f"Expected: [0, 1]\n")
    
    # Test Case 2
    nums2 = [3, 2, 4]
    target2 = 6
    print(f"Input: nums = {nums2}, target = {target2}")
    print(f"Output: {two_sum(nums2, target2)}")
    print(f"Expected: [1, 2]\n")
    
    # Test Case 3
    nums3 = [3, 3]
    target3 = 6
    print(f"Input: nums = {nums3}, target = {target3}")
    print(f"Output: {two_sum(nums3, target3)}")
    print(f"Expected: [0, 1]\n")
    
    # Test Case 4: Negative numbers
    nums4 = [-1, -2, -3, -4, -5]
    target4 = -8
    print(f"Input: nums = {nums4}, target = {target4}")
    print(f"Output: {two_sum(nums4, target4)}")
    print(f"Expected: [2, 4] (since -3 + -5 = -8)\n")
