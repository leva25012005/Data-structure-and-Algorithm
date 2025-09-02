import os
import json
from datetime import datetime

# Đường dẫn file JSON
json_file = r"E:\Github\Data-structure-and-Algorithm\Data\Stage 1\1.Math.json"

# Đọc dữ liệu JSON (danh sách các bài toán)
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Tên folder từ tên file json
base_name = os.path.splitext(os.path.basename(json_file))[0]

# Tạo file Docs .md
docs_folder = r"E:\Github\Data-structure-and-Algorithm\Docs"
os.makedirs(docs_folder, exist_ok=True)
docs_file = os.path.join(docs_folder, f"{base_name}.md")

# Tạo Solutions folder
solutions_folder = os.path.join(r"E:\Github\Data-structure-and-Algorithm\Solutions", base_name)
os.makedirs(solutions_folder, exist_ok=True)

def clean_filename(title):
    """Làm sạch tên file, loại bỏ ký tự không hợp lệ"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        title = title.replace(char, '')
    return title.replace(' ', '_')

def get_difficulty_badge(difficulty):
    """Tạo badge màu sắc cho độ khó"""
    colors = {
        'Easy': '🟢',
        'Medium': '🟡', 
        'Hard': '🔴'
    }
    return f"{colors.get(difficulty, '⚪')} **{difficulty}**"

def get_frequency_badge(frequency):
    """Tạo badge cho frequency của company"""
    if frequency >= 80:
        return f"🔥 {frequency}%"
    elif frequency >= 60:
        return f"⭐ {frequency}%"
    elif frequency >= 40:
        return f"📈 {frequency}%"
    else:
        return f"📊 {frequency}%"

# Lặp qua từng bài trong list JSON
for item in data:
    qid = item["questionFrontendId"]
    title = item["title"]
    clean_title = clean_filename(title)
    filename = f"{qid}_{clean_title}.md"
    filepath = os.path.join(solutions_folder, filename)
    
    # Tạo URL cho LeetCode problem
    title_slug = item.get("titleSlug", title.lower().replace(" ", "-"))
    leetcode_url = f"https://leetcode.com/problems/{title_slug}/"
    
    with open(filepath, "w", encoding="utf-8") as f:
        # Header với styling đẹp
        f.write(f"<div align=\"center\">\n\n")
        f.write(f"# 🧠 [{qid}. {title}]({leetcode_url})\n\n")
        f.write(f"[![LeetCode](<https://img.shields.io/badge/LeetCode-Problem%20{qid}-FFA116?style=for-the-badge&logo=leetcode&logoColor=white>)]({leetcode_url})\n\n")
        f.write(f"</div>\n\n")
        f.write("---\n\n")
        
        # Problem Overview với styling
        f.write("## 📋 Problem Overview\n\n")
        f.write("| Property | Value |\n")
        f.write("|----------|-------|\n")
        f.write(f"| **Difficulty** | {get_difficulty_badge(item['difficulty'])} |\n")
        f.write(f"| **Acceptance Rate** | `{item['acRate']:.1f}%` |\n")
        f.write(f"| **Problem Link** | [Open in LeetCode]({leetcode_url}) |\n")
        f.write(f"| **Category** | `{base_name}` |\n\n")
        
        # Progress Tracking Section
        f.write("## ⏰ Progress Tracking\n\n")
        f.write("| Status | Date | Notes |\n")
        f.write("|--------|------|-------|\n")
        f.write("| 🎯 **Attempted** | `YYYY-MM-DD` | First attempt, understanding the problem |\n")
        f.write("| ✅ **Solved** | `YYYY-MM-DD` | Successfully implemented solution |\n")
        f.write("| 🔄 **Review 1** | `YYYY-MM-DD` | First review, optimization |\n")
        f.write("| 🔄 **Review 2** | `YYYY-MM-DD` | Second review, different approaches |\n")
        f.write("| 🔄 **Review 3** | `YYYY-MM-DD` | Final review, mastery |\n\n")
        
        # Tags section với styling đẹp
        if item.get("topicTags"):
            f.write("## 🏷️ Topics & Tags\n\n")
            f.write("<div align=\"center\">\n\n")
            for tag in item.get("topicTags", []):
                f.write(f"![{tag['name']}](https://img.shields.io/badge/-{tag['name'].replace(' ', '%20')}-blue?style=flat-square) ")
            f.write("\n\n</div>\n\n")
        
        # Similar Questions với table đẹp
        similar_questions = item.get("similarQuestions", [])
        if similar_questions:
            f.write("## 🔗 Related Problems\n\n")
            f.write("| Problem | Difficulty | Relationship |\n")
            f.write("|---------|------------|-------------|\n")
            for i, sq in enumerate(similar_questions):
                sq_url = f"https://leetcode.com/problems/{sq['titleSlug']}/"
                difficulty_badge = get_difficulty_badge(sq['difficulty'])
                relationship = "Similar logic" if i == 0 else "Related concept"
                f.write(f"| [{sq['title']}]({sq_url}) | {difficulty_badge} | {relationship} |\n")
            f.write("\n")
        
        # Companies section với frequency badges
        companies = item.get("companies", [])
        if companies:
            f.write("## 🏢 Companies Asked (Frequency)\n\n")
            
            # Sort companies by frequency
            sorted_companies = sorted(companies, key=lambda x: x['frequency'], reverse=True)
            
            f.write("### 🔥 High Frequency (80%+)\n")
            high_freq = [c for c in sorted_companies if c['frequency'] >= 80]
            if high_freq:
                for comp in high_freq:
                    f.write(f"- **{comp['name']}** {get_frequency_badge(comp['frequency'])}\n")
            else:
                f.write("*No high frequency companies*\n")
            f.write("\n")
            
            f.write("### ⭐ Medium Frequency (60-79%)\n")
            med_freq = [c for c in sorted_companies if 60 <= c['frequency'] < 80]
            if med_freq:
                for comp in med_freq:
                    f.write(f"- **{comp['name']}** {get_frequency_badge(comp['frequency'])}\n")
            else:
                f.write("*No medium frequency companies*\n")
            f.write("\n")
            
            f.write("### 📈 Regular Frequency (40-59%)\n")
            reg_freq = [c for c in sorted_companies if 40 <= c['frequency'] < 60]
            if reg_freq:
                for comp in reg_freq:
                    f.write(f"- **{comp['name']}** {get_frequency_badge(comp['frequency'])}\n")
            else:
                f.write("*No regular frequency companies*\n")
            f.write("\n")
            
            # Show low frequency in collapsed section
            low_freq = [c for c in sorted_companies if c['frequency'] < 40]
            if low_freq:
                f.write("<details>\n")
                f.write("<summary>📊 Low Frequency Companies (Click to expand)</summary>\n\n")
                for comp in low_freq:
                    f.write(f"- **{comp['name']}** {get_frequency_badge(comp['frequency'])}\n")
                f.write("\n</details>\n\n")
        
        # Solution template với multiple approaches
        f.write("---\n\n")
        f.write("## 💡 Solutions\n\n")
        
        # Approach 1 - Brute Force
        f.write("### 🥉 Approach 1: Brute Force\n\n")
        f.write("#### 📝 Intuition\n")
        f.write("> Mô tả ý tưởng đơn giản nhất để giải quyết bài toán\n\n")
        
        f.write("#### 🔍 Algorithm\n")
        f.write("1. **Step 1:** Mô tả bước đầu tiên\n")
        f.write("2. **Step 2:** Mô tả bước thứ hai\n")
        f.write("3. **Step 3:** Mô tả bước cuối cùng\n\n")
        
        f.write("#### 💻 Implementation\n\n")
        f.write("```cpp\n")
        f.write("// Brute force approach\n")
        f.write("//\n")
        f.write("// Args:\n")
        f.write("//   nums: Input parameter\n")
        f.write("//\n")
        f.write("// Returns:\n")
        f.write("//   Result\n")
        f.write("\n")
        f.write("class Solution {\n")
        f.write("public:\n")
        f.write("    int solutionBruteForce(vector<int>& nums) {\n")
        f.write("        // Implementation here\n")
        f.write("        return 0;\n")
        f.write("    }\n")
        f.write("};\n")
        f.write("```\n\n")

        
        f.write("#### 📊 Complexity Analysis\n")
        f.write("- **Time Complexity:** `O(?)` - Giải thích\n")
        f.write("- **Space Complexity:** `O(?)` - Giải thích\n\n")
        
        f.write("#### ⚠️ Pros & Cons\n")
        f.write("- ✅ **Pros:** Đơn giản, dễ hiểu\n")
        f.write("- ❌ **Cons:** Hiệu suất thấp\n\n")
        
        # Approach 2 - Optimized
        f.write("### 🥈 Approach 2: Optimized Solution\n\n")
        f.write("#### 📝 Intuition\n")
        f.write("> Mô tả cách tối ưu hóa từ approach đầu tiên\n\n")
        
        f.write("#### 🔍 Algorithm\n")
        f.write("1. **Step 1:** Bước cải tiến đầu tiên\n")
        f.write("2. **Step 2:** Bước cải tiến thứ hai\n")
        f.write("3. **Step 3:** Bước hoàn thiện\n\n")
        
        f.write("#### 💻 Implementation\n\n")
        f.write("```cpp\n")
        f.write("// Optimized approach with better complexity\n")
        f.write("//\n")
        f.write("// Args:\n")
        f.write("//   nums: Input parameter\n")
        f.write("//\n")
        f.write("// Returns:\n")
        f.write("//   Result\n")
        f.write("\n")
        f.write("class Solution {\n")
        f.write("public:\n")
        f.write("    int solutionOptimized(vector<int>& nums) {\n")
        f.write("        // Optimized implementation here\n")
        f.write("        return 0;\n")
        f.write("    }\n")
        f.write("};\n")
        f.write("```\n\n")


        
        f.write("#### 📊 Complexity Analysis\n")
        f.write("- **Time Complexity:** `O(?)` - Giải thích cải tiến\n")
        f.write("- **Space Complexity:** `O(?)` - Giải thích cải tiến\n\n")

        # Approach 3 - Best Solution
        f.write("### 🥇 Approach 3: Optimal Solution ⭐\n\n")
        f.write("#### 📝 Intuition\n")
        f.write("> Mô tả giải pháp tốt nhất, elegant nhất\n\n")

        f.write("#### 🔍 Algorithm\n")
        f.write("1. **Step 1:** Bước tối ưu đầu tiên\n")
        f.write("2. **Step 2:** Bước tối ưu thứ hai\n")
        f.write("3. **Step 3:** Bước hoàn hảo\n\n")

        f.write("#### 💻 Implementation\n\n")
        f.write("```cpp\n")
        f.write("// Most optimal and elegant solution\n")
        f.write("//\n")
        f.write("// Args:\n")
        f.write("//   nums: Input parameter\n")
        f.write("//\n")
        f.write("// Returns:\n")
        f.write("//   Result\n")
        f.write("\n")
        f.write("class Solution {\n")
        f.write("public:\n")
        f.write("    int solutionOptimal(vector<int>& nums) {\n")
        f.write("        // Optimal implementation here\n")
        f.write("        return 0;\n")
        f.write("    }\n")
        f.write("};\n")
        f.write("```\n\n")

        
        f.write("#### 📊 Complexity Analysis\n")
        f.write("- **Time Complexity:** `O(?)` - Tối ưu nhất có thể\n")
        f.write("- **Space Complexity:** `O(?)` - Tối ưu nhất có thể\n\n")
        
        f.write("#### 🎯 Why This is Optimal?\n")
        f.write("- Lý do 1: ...\n")
        f.write("- Lý do 2: ...\n")
        f.write("- Lý do 3: ...\n\n")
        
        # Test Cases
        f.write("---\n\n")
        f.write("## 🧪 Test Cases\n\n")
        f.write("```python\n")
        f.write("# Test Case 1: Basic example\n")
        f.write("input1 = []\n")
        f.write("expected1 = []\n")
        f.write("assert solution_optimal(input1) == expected1\n\n")
        
        f.write("# Test Case 2: Edge case\n")
        f.write("input2 = []\n")
        f.write("expected2 = []\n")
        f.write("assert solution_optimal(input2) == expected2\n\n")
        
        f.write("# Test Case 3: Complex case\n")
        f.write("input3 = []\n")
        f.write("expected3 = []\n")
        f.write("assert solution_optimal(input3) == expected3\n")
        f.write("```\n\n")
        
        # Learning Notes
        f.write("## 📚 Key Learnings & Notes\n\n")
        f.write("### 🔑 Key Insights\n")
        f.write("- **Insight 1:** Điểm quan trọng số 1\n")
        f.write("- **Insight 2:** Điểm quan trọng số 2\n")
        f.write("- **Insight 3:** Điểm quan trọng số 3\n\n")
        
        f.write("### 💭 Common Mistakes to Avoid\n")
        f.write("- ❌ **Mistake 1:** Lỗi thường gặp và cách tránh\n")
        f.write("- ❌ **Mistake 2:** Lỗi thường gặp và cách tránh\n")
        f.write("- ❌ **Mistake 3:** Lỗi thường gặp và cách tránh\n\n")
        
        f.write("### 🎯 Patterns & Techniques Used\n")
        f.write("- **Pattern 1:** Tên pattern và ứng dụng\n")
        f.write("- **Pattern 2:** Tên pattern và ứng dụng\n")
        f.write("- **Technique:** Kỹ thuật đặc biệt được sử dụng\n\n")
        
        f.write("### 🔄 Follow-up Questions\n")
        f.write("1. **Q:** Câu hỏi mở rộng 1?\n")
        f.write("   **A:** Trả lời và hướng giải quyết\n\n")
        f.write("2. **Q:** Câu hỏi mở rộng 2?\n")
        f.write("   **A:** Trả lời và hướng giải quyết\n\n")
        
        # Footer
        f.write("---\n\n")
        f.write("<div align=\"center\">\n\n")
        f.write(f"**🎯 Problem {qid} Completed!**\n\n")
        f.write("*Happy Coding! 🚀*\n\n")
        f.write("</div>\n")

# Tạo file docs tổng hợp với tracking (Enhanced Version)
with open(docs_file, "w", encoding="utf-8") as f:
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    f.write("<div align=\"center\">\n\n")
    f.write(f"# 📊 {base_name} - LeetCode Progress Tracker\n\n")
    f.write(f"![Problems](https://img.shields.io/badge/Total%20Problems-{len(data)}-blue?style=for-the-badge)\n")
    f.write(f"![Progress](https://img.shields.io/badge/Completed-0%2F{len(data)}-red?style=for-the-badge)\n")
    f.write(f"![Last Updated](https://img.shields.io/badge/Last%20Updated-{current_date}-green?style=for-the-badge)\n\n")
    f.write("</div>\n\n")
    f.write("---\n\n")
    
    # Table of Contents
    f.write("## 📑 Table of Contents\n\n")
    f.write("1. [📈 Progress Statistics](#-progress-statistics)\n")
    f.write("2. [🏢 Top Companies by Question Frequency](#-top-companies-by-question-frequency)\n")
    f.write("3. [🎯 Pattern Recognition Guide](#-pattern-recognition-guide)\n")
    f.write("4. [❌ Common Mistakes & How to Avoid](#-common-mistakes--how-to-avoid)\n")
    f.write("5. [📋 Problems Progress Tracker](#-problems-progress-tracker)\n")
    f.write("6. [📖 How to Use This Tracker](#-how-to-use-this-tracker)\n\n")
    
    # Statistics
    difficulty_stats = {}
    for item in data:
        diff = item['difficulty']
        difficulty_stats[diff] = difficulty_stats.get(diff, 0) + 1
    
    f.write("## 📈 Progress Statistics\n\n")
    f.write("| Difficulty | Total | Solved | Remaining | Progress |\n")
    f.write("|------------|-------|--------|-----------|----------|\n")
    for diff in ['Easy', 'Medium', 'Hard']:
        if diff in difficulty_stats:
            count = difficulty_stats[diff]
            badge = get_difficulty_badge(diff)
            f.write(f"| {badge} | `{count}` | `0` | `{count}` | ![Progress](https://img.shields.io/badge/Progress-0%25-red) |\n")
    f.write("\n")
    
    # Company frequency analysis
    f.write("## 🏢 Top Companies by Question Frequency\n\n")
    company_freq = {}
    for item in data:
        for comp in item.get("companies", []):
            if comp['name'] not in company_freq:
                company_freq[comp['name']] = []
            company_freq[comp['name']].append(comp['frequency'])
    
    # Calculate average frequency per company
    company_avg = {}
    for company, freqs in company_freq.items():
        company_avg[company] = sum(freqs) / len(freqs)
    
    sorted_companies = sorted(company_avg.items(), key=lambda x: (len(company_freq[x[0]]), x[1]), reverse=True)[:10]
    
    f.write("| Rank | Company | Questions | Avg Frequency | Total Score |\n")
    f.write("|------|---------|-----------|---------------|-------------|\n")
    for i, (company, avg_freq) in enumerate(sorted_companies, 1):
        question_count = len(company_freq[company])
        total_score = question_count * avg_freq
        f.write(f"| {i} | **{company}** | `{question_count}` | `{avg_freq:.1f}%` | `{total_score:.1f}` |\n")
    f.write("\n")
    
    # Pattern Recognition Guide - NEW SECTION
    f.write("## 🎯 Pattern Recognition Guide\n\n")
    f.write("### 🔍 How to Identify Problem Types\n\n")
    
    # Determine the category and provide specific patterns
    category_patterns = {
        "Array": {
            "keywords": ["array", "subarray", "subsequence", "sliding window", "two pointers"],
            "signals": [
                "Finding pairs/triplets with specific sum",
                "Maximum/minimum subarray problems", 
                "Sliding window operations",
                "Two pointers technique applicable"
            ],
            "common_approaches": [
                "Two Pointers: When dealing with sorted arrays or finding pairs",
                "Sliding Window: For subarray problems with constraints",
                "Prefix Sum: For range sum queries",
                "Binary Search: For searching in sorted arrays"
            ]
        },
        "String": {
            "keywords": ["string", "substring", "palindrome", "anagram", "pattern"],
            "signals": [
                "String matching or pattern finding",
                "Palindrome detection",
                "Anagram or character frequency problems",
                "String transformation"
            ],
            "common_approaches": [
                "Hash Map: For character frequency counting",
                "Two Pointers: For palindrome checking",
                "Sliding Window: For substring problems",
                "Dynamic Programming: For string matching"
            ]
        },
        "Math": {
            "keywords": ["math", "number", "digit", "prime", "factorial", "gcd"],
            "signals": [
                "Mathematical calculations or formulas",
                "Number theory problems",
                "Digit manipulation",
                "Geometric calculations"
            ],
            "common_approaches": [
                "Mathematical Formulas: Direct calculation approach",
                "Iteration: For digit processing",
                "Recursion: For factorial-like problems",
                "Modular Arithmetic: For large number operations"
            ]
        },
        "Tree": {
            "keywords": ["tree", "binary tree", "BST", "node", "root"],
            "signals": [
                "Tree traversal problems",
                "Finding paths or depths",
                "Tree construction/modification",
                "Binary Search Tree operations"
            ],
            "common_approaches": [
                "DFS (Recursion): For tree traversal and path problems",
                "BFS (Queue): For level-order operations",
                "Divide & Conquer: For tree construction",
                "Hash Map: For node mapping problems"
            ]
        },
        "Graph": {
            "keywords": ["graph", "connected", "path", "cycle", "edge"],
            "signals": [
                "Finding paths between nodes",
                "Detecting cycles",
                "Connected components",
                "Shortest path problems"
            ],
            "common_approaches": [
                "DFS: For connectivity and cycle detection",
                "BFS: For shortest path in unweighted graphs",
                "Union-Find: For connected components",
                "Dijkstra/Bellman-Ford: For weighted shortest paths"
            ]
        },
        "DP": {
            "keywords": ["maximum", "minimum", "count", "ways", "optimal"],
            "signals": [
                "Optimization problems (max/min)",
                "Counting number of ways",
                "Overlapping subproblems",
                "Decision making at each step"
            ],
            "common_approaches": [
                "1D DP: For linear decision problems",
                "2D DP: For grid or string matching problems",
                "Memoization: Top-down approach",
                "Tabulation: Bottom-up approach"
            ]
        }
    }
    
    # Try to determine the most likely category based on the base_name
    detected_category = None
    for category in category_patterns.keys():
        if category.lower() in base_name.lower():
            detected_category = category
            break
    
    if not detected_category:
        # Default to a general approach
        detected_category = "General"
    
    if detected_category in category_patterns:
        pattern_info = category_patterns[detected_category]
        
        f.write(f"### 🔎 **{detected_category}** Problem Recognition\n\n")
        
        f.write("#### 🚨 Key Signal Words\n")
        f.write("Look out for these keywords in problem statements:\n\n")
        for keyword in pattern_info["keywords"]:
            f.write(f"- `{keyword}`\n")
        f.write("\n")
        
        f.write("#### 🎯 Problem Signals\n")
        f.write("You should consider this category when you see:\n\n")
        for signal in pattern_info["signals"]:
            f.write(f"- ✅ {signal}\n")
        f.write("\n")
        
        f.write("#### 🛠️ Common Solution Approaches\n")
        for approach in pattern_info["common_approaches"]:
            f.write(f"- **{approach}**\n")
        f.write("\n")
        
    else:
        f.write("### 🔎 General Problem Recognition\n\n")
        f.write("#### 📝 Step-by-Step Analysis\n")
        f.write("1. **Read Carefully**: Identify input/output format\n")
        f.write("2. **Find Constraints**: Look at data size limits\n")
        f.write("3. **Identify Pattern**: Look for keywords and problem type\n")
        f.write("4. **Choose Approach**: Select appropriate algorithm/data structure\n")
        f.write("5. **Optimize**: Consider time/space complexity improvements\n\n")
    
    # Common Mistakes Section - NEW SECTION
    f.write("## ❌ Common Mistakes & How to Avoid\n\n")
    
    f.write("### 🚫 Algorithm & Logic Mistakes\n\n")
    f.write("| Mistake | Description | How to Avoid | Example |\n")
    f.write("|---------|-------------|--------------|----------|\n")
    f.write("| **Off-by-One Error** | Index bounds incorrect | Always double-check loop conditions | `for i in range(n-1)` vs `range(n)` |\n")
    f.write("| **Wrong Base Case** | Incorrect recursion termination | Test with smallest valid input | Forgetting `if n == 0: return 1` in factorial |\n")
    f.write("| **Integer Overflow** | Numbers exceed data type limits | Use appropriate data types | Use `long long` in C++ for large numbers |\n")
    f.write("| **Null Pointer** | Accessing null/None objects | Always check before access | `if node is not None:` before `node.val` |\n")
    f.write("| **Incorrect Comparison** | Wrong comparison operators | Be careful with edge cases | `<=` vs `<` in binary search |\n\n")
    
    f.write("### 🐛 Implementation Mistakes\n\n")
    f.write("| Mistake | Description | How to Avoid | Example |\n")
    f.write("|---------|-------------|--------------|----------|\n")
    f.write("| **Variable Scope** | Using wrong variable scope | Use descriptive names | Don't reuse `i` in nested loops |\n")
    f.write("| **Modifying While Iterating** | Changing collection during iteration | Use separate collections | Copy list before modification |\n")
    f.write("| **Shallow vs Deep Copy** | Incorrect copying of data structures | Understand copy semantics | `list.copy()` vs `copy.deepcopy()` |\n")
    f.write("| **String Immutability** | Treating strings as mutable | Use StringBuilder/list for modifications | Don't do `s += char` in loops |\n")
    f.write("| **Hash Map Key Issues** | Using mutable objects as keys | Use immutable keys only | Use tuple instead of list as key |\n\n")
    
    f.write("### 💭 Logical Thinking Mistakes\n\n")
    f.write("| Mistake | Description | How to Avoid | Prevention |\n")
    f.write("|---------|-------------|--------------|------------|\n")
    f.write("| **Assumptions** | Making incorrect assumptions about input | Read problem statement carefully | List all constraints explicitly |\n")
    f.write("| **Edge Cases** | Not considering boundary conditions | Think about min/max/empty inputs | Test with `[]`, `[1]`, large arrays |\n")
    f.write("| **Complexity Misunderstanding** | Wrong time/space analysis | Practice complexity analysis | Count nested loops and recursive calls |\n")
    f.write("| **Greedy Misconception** | Thinking local optimal = global optimal | Verify greedy choice property | Check if counter-examples exist |\n")
    f.write("| **Pattern Misapplication** | Using wrong algorithmic pattern | Match problem characteristics carefully | Don't force DP on every optimization problem |\n\n")
    
    f.write("### 🎯 Prevention Strategies\n\n")
    f.write("#### ✅ Before Coding Checklist\n")
    f.write("- [ ] **Understand the problem completely**\n")
    f.write("  - What exactly is the input and output?\n")
    f.write("  - What are the constraints?\n")
    f.write("  - Are there any special cases?\n\n")
    f.write("- [ ] **Plan your approach**\n")
    f.write("  - What algorithm/data structure will you use?\n")
    f.write("  - What's the expected time and space complexity?\n")
    f.write("  - Can you trace through a small example?\n\n")
    f.write("- [ ] **Consider edge cases**\n")
    f.write("  - Empty input\n")
    f.write("  - Single element\n")
    f.write("  - Maximum constraint values\n")
    f.write("  - Negative numbers (if applicable)\n\n")
    
    f.write("#### 🔍 During Coding Best Practices\n")
    f.write("- **Write clean, readable code** with meaningful variable names\n")
    f.write("- **Add comments** for complex logic\n")
    f.write("- **Test frequently** with small examples\n")
    f.write("- **Handle edge cases explicitly**\n")
    f.write("- **Double-check array bounds** and null checks\n\n")
    
    f.write("#### 🧪 After Coding Verification\n")
    f.write("- **Trace through your code** with the given examples\n")
    f.write("- **Test edge cases** you identified\n")
    f.write("- **Verify time/space complexity** matches requirements\n")
    f.write("- **Review for common mistake patterns**\n\n")
    
    # Problems tracking table
    f.write("## 📋 Problems Progress Tracker\n\n")
    f.write("| # | Problem | Difficulty | Status | Completed | Review 1 | Review 2 | Review 3 | Mistakes Made | Notes |\n")
    f.write("|---|---------|------------|--------|-----------|----------|----------|----------|---------------|-------|\n")
    
    for item in data:
        qid = item["questionFrontendId"]
        title = item["title"]
        title_slug = item.get("titleSlug", title.lower().replace(" ", "-"))
        leetcode_url = f"https://leetcode.com/problems/{title_slug}/"
        difficulty_badge = get_difficulty_badge(item['difficulty'])
        
        # Create link to solution file
        clean_title = clean_filename(title)
        solution_file = f"{qid}_{clean_title}.md"
        solution_link = f"Solutions/{base_name}/{solution_file}"
        
        f.write(f"| {qid} | [{title}]({solution_link}) | {difficulty_badge} | ⏳ | `____-__-__` | `____-__-__` | `____-__-__` | `____-__-__` |  |  |\n")
    
    f.write("\n")
    
    # Legend and Instructions (Enhanced)
    f.write("## 📖 How to Use This Tracker\n\n")
    f.write("### Status Icons\n")
    f.write("- ⏳ **Pending** - Not started\n")
    f.write("- 🔄 **In Progress** - Currently working on\n")
    f.write("- ✅ **Completed** - Successfully solved\n")
    f.write("- 🎯 **Mastered** - Fully understood and optimized\n")
    f.write("- 🔴 **Stuck** - Need help or hints\n")
    f.write("- ⚠️ **Review Needed** - Solution works but needs optimization\n\n")
    
    f.write("### Date Format\n")
    f.write("- Use format: `YYYY-MM-DD`\n")
    f.write("- **Completed:** Date when you first solved the problem\n")
    f.write("- **Review 1:** First review (1-2 weeks after completion)\n")
    f.write("- **Review 2:** Second review (1 month after completion)\n")
    f.write("- **Review 3:** Final review (3 months after completion)\n\n")
    
    f.write("### Mistakes Tracking\n")
    f.write("Use abbreviations in the 'Mistakes Made' column:\n")
    f.write("- **OBO** - Off-by-one error\n")
    f.write("- **NPE** - Null pointer exception\n")
    f.write("- **EC** - Missed edge cases\n")
    f.write("- **TC** - Time complexity issues\n")
    f.write("- **SC** - Space complexity issues\n")
    f.write("- **LOG** - Logical error\n")
    f.write("- **IMP** - Implementation mistake\n")
    f.write("- **ASS** - Wrong assumptions\n\n")
    
    f.write("### Tips for Effective Learning\n")
    f.write("1. 🎯 **Focus on understanding** rather than just solving\n")
    f.write("2. 📝 **Document your approach** and mistakes in the solution files\n")
    f.write("3. 🔄 **Regular reviews** help retain knowledge and spot patterns\n")
    f.write("4. 💡 **Learn multiple approaches** for the same problem\n")
    f.write("5. 🏢 **Pay attention to company frequency** for interview prep\n")
    f.write("6. ❌ **Track your mistakes** to avoid repeating them\n")
    f.write("7. 🧠 **Use the pattern recognition guide** to identify problem types quickly\n\n")
    
    # Quick Stats Summary (Enhanced)
    f.write("## 🎯 Quick Actions & Study Plan\n\n")
    f.write("### 📅 Daily Routine\n")
    f.write("- [ ] **Morning (30 min):** Review 2-3 previously solved problems\n")
    f.write("- [ ] **Evening (60-90 min):** Solve 1-2 new problems\n")
    f.write("- [ ] **Weekend:** Focus on weak areas and pattern practice\n\n")
    
    f.write("### 🎯 Priority Actions\n")
    f.write("- [ ] Set up daily coding schedule\n")
    f.write("- [ ] Prioritize high-frequency company problems\n")
    f.write("- [ ] Focus on weak topic areas identified in mistakes\n")
    f.write("- [ ] Schedule regular review sessions (spaced repetition)\n")
    f.write("- [ ] Track time spent on each problem\n")
    f.write("- [ ] Create a mistake journal for common errors\n")
    f.write("- [ ] Practice pattern recognition with new problems\n\n")
    
    f.write("### 📊 Weekly Goals\n")
    f.write("- [ ] **Week 1-2:** Focus on easy problems, build confidence\n")
    f.write("- [ ] **Week 3-4:** Mix easy/medium, identify patterns\n")
    f.write("- [ ] **Week 5-8:** Medium problems, optimize solutions\n")
    f.write("- [ ] **Week 9+:** Hard problems, interview-level proficiency\n\n")
    
    f.write("---\n\n")
    f.write("<div align=\"center\">\n\n")
    f.write(f"*Generated on {current_date} from `{os.path.basename(json_file)}`*\n\n")
    f.write("**Happy Coding! 🚀 Learn from Mistakes! 📈 Keep Going! 💪**\n\n")
    f.write("</div>\n")

print(f"✅ Successfully generated {len(data)} problem files!")
print(f"📄 Documentation file: {docs_file}")
print(f"📁 Solutions folder: {solutions_folder}")
print(f"🎯 Total problems processed: {len(data)}")
print(f"📊 Difficulty breakdown:")
for diff in ['Easy', 'Medium', 'Hard']:
    count = len([item for item in data if item['difficulty'] == diff])
    if count > 0:
        print(f"   {get_difficulty_badge(diff)}: {count} problems")
print("\n🚀 Ready to start your coding journey!")