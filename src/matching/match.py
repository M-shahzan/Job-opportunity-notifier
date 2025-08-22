import pandas as pd

def load_profiles(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def match_jobs(profiles: pd.DataFrame, jobs: pd.DataFrame) -> pd.DataFrame:
    """Simple skill-based matching."""
    matches = []
    for _, user in profiles.iterrows():
        user_skills = set(user['skills'].split(','))
        for _, job in jobs.iterrows():
            job_skills = set(job['skills_required'].split(','))
            if user_skills & job_skills:
                matches.append({
                    'user_id': user['user_id'],
                    'job_id': job['job_id']
                })
    return pd.DataFrame(matches)

if __name__ == "__main__":
    users = load_profiles("data/external/user_profiles.csv")
    jobs = pd.read_csv("data/processed/clean_jobs.csv")
    result = match_jobs(users, jobs)
    result.to_csv("data/processed/matches.csv", index=False)
    print("Matches saved to data/processed/matches.csv")
