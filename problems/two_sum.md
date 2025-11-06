# Two Sum

## Difficulty: Easy

## Problem Statement

Given an array of integers `nums` and an integer `target`, return indices of the two numbers in the array such that they add up to `target`.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

## Input Format

- First line: An array of integers `nums`
- Second line: An integer `target`

## Output Format

- An array of two integers representing the indices of the two numbers that add up to the target

## Constraints

- 2 ≤ nums.length ≤ 10^4
- -10^9 ≤ nums[i] ≤ 10^9
- -10^9 ≤ target ≤ 10^9
- Only one valid answer exists

## Examples

### Example 1:
```
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
```

### Example 2:
```
Input: nums = [3,2,4], target = 6
Output: [1,2]
Explanation: nums[1] + nums[2] == 6, so return [1, 2].
```

### Example 3:
```
Input: nums = [3,3], target = 6
Output: [0,1]
Explanation: nums[0] + nums[1] == 6, so return [0, 1].
```

## Follow-up

Can you come up with an algorithm that has better than O(n²) time complexity?

## Tags

`Array` `Hash Table` `Two Pointers`

## Hints

1. Think about using a hash map to store values you've already seen
2. For each element, check if (target - current element) exists in your hash map
3. Remember to handle the case where you can't use the same element twice

---

*Problem created for Axiom 2025 by BIT ISE Team*
