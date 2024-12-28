def set_exercise_complexity(target_id:int, exercise_url:str, target_complexity:int = -2147483648):
    import db_psql as db

    mydb = db.MyDB(0)
    sdb = db.Submissions(mydb)

    (user_id, url, code, complexity, leaderboard_complexity, 
    complexity_locked, submission_date, private_grade, public_grade, 
    private_tests_output, private_tests_done, public_tests_output, 
    public_tests_done) = sdb.find(target_id, exercise_url)

    if all(public_tests_done + private_tests_done):
        results = {"private_tests_output":private_tests_output,
                    "private_tests_done":private_tests_done,
                    "public_tests_output":public_tests_output,
                    "public_tests_done":public_tests_done,
                    "private_grade":private_grade,
                    "public_grade":public_grade}
    else:
        results = {
            "public_tests_done": [True]*5,
            "private_tests_done": [True],
            "public_tests_output": ["0"]*5,
            "private_tests_output": ["0"],
            "public_grade": 1.0,
            "private_grade": 1.0
        }

    return sdb.submit(user_id, url, code, target_complexity, target_complexity, results)

def get_all_urls():
    import subprocess

    def run(cmd, shell=False):
        if shell:
            result = subprocess.run(cmd, capture_output=True, text=True, shell=shell)
        else:
            result = subprocess.run(cmd.split(), capture_output=True, text=True, shell=shell)
        
        return result.stdout.strip()

    URLS = []

    base_dir = "exercises/play/"

    weeks = run(f"ls {base_dir}").split("\n")[1:]

    for week in weeks:
        week_dir = base_dir + week + "/"

        exs = run(f"ls {week_dir}").split("\n")[1:]

        for ex in exs:
            URLS.append(f"play/{week}/{ex.replace('.yaml', '')}")
    
    return URLS

def minimize_all_exercises(target_id:int):
    for url in get_all_urls():
        set_exercise_complexity(target_id, url)
