from constituency import get_constituencies   # or generate_constituencies if you renamed it
from voter import generate_voters
from candidate import generate_candidates
from Polling_booth import generate_polling_booths

def main():
    print("🚀 Starting synthetic dataset generation...")

    df_const = get_constituencies()
    df_voters = generate_voters()
    df_candidates = generate_candidates()
    df_booths = generate_polling_booths()

    print("✅ All datasets generated successfully!")

if __name__ == "__main__":
    main()
