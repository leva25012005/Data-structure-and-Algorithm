import os
import json

# Đường dẫn file JSON
json_file = r"E:\Github\Data-structure-and-Algorithm\Data\Stage 1\1.Math.json"

# Đọc dữ liệu JSON (danh sách các bài toán)
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Tên folder từ tên file json
base_name = os.path.splitext(os.path.basename(json_file))[0]

# Tạo Docs folder
docs_folder = os.path.join(r"E:\Github\Data-structure-and-Algorithm\Docs", base_name)
os.makedirs(docs_folder, exist_ok=True)

# Tạo Solutions/LeetCode folder
solutions_folder = os.path.join(r"E:\Github\Data-structure-and-Algorithm\Solutions", base_name)
os.makedirs(solutions_folder, exist_ok=True)

# Lặp qua từng bài trong list JSON
for item in data:
    qid = item["questionFrontendId"]
    title = item["title"].replace(" ", "_")
    filename = f"{qid}_{title}.md"
    filepath = os.path.join(solutions_folder, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {qid}. {item['title']}\n\n")
        f.write(f"**Difficulty:** {item['difficulty']}\n")
        f.write(f"**Acceptance Rate:** {item['acRate']:.2f}%\n\n")

        # Tags
        f.write("## Tags\n")
        for tag in item.get("topicTags", []):
            f.write(f"- {tag['name']}\n")
        f.write("\n")

        # Similar Questions
        f.write("## Similar Questions\n")
        for sq in item.get("similarQuestions", []):
            f.write(f"- [{sq['title']}](https://leetcode.com/problems/{sq['titleSlug']}/) ({sq['difficulty']})\n")
        f.write("\n")

        # Companies
        f.write("## Asked By (Companies)\n")
        for comp in item.get("companies", []):
            f.write(f"- {comp['name']} ({comp['frequency']})\n")
