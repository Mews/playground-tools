def set_exercise_complexity(target_id:int, 
                            exercise_url:str, 
                            target_complexity:int, 
                            keep_solution:bool = True,
                            default_code:str = " "):

    import db_psql as db

    mydb = db.MyDB(0)
    sdb = db.Submissions(mydb)

    query_result = sdb.find(target_id, exercise_url)

    if query_result:
        (user_id, url, code, complexity, leaderboard_complexity, 
        complexity_locked, submission_date, private_grade, public_grade, 
        private_tests_output, private_tests_done, public_tests_output, 
        public_tests_done) = query_result
        
        if not keep_solution:
            code = default_code

    else:
        user_id = target_id
        url = exercise_url
        code = default_code
        private_grade = 1.0
        public_grade = 1.0
        private_tests_output = ["None"]
        private_tests_done = [True]
        public_tests_output = ["None"]*5
        public_tests_done = [True]*5


    if all(public_tests_done + private_tests_done) and keep_solution:
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
            "public_tests_output": ["None"]*5,
            "private_tests_output": ["None"],
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

def set_all_exercises(target_id:int, complexity:int, keep_solutions:bool=True, default_code:str = " "):
    """
    This function sets the complexity of all playground exercicies to a given complexity for a certain student.
    
    Arguments:
    target_id [int] = The student id of the student whose complexities will be changed

    complexity [int] = The complexity that every exercise will be changed to

    keep_solutions [bool] [default:True] = Whether or not to keep the solutions the student has already submited
                                           For exercises that the student hasn't submited any code, this argument has no effect.
                                           If set to False, the code for all submissions will be replaced with the code passed as default_code
    
    default_code [str] [default:" "] = The code that will be submited in case the student hasn't submited anything in a particular exercise,
                                       or if keep_solutions is set to False.
    """

    for url in get_all_urls():
        set_exercise_complexity(target_id, 
                                url, 
                                target_complexity=complexity, 
                                keep_solution=keep_solutions, 
                                default_code=default_code)
