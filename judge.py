import time
import subprocess
from bson import ObjectId
from datetime import datetime
from app import create_app, mongo

# Setup Flask context to access DB
app = create_app()
app.app_context().push()

def run_python_code(code: str) -> dict:
    """Safely execute Python code in a subprocess"""
    try:
        start_time = time.time()
        process = subprocess.run(
            ['python', '-c', code],
            text=True,
            input="",
            capture_output=True,
            timeout=5  # seconds
        )
        end_time = time.time()

        return {
            "status": "completed" if process.returncode == 0 else "failed",
            "output": process.stdout if process.returncode == 0 else process.stderr,
            "execution_time": round(end_time - start_time, 4),
            "memory_usage": None  # Placeholder
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "failed",
            "output": "Execution timed out.",
            "execution_time": 5,
            "memory_usage": None
        }
    except Exception as e:
        return {
            "status": "failed",
            "output": str(e),
            "execution_time": 0,
            "memory_usage": None
        }

def judge_loop():
    print("🚀 Judge engine started!")
    while True:
        try:
            # Fetch one queued submission
            sub = mongo.db.submissions.find_one_and_update(
                {"status": "queued"},
                {"$set": {"status": "processing"}}
            )

            if not sub:
                print("🕐 No queued submissions. Sleeping 3s...")
                time.sleep(3)
                continue

            print(f"⚙️  Processing submission: {sub['_id']}")
            code = sub['code']
            language = sub['language']

            if language == 'python':
                result = run_python_code(code)
            else:
                result = {
                    "status": "failed",
                    "output": f"Language '{language}' is not supported yet.",
                    "execution_time": 0,
                    "memory_usage": None
                }

            # Update submission with result
            mongo.db.submissions.update_one(
                {"_id": ObjectId(sub["_id"])},
                {"$set": {
                    "status": result['status'],
                    "results": [{"output": result['output']}],
                    "execution_time": result['execution_time'],
                    "memory_usage": result['memory_usage']
                }}
            )

            print(f"✅ Done: {sub['_id']} - {result['status']}")

        except Exception as e:
            print(f"❌ Judge error: {type(e).__name__} - {str(e)}")
            time.sleep(2)

if __name__ == '__main__':
    judge_loop()
