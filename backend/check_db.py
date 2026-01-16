from sqlmodel import Session, select
from core.db import engine
from models import Task

def check_task_status():
    with Session(engine) as session:
        # Get all tasks
        tasks = session.exec(select(Task)).all()
        
        print("\n📋 All Tasks in Database:")
        print("-" * 80)
        for task in tasks:
            print(f"ID: {task.id}")
            print(f"Title: {task.title}")
            print(f"Status: {task.status}")
            print(f"Completed: {task.completed}")
            print(f"Priority: {task.priority}")
            print("-" * 80)
        
        # Test update
        if tasks:
            test_task = tasks[0]
            print(f"\n🧪 Testing update on task {test_task.id}...")
            print(f"Before: status={test_task.status}, completed={test_task.completed}")
            
            test_task.status = "completed"
            test_task.completed = True
            session.add(test_task)
            session.commit()
            session.refresh(test_task)
            
            print(f"After: status={test_task.status}, completed={test_task.completed}")
            
            if test_task.status == "completed":
                print("✅ Update successful!")
            else:
                print("❌ Update failed - database issue detected!")

if __name__ == "__main__":
    check_task_status()