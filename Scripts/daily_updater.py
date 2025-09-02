from progress_tracker import ProgressTracker

tracker = ProgressTracker()

# Hôm nay làm được những bài gì?
today_completed = ["1", "7", "9"]  # List các QID hoàn thành
tracker.mark_completed("1.Math", today_completed, 
                      mistakes="OBO,LOG", 
                      notes="Good progress today!")

# Kiểm tra bài nào cần review
due = tracker.get_due_reviews("1.Math")
print(f"Cần review: {due}")