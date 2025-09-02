import os
import json
import re
from datetime import datetime, timedelta
import glob

class ProgressTracker:
    def __init__(self, base_path="E:\\Github\\Data-structure-and-Algorithm"):
        self.base_path = base_path
        self.docs_folder = os.path.join(base_path, "Docs")
        self.solutions_folder = os.path.join(base_path, "Solutions")
        self.data_folder = os.path.join(base_path, "Data", "Stage 1")
        
    def load_json_data(self, json_filename):
        """Load problem data from JSON file"""
        json_file = os.path.join(self.data_folder, json_filename)
        with open(json_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def get_current_progress(self, markdown_file):
        """Extract current progress from markdown table"""
        if not os.path.exists(markdown_file):
            return {}
        
        with open(markdown_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Find the progress table
        table_pattern = r'\| # \| Problem.*?\n((?:\|.*?\n)*)'
        match = re.search(table_pattern, content, re.DOTALL)
        
        if not match:
            return {}
        
        progress = {}
        lines = match.group(1).strip().split('\n')
        
        for line in lines:
            if line.strip() and '|' in line:
                parts = [p.strip() for p in line.split('|')[1:-1]]  # Remove empty first/last
                if len(parts) >= 9 and parts[0].isdigit():
                    qid = parts[0]
                    status = parts[2]
                    completed = parts[4].replace('`', '')
                    review1 = parts[5].replace('`', '')
                    review2 = parts[6].replace('`', '')
                    review3 = parts[7].replace('`', '')
                    mistakes = parts[8]
                    notes = parts[9] if len(parts) > 9 else ""
                    
                    progress[qid] = {
                        'status': status,
                        'completed': completed,
                        'review1': review1,
                        'review2': review2,
                        'review3': review3,
                        'mistakes': mistakes,
                        'notes': notes
                    }
        
        return progress
    
    def update_individual_solution_file(self, qid, title, status, completed_date, mistakes="", notes=""):
        """Update progress table in individual solution file"""
        base_name = self.current_category
        clean_title = self.clean_filename(title)
        solution_file = os.path.join(self.solutions_folder, base_name, f"{qid}_{clean_title}.md")
        
        if not os.path.exists(solution_file):
            print(f"⚠️  Solution file not found: {solution_file}")
            return False
        
        with open(solution_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Update the progress tracking table - FIXED
        # Look for markdown table specifically
        markdown_table_start = content.find("| Status | Date | Notes |\n|--------|------|-------|")
        if markdown_table_start != -1:
            # Find end of markdown table - look for next section or empty line
            table_end = markdown_table_start
            lines = content[markdown_table_start:].split('\n')
            
            # Count table lines (header + separator + data rows)
            for i, line in enumerate(lines):
                if not line.strip() or not line.startswith('|'):
                    table_end = markdown_table_start + len('\n'.join(lines[:i]))
                    break
            
            new_table = "| Status | Date | Notes |\n|--------|------|-------|\n"
            
            if status in ['✅', '🎯']:
                new_table += f"| 🎯 **Attempted** | `{completed_date}` | First attempt, understanding the problem |\n"
                new_table += f"| {status} **Solved** | `{completed_date}` | Successfully implemented solution"
                if mistakes:
                    new_table += f" (Mistakes: {mistakes})"
                new_table += " |\n"
            else:
                new_table += f"| 🎯 **Attempted** | `{completed_date}` | {notes or 'Working on solution...'} |\n"
                new_table += "| ✅ **Solved** | `YYYY-MM-DD` | Successfully implemented solution |\n"
            
            new_table += "| 🔄 **Review 1** | `YYYY-MM-DD` | First review, optimization |\n"
            new_table += "| 🔄 **Review 2** | `YYYY-MM-DD` | Second review, different approaches |\n"
            new_table += "| 🔄 **Review 3** | `YYYY-MM-DD` | Final review, mastery |"
            
            # Replace only the markdown table part
            updated_content = content[:markdown_table_start] + new_table + content[table_end:]
        else:
            updated_content = content
        
        with open(solution_file, "w", encoding="utf-8") as f:
            f.write(updated_content)
        
        return True
    
    def clean_filename(self, title):
        """Clean filename by removing invalid characters"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            title = title.replace(char, '')
        return title.replace(' ', '_')
    
    def update_progress(self, category, updates):
        """
        Update progress for problems in a category
        
        Args:
            category: Category name (e.g., "1.Math")
            updates: List of dictionaries with progress updates
                    [{"qid": "1", "status": "✅", "completed": "2024-01-15", "mistakes": "OBO", "notes": "Easy problem"}]
        """
        self.current_category = category
        
        # Load JSON data
        json_filename = f"{category}.json"
        try:
            data = self.load_json_data(json_filename)
        except FileNotFoundError:
            print(f"❌ JSON file not found: {json_filename}")
            return False
        
        # Load current progress
        docs_file = os.path.join(self.docs_folder, f"{category}.md")
        current_progress = self.get_current_progress(docs_file)
        
        # Apply updates
        for update in updates:
            qid = str(update["qid"])
            
            if qid not in current_progress:
                current_progress[qid] = {
                    'status': '⏳',
                    'completed': '____-__-__',
                    'review1': '____-__-__',
                    'review2': '____-__-__',
                    'review3': '____-__-__',
                    'mistakes': '',
                    'notes': ''
                }
            
            # Update values
            current_progress[qid]['status'] = update.get('status', current_progress[qid]['status'])
            current_progress[qid]['completed'] = update.get('completed', current_progress[qid]['completed'])
            current_progress[qid]['review1'] = update.get('review1', current_progress[qid]['review1'])
            current_progress[qid]['review2'] = update.get('review2', current_progress[qid]['review2'])
            current_progress[qid]['review3'] = update.get('review3', current_progress[qid]['review3'])
            current_progress[qid]['mistakes'] = update.get('mistakes', current_progress[qid]['mistakes'])
            current_progress[qid]['notes'] = update.get('notes', current_progress[qid]['notes'])
            
            # Update individual solution file
            problem = next((item for item in data if str(item["questionFrontendId"]) == qid), None)
            if problem:
                self.update_individual_solution_file(
                    qid, 
                    problem["title"], 
                    current_progress[qid]['status'], 
                    current_progress[qid]['completed'],
                    current_progress[qid]['mistakes'],
                    current_progress[qid]['notes']
                )
        
        # Regenerate the main documentation file with updated progress
        self.regenerate_docs_file(category, data, current_progress)
        
        return True
    
    def regenerate_docs_file(self, category, data, progress):
        """Regenerate the main docs file with updated progress"""
        docs_file = os.path.join(self.docs_folder, f"{category}.md")
        
        # Calculate statistics
        total_problems = len(data)
        completed_problems = len([p for p in progress.values() if p['status'] in ['✅', '🎯']])
        completion_percentage = (completed_problems / total_problems * 100) if total_problems > 0 else 0
        
        # Read current file and update statistics section
        if os.path.exists(docs_file):
            with open(docs_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Update the header badges
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            # Update progress badge
            if completion_percentage == 0:
                progress_color = "red"
            elif completion_percentage < 50:
                progress_color = "orange"
            elif completion_percentage < 100:
                progress_color = "yellow"
            else:
                progress_color = "green"
            
            content = re.sub(
                r'!\[Progress\]\(https://img\.shields\.io/badge/Completed-.*?\)',
                f'![Progress](https://img.shields.io/badge/Completed-{completed_problems}%2F{total_problems}-{progress_color}?style=for-the-badge)',
                content
            )
            
            content = re.sub(
                r'!\[Last Updated\]\(https://img\.shields\.io/badge/Last%20Updated-.*?\)',
                f'![Last Updated](https://img.shields.io/badge/Last%20Updated-{current_date}-green?style=for-the-badge)',
                content
            )
            
            # Update progress table
            table_start = content.find("| # | Problem | Difficulty | Status |")
            if table_start != -1:
                table_end = content.find("\n\n", table_start)
                
                new_table = "| # | Problem | Difficulty | Status | Completed | Review 1 | Review 2 | Review 3 | Mistakes Made | Notes |\n"
                new_table += "|---|---------|------------|--------|-----------|----------|----------|----------|---------------|-------|\n"
                
                for item in data:
                    qid = str(item["questionFrontendId"])
                    title = item["title"]
                    title_slug = item.get("titleSlug", title.lower().replace(" ", "-"))
                    leetcode_url = f"https://leetcode.com/problems/{title_slug}/"
                    difficulty_badge = self.get_difficulty_badge(item['difficulty'])
                    
                    # Create link to solution file
                    clean_title = self.clean_filename(title)
                    solution_file = f"{qid}_{clean_title}.md"
                    solution_link = f"Solutions/{category}/{solution_file}"
                    
                    # Get progress info
                    prog = progress.get(qid, {
                        'status': '⏳',
                        'completed': '____-__-__',
                        'review1': '____-__-__',
                        'review2': '____-__-__',
                        'review3': '____-__-__',
                        'mistakes': '',
                        'notes': ''
                    })
                    
                    new_table += f"| {qid} | [{title}]({solution_link}) | {difficulty_badge} | {prog['status']} | `{prog['completed']}` | `{prog['review1']}` | `{prog['review2']}` | `{prog['review3']}` | {prog['mistakes']} | {prog['notes']} |\n"
                
                content = content[:table_start] + new_table + content[table_end:]
            
            # Update statistics section
            difficulty_stats = {}
            for item in data:
                diff = item['difficulty']
                difficulty_stats[diff] = difficulty_stats.get(diff, 0) + 1
            
            # Update difficulty progress statistics
            stats_pattern = r'(\| Difficulty \| Total \| Solved \| Remaining \| Progress \|.*?\n\|.*?\n)(.*?)(\n.*?\*\*)'
            
            new_stats = ""
            for diff in ['Easy', 'Medium', 'Hard']:
                if diff in difficulty_stats:
                    total_count = difficulty_stats[diff]
                    solved_count = len([p for qid, p in progress.items() 
                                      if p['status'] in ['✅', '🎯'] 
                                      and any(item['difficulty'] == diff 
                                            for item in data 
                                            if str(item["questionFrontendId"]) == qid)])
                    remaining_count = total_count - solved_count
                    progress_pct = (solved_count / total_count * 100) if total_count > 0 else 0
                    
                    if progress_pct == 0:
                        progress_color = "red"
                    elif progress_pct < 50:
                        progress_color = "orange"
                    elif progress_pct < 100:
                        progress_color = "yellow"  
                    else:
                        progress_color = "green"
                    
                    difficulty_badge = self.get_difficulty_badge(diff)
                    new_stats += f"| {difficulty_badge} | `{total_count}` | `{solved_count}` | `{remaining_count}` | ![Progress](https://img.shields.io/badge/Progress-{progress_pct:.0f}%25-{progress_color}) |\n"
            
            content = re.sub(stats_pattern, f"\\1{new_stats}\\3", content, flags=re.DOTALL)
            
            with open(docs_file, "w", encoding="utf-8") as f:
                f.write(content)
    
    def get_difficulty_badge(self, difficulty):
        """Get difficulty badge with emoji"""
        colors = {
            'Easy': '🟢',
            'Medium': '🟡', 
            'Hard': '🔴'
        }
        return f"{colors.get(difficulty, '⚪')} **{difficulty}**"
    
    def bulk_update_from_file(self, category, update_file):
        """
        Bulk update from a CSV/text file
        Format: qid,status,completed,mistakes,notes
        """
        if not os.path.exists(update_file):
            print(f"❌ Update file not found: {update_file}")
            return False
        
        updates = []
        with open(update_file, "r", encoding="utf-8") as f:
            lines = f.readlines()[1:]  # Skip header
            
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    update = {
                        "qid": parts[0],
                        "status": parts[1],
                        "completed": parts[2],
                        "mistakes": parts[3] if len(parts) > 3 else "",
                        "notes": parts[4] if len(parts) > 4 else ""
                    }
                    updates.append(update)
        
        return self.update_progress(category, updates)
    
    def mark_completed(self, category, qid_list, date=None, mistakes="", notes=""):
        """Quick function to mark multiple problems as completed"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        updates = []
        for qid in qid_list:
            updates.append({
                "qid": qid,
                "status": "✅",
                "completed": date,
                "mistakes": mistakes,
                "notes": notes
            })
        
        return self.update_progress(category, updates)
    
    def mark_review(self, category, qid, review_number, date=None, notes=""):
        """Mark a problem for review (1, 2, or 3)"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        if review_number not in [1, 2, 3]:
            print("❌ Review number must be 1, 2, or 3")
            return False
        
        update = {"qid": qid}
        update[f"review{review_number}"] = date
        if notes:
            update["notes"] = notes
        
        return self.update_progress(category, [update])
    
    def get_due_reviews(self, category):
        """Get problems that are due for review based on spaced repetition"""
        docs_file = os.path.join(self.docs_folder, f"{category}.md")
        progress = self.get_current_progress(docs_file)
        
        today = datetime.now()
        due_reviews = {"review1": [], "review2": [], "review3": []}
        
        for qid, prog in progress.items():
            if prog['status'] in ['✅', '🎯'] and prog['completed'] != '____-__-__':
                try:
                    completed_date = datetime.strptime(prog['completed'], "%Y-%m-%d")
                    
                    # Review 1: 1-2 weeks after completion
                    if prog['review1'] == '____-__-__' and (today - completed_date).days >= 7:
                        due_reviews["review1"].append(qid)
                    
                    # Review 2: 1 month after completion
                    elif prog['review2'] == '____-__-__' and prog['review1'] != '____-__-__' and (today - completed_date).days >= 30:
                        due_reviews["review2"].append(qid)
                    
                    # Review 3: 3 months after completion
                    elif prog['review3'] == '____-__-__' and prog['review2'] != '____-__-__' and (today - completed_date).days >= 90:
                        due_reviews["review3"].append(qid)
                
                except ValueError:
                    continue
        
        return due_reviews

# Usage Examples:
if __name__ == "__main__":
    tracker = ProgressTracker()
    
    # Example 1: Mark single problem as completed
    tracker.mark_completed("1.Math", ["7"], notes="Easy problem, solved quickly")
    
    # Example 2: Mark multiple problems as completed
    # tracker.mark_completed("1.Math", ["1", "7", "9"], mistakes="OBO", notes="Array problems")
    
    # Example 3: Individual updates
    # updates = [
    #     {"qid": "1", "status": "✅", "completed": "2024-01-15", "mistakes": "None", "notes": "Two Sum - easy"},
    #     {"qid": "7", "status": "🔄", "completed": "2024-01-16", "mistakes": "LOG", "notes": "Need to review edge cases"},
    # ]
    # tracker.update_progress("1.Math", updates)
    
    # Example 4: Mark review
    # tracker.mark_review("1.Math", "1", 1, notes="Reviewed different approaches")
    
    # Example 5: Check due reviews
    # due = tracker.get_due_reviews("1.Math")
    # print("Due reviews:", due)
    
    print("Progress Tracker initialized!")
    print("Available methods:")
    print("- mark_completed(category, qid_list, date, mistakes, notes)")
    print("- mark_review(category, qid, review_number, date, notes)")
    print("- update_progress(category, updates_list)")
    print("- get_due_reviews(category)")
    print("- bulk_update_from_file(category, csv_file)")