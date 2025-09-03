<div align="center">

# 🧠 [7. Reverse Integer](https://leetcode.com/problems/reverse-integer/)

[![LeetCode](https://img.shields.io/badge/LeetCode-Problem%207-FFA116?style=for-the-badge&logo=leetcode&logoColor=white)](https://leetcode.com/problems/reverse-integer/)

</div>

---

## 📋 Problem Overview

| Property            | Value                                                              |
| ------------------- | ------------------------------------------------------------------ |
| **Difficulty**      | 🟡 **Medium**                                                      |
| **Acceptance Rate** | `30.7%`                                                            |
| **Problem Link**    | [Open in LeetCode](https://leetcode.com/problems/reverse-integer/) |
| **Category**        | `1.Math`                                                           |

### 📝Description

<!-- description:start -->

<p>Given a signed 32-bit integer <code>x</code>, return <code>x</code><em> with its digits reversed</em>. If reversing <code>x</code> causes the value to go outside the signed 32-bit integer range <code>[-2<sup>31</sup>, 2<sup>31</sup> - 1]</code>, then return <code>0</code>.</p>

<p><strong>Assume the environment does not allow you to store 64-bit integers (signed or unsigned).</strong></p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> x = 123
<strong>Output:</strong> 321
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> x = -123
<strong>Output:</strong> -321
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> x = 120
<strong>Output:</strong> 21
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>-2<sup>31</sup> &lt;= x &lt;= 2<sup>31</sup> - 1</code></li>
</ul>

<!-- description:end -->

## ⏰ Progress Tracking

| Status           | Date         | Notes                                    |
| ---------------- | ------------ | ---------------------------------------- |
| 🎯 **Attempted** | `2025-09-02` | First attempt, understanding the problem |
| ✅ **Solved**    | `2025-09-02` | Successfully implemented solution        |
| 🔄 **Review 1**  | `YYYY-MM-DD` | First review, optimization               |
| 🔄 **Review 2**  | `YYYY-MM-DD` | Second review, different approaches      |
| 🔄 **Review 3**  | `YYYY-MM-DD` | Final review, mastery                    |

## 🏷️ Topics & Tags

<div align="center">

![Math](https://img.shields.io/badge/-Math-blue?style=flat-square)

</div>

## 🔗 Related Problems

| Problem                                                                                                                                                 | Difficulty    | Relationship    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | --------------- |
| [String to Integer (atoi)](https://leetcode.com/problems/string-to-integer-atoi/)                                                                       | 🟡 **Medium** | Similar logic   |
| [Reverse Bits](https://leetcode.com/problems/reverse-bits/)                                                                                             | 🟢 **Easy**   | Related concept |
| [A Number After a Double Reversal](https://leetcode.com/problems/a-number-after-a-double-reversal/)                                                     | 🟢 **Easy**   | Related concept |
| [Count Number of Distinct Integers After Reverse Operations](https://leetcode.com/problems/count-number-of-distinct-integers-after-reverse-operations/) | 🟡 **Medium** | Related concept |

## 🏢 Companies Asked (Frequency)

### 🔥 High Frequency (80%+)

- **Tech Mahindra** 🔥 88.9%
- **LTI** 🔥 88.8%
- **Wipro** 🔥 82.8%

### ⭐ Medium Frequency (60-79%)

- **Accenture** ⭐ 75.0%
- **Adobe** ⭐ 74.3%
- **Bloomberg** ⭐ 72.7%
- **Apple** ⭐ 71.6%
- **Deloitte** ⭐ 69.7%
- **Intel** ⭐ 69.6%
- **Cognizant** ⭐ 66.5%
- **Amazon** ⭐ 65.3%
- **Microsoft** ⭐ 62.5%
- **Infosys** ⭐ 62.1%

### 📈 Regular Frequency (40-59%)

- **tcs** 📈 59.9%
- **Qualcomm** 📈 56.6%
- **EPAM Systems** 📈 56.5%
- **Uber** 📈 53.3%
- **Yahoo** 📈 51.6%
- **Meta** 📈 49.4%
- **Nvidia** 📈 47.7%
- **Samsung** 📈 44.4%

<details>
<summary>📊 Low Frequency Companies (Click to expand)</summary>

- **Yandex** 📊 35.9%

</details>

---

## 💡 Solutions

### 🥉 Approach 1: Brute Force

#### 📝 Intuition

> We can build the reverse interger one digit at a time, while we canm check beforehamd **whether or not appending another digit would cause overflow**

#### 🔍 Algorithm

1. **Step 1:** **Initialize variables**
   - Set `reverse_number = 0`.
   - While `x != 0`, extract the last digit:  
      -`digit = x % 10`
     - Update `x = x / 10`.
2. **Step 2:** **Check for overflow**
   - Before updating `reverse_number`, check:
     - If `reverse_number > INT_MAX / 10`  
       or (`reverse_number == INT_MAX / 10` and `digit > 7`) → return `0`.
     - If `reverse_number < INT_MIN / 10`  
       or (`reverse_number == INT_MIN / 10` and `digit < -8`) → return `0`.
3. **Step 3:** **Update result**
   - If safe, compute:
     - `reverse_number = reverse_number * 10 + digit`.
   - Repeat until `x == 0`.
   - Return `reverse_number

#### 💻 Implementation

```cpp
// Brute force approach
//
// Args:
//   x: The integer input that will be reversed.
//      Can be positive, negative, or zero.
//
// Returns:
//   The reversed integer if it fits in 32-bit signed range.
//   If the reversed value overflows (outside [-2^31, 2^31 - 1]),
//   the function returns 0.

class Solution {
public:
    int reverse(int x) {
        int reverse_number = 0;
        while(x != 0) {
            int digit = x % 10;
            x /= 10;

            // Check for overflow BEFORE multiplying
            if (reverse_number > INT_MAX / 10 ||
                (reverse_number == INT_MAX / 10 && digit > 7)) {
                return 0; // Positive overflow
            }
            if (reverse_number < INT_MIN / 10 ||
                (reverse_number == INT_MIN / 10 && digit < -8)) {
                return 0; // Negative overflow
            }

             reverse_number = reverse_number * 10 + digit;
        }
        return reverse_number;
    }
};
```

#### 📊 Complexity Analysis

- **Time Complexity:** `O(log₁₀(n))`
  - Because we process each digit of `x` once.
  - For a 32-bit integer, the maximum number of digits is 10 → so it's effectively constant time, but formally `O(log n)`.
- **Space Complexity:** `O(1)`
  - We only use a few integer variables (`reverse_number`, `digit`), no extra data structures.

#### ⚠️ Pros & Cons

- ✅ **Pros:**

  - Simple, easy to implement
  - Constant extra space
  - Works directly with integer math (no need for string conversion)

- ❌ **Cons:**
  - Needs careful overflow handling
  - Still limited to 32-bit signed integers
  - Cannot be directly reused for arbitrary-length numbers

#### 🎯 Why This is Optimal?

- O(1) space: uses only temporary variables, no extra data structures.
- O(log₁₀n) time: processes each digit once, which is the minimum possible.
- Direct digit manipulation: no string or array conversion needed.
- Overflow checked in-place: guarantees correctness within 32-bit signed range.
- Simple and clean implementation: just a while loop with % and /.
- No external dependencies: relies only on basic arithmetic.
- Works for all cases: handles positive, negative, and zero inputs.

---

## 📚 Key Learnings & Notes

### 🔑 Key Insights

- **Insight 1:** Reversing an integer can be done digit by digit using `%` and `/`.
- **Insight 2:** Overflow must be checked _before_ multiplying and adding digits.
- **Insight 3:** No need to convert the number to a string → faster and memory-efficient.
- **Insight 4:** Negative numbers work naturally with the same logic.
- **Insight 5:** The minimum time complexity is proportional to the number of digits.

### 💭 Common Mistakes to Avoid

- ❌ **Mistake 1:** Checking for overflow _after_ updating the reversed number → may cause undefined behavior.
- ❌ **Mistake 2:** Forgetting that negative numbers must also be handled.
- ❌ **Mistake 3:** Using `abs(x)` without caution → `INT_MIN` cannot be represented as positive.
- ❌ **Mistake 4:** Relying on `long long` and then casting down → not acceptable in strict interview settings.
- ❌ **Mistake 5:** Converting to string unnecessarily → wastes memory and time.

### 🎯 Patterns & Techniques Used

- **Pattern:** Digit-by-digit decomposition (extract last digit, reduce original).
- **Pattern:** Overflow-safe accumulation (check boundaries before operation).
- **Technique:** Constant-space arithmetic manipulation instead of string processing.
- **Technique:** Early termination if overflow is detected.

### 🔄 Follow-up Questions

1. **Q:** How would you modify this if the input was a 64-bit integer instead of 32-bit?
   **A:** Adjust the overflow boundaries to `[-2^63, 2^63 - 1]` and use `long long` in C++.

2. **Q:** What if we wanted to reverse only the digits of a positive number, ignoring overflow?
   **A:** Skip the overflow check logic and directly compute until `x == 0`.

3. **Q:** Can you solve the same problem using string manipulation? What are the trade-offs?
   **A:** Yes, convert `x` to a string, reverse it, and convert back. It’s simpler to implement but uses extra O(n) space and is less efficient.

4. **Q:** How would you extend this logic to reverse digits in other bases (e.g., base 16)?
   **A:** Replace `% 10` and `/ 10` with `% base` and `/ base`, adjusting overflow checks accordingly.

<div align="center">

**🎯 Problem 7 Completed!**

_Happy Coding! 🚀_

</div>
```
