from app.risk_engine import analyze

def test_auth_change_scores_3():
    mr_data = {
        "title": "Debug: auth change",
        "changes": [
            {
                "new_path": "auth/login.py",
                "diff": "+ changed auth logic\n- old line"
            },
            {
                "new_path": "src/service.py",
                "diff": "+ new behavior"
            }
        ]
    }

    result = analyze(mr_data["changes"])
    assert result.score == 3


def test_ci_change_scores_5():
    mr_data = {
        "title": "Debug: CI change",
        "changes": [
            {
                "new_path": ".gitlab-ci.yml",
                "diff": "+ change pipeline"
            }
        ]
    }

    result = analyze(mr_data["changes"])
    assert result.score == 5 
    
def test_migration_change_scores_3():
    mr_data = {
        "title": "Debug: migration change",
        "changes": [
            {
                "new_path": "db/migrations/001_add_users.sql",
                "diff": "+ CREATE TABLE users"
            }
        ]
    }

    result = analyze(mr_data["changes"])
    assert result.score == 3
    
def test_README_1():
    mr_data = {
        "title": "Debug: README change",
        "changes": [
            {
                "new_path": "README.md",
                "diff": "+ update documentation"
            }
        ]
    }
    
    result = analyze(mr_data["changes"])
    assert result.score == 1
    
def test_rename_files_scores_1():
    mr_data = {
        "title": "Debug: rename files",
        "changes": [
            {
                "new_path": "src/new_service.py",
                "diff": "+ renamed from src/old_service.py"
            }
        ]
    }

    result = analyze(mr_data["changes"])
    assert result.score == 1
    
def test_mixture_5():
    mr_data = {
        "title": "Debug: mixed changes",
        "changes": [
            {
                "new_path": "auth/login.py",
                "diff": "+ changed auth logic\n- old line"
            },
            {
                "new_path": ".gitlab-ci.yml",
                "diff": "+ change pipeline"
            },
            {
                "new_path": "README.md",
                "diff": "+ update documentation"
            }
        ]
    }

    result = analyze(mr_data["changes"])
    assert result.score == 5 # tests auth +2, gitlab +2 and README +1 (heuristics)